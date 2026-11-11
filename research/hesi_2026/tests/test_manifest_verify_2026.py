import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.manifest_verify import (
    MANIFEST_VERSION,
    ManifestVerifyError,
    verify_input_manifest,
    verify_input_manifest_or_abort,
)
from sources.pinned import PINNED_SOURCES

MANIFEST = Path(__file__).resolve().parents[1] / "audit" / "input_manifest_2026.json"


class ManifestVerify2026(unittest.TestCase):
    def test_default_manifest_passes(self):
        report = verify_input_manifest_or_abort()
        self.assertEqual(report["status"], "PASS")
        self.assertGreaterEqual(report["verified_count"], 7)

    def test_manifest_pins_align_with_pinned_registry(self):
        data = json.loads(MANIFEST.read_text())
        for key, meta in data["pins"].items():
            self.assertIn(key, PINNED_SOURCES, msg=f"manifest pin {key} missing from PINNED_SOURCES")
            src = PINNED_SOURCES[key]
            self.assertEqual(meta["sha256"], src.sha256)
            self.assertEqual(meta["rel_path"], src.rel_path)

    def test_malformed_manifest_abort(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write('{"manifest_version": "wrong", "pins": {}}')
            bad = Path(f.name)
        try:
            with self.assertRaises(ManifestVerifyError):
                verify_input_manifest(bad)
        finally:
            bad.unlink()

    def test_hash_mismatch_abort(self):
        data = json.loads(MANIFEST.read_text())
        first_key = next(iter(data["pins"]))
        data["pins"][first_key]["sha256"] = "0" * 64
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            bad = Path(f.name)
        try:
            with self.assertRaises(ManifestVerifyError):
                verify_input_manifest(bad)
        finally:
            bad.unlink()

    def test_manifest_version_constant(self):
        data = json.loads(MANIFEST.read_text())
        self.assertEqual(data["manifest_version"], MANIFEST_VERSION)


if __name__ == "__main__":
    unittest.main()
