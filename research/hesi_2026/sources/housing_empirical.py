"""Empirical housing from pinned PUMA FMR table."""
from __future__ import annotations

import csv
from math import ceil
from pathlib import Path
from typing import Any, Mapping

from sources.pinned import PINNED_SOURCES


def _required_bedrooms(adults: int, children: int, partners: int) -> int:
    return adults - min(partners, 1) + ceil(children / 2)


def _load_puma_table(path: Path) -> dict[str, dict[str, str]]:
    rows = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            rows[row["puma_geoid"]] = row
    return rows


def price_housing_annual(
    household: Mapping[str, Any],
    *,
    geography_pin_key: str = "puma_fmr_screened_fy2026",
) -> dict[str, Any]:
    pin = PINNED_SOURCES[geography_pin_key]
    pin.verify()
    puma = str(household.get("puma_geoid", ""))
    if not puma:
        raise ValueError("empirical housing requires puma_geoid")
    table = _load_puma_table(pin.path)
    if puma not in table:
        raise ValueError(f"puma_geoid {puma} not in pinned geography table")
    rec = table[puma]
    status = rec.get("status", "")
    if status != "COMPLETE_UNAMBIGUOUS":
        raise ValueError(f"puma {puma} status {status!r}; no imputation")
    br = _required_bedrooms(
        int(household["adults"]),
        int(household["children"]),
        int(household["partners"]),
    )
    if br < 0 or br > 4:
        raise ValueError(f"bedroom requirement {br} outside HUD 0-4 FMR columns")
    col = f"monthly_{br}br_benchmark"
    monthly = float(rec[col])
    if monthly <= 0:
        raise ValueError(f"missing benchmark rent for {puma} bedroom {br}")
    annual = round(monthly * 12, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": monthly,
        "bedrooms": br,
        "source_vintage": pin.source_vintage,
        "input_sha256": pin.sha256,
        "input_path": str(pin.path),
        "geographic_applicability": f"puma_{puma}_{status}",
        "household_applicability": "replacement_rent_normative_not_observed",
        "imputation": "none",
        "calculation_mode": "empirical_pinned",
    }
