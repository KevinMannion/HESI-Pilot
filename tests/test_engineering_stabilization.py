"""Phase 1 engineering checks. Do not rewrite frozen scientific results."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class FrozenScientificFiles(unittest.TestCase):
    def test_national_r22(self):
        p = ROOT / "core_r24/results/national_R22/common_cohort_results.csv"
        self.assertEqual(sha256(p), "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7")

    def test_nowcast_nogo(self):
        go = json.loads((ROOT / "research/september2026_income_nowcast/reports/GO_NOGO.json").read_text())
        self.assertEqual(go["decision"], "NO-GO")


class Requirements(unittest.TestCase):
    def test_openpyxl_and_xlrd_listed(self):
        text = (ROOT / "requirements.txt").read_text()
        self.assertIn("openpyxl", text)
        self.assertIn("xlrd", text)


class TrackedFileWrites(unittest.TestCase):
    def test_transport_run_does_not_rewrite_golden(self):
        path = ROOT / "research/september2026_core_r2/transportation/transport_reference_2026_09.csv"
        before = sha256(path)
        subprocess.run([sys.executable, "run_standard.py"], cwd=path.parent, check=True, capture_output=True)
        self.assertEqual(sha256(path), before)
        self.assertEqual(before, "19cc412e1d13662782ee57315f148f0a2187e1fd1613052c3aebd3397a687af6")

    def test_housing_verify_does_not_rewrite_golden(self):
        csv_path = ROOT / "research/september2026_core_r2/housing/executed_results.csv"
        audit = ROOT / "research/september2026_core_r2/housing/audit.json"
        b1, b2 = sha256(csv_path), sha256(audit)
        subprocess.run([sys.executable, "verify.py"], cwd=csv_path.parent, check=True, capture_output=True)
        self.assertEqual(sha256(csv_path), b1)
        self.assertEqual(sha256(audit), b2)

    def test_prepare_default_does_not_target_tracked_docs(self):
        src = (ROOT / "research/historical_matched_baseline/src/prepare_2024_cost_inputs.py").read_text()
        self.assertIn("write-tracked-docs", src)
        self.assertIn("docs_dir = PIPE if args.write_tracked_docs else out", src)


if __name__ == "__main__":
    unittest.main()
