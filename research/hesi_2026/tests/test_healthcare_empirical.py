import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from components.healthcare import HealthcareComponent
from sources.cms_rates import validate_rate_file
from sources.healthcare_benchmark import second_lowest_silver_monthly, slcsp_monthly
from sources.healthcare_empirical import price_healthcare_annual, verify_healthcare_sources
from sources.pinned import verify_all_pins

REF_FIXTURE_SLCSP_MONTHLY_AGE40 = 475.0
REF_FAMILY_MONTHLY_HOUSEHOLD = 810.0  # household one-plan SLCSP ages 40+10 in sample CSV


class HealthcareEmpirical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        verify_all_pins()

    def test_cms_rate_file_validates(self):
        path = Path(__file__).resolve().parents[1] / "fixtures" / "cms2026_marketplace_rates_sample.csv"
        meta = validate_rate_file(path, business_year=2026)
        self.assertGreaterEqual(meta["silver_row_count"], 3)
        self.assertEqual(meta["business_year"], 2026)

    def test_slcsp_second_lowest_silver_age40(self):
        path = Path(__file__).resolve().parents[1] / "fixtures" / "cms2026_marketplace_rates_sample.csv"
        from sources.cms_rates import load_cms_rate_rows

        rows = load_cms_rate_rows(path, business_year=2026)
        monthly = slcsp_monthly(rows, rating_area_id="AL_RA01", age=40)
        self.assertEqual(monthly, REF_FIXTURE_SLCSP_MONTHLY_AGE40)
        self.assertEqual(second_lowest_silver_monthly([450.0, 475.0, 500.0]), 475.0)

    def test_household_healthcare_annual_two_members(self):
        hh = {
            "puma_geoid": "0100100",
            "state_code": "AL",
            "members": [{"age": 40}, {"age": 10}],
        }
        detail = price_healthcare_annual(
            hh,
            rates_pin_key="cms2026_marketplace_rates_sample",
            crosswalk_pin_key="puma_to_marketplace_rating_area_sample",
        )
        self.assertEqual(detail["monthly_usd"], REF_FAMILY_MONTHLY_HOUSEHOLD)
        self.assertEqual(detail["benchmark_rule"], "second_lowest_silver")
        self.assertEqual(detail["benchmark_construction"]["method"], "single_plan_household_second_lowest_silver")

    def test_healthcare_component_empirical_mode(self):
        hh = {"puma_geoid": "0100100", "members": [{"age": 40}]}
        ctx = {
            "calculation_mode": "empirical_pinned",
            "healthcare_policy_approved": True,
            "healthcare_rates_pin_key": "cms2026_marketplace_rates_sample",
            "healthcare_crosswalk_pin_key": "puma_to_marketplace_rating_area_sample",
        }
        result = HealthcareComponent().price(hh, context=ctx)
        self.assertEqual(result.missing_status.value, "priced")
        self.assertEqual(result.annual_usd, REF_FIXTURE_SLCSP_MONTHLY_AGE40 * 12)
        self.assertTrue(result.policy_approved)

    def test_verify_healthcare_sources_all_pairs_constructible(self):
        report = verify_healthcare_sources(business_year=2026)
        bench = report["benchmark_construction"]
        self.assertEqual(bench["constructible_pairs"], bench["total_pairs"])


if __name__ == "__main__":
    unittest.main()
