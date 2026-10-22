"""Gates for 2024 cost-input preparation. Does not compute a national share."""
import json
import hashlib
from pathlib import Path
import unittest

PIPE = Path(__file__).resolve().parents[1]
ROOT = PIPE.parents[1]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class FrozenUntouched(unittest.TestCase):
    def test_national_r22(self):
        p = ROOT / "core_r24/results/national_R22/common_cohort_results.csv"
        self.assertEqual(sha256(p), "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7")

    def test_puma(self):
        p = ROOT / "core_r24/inputs/puma_fmr_screened.csv"
        self.assertEqual(sha256(p), "210a7ec6ae756ca8034cf3b7bff8afb3480d53186834cc7b304b913445f2a3ee")

    def test_usda_frozen(self):
        p = ROOT / "core_r24/inputs/source_2024_2026.csv"
        self.assertEqual(sha256(p), "90bc39d1a569073b9530ca0a78a4ccf19c781c4a42dd70c51a0bed9e1907602c")


class Readiness(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((PIPE / "MATCHED_YEAR_READINESS.json").read_text())

    def test_no_share_computed(self):
        self.assertEqual(self.doc["recommendation"]["execute_2024_matched_year_national_percentage_this_round"], "NO-GO")
        self.assertEqual(self.doc["r24_share_untouched"], "18.9918%")

    def test_input_prep_pass(self):
        self.assertEqual(self.doc["recommendation"]["input_preparation"], "PASS")
        failed = [g["name"] for g in self.doc["gates"] if g["status"] != "PASS"]
        self.assertEqual(failed, [])

    def test_outputs_exist(self):
        for name in [
            "county_model_ready_calendar2024_dayweight.csv",
            "county_model_ready_FY2024_revised.csv",
            "county_model_ready_FY2025_original.csv",
            "puma_fmr_calendar_2024.csv",
            "usda_2024_monthly_from_thrifty_workbook.csv",
            "eia_us_regular_weekly_2024.csv",
            "transport_reference_2024.csv",
        ]:
            self.assertTrue((PIPE / "outputs" / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
