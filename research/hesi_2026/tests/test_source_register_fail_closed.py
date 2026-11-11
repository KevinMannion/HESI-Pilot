import csv
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.source_register import (
    SourceRegisterAbortError,
    validate_required_source_pins_or_abort,
    validate_source_register,
)
from sources.cms_marketplace_ingest import verify_cms_marketplace_register
from sources.ndcp_childcare import price_childcare_ndcp_county


REGISTER_COLUMNS = [
    "source_id",
    "component",
    "title",
    "url",
    "publisher",
    "publication_date",
    "vintage",
    "coverage",
    "local_path",
    "sha256",
    "verification_status",
    "unresolved_gaps",
    "blocks",
    "limitations",
    "adjustment_2026",
    "origin",
]


def _write_min_register(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=REGISTER_COLUMNS)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in REGISTER_COLUMNS})


class SourceRegisterFailClosed(unittest.TestCase):
    def setUp(self):
        self._prev_root = os.environ.get("HESI_DATA_ROOT")
        self._tmp = tempfile.TemporaryDirectory()
        os.environ["HESI_DATA_ROOT"] = self._tmp.name

    def tearDown(self):
        if self._prev_root is None:
            os.environ.pop("HESI_DATA_ROOT", None)
        else:
            os.environ["HESI_DATA_ROOT"] = self._prev_root
        self._tmp.cleanup()

    def test_metadata_inspection_does_not_abort_on_missing(self):
        report = validate_source_register()
        self.assertIn(report["status"], ("PASS", "HASH_MISMATCH"))
        self.assertGreater(len(report["missing_files"]), 0)

    def test_missing_required_file_aborts(self):
        reg = Path(self._tmp.name) / "mini_register.csv"
        _write_min_register(
            reg,
            [
                {
                    "source_id": "T-MISSING",
                    "component": "test",
                    "local_path": "/workspace/hesi-data/missing/file.bin",
                    "sha256": "0" * 64,
                    "verification_status": "VERIFIED-PINNED",
                }
            ],
        )
        with self.assertRaises(SourceRegisterAbortError) as ctx:
            validate_required_source_pins_or_abort(["T-MISSING"], register_path=reg)
        self.assertIn("missing", str(ctx.exception).lower())

    def test_incorrect_sha_aborts(self):
        data = b"pinned-bytes"
        rel = "files/pin.bin"
        target = Path(self._tmp.name) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        reg = Path(self._tmp.name) / "mini_register.csv"
        _write_min_register(
            reg,
            [
                {
                    "source_id": "T-BAD",
                    "component": "test",
                    "local_path": f"/workspace/hesi-data/{rel}",
                    "sha256": "f" * 64,
                    "verification_status": "VERIFIED-PINNED",
                }
            ],
        )
        with self.assertRaises(SourceRegisterAbortError) as ctx:
            validate_required_source_pins_or_abort(["T-BAD"], register_path=reg)
        self.assertIn("mismatch", str(ctx.exception).lower())

    def test_valid_required_file_passes(self):
        data = b"pinned-bytes-ok"
        rel = "files/ok.bin"
        target = Path(self._tmp.name) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        want = hashlib.sha256(data).hexdigest()
        reg = Path(self._tmp.name) / "mini_register.csv"
        _write_min_register(
            reg,
            [
                {
                    "source_id": "T-OK",
                    "component": "test",
                    "local_path": f"/workspace/hesi-data/{rel}",
                    "sha256": want,
                    "verification_status": "VERIFIED-PINNED",
                },
                {
                    "source_id": "T-OTHER-MISSING",
                    "component": "test",
                    "local_path": "/workspace/hesi-data/nowhere.bin",
                    "sha256": "e" * 64,
                    "verification_status": "VERIFIED-PINNED",
                },
            ],
        )
        got = validate_required_source_pins_or_abort(["T-OK"], register_path=reg)
        self.assertEqual(got["T-OK"], want)

    def test_synthetic_ndcp_fixture_without_bundle(self):
        if "HESI_DATA_ROOT" in os.environ:
            del os.environ["HESI_DATA_ROOT"]
        hh = {"county_fips": "36119", "members": [{"age": 4}]}
        detail = price_childcare_ndcp_county(hh, data_source="fixture")
        self.assertGreater(detail["annual_usd"], 0)
        self.assertTrue(detail["ndcp_source"].get("fixture_fallback"))

    def test_ndcp_register_path_aborts_without_bundle(self):
        hh = {"county_fips": "36119", "members": [{"age": 4}]}
        with self.assertRaises(SourceRegisterAbortError):
            price_childcare_ndcp_county(hh, data_source="register")

    def test_cms_real_entrypoint_cannot_bypass_validation(self):
        with self.assertRaises(SourceRegisterAbortError):
            verify_cms_marketplace_register()


if __name__ == "__main__":
    unittest.main()
