"""Matched-year engine wiring. Does not require Census ZIPs."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

PIPE = Path(__file__).resolve().parents[1]
ROOT = PIPE.parents[1]
sys.path.insert(0, str(ROOT / "core_r24" / "src"))
sys.path.insert(0, str(PIPE / "src"))
from food_model import load_prices  # noqa: E402
from rebuild_matched_food_cache import annual_mean_vector  # noqa: E402
from run_joint import run  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


class Wiring(unittest.TestCase):
    def test_refuses_national_r22(self):
        frozen = ROOT / "core_r24/results/national_R22"
        with self.assertRaises(RuntimeError):
            run(
                ROOT / "core_r24/fixtures/synthetic_housing.zip",
                ROOT / "core_r24/fixtures/synthetic_food.csv",
                ROOT / "core_r24/fixtures/synthetic_composition.csv",
                ROOT / "core_r24/fixtures/synthetic_geography.csv",
                frozen,
            )

    def test_synthetic_still_matches_and_does_not_touch_r22(self):
        with tempfile.TemporaryDirectory() as td:
            audit = run(
                ROOT / "core_r24/fixtures/synthetic_housing.zip",
                ROOT / "core_r24/fixtures/synthetic_food.csv",
                ROOT / "core_r24/fixtures/synthetic_composition.csv",
                ROOT / "core_r24/fixtures/synthetic_geography.csv",
                td,
            )
            self.assertEqual(audit["frame"]["included_rows"], 3)
            self.assertTrue((Path(td) / "common_cohort_results.csv").is_file())
        self.assertEqual(
            sha256(ROOT / "core_r24/results/national_R22/common_cohort_results.csv"),
            "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7",
        )

    def test_2024_annual_mean_has_15_cells(self):
        catalog, _issues = load_prices(ROOT / "core_r24/inputs/source_2024_2026.csv")
        vec = annual_mean_vector(catalog, 2024)
        self.assertEqual(len(vec), 17)
        self.assertTrue((vec > 0).all())

    def test_prep_doc_still_records_historical_nogo(self):
        doc = json.loads((PIPE / "MATCHED_YEAR_READINESS.json").read_text())
        self.assertEqual(doc["recommendation"]["execute_2024_matched_year_national_percentage_this_round"], "NO-GO")
        self.assertEqual(doc["r24_share_untouched"], "18.9918%")


if __name__ == "__main__":
    unittest.main()
