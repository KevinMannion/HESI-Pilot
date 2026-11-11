import hashlib
import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.source_register import (
    load_s3_bounded_source_ids,
    load_source_register,
    validate_s3_bounded_pins,
    validate_source_register,
)
from tests.test_source_register_fail_closed import _write_min_register
from components.childcare import ChildcareComponent
from components.healthcare import HealthcareComponent
from components.housing import HousingComponent
from components.other_necessities import OtherNecessitiesComponent
from components.transportation import TransportationComponent
from gating import NATIONAL_HEADLINE_ENABLED
from resources.disposable import disposable_from_fixture
from sources.childcare_cpi_bridge import apply_cpi_bridge
from sources.housing_fmr_q4_schedule import select_fmr_vintage
from sources.ndcp_childcare import price_childcare_ndcp_county
from sources.transport_normative import assert_not_retired_flat_primary, price_transport_normative
from sources.transport_empirical import price_transport_annual
from sources.transport_normative import NormativeTransportError


@contextmanager
def _isolated_hesi_roots():
    """Point HESI_DATA_ROOT / HESI_SCRATCH_ROOT at empty temp dirs for deterministic pin checks."""
    prev_data = os.environ.get("HESI_DATA_ROOT")
    prev_scratch = os.environ.get("HESI_SCRATCH_ROOT")
    tmp = tempfile.TemporaryDirectory()
    data = Path(tmp.name) / "hesi-data"
    scratch = Path(tmp.name) / "scratch"
    data.mkdir()
    scratch.mkdir()
    os.environ["HESI_DATA_ROOT"] = str(data)
    os.environ["HESI_SCRATCH_ROOT"] = str(scratch)
    try:
        yield tmp, data, scratch
    finally:
        for key, prev in (("HESI_DATA_ROOT", prev_data), ("HESI_SCRATCH_ROOT", prev_scratch)):
            if prev is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = prev
        tmp.cleanup()


