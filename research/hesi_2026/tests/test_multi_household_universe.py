import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from universe import accumulate_universe

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_universe.json"


class MultiHouseholdUniverse(unittest.TestCase):
    def test_reconciles_frozen_r24_weights(self):
        data = json.loads(FIX.read_text())
        ledger, tenure = accumulate_universe(data["records"])
        self.assertAlmostEqual(ledger.occupied_weight, data["occupied_weight"], places=0)
        self.assertAlmostEqual(ledger.included_weight, data["included_weight"], places=0)
        ledger.reconcile(tolerance=1.0)
        self.assertAlmostEqual(
            tenure.weights["owner"] + tenure.weights["renter"] + tenure.weights["rent_free"] + tenure.weights["other_tenure"],
            ledger.included_weight,
            places=0,
        )
        self.assertAlmostEqual(tenure.weights["rent_free"], 2022837.0, places=0)
        self.assertAlmostEqual(ledger.composition_excluded_weight, 17463.0, places=0)


if __name__ == "__main__":
    unittest.main()
