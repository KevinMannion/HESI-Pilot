"""Other necessities residual bundle from pinned CES-style reference table."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping

from sources.pinned import PINNED_SOURCES


def _load_bundle(path: Path, bundle_id: str) -> dict[str, str | float]:
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            if row["bundle_id"] == bundle_id:
                return {
                    "reference_adult_annual_usd": float(row["reference_adult_annual_usd"]),
                    "per_additional_person_annual_usd": float(row["per_additional_person_annual_usd"]),
                    "source_vintage_label": row["source_vintage_label"],
                    "excludes": row["excludes"],
                }
    raise ValueError(f"bundle_id {bundle_id!r} not in table")


def _person_count(household: Mapping[str, Any]) -> int:
    members = household.get("members")
    if members:
        return len(members)
    if "np" in household:
        return int(household["np"])
    adults = int(household.get("adults", 0))
    children = int(household.get("children", 0))
    n = adults + children
    if n <= 0:
        raise ValueError("household person count required")
    return n


def price_other_necessities_annual(
    household: Mapping[str, Any],
    *,
    bundle_pin_key: str = "ces_other_necessities_baseline_sample",
    bundle_id: str = "national_residual_essentials_2026",
) -> dict[str, Any]:
    pin = PINNED_SOURCES[bundle_pin_key]
    pin.verify()
    bundle = _load_bundle(pin.path, bundle_id)
    n = _person_count(household)
    ref = float(bundle["reference_adult_annual_usd"])
    addl = float(bundle["per_additional_person_annual_usd"])
    annual = round(ref + max(0, n - 1) * addl, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": round(annual / 12, 2),
        "person_count": n,
        "bundle_id": bundle_id,
        "source_vintage": str(bundle["source_vintage_label"]),
        "input_sha256": pin.sha256,
        "geographic_applicability": "national_index_fixture",
        "household_applicability": "residual_essentials_scaled_by_np",
        "scientific_status": "research_fixture_policy_gated",
        "excludes": str(bundle["excludes"]),
        "limitations": ["No subnational price index in fixture", "CES category mapping not finalized"],
    }
