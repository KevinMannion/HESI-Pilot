"""Tests for provisional five-tier classification (engineering thresholds only)."""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from classification.provisional_five_tier import (
    AFFORDABILITY_BOUNDARY_RATIO,
    ProvisionalClassificationError,
    ProvisionalTierThresholds,
    classify_provisional_five_tier,
    assign_tier_from_ratio,
)
from classification.sensitivity import compare_classifications, sweep_assumption_variants, summarize_sensitivity
from components.other_essentials_interface import price_other_essentials_o_unresolved

# Test-only thresholds — not science-approved.
TEST_THRESHOLDS = ProvisionalTierThresholds(0.5, 0.85, 1.0, 1.25)


def _six_costs(**overrides: float) -> dict[str, float]:
    base = {
        "housing": 10000.0,
        "food": 8000.0,
        "transportation": 6000.0,
        "healthcare": 5000.0,
        "childcare": 4000.0,
        "other_necessities": 3000.0,
    }
    base.update(overrides)
    return base


class ProvisionalFiveTier(unittest.TestCase):
    def test_complete_six_costs_and_tier(self):
        costs = _six_costs()
        c = sum(costs.values())
        d = c * 1.3
        out = classify_provisional_five_tier(
            disposable_usd=d,
            costs=costs,
            tier_thresholds=TEST_THRESHOLDS,
        )
        self.assertEqual(out.status, "complete")
        self.assertAlmostEqual(out.total_essential_c_usd, c)
        self.assertAlmostEqual(out.annual_surplus_usd, d - c)
        self.assertAlmostEqual(out.affordability_ratio, d / c, places=5)
        self.assertEqual(out.tier_number, 5)

    def test_missing_cost_fail_closed(self):
        costs = _six_costs()
        del costs["other_necessities"]
        out = classify_provisional_five_tier(disposable_usd=50000, costs=costs)
        self.assertEqual(out.status, "unresolved")
        self.assertIsNone(out.total_essential_c_usd)
        self.assertIn("missing_component:other_necessities", out.blockers)

    def test_zero_essential_total(self):
        costs = {k: 0.0 for k in _six_costs()}
        out = classify_provisional_five_tier(disposable_usd=1000, costs=costs)
        self.assertEqual(out.status, "unresolved")
        self.assertIn("zero_or_negative_essential_total", out.blockers)

    def test_negative_disposable_allowed(self):
        costs = _six_costs()
        c = sum(costs.values())
        out = classify_provisional_five_tier(
            disposable_usd=-1000,
            costs=costs,
            tier_thresholds=TEST_THRESHOLDS,
        )
        self.assertEqual(out.status, "complete")
        self.assertLess(out.annual_surplus_usd or 0, 0)
        self.assertEqual(out.tier_number, 1)

    def test_exact_affordability_boundary_r1(self):
        costs = _six_costs()
        c = sum(costs.values())
        out = classify_provisional_five_tier(
            disposable_usd=c,
            costs=costs,
            tier_thresholds=TEST_THRESHOLDS,
        )
        self.assertAlmostEqual(out.affordability_ratio, AFFORDABILITY_BOUNDARY_RATIO)
        self.assertEqual(out.tier_number, 4)

    def test_exact_tier_boundary(self):
        costs = _six_costs()
        c = sum(costs.values())
        d = c * 1.0
        out = classify_provisional_five_tier(disposable_usd=d, costs=costs, tier_thresholds=TEST_THRESHOLDS)
        self.assertEqual(out.tier_number, 4)
        n, _, _ = assign_tier_from_ratio(1.0, TEST_THRESHOLDS)
        self.assertEqual(n, 4)

    def test_thresholds_must_be_unapproved(self):
        bad = ProvisionalTierThresholds(0.5, 0.85, 1.0, 1.25, policy_approved=True)
        with self.assertRaises(ProvisionalClassificationError):
            bad.validate()

    def test_configuration_change_moves_tier(self):
        costs = _six_costs()
        c = sum(costs.values())
        tight = ProvisionalTierThresholds(0.9, 1.0, 1.1, 1.2)
        loose = ProvisionalTierThresholds(0.3, 0.5, 0.7, 0.9)
        r = 0.88
        d = c * r
        before = classify_provisional_five_tier(disposable_usd=d, costs=costs, tier_thresholds=tight)
        after = classify_provisional_five_tier(disposable_usd=d, costs=costs, tier_thresholds=loose)
        self.assertNotEqual(before.tier_number, after.tier_number)

    def test_nonfinite_disposable(self):
        out = classify_provisional_five_tier(disposable_usd=float("nan"), costs=_six_costs())
        self.assertEqual(out.status, "unresolved")
        self.assertIn("nonfinite_disposable", out.blockers)

    def test_sensitivity_affordability_flip(self):
        costs = _six_costs()
        c = sum(costs.values())
        base = classify_provisional_five_tier(disposable_usd=c * 0.95, costs=costs, tier_thresholds=TEST_THRESHOLDS)
        after = classify_provisional_five_tier(disposable_usd=c * 1.05, costs=costs, tier_thresholds=TEST_THRESHOLDS)
        delta = compare_classifications(household_id="h1", before=base, after=after)
        self.assertTrue(delta.crossed_affordability_boundary)

    def test_sensitivity_sweep(self):
        costs = _six_costs()
        c = sum(costs.values())
        recs = [{"household_id": "h1", "disposable_usd": c * 0.9, "costs": costs, "tier_thresholds": TEST_THRESHOLDS}]
        variants = [{"label": "higher_d", "disposable_usd": c * 1.2}]
        deltas = sweep_assumption_variants(recs, variants)
        summary = summarize_sensitivity(deltas)
        self.assertEqual(summary["national_weights_applied"], False)
        self.assertIsNone(summary["confidence_intervals"])


class OtherEssentialsInterface(unittest.TestCase):
    def test_sprint2e_unresolved(self):
        res = price_other_essentials_o_unresolved({"state_code": "AL"}, context={})
        self.assertEqual(res.missing_status.value, "missing_unapproved_policy")
        self.assertIsNone(res.annual_usd)
        self.assertIn("apparel", res.metadata["other_essentials_vector_spec"]["categories"])


if __name__ == "__main__":
    unittest.main()
