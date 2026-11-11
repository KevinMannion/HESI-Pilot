import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from policies import DEFAULT_UNIVERSE_POLICIES
from universe import accumulate_universe, classify_household, tenure_label


class UniverseSynthetic(unittest.TestCase):
    def test_tenure_rent_free_included_in_ledger(self):
        records = [
            {
                "weight": 100.0,
                "ten": 4,
                "adults": 1,
                "children": 0,
                "partners": 0,
                "np": 1,
                "n_infant": 0,
                "geography_complete": True,
                "composition_valid": True,
                "monthly_joint_cost": 2000.0,
            },
            {
                "weight": 50.0,
                "ten": 3,
                "adults": 2,
                "children": 1,
                "partners": 1,
                "np": 3,
                "n_infant": 0,
                "geography_complete": True,
                "composition_valid": True,
                "monthly_joint_cost": 3000.0,
            },
        ]
        ledger, tenure = accumulate_universe(records, policies=DEFAULT_UNIVERSE_POLICIES)
        self.assertAlmostEqual(ledger.included_weight, 150.0)
        self.assertAlmostEqual(tenure.weights["rent_free"], 100.0)
        self.assertAlmostEqual(tenure.weights["renter"], 50.0)
        ledger.reconcile()

    def test_exclusion_categories_sum(self):
        records = [
            {"weight": 10, "ten": 1, "adults": 1, "children": 0, "partners": 0, "np": 1, "n_infant": 0, "geography_complete": False, "composition_valid": True},
            {"weight": 5, "ten": 1, "adults": 1, "children": 0, "partners": 0, "np": 2, "n_infant": 0, "geography_complete": True, "composition_valid": False},
            {"weight": 7, "ten": 1, "adults": 5, "children": 0, "partners": 0, "np": 5, "n_infant": 0, "geography_complete": True, "composition_valid": True},
            {"weight": 3, "ten": 1, "adults": 1, "children": 1, "partners": 0, "np": 2, "n_infant": 1, "geography_complete": True, "composition_valid": True},
            {"weight": 100, "ten": 2, "adults": 2, "children": 0, "partners": 1, "np": 2, "n_infant": 0, "geography_complete": True, "composition_valid": True, "monthly_joint_cost": 1.0},
        ]
        ledger, _ = accumulate_universe(records)
        self.assertEqual(classify_household(records[0], policies=DEFAULT_UNIVERSE_POLICIES, geography_ok=False, composition_ok=True), "geography_excluded")
        self.assertEqual(ledger.geography_excluded_weight, 10)
        self.assertEqual(ledger.composition_excluded_weight, 5)
        self.assertEqual(ledger.over4_excluded_weight, 7)
        self.assertEqual(ledger.infant_excluded_weight, 3)
        self.assertEqual(ledger.included_weight, 100)

    def test_tenure_label_other(self):
        self.assertEqual(tenure_label(9), "other_tenure")


if __name__ == "__main__":
    unittest.main()
