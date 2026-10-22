"""BLS_ANNUAL_FACTORS.json source_sha256 is a vintage lock of the API bundle, not of this JSON file."""
import hashlib
import json
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTORS = ROOT / "factor_sources" / "BLS_ANNUAL_FACTORS.json"
LOCKED = "bb68500e563ba28ebf75be4bbcf634d2c993a5095729a821ffd4f7de6221a231"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class BLSSourceHash(unittest.TestCase):
    def test_committed_source_sha256_is_the_lock(self):
        rec = json.loads(FACTORS.read_text())
        self.assertEqual(rec["source_sha256"], LOCKED)
        self.assertNotEqual(sha256(FACTORS), rec["source_sha256"])

    def test_operator_bundle_matches_when_present(self):
        rec = json.loads(FACTORS.read_text())
        raw = rec["source_file"].replace("$HESI_OPERATOR_HOME", str(Path.home()))
        raw = os.path.expandvars(raw)
        p = Path(raw)
        if not p.is_file():
            self.skipTest("operator BLS API bundle not on this machine")
        self.assertEqual(sha256(p), LOCKED)


if __name__ == "__main__":
    unittest.main()
