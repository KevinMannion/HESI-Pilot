import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nd_accounting import (
    DoubleCountError,
    SubsidyAllocationProbe,
    assert_ptc_cost_only,
    assert_refundable_resources_only,
    assert_snap_disposable_only,
    verify_nd_subsidy_invariants,
)


class NdDoubleCountSynthetic(unittest.TestCase):
    def test_compliant_probe_passes(self):
        probe = SubsidyAllocationProbe(
            ptc_applied_to_healthcare_cost_usd=2400.0,
            snap_applied_to_disposable_usd=1800.0,
            refundable_credits_applied_to_disposable_usd=500.0,
        )
        verify_nd_subsidy_invariants(probe)

    def test_ptc_in_disposable_fails(self):
        probe = SubsidyAllocationProbe(
            ptc_applied_to_healthcare_cost_usd=100.0,
            ptc_applied_to_disposable_usd=50.0,
        )
        with self.assertRaises(DoubleCountError):
            assert_ptc_cost_only(probe)
        with self.assertRaises(DoubleCountError):
            verify_nd_subsidy_invariants(probe)

    def test_snap_in_food_cost_fails(self):
        probe = SubsidyAllocationProbe(snap_applied_to_disposable_usd=100.0, snap_applied_to_food_cost_usd=1.0)
        with self.assertRaises(DoubleCountError):
            assert_snap_disposable_only(probe)

    def test_refundable_in_costs_fails(self):
        probe = SubsidyAllocationProbe(
            refundable_credits_applied_to_disposable_usd=200.0,
            refundable_credits_applied_to_costs_usd=0.01,
        )
        with self.assertRaises(DoubleCountError):
            assert_refundable_resources_only(probe)

    def test_employer_premium_charged_fails(self):
        probe = SubsidyAllocationProbe(employer_premium_charged_to_household_usd=120.0)
        with self.assertRaises(DoubleCountError):
            verify_nd_subsidy_invariants(probe)

    def test_ptc_only_in_healthcare_allowed_nonzero(self):
        probe = SubsidyAllocationProbe(ptc_applied_to_healthcare_cost_usd=5000.0)
        verify_nd_subsidy_invariants(probe)
        self.assertGreater(probe.ptc_applied_to_healthcare_cost_usd, 0)

    def test_from_mapping_round_trip(self):
        probe = SubsidyAllocationProbe.from_mapping({"snap_applied_to_disposable_usd": 42})
        self.assertEqual(probe.snap_applied_to_disposable_usd, 42.0)


if __name__ == "__main__":
    unittest.main()
