"""P0-01: refuse ancestor/symlink/nonempty destinations without touching real artifacts."""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "tools"))
import protected_paths
from protected_paths import assert_output_allowed, promote_staging_to_output


def _listing(path):
    files = []
    for p in sorted(Path(path).rglob("*")):
        if p.is_file() or p.is_symlink():
            digest = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() and not p.is_symlink() else "symlink"
            files.append((str(p.relative_to(path)), digest, p.is_symlink()))
    return files


class DisposableOutputSafety(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory(prefix="hesi_p001_")
        self.repo = Path(self.td.name) / "repo"
        self.core = self.repo / "core_r24"
        self.frozen = self.core / "results" / "national_R22"
        self.results = self.core / "results"
        self.matched = self.repo / "research/historical_matched_baseline/results/matched2024_provisional"
        self.frozen.mkdir(parents=True)
        self.matched.mkdir(parents=True)
        self.git = self.repo / ".git"
        self.git.mkdir()
        (self.git / "objects").mkdir()
        (self.git / "objects" / "pack").mkdir()
        (self.git / "HEAD").write_text("ref: refs/heads/main\n")
        (self.core / "src").mkdir(parents=True)
        (self.core / "tools").mkdir(parents=True)
        (self.core / "src" / "run_joint.py").write_text("# sentinel\n")
        (self.core / "tools" / "protected_paths.py").write_text("# sentinel\n")
        (self.frozen / "sentinel.txt").write_text("FROZEN\n")
        (self.matched / "lock.txt").write_text("LOCK\n")
        (self.repo / "results.csv").write_text("pilot\n")
        self.before = _listing(self.repo)
        self.patches = [
            mock.patch.object(protected_paths, "CORE", self.core),
            mock.patch.object(protected_paths, "REPO", self.repo),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.assertEqual(_listing(self.repo), self.before)
        self.td.cleanup()

    def _reject(self, target):
        with self.assertRaises(RuntimeError) as ctx:
            assert_output_allowed(target, "test")
        self.assertRegex(str(ctx.exception), "PROTECTED OUTPUT PATH|UNSAFE OUTPUT")
        self.assertEqual(_listing(self.repo), self.before)

    def test_rejects_repository_root(self):
        self._reject(self.repo)

    def test_rejects_core_r24_results_parent(self):
        self._reject(self.results)

    def test_rejects_parent_of_frozen_output(self):
        self._reject(self.core)
        self._reject(self.matched.parent)

    def test_rejects_frozen_directory_itself(self):
        self._reject(self.frozen)
        self._reject(self.matched)

    def test_rejects_symlink_to_protected_location(self):
        link = Path(self.td.name) / "link_to_frozen"
        link.symlink_to(self.frozen, target_is_directory=True)
        self._reject(link)
        parent_link = Path(self.td.name) / "link_to_results"
        parent_link.symlink_to(self.results, target_is_directory=True)
        self._reject(parent_link)
        self.assertTrue(link.exists())
        self.assertTrue(parent_link.exists())

    def test_rejects_nonempty_unowned_destination_without_deleting_it(self):
        dest = Path(self.td.name) / "unowned"
        dest.mkdir()
        victim = dest / "do_not_delete.txt"
        victim.write_text("keep-me\n")
        staging = Path(self.td.name) / "staging"
        staging.mkdir()
        (staging / "new.txt").write_text("new\n")
        before_dest = victim.read_text()
        with self.assertRaises(RuntimeError) as ctx:
            promote_staging_to_output(staging, dest, "test")
        self.assertIn("nonempty", str(ctx.exception).lower())
        self.assertEqual(victim.read_text(), before_dest)
        self.assertEqual(sorted(p.name for p in dest.iterdir()), ["do_not_delete.txt"])
        self.assertEqual(_listing(self.repo), self.before)

    def test_allows_new_scratch_directory_without_touching_fixtures(self):
        dest = Path(self.td.name) / "scratch_ok"
        staging = Path(self.td.name) / "staging_ok"
        staging.mkdir()
        (staging / "national").mkdir()
        (staging / "national" / "audit.json").write_text("{}\n")
        promote_staging_to_output(staging, dest, "test")
        self.assertTrue((dest / "national" / "audit.json").is_file())
        self.assertEqual(_listing(self.repo), self.before)

    def test_rejects_git_metadata_and_core_source_trees(self):
        self._reject(self.git)
        self._reject(self.git / "objects")
        self._reject(self.git / "objects" / "pack" / "out")
        self._reject(self.core / "src")
        self._reject(self.core / "src" / "scratch_out")
        self._reject(self.core / "tools")
        self._reject(self.core / "tools" / "nested" / "out")

    def test_rejects_symlink_aliases_into_git_or_source_zones(self):
        link_git = Path(self.td.name) / "alias_git"
        link_git.symlink_to(self.git / "objects", target_is_directory=True)
        self._reject(link_git)
        link_src = Path(self.td.name) / "alias_src"
        link_src.symlink_to(self.core / "src", target_is_directory=True)
        self._reject(link_src)

    def test_promote_refuses_git_before_writing_report(self):
        dest = self.git / "hesi_repro_out"
        staging = Path(self.td.name) / "staging_git"
        staging.mkdir()
        (staging / "REPRODUCTION_REPORT.json").write_text("{}\n")
        with self.assertRaises(RuntimeError) as ctx:
            promote_staging_to_output(staging, dest, "test")
        self.assertRegex(str(ctx.exception), "PROTECTED OUTPUT PATH|UNSAFE OUTPUT")
        self.assertFalse(dest.exists())
        self.assertEqual(_listing(self.repo), self.before)

    def test_allows_documented_exploratory_scratch_under_core(self):
        dest = self.core / "local_reproduction"
        resolved = assert_output_allowed(dest, "test")
        self.assertEqual(resolved, dest.resolve())
        self.assertEqual(_listing(self.repo), self.before)

    def test_reproduce_cli_rejects_symlink_output_before_input_verification(self):
        scratch = Path(self.td.name) / "allowed_scratch"
        scratch.mkdir()
        link = Path(self.td.name) / "output_link"
        link.symlink_to(scratch, target_is_directory=True)
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
                str(link),
                "--exploratory",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        combined = proc.stderr + proc.stdout
        self.assertNotEqual(proc.returncode, 0)
        self.assertRegex(combined, "UNSAFE OUTPUT|symlink")
        self.assertNotIn("SOURCE VERIFIED", combined)
        self.assertEqual(_listing(self.repo), self.before)


if __name__ == "__main__":
    unittest.main()
