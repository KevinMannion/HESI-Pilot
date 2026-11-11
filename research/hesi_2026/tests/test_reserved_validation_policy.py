"""Synthetic tests for CPS ASEC 2026 reserved validation policy (no reserved files)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.reserved_validation_policy import (
    DESIGNATION_PRIOR_EXPOSURE,
    LABEL_HISTORICAL_BENCHMARK,
    ReservedValidationAccessError,
    WorkflowKind,
    assert_official_entry_allowed,
    collect_reserved_hits,
    historical_benchmark_label,
)


class ReservedValidationPolicy(unittest.TestCase):
    def test_benign_context_no_hits(self):
        self.assertEqual(
            collect_reserved_hits({"pin": "puma_fmr_screened_fy2026", "puma": "0101403"}),
            [],
        )

    def test_synthetic_zip_path_blocked(self):
        with self.assertRaises(ReservedValidationAccessError):
            assert_official_entry_allowed(
                workflow=WorkflowKind.VALIDATION,
                paths=["/tmp/SYNTHETIC_NOT_REAL/asecpub26csv.zip"],
            )

    def test_sha256_prefix_blocked(self):
        with self.assertRaises(ReservedValidationAccessError):
            assert_official_entry_allowed(
                workflow=WorkflowKind.CALIBRATION,
                context={"note": "re-hash fe819d0d2fc4470c confirmed"},
            )

    def test_derived_json_name_blocked(self):
        with self.assertRaises(ReservedValidationAccessError):
            assert_official_entry_allowed(
                workflow=WorkflowKind.VALIDATION,
                paths=["reports/ASEC_2026_HOUSEHOLD_SOURCE_TOTALS.json"],
            )

    def test_p60_fragment_blocked(self):
        with self.assertRaises(ReservedValidationAccessError):
            assert_official_entry_allowed(
                workflow=WorkflowKind.MODELING,
                context={"report": "census/p60-289.pdf"},
            )

    def test_historical_benchmark_label(self):
        meta = historical_benchmark_label(
            artifact_kind="phase3_sidecar",
            reference="INCOME_NOWCAST_VALIDATION_REPORT.json#asec_independent_benchmark",
        )
        self.assertEqual(meta["validation_designation"], DESIGNATION_PRIOR_EXPOSURE)
        self.assertEqual(meta["benchmark_class"], LABEL_HISTORICAL_BENCHMARK)
        self.assertTrue(meta["not_blind_independent_validation"])


class ReservedPipelineIntegration(unittest.TestCase):
    def test_pipeline_blocks_reserved_in_cost_context(self):
        from pipeline import run_household_pipeline

        hh = {"ten": 1, "geography_complete": True, "composition_valid": True, "weight": 1.0}
        ctx = {"validation_asec_path": "/data/asecpub26csv.zip"}
        with self.assertRaises(ReservedValidationAccessError):
            run_household_pipeline(hh, cost_context=ctx)

    def test_prototype_blocks_reserved_scenario_ref(self):
        from prototype_runner import run_reviewer_prototype

        scenario = {
            "scenario_id": "bad",
            "household": {"ten": 1, "geography_complete": True, "composition_valid": True},
            "cost_context": {},
            "benchmark_sha256": "f4d61659cae9d6698405b17e246abbac09ea65f8a3e4587e291ab4363af9ac85",
        }
        with self.assertRaises(ReservedValidationAccessError):
            run_reviewer_prototype(scenario)


class TrackDLoaderBlocked(unittest.TestCase):
    def test_guard_import_blocks_zip_arg(self):
        root = Path(__file__).resolve().parents[2] / "september2026_income_nowcast" / "src"
        sys.path.insert(0, str(root))
        from _reserved_validation_guard import enforce_blocked

        with self.assertRaises(ReservedValidationAccessError):
            enforce_blocked(
                workflow="official_calibration",
                paths=["/synthetic/asecpub26csv.zip"],
            )


if __name__ == "__main__":
    unittest.main()
