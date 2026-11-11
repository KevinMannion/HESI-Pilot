import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from universe_audit_experimental import build_experimental_universe_audit


class UniverseAuditExperimental(unittest.TestCase):
    def test_reports_exclusions_tenure_and_reconciliation(self):
        records = [
            {"weight": 10, "ten": 1, "adults": 1, "children": 0, "partners": 0, "np": 1, "n_infant": 0, "geography_complete": False, "composition_valid": True},
            {"weight": 5, "ten": 3, "adults": 1, "children": 0, "partners": 0, "np": 2, "n_infant": 0, "geography_complete": True, "composition_valid": False},
            {"weight": 7, "ten": 2, "adults": 5, "children": 0, "partners": 0, "np": 5, "n_infant": 0, "geography_complete": True, "composition_valid": True},
            {"weight": 3, "ten": 4, "adults": 1, "children": 1, "partners": 0, "np": 2, "n_infant": 1, "geography_complete": True, "composition_valid": True},
            {
                "weight": 100,
                "ten": 2,
                "adults": 2,
                "children": 0,
                "partners": 1,
                "np": 2,
                "n_infant": 0,
                "geography_complete": True,
                "composition_valid": True,
                "monthly_joint_cost": 1.0,
            },
        ]
        audit = build_experimental_universe_audit(records)
        self.assertTrue(audit["reconciliation"]["partition_sums_to_occupied"])
        self.assertTrue(audit["reconciliation"]["tenure_included_sums_to_included"])
        self.assertTrue(audit["reconciliation"]["tenure_occupied_sums_to_occupied"])
        self.assertEqual(audit["weights"]["included_legacy"], 100.0)
        self.assertEqual(audit["weights"]["potential_readmission_weight_reported_not_applied"], 25.0)
        tenure = audit["tenure_all_occupied"]
        self.assertAlmostEqual(sum(tenure.values()), 125.0)
        self.assertIn("owner", tenure)
        self.assertIn("renter", tenure)
        self.assertIn("rent_free", tenure)

    def test_readmission_labels_present_on_excluded_only(self):
        records = [
            {"weight": 1, "ten": 1, "adults": 1, "children": 0, "partners": 0, "np": 1, "n_infant": 0, "geography_complete": False, "composition_valid": True},
        ]
        audit = build_experimental_universe_audit(records)
        self.assertEqual(len(audit["per_record_flags"]), 1)
        self.assertIn("potential_readmission_label", audit["per_record_flags"][0])


if __name__ == "__main__":
    unittest.main()
