import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.source_register import SourceRegisterAbortError
from components.childcare import ChildcareComponent
from prototype_runner import load_scenario_file, run_reviewer_prototype

SCEN_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "prototype_scenarios"
SOURCE_BACKED = SCEN_DIR / "source_backed_al_family_2026.json"


def _bundle_mounted() -> bool:
    return bool(os.environ.get("HESI_DATA_ROOT"))


class SourceBackedPrototype(unittest.TestCase):
    def test_childcare_register_fail_closed_without_bundle(self):
        scenario = load_scenario_file(SOURCE_BACKED)
        ctx = scenario["cost_context"]
        prior = os.environ.pop("HESI_DATA_ROOT", None)
        try:
            with self.assertRaises(SourceRegisterAbortError):
                ChildcareComponent().price(
                    scenario["household"],
                    context=ctx,
                )
        finally:
            if prior is not None:
                os.environ["HESI_DATA_ROOT"] = prior

    @unittest.skipUnless(_bundle_mounted(), "HESI_DATA_ROOT required for P4-C01")
    def test_source_backed_childcare_ndcp_2022_observed(self):
        scenario = load_scenario_file(SOURCE_BACKED)
        res = ChildcareComponent().price(scenario["household"], context=scenario["cost_context"])
        self.assertEqual(res.missing_status.value, "priced")
        self.assertFalse(res.policy_approved)
        self.assertIn("2022", str(res.source_vintage or res.metadata.get("ndcp_study_year_observed", "")))
        self.assertEqual(res.metadata.get("cpi_bridge", {}).get("bridge_key", ""), "none")
        self.assertIn("register", res.metadata.get("ndcp_source", {}).get("ingest_mode", ""))

    @unittest.skipUnless(_bundle_mounted(), "HESI_DATA_ROOT required for BLS CE registers")
    def test_source_backed_partial_due_to_other_necessities(self):
        payload = run_reviewer_prototype(load_scenario_file(SOURCE_BACKED))
        self.assertEqual(payload["reviewer_prototype"]["status"], "PARTIAL_UNRESOLVED")
        other = next(c for c in payload["audit"]["essential_costs"] if c["component"] == "other_necessities")
        self.assertEqual(other["missing_status"], "missing_data")
        self.assertIn("unapproved", other["notes"].lower())

    @unittest.skipUnless(_bundle_mounted(), "HESI_DATA_ROOT required")
    def test_mapping_doc_present(self):
        mapping = json.loads(
            (SCEN_DIR / "al_puma_0101403_jefferson_county_01073_mapping.json").read_text()
        )
        self.assertEqual(mapping["ndcp_county_fips"], "01073")
        self.assertEqual(mapping["jefferson_county_fips"], "01073")
        self.assertEqual(mapping["puma_geoid"], "0101403")
        self.assertTrue(mapping["overlap_evidence"]["puma0100100_jefferson_incompatible"])


import importlib.util

HAS_PE = importlib.util.find_spec("policyengine_us") is not None


@unittest.skipUnless(HAS_PE, "policyengine-us not installed")
class PolicyEngineHouseholdTy2026(unittest.TestCase):
    def test_married_couple_one_child_reproducible(self):
        from resources.policyengine_ty2026 import build_synthetic_household_ty2026, calculate_ty2026_household

        situation = build_synthetic_household_ty2026(
            state_code="AL",
            primary_adult_age=35,
            spouse_adult_age=33,
            child_ages=[4],
            primary_employment_income=48000,
            spouse_employment_income=24000,
        )
        self.assertIn("adult_primary", situation["people"])
        hh = {
            "state_code": "AL",
            "members": [{"age": 35}, {"age": 33}, {"age": 4}],
            "policyengine_synthetic": {
                "primary_employment_income": 48000,
                "spouse_employment_income": 24000,
            },
        }
        a = calculate_ty2026_household(hh)
        b = calculate_ty2026_household(hh)
        self.assertEqual(a["income_tax_household_usd"], b["income_tax_household_usd"])
        self.assertTrue(a["inputs_labeled_hypothetical"])
        self.assertIn("snap_benefit", a["unresolved_components"])


if __name__ == "__main__":
    unittest.main()
