"""Inner-CSV checksum path must not skip hashes or confuse ZIP hashes with content hashes."""
import io, json, unittest, zipfile, hashlib, tempfile
from pathlib import Path
import sys

P = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(P / "tools"))
from pums_archive import verify_official_person_zip, verify_housing_zip, verify_split_person_zips, load_lock, csv_members


def _zip_with(member, payload):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(member, payload)
    return buf.getvalue()


class InnerHashLock(unittest.TestCase):
    def test_lock_lists_both_layers(self):
        lock = load_lock()
        self.assertNotEqual(lock["r24_locked_zip_sha256"]["person_part_1"], lock["official_census_zip_sha256_not_a_substitute_for_inner_hashes"]["csv_pus.zip"])
        self.assertEqual(len(lock["inner_csv_sha256"]["psam_pusa.csv"]), 64)

    def test_official_zip_rejected_if_inner_csv_wrong(self):
        lock = {
            "inner_csv_sha256": {
                "psam_pusa.csv": hashlib.sha256(b"A").hexdigest(),
                "psam_pusb.csv": hashlib.sha256(b"B").hexdigest(),
            }
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "csv_pus.zip"
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                z.writestr("psam_pusa.csv", b"A")
                z.writestr("psam_pusb.csv", b"WRONG")
            p.write_bytes(buf.getvalue())
            with self.assertRaises(RuntimeError) as ctx:
                verify_official_person_zip(p, lock)
            self.assertIn("INNER CSV HASH MISMATCH", str(ctx.exception))

    def test_official_zip_accepted_when_inner_hashes_match_even_if_container_differs(self):
        a, b = b"person-a-records\n", b"person-b-records\n"
        lock = {
            "inner_csv_sha256": {
                "psam_pusa.csv": hashlib.sha256(a).hexdigest(),
                "psam_pusb.csv": hashlib.sha256(b).hexdigest(),
            }
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "csv_pus.zip"
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr("psam_pusa.csv", a)
                z.writestr("psam_pusb.csv", b)
                z.writestr("ACS2024_PUMS_README.pdf", b"readme")
            p.write_bytes(buf.getvalue())
            report = verify_official_person_zip(p, lock)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["mode"], "official_combined_zip")

    def test_split_zips_still_require_r24_zip_hashes(self):
        lock = json.loads((P / "PUMS_ARCHIVE_LOCK.json").read_text())
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "part1.zip"
            b = Path(td) / "part2.zip"
            a.write_bytes(_zip_with("psam_pusa.csv", b"x"))
            b.write_bytes(_zip_with("psam_pusb.csv", b"y"))
            with self.assertRaises(RuntimeError) as ctx:
                verify_split_person_zips(a, b, lock)
            self.assertIn("INPUT HASH MISMATCH", str(ctx.exception))

    def test_duplicate_inner_csv_members_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "dup.zip"
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                z.writestr("folder/psam_pusa.csv", b"A")
                z.writestr("other/psam_pusa.csv", b"A2")
            p.write_bytes(buf.getvalue())
            with self.assertRaises(RuntimeError) as ctx:
                csv_members(p, "psam_pus")
            self.assertIn("Duplicate inner CSV members", str(ctx.exception))

    def test_unexpected_inner_csv_rejected(self):
        lock = {
            "inner_csv_sha256": {
                "psam_pusa.csv": hashlib.sha256(b"A").hexdigest(),
                "psam_pusb.csv": hashlib.sha256(b"B").hexdigest(),
            }
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "csv_pus.zip"
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                z.writestr("psam_pusa.csv", b"A")
                z.writestr("psam_pusb.csv", b"B")
                z.writestr("psam_pusc.csv", b"C")
            p.write_bytes(buf.getvalue())
            with self.assertRaises(RuntimeError) as ctx:
                verify_official_person_zip(p, lock)
            self.assertIn("unexpected inner CSV", str(ctx.exception))

    def test_housing_zip_bad_hash_without_matching_inner_csvs_rejected(self):
        lock = json.loads((P / "PUMS_ARCHIVE_LOCK.json").read_text())
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "csv_hus.zip"
            p.write_bytes(_zip_with("not_housing.txt", b"nope"))
            with self.assertRaises(RuntimeError) as ctx:
                verify_housing_zip(p, lock)
            msg = str(ctx.exception)
            self.assertTrue(
                "missing inner CSV" in msg
                or "HASH MISMATCH" in msg
                or "INPUT MISSING" in msg
            )

    def test_missing_archive_is_rejected(self):
        lock = json.loads((P / "PUMS_ARCHIVE_LOCK.json").read_text())
        with self.assertRaises(RuntimeError) as ctx:
            verify_housing_zip("/tmp/hesi_missing_housing_does_not_exist.zip", lock)
        self.assertIn("INPUT MISSING", str(ctx.exception))

    def test_housing_inner_hashes_required_even_if_operator_supplies_matching_zip_digest(self):
        a, b = b"husa\n", b"husb\n"
        payload = _zip_with("psam_husa.csv", a)
        # incomplete zip: matching a fake zip digest must not skip the missing husb CSV
        lock = {
            "r24_locked_zip_sha256": {"housing_csv_hus.zip": hashlib.sha256(payload).hexdigest()},
            "inner_csv_sha256": {
                "psam_husa.csv": hashlib.sha256(a).hexdigest(),
                "psam_husb.csv": hashlib.sha256(b).hexdigest(),
            },
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "csv_hus.zip"
            p.write_bytes(payload)
            with self.assertRaises(RuntimeError) as ctx:
                verify_housing_zip(p, lock)
            self.assertIn("missing inner CSV", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
