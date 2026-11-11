import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sources.bls_ce_workbook import BlsCeWorkbookError, extract_ce_observed_national_means


@unittest.skipUnless(bool(os.environ.get("HESI_DATA_ROOT")), "HESI_DATA_ROOT required")
class BlsCeWorkbook(unittest.TestCase):
    def test_extract_cy2025_quintile_and_size_means(self):
        obs = extract_ce_observed_national_means()
        self.assertIn("P4-O01", obs["source_ids"])
        q2 = obs["table_1101_second_quintile_mean_annual_usd"]
        two = obs["table_1400_two_or_more_people_mean_annual_usd"]
        self.assertGreater(q2, 40000)
        self.assertGreater(two, q2)
        self.assertFalse(obs["policy_approved"])

    def test_essential_cost_path_unresolved(self):
        from sources.bls_ce_workbook import price_other_ce_register_or_unresolved

        with self.assertRaises(BlsCeWorkbookError) as ctx:
            price_other_ce_register_or_unresolved({"np": 3})
        self.assertIn("unapproved", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
