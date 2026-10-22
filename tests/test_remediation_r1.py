"""Locks and labeling checks for methods-review remediation round 1."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class FrozenResults(unittest.TestCase):
    def test_national_r22(self):
        p = ROOT / "core_r24/results/national_R22/common_cohort_results.csv"
        self.assertEqual(sha256(p), "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7")
        import csv
        with p.open() as f:
            rows = {r["metric"]: r for r in csv.DictReader(f)}
        self.assertAlmostEqual(float(rows["share_income_below_three_costs_PROVISIONAL"]["mean"]), 0.18991790144753254)
        rebuilt = ROOT / "core_r24/results/rebuilt_from_raw/common_cohort_results.csv"
        with rebuilt.open() as f:
            r2 = {r["metric"]: r for r in csv.DictReader(f)}
        self.assertAlmostEqual(float(r2["share_below_cost_NO_CAR_sensitivity"]["mean"]), 0.14032179786488938)

    def test_nowcast_nogo(self):
        go = json.loads((ROOT / "research/september2026_income_nowcast/reports/GO_NOGO.json").read_text())
        self.assertEqual(go["decision"], "NO-GO")


class TenureDecomposition(unittest.TestCase):
    def test_audit_json_and_decomposition_add(self):
        audit = json.loads((ROOT / "audit.json").read_text())
        self.assertEqual(audit["excluded_by_primary_reason"]["unsupported_tenure"], 206820)
        decomp = json.loads((ROOT / "research/pilot_tenure_audit.json").read_text())
        d = decomp["decomposition_unweighted"]
        self.assertEqual(d["np_gt_0_and_TYPEHUGQ_not_1_group_quarters_TEN_missing"] + d["np_gt_0_and_TYPEHUGQ_1_and_TEN_eq_4_rent_free"], 206820)


class PublicRounding(unittest.TestCase):
    def test_one_decimal_percent(self):
        self.assertEqual(round(18.9918, 1), 19.0)
        self.assertEqual(round(14.0322, 1), 14.0)