class Sprint2ASourceRegister(unittest.TestCase):
    def test_register_schema_loads(self):
        rows = load_source_register()
        self.assertGreater(len(rows), 100)

    def test_register_validation_no_mismatch_on_missing(self):
        report = validate_source_register(verify_bytes=True)
        self.assertIn(report["status"], ("PASS", "HASH_MISMATCH"))
        self.assertGreater(report["row_count"], 100)

    def test_s3_bounded_report(self):
        """Production allowlist + register: present and missing partition the allowlist (install-agnostic)."""
        want = load_s3_bounded_source_ids()
        s3 = validate_s3_bounded_pins()
        self.assertEqual(s3["s3_allowlist_count"], len(want))
        present = set(s3["present_verified"])
        missing = set(s3["missing_or_unverified"])
        self.assertEqual(present | missing, set(want))
        self.assertFalse(present & missing)
        self.assertEqual(len(present) + len(missing), len(want))
        for row in s3["detail"]:
            self.assertIn(row["source_id"], want)

    @patch("audit.source_register.load_s3_bounded_source_ids")
    def test_s3_bounded_isolated_all_files_missing(self, mock_allowlist):
        mock_allowlist.return_value = ["S3-M1", "S3-M2"]
        with _isolated_hesi_roots() as (tmp, _data, _scratch):
            reg = Path(tmp.name) / "mini_reg.csv"
            _write_min_register(
                reg,
                [
                    {
                        "source_id": "S3-M1",
                        "component": "test",
                        "local_path": "/workspace/hesi-data/missing/one.bin",
                        "sha256": "1" * 64,
                        "verification_status": "VERIFIED-PINNED",
                    },
                    {
                        "source_id": "S3-M2",
                        "component": "test",
                        "local_path": "/workspace/scratch/missing/two.whl",
                        "sha256": "2" * 64,
                        "verification_status": "VERIFIED-PINNED",
                    },
                ],
            )
            s3 = validate_s3_bounded_pins(register_path=reg)
        self.assertEqual(s3["s3_allowlist_count"], 2)
        self.assertEqual(s3["present_verified"], [])
        self.assertEqual(s3["missing_or_unverified"], ["S3-M1", "S3-M2"])
        for row in s3["detail"]:
            self.assertTrue(row.get("missing") or row.get("error"))

    @patch("audit.source_register.load_s3_bounded_source_ids")
    def test_s3_bounded_isolated_hash_mismatch(self, mock_allowlist):
        mock_allowlist.return_value = ["S3-BAD"]
        with _isolated_hesi_roots() as (tmp, data, _scratch):
            rel = "pins/bad.bin"
            target = data / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"on-disk-bytes")
            reg = Path(tmp.name) / "mini_reg.csv"
            _write_min_register(
                reg,
                [
                    {
                        "source_id": "S3-BAD",
                        "component": "test",
                        "local_path": f"/workspace/hesi-data/{rel}",
                        "sha256": "f" * 64,
                        "verification_status": "VERIFIED-PINNED",
                    },
                ],
            )
            s3 = validate_s3_bounded_pins(register_path=reg)
        self.assertEqual(s3["present_verified"], [])
        self.assertEqual(s3["missing_or_unverified"], ["S3-BAD"])
        detail = s3["detail"][0]
        self.assertFalse(detail["sha256_match"])
        self.assertNotEqual(detail["got"], detail["want"])

    @patch("audit.source_register.load_s3_bounded_source_ids")
    def test_s3_bounded_isolated_present_verified(self, mock_allowlist):
        with _isolated_hesi_roots() as (tmp, data, scratch):
            rel_data = "verified/data.csv"
            rel_scratch = "verified/pkg.whl"
            data_file = data / rel_data
            scratch_file = scratch / rel_scratch
            data_file.parent.mkdir(parents=True, exist_ok=True)
            scratch_file.parent.mkdir(parents=True, exist_ok=True)
            data_bytes = b"verified-data-bytes"
            scratch_bytes = b"verified-scratch-bytes"
            data_file.write_bytes(data_bytes)
            scratch_file.write_bytes(scratch_bytes)
            want_data = hashlib.sha256(data_bytes).hexdigest()
            want_scratch = hashlib.sha256(scratch_bytes).hexdigest()
            reg = Path(tmp.name) / "mini_reg.csv"
            _write_min_register(
                reg,
                [
                    {
                        "source_id": "S3-OK",
                        "component": "test",
                        "local_path": f"/workspace/hesi-data/{rel_data}",
                        "sha256": want_data,
                        "verification_status": "VERIFIED-PINNED",
                    },
                    {
                        "source_id": "S3-OK-SCRATCH",
                        "component": "test",
                        "local_path": f"/workspace/scratch/{rel_scratch}",
                        "sha256": want_scratch,
                        "verification_status": "VERIFIED-PINNED",
                    },
                ],
            )
            mock_allowlist.return_value = ["S3-OK", "S3-OK-SCRATCH", "S3-NOT-IN-REGISTER"]
            s3 = validate_s3_bounded_pins(register_path=reg)
        self.assertEqual(set(s3["present_verified"]), {"S3-OK", "S3-OK-SCRATCH"})
        self.assertEqual(s3["missing_or_unverified"], ["S3-NOT-IN-REGISTER"])
        self.assertEqual(s3["detail"][-1]["error"], "not_in_register")


class Sprint2AChildcare(unittest.TestCase):
    def test_ndcp_westchester_fixture(self):
        hh = {
            "county_fips": "36119",
            "members": [{"age": 1}, {"age": 4}],
        }
        detail = price_childcare_ndcp_county(hh, cpi_bridge="none")
        self.assertFalse(detail["policy_approved"])
        self.assertGreater(detail["annual_usd"], 0)

    def test_cpi_bridge_requires_explicit_factor(self):
        with self.assertRaises(ValueError):
            apply_cpi_bridge(bridge_key="owner_supplied_factor", factor=None)

    def test_component_ndcp_mode(self):
        hh = {"county_fips": "36119", "members": [{"age": 5}]}
        res = ChildcareComponent().price(hh, context={"calculation_mode": "ndcp_county"})
        self.assertEqual(res.missing_status.value, "priced")
        self.assertFalse(res.policy_approved)


