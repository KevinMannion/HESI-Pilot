import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gating import NATIONAL_HEADLINE_ENABLED
from prototype_runner import (
    canonical_calculation_hash,
    load_scenario_file,
    run_reviewer_prototype,
    write_reviewer_prototype_run,
)

SCEN_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "prototype_scenarios"
GOLDEN = SCEN_DIR / "canonical_hashes_v0.1.json"


class PrototypeReproducibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.golden = json.loads(GOLDEN.read_text())

    def test_national_headline_disabled(self):
        self.assertFalse(NATIONAL_HEADLINE_ENABLED)

    def test_canonical_hashes_match_golden(self):
        for scenario_id, expect in self.golden.items():
            scenario = load_scenario_file(SCEN_DIR / f"{scenario_id}.json")
            payload = run_reviewer_prototype(scenario)
            got = canonical_calculation_hash(payload["audit"])
            self.assertEqual(
                expect["canonical_calculation_sha256"],
                got,
                msg=f"canonical hash drift for {scenario_id}",
            )
            self.assertEqual(payload["reviewer_prototype"]["status"], expect["status"])
            self.assertIsNone(
                payload["reviewer_prototype"]["approved_hesi_economic_security_classification"]
            )
            self.assertFalse(payload["reviewer_prototype"]["approved_status_enabled"])

    def test_complete_provisional_has_six_numeric_costs_and_ratio(self):
        scenario = load_scenario_file(SCEN_DIR / "complete_provisional_al_family.json")
        payload = run_reviewer_prototype(scenario)
        rp = payload["reviewer_prototype"]
        self.assertEqual(rp["status"], "COMPLETE_PROVISIONAL")
        self.assertIsNotNone(rp["provisional_six_component_essential_annual_usd"])
        self.assertIsNotNone(rp["provisional_resources_to_essential_ratio"])
        self.assertFalse(payload["audit"]["adequacy"]["computable"])

    def test_partial_three_pillar_unresolved(self):
        scenario = load_scenario_file(SCEN_DIR / "partial_three_pillar_synthetic.json")
        payload = run_reviewer_prototype(scenario)
        self.assertEqual(payload["reviewer_prototype"]["status"], "PARTIAL_UNRESOLVED")
        unpriced = payload["reviewer_prototype"]["unpriced_or_blocked_components"]
        self.assertTrue({"healthcare", "childcare", "other_necessities"}.issubset(set(unpriced)))

    def test_cli_writes_manifest_and_stable_canonical(self):
        scenario = load_scenario_file(SCEN_DIR / "partial_missing_disposable.json")
        payload = run_reviewer_prototype(scenario)
        with tempfile.TemporaryDirectory() as td:
            paths = write_reviewer_prototype_run(Path(td), payload, run_id="repro_test")
            manifest = json.loads(paths["manifest"].read_text())
            self.assertEqual(
                manifest["canonical_calculation_sha256"],
                payload["canonical_calculation_sha256"],
            )
            self.assertIn("git_commit", manifest)
            self.assertIn("volatile_metadata_separated", manifest)


if __name__ == "__main__":
    unittest.main()
