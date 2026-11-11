"""BLS Consumer Expenditure table ingest and unapproved quintile x size fallback."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any, Mapping

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import load_source_register

REPO = Path(__file__).resolve().parents[3]
FALLBACK_FIXTURE = REPO / "research/hesi_2026/fixtures/inputs/bls_ce_quintile_size_fallback_sample.csv"


def _register_source(source_id: str) -> dict[str, Any]:
    for row in load_source_register():
        if row.source_id == source_id:
            resolved = resolve_register_local_path(row.local_path) if row.local_path else None
            meta: dict[str, Any] = {
                "source_id": source_id,
                "register_local_path": row.local_path,
                "verification_status": row.verification_status,
            }
            if resolved and resolved.is_file() and row.sha256:
                got = hashlib.sha256(resolved.read_bytes()).hexdigest()
                meta["path"] = str(resolved)
                meta["sha256_match"] = got == row.sha256.lower()
            else:
                meta["missing"] = True
            return meta
    return {"source_id": source_id, "error": "not_in_register"}


def _load_fallback_fixture() -> dict[str, float]:
    out: dict[str, float] = {}
    with open(FALLBACK_FIXTURE, newline="") as f:
        for row in csv.DictReader(f):
            out[row["table_id"].strip()] = float(row["value_usd"])
    return out


def price_other_ce_fallback(
    household: Mapping[str, Any],
    *,
    use_fallback: bool = True,
) -> dict[str, Any]:
    """Proposed separability fallback (OA-23 / A r1). Observed spending is NOT a minimum-adequacy standard."""
    if not use_fallback:
        raise ValueError("BLS CE pinned tables required; no substitution without fallback option")
    n = int(household.get("np") or len(household.get("members") or []))
    if n <= 0:
        raise ValueError("person count required")
    fixture = _load_fallback_fixture()
    q2 = fixture["1101_q2_2025"]
    size_mult = 1.0 if n == 1 else fixture["1400_two_or_more_2025"] / q2
    base = q2 * size_mult
    internet = fixture["spm_internet_2a2c_calc"] if n >= 4 else fixture["spm_internet_2a2c_calc"] * (n / 4)
    annual = round(base + internet, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": round(annual / 12, 2),
        "person_count": n,
        "method": "ce_table_1101_x_1400_separability_fallback",
        "policy_approved": False,
        "scientific_status": "unapproved_observed_spending_fallback_not_minimum_adequacy",
        "register_p4_o01": _register_source("P4-O01"),
        "register_p4_o02": _register_source("P4-O02"),
        "fixture_path": str(FALLBACK_FIXTURE),
        "limitations": [
            "Separability of quintile and size untested",
            "Internet via SPM renter share calculation (unapproved)",
            "Does not represent a proven minimum-adequacy standard",
        ],
    }
