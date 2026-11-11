"""T-03: matched-year output paths must not touch frozen or protected directories."""
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SRC = ROOT / "src"
CORE = REPO / "core_r24"
FROZEN = ROOT / "results" / "matched2024_provisional"
FIX = CORE / "fixtures" / "synthetic_housing.zip"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class MatchedOutputSafety(unittest.TestCase):
    def test_run_matched_national_rejects_frozen_out_before_scenario_runs(self):
        sentinel = FROZEN / "EXECUTION_REPORT.json"
        self.assertTrue(sentinel.is_file())
        before = sha256(sentinel)
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SRC / "run_matched_national.py"),
                    "--housing",
                    str(FIX),
                    "--person-a",
                    str(FIX),
                    "--person-b",
                    str(FIX),
                    "--out",
                    str(FROZEN),
                    "--cache",
                    td,
                    "--exploratory",
                ],
                cwd=REPO,
                capture_output=True,
                text=True,
            )
        combined = proc.stderr + proc.stdout
        self.assertNotEqual(proc.returncode, 0)
        self.assertRegex(combined, "PROTECTED OUTPUT PATH|UNSAFE OUTPUT")
        self.assertNotIn("RUN calendar_2024_dayweight", combined)
        self.assertEqual(sha256(sentinel), before)

    def test_run_matched_national_rejects_symlink_out_before_input_validation(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td) / "scratch"
            scratch.mkdir()
            link = Path(td) / "out_link"
            link.symlink_to(scratch, target_is_directory=True)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SRC / "run_matched_national.py"),
                    "--housing",
                    str(FIX),
                    "--person-a",
                    str(FIX),
                    "--person-b",
                    str(FIX),
                    "--out",
                    str(link),
                    "--cache",
                    str(Path(td) / "cache"),
                    "--exploratory",
                ],
                cwd=REPO,
                capture_output=True,
                text=True,
            )
        combined = proc.stderr + proc.stdout
        self.assertNotEqual(proc.returncode, 0)
        self.assertRegex(combined, "UNSAFE OUTPUT|symlink")
        self.assertNotIn("INPUT_VALIDATION.json", combined)

    def test_run_matched_national_official_requires_explicit_out(self):
        proc = subprocess.run(
            [sys.executable, str(SRC / "run_matched_national.py"), "--housing", str(FIX)],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--out", proc.stderr + proc.stdout)

    def test_validate_matched_inputs_refuses_frozen_report_parent(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SRC / "validate_matched_inputs.py"),
                    "--housing",
                    str(FIX),
                    "--person-a",
                    str(FIX),
                    "--person-b",
                    str(FIX),
                    "--out",
                    str(FROZEN / "INPUT_VALIDATION.json"),
                ],
                cwd=REPO,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(proc.returncode, 0)
        self.assertRegex(proc.stderr + proc.stdout, "PROTECTED OUTPUT PATH|UNSAFE OUTPUT")

    def test_exploratory_default_out_is_not_provisional(self):
        src = (SRC / "run_matched_national.py").read_text()
        self.assertNotIn('default=str(PIPE / "results/matched2024_provisional")', src)
        self.assertIn('local_runs/matched2024', src)


if __name__ == "__main__":
    unittest.main()