class Sprint2AHealthcare(unittest.TestCase):
    def test_meps_bounds_distinct_coverage(self):
        emp = HealthcareComponent().price(
            {"state_code": "NY", "employer_coverage": True, "members": [{"age": 40}]},
            context={"calculation_mode": "meps_bounds"},
        )
        unins = HealthcareComponent().price(
            {"state_code": "NY", "members": [{"age": 40}]},
            context={"calculation_mode": "meps_bounds"},
        )
        emp_oop = (emp.metadata or {})["out_of_pocket"]["annual_usd"]
        unins_oop = (unins.metadata or {})["out_of_pocket"]["annual_usd"]
        self.assertGreater(unins_oop, emp_oop)
        self.assertEqual((emp.metadata or {})["coverage_type"], "employer")
        self.assertEqual((unins.metadata or {})["coverage_type"], "uninsured")


class Sprint2AOther(unittest.TestCase):
    def test_ce_fallback_unapproved_label(self):
        res = OtherNecessitiesComponent().price(
            {"np": 4},
            context={"calculation_mode": "bls_ce_fallback"},
        )
        self.assertFalse(res.policy_approved)
        self.assertIn("unapproved", (res.notes or "").lower())


class Sprint2AHousing(unittest.TestCase):
    def test_legacy_unchanged_without_schedule_flag(self):
        hh = {"puma_geoid": "0101201", "adults": 2, "children": 0, "partners": 1}
        leg = HousingComponent().price(hh, context={"calculation_mode": "empirical_pinned"})
        overlay = HousingComponent().price(
            hh,
            context={
                "calculation_mode": "fmr_q4_schedule_unapproved",
                "fmr_area_label": "santa_ana",
                "calendar_month": 11,
            },
        )
        self.assertEqual(leg.annual_usd, overlay.annual_usd)

    def test_napa_q4_fy26_rev_fixture(self):
        choice = select_fmr_vintage("napa", 11)
        self.assertEqual(choice.vintage, "q4_fy26_rev")


class Sprint2ADisposable(unittest.TestCase):
    def test_ptc_excluded_from_d(self):
        with self.assertRaises(ValueError):
            disposable_from_fixture(
                {
                    "disposable_named_variables": {
                        "employment_income": 50000,
                        "premium_tax_credit": 1200,
                    }
                }
            )

    def test_named_fixture_computes_d(self):
        res = disposable_from_fixture(
            {
                "disposable_named_variables": {
                    "employment_income": 50000,
                    "income_tax_before_refundable_credits": 5000,
                    "fica_payroll_tax": 3000,
                    "eitc": 0,
                    "refundable_ctc": 0,
                    "refundable_aotc": 0,
                }
            }
        )
        self.assertEqual(res.annual_disposable_usd, 42000.0)


class Sprint2ATransport(unittest.TestCase):
    def test_empirical_primary_still_flat(self):
        d = price_transport_annual({}, scenario="reference")
        self.assertAlmostEqual(d["annual_usd"], 7264.7)

    def test_normative_not_primary_and_veh_zero_default_off(self):
        hh = {"adults": 2, "drivers": 2, "veh": 0, "workers": 2}
        d = price_transport_normative(hh, access_class="LOW", use_veh_zero_rule=False)
        self.assertEqual(d["primary_economic_security_definition"], "empirical_pinned_one_vehicle_provisional")
        self.assertGreater(d["vehicles_assigned"], 0)

    def test_retired_flat_guard(self):
        with self.assertRaises(NormativeTransportError):
            assert_not_retired_flat_primary(7264.7)

    def test_headline_still_disabled(self):
        self.assertFalse(NATIONAL_HEADLINE_ENABLED)


if __name__ == "__main__":
    unittest.main()
