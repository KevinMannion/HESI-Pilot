"""Checkpoint: freeze 2024 provisional outputs; do not touch R2.4 or nowcast NO-GO."""
import csv
import hashlib
import json
import math
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

PIPE = Path(__file__).resolve().parents[1]
ROOT = PIPE.parents[1]
OUT = PIPE / "results" / "matched2024_provisional"
R22 = "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class FrozenReferences(unittest.TestCase):
    def test_national_r22(self):
        p = ROOT / "core_r24/results/national_R22/common_cohort_results.csv"
        self.assertEqual(sha256(p), R22)
        with p.open() as f:
            rows = {r["metric"]: r for r in csv.DictReader(f)}
        self.assertAlmostEqual(float(rows["share_income_below_three_costs_PROVISIONAL"]["mean"]), 0.18991790144753254)

    def test_pilot(self):
        with (ROOT / "results.csv").open() as f:
            row = next(csv.DictReader(f))
        self.assertEqual(row["pct_below_housing_plus_food"], "10.301")

    def test_nowcast_nogo(self):
        go = json.loads((ROOT / "research/september2026_income_nowcast/reports/GO_NOGO.json").read_text())
        self.assertEqual(go["decision"], "NO-GO")


class HouseholdSpecific(unittest.TestCase):
    def test_not_uniform_g3_threshold(self):
        audit = json.loads((OUT / "calendar_2024_dayweight/audit.json").read_text())
        self.assertEqual(audit["food_column"], "thrifty_2024annual")
        self.assertEqual(audit["share_metric"], "share_income_below_three_costs_2024matched_MODELED")
        self.assertIn("not G3 uniform", audit["reference"])
        with (OUT / "calendar_2024_dayweight/common_cohort_results.csv").open() as f:
            rows = {r["metric"]: float(r["mean"]) for r in csv.DictReader(f)}
        combined = rows["food_month"] + rows["housing_month"] + rows["one_vehicle_month_GASOLINE_2024_NONFUEL_HELD"]
        self.assertAlmostEqual(combined, rows["total_month_PROVISIONAL"], places=7)
        self.assertNotAlmostEqual(rows["total_month_PROVISIONAL"], 2894.90805340822, places=2)

    def test_food_and_housing_vary_transport_is_constant(self):
        with (OUT / "calendar_2024_dayweight/common_cohort_results.csv").open() as f:
            rows = {r["metric"]: r for r in csv.DictReader(f)}
        self.assertGreater(float(rows["food_month"]["se_sdr"]), 0.1)
        self.assertGreater(float(rows["housing_month"]["se_sdr"]), 0.1)
        self.assertLess(float(rows["one_vehicle_month_GASOLINE_2024_NONFUEL_HELD"]["se_sdr"]), 1e-8)


class FrameAndReplicates(unittest.TestCase):
    def test_eligibility_matches_r24(self):
        a = json.loads((ROOT / "core_r24/results/national_R22/audit.json").read_text())["frame"]
        b = json.loads((OUT / "calendar_2024_dayweight/audit.json").read_text())["frame"]
        self.assertEqual(a, b)
        self.assertEqual(b["included_rows"], 1235731)
        self.assertEqual(b["included_weight"], 121036726.0)
        self.assertEqual(b["geography_excluded_rows"], 64079)

    def test_eighty_replicates_and_sdr_formula(self):
        d = pd.read_csv(OUT / "calendar_2024_dayweight/replicate_results.csv")
        self.assertEqual(len(d), 80)
        self.assertEqual(list(d.replicate), list(range(1, 81)))
        share = pd.read_csv(OUT / "calendar_2024_dayweight/common_cohort_results.csv").set_index("metric")
        p = share.loc["share_income_below_three_costs_2024matched_MODELED", "mean"]
        se = share.loc["share_income_below_three_costs_2024matched_MODELED", "se_sdr"]
        se2 = math.sqrt((4 / 80) * ((d.share_below.to_numpy() - p) ** 2).sum())
        self.assertTrue(np.isclose(se, se2, atol=1e-12, rtol=0))


class Protocol(unittest.TestCase):
    def test_day_weights(self):
        src = (PIPE / "src/prepare_2024_cost_inputs.py").read_text()
        self.assertIn("DAYS_FY24_ORIG = 70", src)
        self.assertIn("DAYS_FY24_REV = 204", src)
        self.assertIn("DAYS_FY25_ORIG = 92", src)
        self.assertIn("DAYS_2024 = 366", src)

    def test_usda_mean_is_twelve_months(self):
        src = (PIPE / "src/rebuild_matched_food_cache.py").read_text()
        self.assertIn("for month in range(1, 13)", src)
        self.assertIn("sum(months) / 12.0", src)

    def test_transport_held_nonfuel(self):
        with (PIPE / "outputs/transport_reference_2024.csv").open() as f:
            rows = list(csv.DictReader(f))
        default = next(r for r in rows if r["scenario"] == "calendar_2024_eia_annual")
        self.assertEqual(default["nonfuel_annual_HELD_NOT_2024_VALIDATED"], "5631.67")
        self.assertEqual(default["transport_annual"], "6870.67")

    def test_artifact_lock(self):
        lock = json.loads((OUT / "ARTIFACT_LOCK.json").read_text())
        self.assertTrue(lock["national_R22_untouched"])
        self.assertEqual(lock["national_R22_sha256"], R22)
        self.assertEqual(len(lock["files"]), 14)
        for rel, meta in lock["files"].items():
            self.assertEqual(sha256(OUT / rel), meta["sha256"], rel)

    def test_readiness_nogo_public(self):
        doc = json.loads((OUT / "RESEARCH_READINESS.json").read_text())
        self.assertEqual(doc["computational_reproduction_attempt"], "GO")
        self.assertEqual(doc["provisional_public_research_release"], "NO-GO")
        self.assertEqual(doc["publish_17_7_percent"], "NO-GO")


if __name__ == "__main__":
    unittest.main()
