"""Empirical transport from pinned scenario table (provisional; not mobility model)."""
from __future__ import annotations

import csv
from typing import Any, Mapping

from sources.pinned import PINNED_SOURCES


def price_transport_annual(
    household: Mapping[str, Any],
    *,
    scenario: str = "reference",
) -> dict[str, Any]:
    _ = household
    pin = PINNED_SOURCES["transport_reference_2026_09"]
    pin.verify()
    with open(pin.path, newline="") as f:
        rows = {r["scenario"]: r for r in csv.DictReader(f)}
    if scenario not in rows:
        raise ValueError(f"unknown transport scenario {scenario!r}")
    row = rows[scenario]
    annual = float(row["annual"])
    monthly = float(row["monthly"])
    return {
        "annual_usd": annual,
        "monthly_usd": monthly,
        "scenario": scenario,
        "source_vintage": pin.source_vintage,
        "input_sha256": pin.sha256,
        "input_path": str(pin.path),
        "geographic_applicability": pin.geographic_applicability,
        "household_applicability": "one_vehicle_assigned_provisional",
        "imputation": "none",
        "calculation_mode": "empirical_pinned",
        "scientific_status": row.get("status", "hypothetical_sensitivity_only"),
    }
