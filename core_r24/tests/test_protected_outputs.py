"""Fail-closed protected scientific outputs: no caches before rejection."""
import hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from protected_paths import assert_output_allowed, protected_directories


def listing(path):
    files = []
    for p in sorted(Path(path).rglob("*")):
        if p.is_file():
            files.append((str(p.relative_to(path)), hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns, p.stat().st_size))
    return files


class ProtectedOutputs(unittest.TestCase):
    def test_assert_rejects_national_r22_before_caller_mkdir(self):
        target = ROOT / "results" / "national_R22"
        before = listing(target)
        with self.assertRaises(RuntimeError) as ctx:
            assert_output_allowed(target, "test")
        self.assertIn("PROTECTED OUTPUT PATH", str(ctx.exception))
        self.assertEqual(listing(target), before)

    def test_run_joint_refuses_frozen_dir(self):
        target = ROOT / "results" / "national_R22"
        before = listing(target)
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "src" / "run_joint.py"),
                "--housing-zip",
                str(ROOT / "fixtures" / "synthetic_housing.zip"),
                "--food-cache",
                str(ROOT / "fixtures" / "synthetic_food.csv"),
                "--composition-cache",
                str(ROOT / "fixtures" / "synthetic_composition.csv"),
                "--geography",
                str(ROOT / "fixtures" / "synthetic_geography.csv"),
                "--out",
                str(target),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("PROTECTED OUTPUT PATH", proc.stderr + proc.stdout)
        self.assertEqual(listing(target), before)

    def test_reproduce_refuses_national_r22_without_writing_caches(self):
        target = ROOT / "results" / "national_R22"
        before = listing(target)
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "reproduce_from_raw.py"),
                "--housing",
                str(ROOT / "fixtures" / "synthetic_housing.zip"),
                "--person-a",
                str(ROOT / "fixtures" / "synthetic_housing.zip"),
                "--person-b",
                str(ROOT / "fixtures" / "synthetic_housing.zip"),
                "--output",
                str(target),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        combined = proc.stderr + proc.stdout
        self.assertIn("PROTECTED OUTPUT PATH", combined)
        self.assertEqual(listing(target), before)
        self.assertFalse((target / "derived_person_caches").exists())

    def test_rebuild_refuses_nested_protected_cache(self):
        target = ROOT / "results" / "national_R22" / "derived_person_caches"
        parent_before = listing(ROOT / "results" / "national_R22")
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "rebuild_raw_person_caches.py"),
                "--person-zips",
                str(ROOT / "fixtures" / "synthetic_housing.zip"),
                "--out",
                str(target),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("PROTECTED OUTPUT PATH", proc.stderr + proc.stdout)
        self.assertEqual(listing(ROOT / "results" / "national_R22"), parent_before)
        self.assertFalse(target.exists())

    def test_stale_part_cache_is_ignored_without_resume(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            tag = hashlib.sha256(str((ROOT / "fixtures" / "synthetic_housing.zip").resolve()).encode()).hexdigest()[:12]
            fake = out / f"food_part_{tag}.pkl"
            out.mkdir(exist_ok=True)
            fake.write_bytes(b"not-a-pickle")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "rebuild_raw_person_caches.py"),
                    "--person-zips",
                    str(ROOT / "fixtures" / "synthetic_housing.zip"),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            # Fixture ZIP has no psam_pus CSVs; rebuild must not treat the fake pickle as a valid cache.
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Resumed", proc.stdout)

    def test_protected_directory_list_covers_frozen_results(self):
        names = {p.name for p in protected_directories()}
        self.assertIn("national_R22", names)
        self.assertIn("rebuilt_from_raw", names)
        self.assertIn("synthetic", names)
        self.assertIn("matched2024_provisional", names)


if __name__ == "__main__":
    unittest.main()
