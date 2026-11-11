import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import SourceRegisterAbortError, validate_required_source_pins_or_abort


class HesiDataRootMapping(unittest.TestCase):
    def setUp(self):
        self._prev_data = os.environ.get("HESI_DATA_ROOT")
        self._prev_scratch = os.environ.get("HESI_SCRATCH_ROOT")
        self._tmp = tempfile.TemporaryDirectory()
        self._data = Path(self._tmp.name) / "hesi-data"
        self._scratch = Path(self._tmp.name) / "scratch"
        self._data.mkdir()
        self._scratch.mkdir()
        os.environ["HESI_DATA_ROOT"] = str(self._data)
        os.environ["HESI_SCRATCH_ROOT"] = str(self._scratch)

    def tearDown(self):
        for key, prev in (("HESI_DATA_ROOT", self._prev_data), ("HESI_SCRATCH_ROOT", self._prev_scratch)):
            if prev is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = prev
        self._tmp.cleanup()

    def test_maps_hesi_data_register_path(self):
        rel = Path("blocker_resolution_2026-11-11/files/example.bin")
        target = self._data / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"data-root-bytes")
        resolved = resolve_register_local_path(f"/workspace/hesi-data/{rel.as_posix()}")
        self.assertEqual(resolved, target.resolve())

    def test_maps_scratch_register_path(self):
        rel = Path("reproducer/pe_ty2026/dl/wheel.whl")
        target = self._scratch / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"scratch-bytes")
        resolved = resolve_register_local_path(f"/workspace/scratch/{rel.as_posix()}")
        self.assertEqual(resolved, target.resolve())

    def test_missing_file_returns_none_even_if_parent_exists(self):
        resolved = resolve_register_local_path("/workspace/hesi-data/hud/missing.xlsx")
        self.assertIsNone(resolved)

    def test_scratch_missing_without_env_returns_none(self):
        os.environ.pop("HESI_SCRATCH_ROOT", None)
        resolved = resolve_register_local_path("/workspace/scratch/reproducer/foo.whl")
        self.assertIsNone(resolved)

    def test_fail_closed_on_scratch_hash_mismatch(self):
        from tests.test_source_register_fail_closed import _write_min_register

        rel = "reproducer/pe_ty2026/refs/doc.pdf"
        target = self._scratch / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"real")
        reg = Path(self._tmp.name) / "reg.csv"
        _write_min_register(
            reg,
            [
                {
                    "source_id": "X-10-TEST",
                    "component": "test",
                    "local_path": f"/workspace/scratch/{rel}",
                    "sha256": "a" * 64,
                    "verification_status": "VERIFIED-PINNED",
                }
            ],
        )
        with self.assertRaises(SourceRegisterAbortError):
            validate_required_source_pins_or_abort(["X-10-TEST"], register_path=reg)


if __name__ == "__main__":
    unittest.main()
