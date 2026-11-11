import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from components.food import FoodComponent
from components.housing import HousingComponent
from components.transportation import TransportationComponent
from components.base import MissingStatus
from gating import NATIONAL_HEADLINE_ENABLED, six_component_complete
from pipeline import run_household_pipeline
from sources.food_empirical import price_food_annual
from sources.housing_empirical import price_housing_annual
from sources.pinned import verify_all_pins
from sources.transport_empirical import price_transport_annual

# Independently checked: USDA Sept 2026 thrifty, 1 adult male 20-50, size factor 1.2
REF_FOOD_ANNUAL_ONE_ADULT = 4593.6
# synthetic PUMA 0100100, 2 BR benchmark 900/mo
REF_HOUSING_FIXTURE_ANNUAL = 10800.0
REF_TRANSPORT_REFERENCE_ANNUAL = 7264.7


class EmpiricalComponentNumerics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        verify_all_pins()

    def test_food_empirical_matches_hand_arithmetic(self):
        hh = {"members": [{"age": 35, "sex": "Male"}]}
        detail = price_food_annual(hh, plan="thrifty")
        self.assertEqual(detail["annual_usd"], REF_FOOD_ANNUAL_ONE_ADULT)
        self.assertEqual(detail["input_sha256"], "90bc39d1a569073b9530ca0a78a4ccf19c781c4a42dd70c51a0bed9e1907602c")

    def test_housing_empirical_synthetic_fixture_puma(self):
        hh = {
            "puma_geoid": "0100100",
            "adults": 2,
            "children": 1,
            "partners": 1,
            "geography_complete": True,
        }
        detail = price_housing_annual(hh, geography_pin_key="synthetic_geography_fixture")
        self.assertEqual(detail["bedrooms"], 2)
        self.assertEqual(detail["monthly_usd"], 900.0)
        self.assertEqual(detail["annual_usd"], REF_HOUSING_FIXTURE_ANNUAL)

    def test_transport_empirical_pinned_reference_row(self):
        detail = price_transport_annual({})
        self.assertEqual(detail["annual_usd"], REF_TRANSPORT_REFERENCE_ANNUAL)
        self.assertIn("hypothetical", detail["scientific_status"])

    def test_empirical_mode_ignores_fixture_double_count(self):
        ctx = {"calculation_mode": "empirical_pinned", "geography_pin_key": "synthetic_geography_fixture"}
        hh = {
            "members": [{"age": 35, "sex": "Male"}],
            "food_annual_usd": 999999.0,
            "puma_geoid": "0100100",
            "adults": 2,
            "children": 1,
            "partners": 1,
        }
        food = FoodComponent().price(hh, context=ctx)
        self.assertEqual(food.annual_usd, REF_FOOD_ANNUAL_ONE_ADULT)
        housing = HousingComponent().price(hh, context=ctx)
        self.assertEqual(housing.annual_usd, REF_HOUSING_FIXTURE_ANNUAL)

    def test_missing_members_fails_without_default(self):
        food = FoodComponent().price({}, context={"calculation_mode": "empirical_pinned"})
        self.assertEqual(food.missing_status, MissingStatus.MISSING_DATA)

    def test_completeness_gate_blocks_production(self):
        self.assertFalse(NATIONAL_HEADLINE_ENABLED)
        hh = {
            "members": [{"age": 35, "sex": "Male"}],
            "puma_geoid": "0100100",
            "adults": 2,
            "children": 1,
            "partners": 1,
            "np": 3,
            "n_infant": 0,
            "ten": 3,
            "geography_complete": True,
            "composition_valid": True,
            "annual_gross_income_usd": 52000,
            "annual_disposable_usd": 47000,
        }
        ctx = {
            "calculation_mode": "empirical_pinned",
            "geography_pin_key": "synthetic_geography_fixture",
            "food_policy_approved": True,
            "housing_policy_approved": True,
            "transport_policy_approved": True,
        }
        result = run_household_pipeline(hh, cost_context=ctx)
        self.assertFalse(result["audit"]["release_gates"]["production_headline_allowed"])
        self.assertFalse(result["audit"]["release_gates"]["six_component_complete"])
        ok, blockers = six_component_complete(result["audit"]["essential_costs"])
        self.assertFalse(ok)
        self.assertTrue(any("healthcare" in b for b in blockers))

    def test_component_inventory_present(self):
        inv = Path(__file__).resolve().parents[1] / "sources" / "component_inventory.json"
        data = json.loads(inv.read_text())
        self.assertEqual(data["healthcare"]["status"], "not_implemented")


if __name__ == "__main__":
    unittest.main()
