"""Missing, empty, malformed manifests and unauthorized bypasses must FAIL."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
from verify_integrity import check_manifest


class ManifestFailClosed(unittest.TestCase):
    def test_missing_manifest(self):
        report = check_manifest(BASE / "does_not_exist_INTEGRITY.json")
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("MISSING", report["failed"][0]["error"])

    def test_empty_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "empty.json"
            p.write_text("")
            report = check_manifest(p)
            self.assertEqual(report["status"], "FAIL")
            self.assertIn("EMPTY", report["failed"][0]["error"])

    def test_malformed_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.json"
            p.write_text("{not json")
            report = check_manifest(p)
            self.assertEqual(report["status"], "FAIL")
            self.assertIn("MALFORMED", report["failed"][0]["error"])

    def test_empty_files_map(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "none.json"
            p.write_text(json.dumps({"files": {}}))
            report = check_manifest(p)
            self.assertEqual(report["status"], "FAIL")

    def test_bypass_env_rejected(self):
        env = dict(os.environ, HESI_SKIP_INTEGRITY="1", PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.run([sys.executable, str(BASE / "verify_integrity.py"), "--all"], cwd=BASE, env=env, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unauthorized bypass", proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main()
