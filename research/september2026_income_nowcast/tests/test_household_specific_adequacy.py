import unittest
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from household_specific_adequacy import (
    FROZEN_R24_MEAN_MONTH,
    backtest_protocol,
    household_specific_share,
    uniform_threshold_share,
)


class ProxyIsNotHouseholdSpecific(unittest.TestCase):
    def test_fixture_where_uniform_and_household_shares_disagree(self):
        # Two households, equal weight. Mean cost is the R2.4 mean.
        # Household A: income just below the mean but above its own cheap cost.
        # Household B: income above the mean but below its own expensive cost.
        income = np.array([2890.0, 2900.0])
        cost = np.array([2000.0, 4000.0])
        w = np.array([1.0, 1.0])
        uniform = uniform_threshold_share(income, w, FROZEN_R24_MEAN_MONTH)
        specific = household_specific_share(income, cost, w)
        self.assertAlmostEqual(uniform, 0.5)
        self.assertAlmostEqual(specific, 0.5)
        # Swap A's income above its cost and the mean: uniform share 0, specific still 0.5
        income2 = np.array([3000.0, 2900.0])
        self.assertAlmostEqual(uniform_threshold_share(income2, w), 0.0)
        self.assertAlmostEqual(household_specific_share(income2, cost, w), 0.5)

    def test_protocol_not_a_nowcast(self):
        p = backtest_protocol()
        self.assertEqual(p["nowcast"], "NO-GO")
        self.assertEqual(p["status"], "DESIGNED_NOT_NATIONALLY_EXECUTED")
        self.assertIn("not the $2,894.91 mean", p["cost"])


if __name__ == "__main__":
    unittest.main()
