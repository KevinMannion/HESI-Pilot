"""Bounded MEPS IC / HC ingest for premium and OOP derivation tests (coverage-type distinct)."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any, Mapping

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import load_source_register

REPO = Path(__file__).resolve().parents[3]
MEPS_IC_FIXTURE = REPO / "research/hesi_2026/fixtures/inputs/meps_ic_employer_premium_sample.csv"
MEPS_HC_FIXTURE = REPO / "research/hesi_2026/fixtures/inputs/meps_hc_oop_by_coverage_sample.csv"


def _verify_register_file(source_id: str) -> dict[str, Any]:
    for row in load_source_register():
        if row.source_id != source_id:
            continue
        resolved = resolve_register_local_path(row.local_path) if row.local_path else None
        out: dict[str, Any] = {"source_id": source_id, "register_path": row.local_path}
        if resolved and resolved.is_file() and row.sha256:
            got = hashlib.sha256(resolved.read_bytes()).hexdigest()
            out.update({"path": str(resolved), "sha256_match": got == row.sha256.lower()})
        else:
            out["missing"] = True
        return out
    return {"source_id": source_id, "error": "not_in_register"}


def _load_ic_fixture() -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    with open(MEPS_IC_FIXTURE, newline="") as f:
        for row in csv.DictReader(f):
            key = (row["state"].strip(), row["coverage_type"].strip())
            out[key] = float(row["employee_contribution_annual_usd"])
    return out


def _load_hc_fixture() -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    with open(MEPS_HC_FIXTURE, newline="") as f:
        for row in csv.DictReader(f):
            key = (row["coverage_type"].strip(), row["age_group"].strip())
            out[key] = float(row["oop_annual_usd"])
    return out


def infer_coverage_type(household: Mapping[str, Any]) -> str:
    explicit = household.get("health_coverage_type")
    if explicit:
        return str(explicit).strip()
    if household.get("medicare"):
        return "medicare"
    if household.get("medicaid"):
        return "medicaid"
    if household.get("employer_coverage"):
        return "employer"
    if household.get("marketplace_coverage"):
        return "marketplace_unsubsidized"
    return "uninsured"


def _age_group(age: int) -> str:
    if age >= 65:
        return "adult_65_plus"
    if age >= 19:
        return "adult_19_64"
    return "child"


def derive_employer_premium_annual(household: Mapping[str, Any]) -> dict[str, Any]:
    state = str(household.get("state_code", household.get("state", ""))).strip()
    if not state:
        raise ValueError("MEPS IC derivation requires state_code")
    cov = infer_coverage_type(household)
    if cov != "employer":
        return {
            "annual_usd": 0.0,
            "coverage_type": cov,
            "component": "employer_premium",
            "scientific_status": "not_applicable_for_coverage",
            "policy_approved": False,
        }
    tier = str(household.get("employer_coverage_tier", "single_employee"))
    table = _load_ic_fixture()
    key = (state, tier)
    if key not in table:
        raise ValueError(f"no MEPS IC employee contribution for {state}/{tier}")
    reg = _verify_register_file("P4-HC22")
    annual = float(table[key])
    return {
        "annual_usd": annual,
        "monthly_usd": round(annual / 12, 2),
        "coverage_type": cov,
        "employer_coverage_tier": tier,
        "component": "employer_premium",
        "meps_ic_register": reg,
        "fixture_path": str(MEPS_IC_FIXTURE),
        "scientific_status": "meps_ic_2025_fixture_bridge_unapproved",
        "policy_approved": False,
        "limitations": ["2025 survey year; 2026 bridge not pinned (G-07)"],
    }


def derive_oop_annual(household: Mapping[str, Any]) -> dict[str, Any]:
    cov = infer_coverage_type(household)
    ages = [int(m["age"]) for m in (household.get("members") or [{"age": household.get("age", 35)}])]
    age = max(ages)
    grp = _age_group(age)
    table = _load_hc_fixture()
    key = (cov, grp)
    if key not in table:
        raise ValueError(f"no MEPS HC OOP fixture for {cov}/{grp}")
    reg = _verify_register_file("P4-HC26")
    annual = float(table[key])
    return {
        "annual_usd": annual,
        "monthly_usd": round(annual / 12, 2),
        "coverage_type": cov,
        "age_group": grp,
        "component": "out_of_pocket",
        "meps_hc_register": reg,
        "fixture_path": str(MEPS_HC_FIXTURE),
        "scientific_status": "meps_hc_2024_fixture_tabulation_placeholder",
        "policy_approved": False,
        "limitations": ["Not MEPS microdata tabulation; medical CPI bridge not pinned"],
    }


def derive_health_bounds(household: Mapping[str, Any]) -> dict[str, Any]:
    cov = infer_coverage_type(household)
    premium = derive_employer_premium_annual(household) if cov == "employer" else {
        "annual_usd": 0.0,
        "coverage_type": cov,
        "component": "employer_premium",
        "scientific_status": "not_applicable_for_coverage",
        "policy_approved": False,
    }
    oop = derive_oop_annual(household)
    total = round(float(premium.get("annual_usd", 0)) + float(oop["annual_usd"]), 2)
    return {
        "annual_usd": total,
        "monthly_usd": round(total / 12, 2),
        "coverage_type": cov,
        "employer_premium": premium,
        "out_of_pocket": oop,
        "scientific_status": "bounded_meps_derivation_tests_only",
        "policy_approved": False,
        "ptc_excluded_from_disposable": True,
    }
