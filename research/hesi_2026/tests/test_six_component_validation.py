import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from components.childcare import ChildcareComponent
from components.healthcare import HealthcareComponent
from components.other_necessities import OtherNecessitiesComponent
from components.registry import default_six_component_registry
from gating import NATIONAL_HEADLINE_ENABLED, six_component_complete
from sources.cms_rates import RateRow, load_cms_rate_rows
from sources.healthcare_benchmark import household_slcsp_monthly, sum_of_individual_slcsp_monthly
from sources.healthcare_empirical import price_healthcare_annual

SAMPLE_RATES = Path(__file__).resolve().parents[1] / "fixtures" / "cms2026_marketplace_rates_sample.csv"


class SixComponentValidation(unittest.TestCase):
    def test_national_headline_stays_disabled(self):
        self.assertFalse(NATIONAL_HEADLINE_ENABLED)

    def test_healthcare_geography_mismatch_fails_closed(self):
        hh = {"puma_geoid": "9999900", "members": [{"age": 40}]}
        with self.assertRaises(ValueError):
            price_healthcare_annual(hh)

    def test_healthcare_missing_member_ages(self):
        hh = {"puma_geoid": "0100100", "adults": 2, "children": 1}
        with self.assertRaises(ValueError):
            price_healthcare_annual(hh)

    def test_household_slcsp_not_sum_of_individual_picks(self):
        rows = load_cms_rate_rows(SAMPLE_RATES, business_year=2026)
        ages = [40, 10]
        household, _ = household_slcsp_monthly(rows, rating_area_id="AL_RA01", member_ages=ages)
        anti = sum_of_individual_slcsp_monthly(rows, rating_area_id="AL_RA01", member_ages=ages)
        detail = price_healthcare_annual(
            {"puma_geoid": "0100100", "members": [{"age": 40}, {"age": 10}]},
            rates_pin_key="cms2026_marketplace_rates_sample",
            crosswalk_pin_key="puma_to_marketplace_rating_area_sample",
        )
        self.assertEqual(detail["monthly_usd"], household)
        self.assertEqual(detail["anti_pattern_sum_individual_slcsp_monthly_usd"], anti)

    def test_childcare_missing_state_in_empirical_mode(self):
        hh = {"members": [{"age": 4}]}
        ctx = {"calculation_mode": "empirical_pinned"}
        res = ChildcareComponent().price(hh, context=ctx)
        self.assertEqual(res.missing_status.value, "missing_data")

    def test_childcare_policy_gate_defaults_false(self):
        hh = {"state_code": "AL", "members": [{"age": 4}]}
        ctx = {"calculation_mode": "empirical_pinned"}
        res = ChildcareComponent().price(hh, context=ctx)
        self.assertEqual(res.missing_status.value, "priced")
        self.assertFalse(res.policy_approved)

    def test_other_necessities_excludes_double_count_in_metadata(self):
        hh = {"np": 2, "members": [{"age": 30}, {"age": 28}]}
        ctx = {"calculation_mode": "empirical_pinned"}
        res = OtherNecessitiesComponent().price(hh, context=ctx)
        self.assertIn("food", res.metadata.get("excludes", ""))

    def test_six_component_policy_approval_blockers(self):
        hh = {
            "puma_geoid": "0100100",
            "state_code": "AL",
            "adults": 2,
            "children": 1,
            "partners": 1,
            "np": 3,
            "members": [{"age": 35}, {"age": 33}, {"age": 4}],
        }
        ctx = {
            "calculation_mode": "empirical_pinned",
            "geography_pin_key": "puma_fmr_screened_fy2026",
            "healthcare_rates_pin_key": "cms2026_rate_puf_bounded_al_ra1",
            "healthcare_crosswalk_pin_key": "puma_to_marketplace_rating_area_bounded_2026",
        }
        costs = [c.price(hh, context=ctx) for c in default_six_component_registry()]
        ok, blockers = six_component_complete([c.to_dict() for c in costs])
        self.assertFalse(ok)
        self.assertTrue(any(b.startswith("unapproved:") for b in blockers))

    def test_healthcare_component_prices_bounded_extract(self):
        hh = {"puma_geoid": "0100100", "members": [{"age": 40}]}
        ctx = {
            "calculation_mode": "empirical_pinned",
            "healthcare_rates_pin_key": "cms2026_rate_puf_bounded_al_ra1",
            "healthcare_crosswalk_pin_key": "puma_to_marketplace_rating_area_bounded_2026",
        }
        res = HealthcareComponent().price(hh, context=ctx)
        self.assertEqual(res.missing_status.value, "priced")
        self.assertGreater(res.annual_usd or 0, 0)


if __name__ == "__main__":
    unittest.main()
