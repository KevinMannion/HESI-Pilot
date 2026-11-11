"""Scratch-only audit manifest tool."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RegenerateAuditMetadata(unittest.TestCase):
    def test_refuses_frozen_national_r22(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/regenerate_audit_metadata.py"),
                "--output-dir",
                str(ROOT / "results/national_R22"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertRegex(proc.stderr + proc.stdout, "PROTECTED|UNSAFE")

    def test_writes_manifest_on_scratch(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "tools/regenerate_audit_metadata.py"), "--output-dir", td],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            manifest = json.loads((Path(td) / "AUDIT_MANIFEST.json").read_text())
            self.assertEqual(manifest["parity_status"], "NOT_CHECKED")
            self.assertEqual(manifest["audit_schema_version"], "hesi_audit_v2")


if __name__ == "__main__":
    unittest.main()
