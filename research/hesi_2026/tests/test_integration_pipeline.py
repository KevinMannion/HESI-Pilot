import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.manifest import build_audit_manifest, write_audit_manifest
from audit.schema import AUDIT_SCHEMA_VERSION
from pipeline import run_household_pipeline, write_pipeline_result

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_household.json"


class IntegrationPipeline(unittest.TestCase):
    def test_synthetic_household_end_to_end(self):
        household = json.loads(FIXTURE.read_text())
        ctx = {
            "housing_vintage": "synthetic_fixture",
            "food_vintage": "synthetic_fixture",
            "transport_vintage": "synthetic_fixture",
            "housing_policy_approved": True,
            "food_policy_approved": True,
            "transport_policy_approved": True,
        }
        result = run_household_pipeline(household, cost_context=ctx, use_policyengine=False)
        audit = result["audit"]
        self.assertEqual(audit["audit_schema_version"], AUDIT_SCHEMA_VERSION)
        self.assertEqual(len(audit["essential_costs"]), 6)
        unpriced = [c["component"] for c in audit["essential_costs"] if c["missing_status"] != "priced"]
        self.assertEqual(set(unpriced), {"healthcare", "childcare", "other_necessities"})
        self.assertFalse(result["adequacy"]["computable"])
        self.assertIsNotNone(result["adequacy"]["partial_three_component_ratio"])
        self.assertIn("rent_free", audit["frame"]["tenure"])

    def test_scratch_audit_manifest(self):
        household = json.loads(FIXTURE.read_text())
        result = run_household_pipeline(household, cost_context={"housing_policy_approved": True, "food_policy_approved": True, "transport_policy_approved": True, "housing_vintage": "x", "food_vintage": "x", "transport_vintage": "x"})
        with tempfile.TemporaryDirectory() as td:
            write_pipeline_result(Path(td), result)
            manifest = build_audit_manifest(
                run_id="test_run",
                output_dir=Path(td),
                comparison_target="none",
                git_commit=None,
                parity_status="NOT_APPLICABLE",
            )
            path = write_audit_manifest(Path(td), manifest)
            self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
