"""Empirical food from pinned USDA table via core_r24 food_model."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "core_r24" / "src"))
from food_model import load_prices, monthly_cost  # noqa: E402

from sources.pinned import PINNED_SOURCES

FOOD_REFERENCE_MONTH = (2026, 9)


def price_food_annual(
    household: Mapping[str, Any],
    *,
    plan: str = "thrifty",
) -> dict[str, Any]:
    pin = PINNED_SOURCES["usda_prices_source_2024_2026"]
    pin.verify()
    members = household.get("members")
    if not members:
        raise ValueError("empirical food requires household['members'] list with age/sex")
    catalog, issues = load_prices(pin.path)
    if issues:
        raise ValueError(f"USDA catalog issues: {issues[:3]}")
    year, month = FOOD_REFERENCE_MONTH
    monthly = monthly_cost(catalog, year, month, plan, list(members))
    annual = round(monthly * 12, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": monthly,
        "source_vintage": pin.source_vintage,
        "input_sha256": pin.sha256,
        "input_path": str(pin.path),
        "geographic_applicability": pin.geographic_applicability,
        "household_applicability": f"thrifty_plan_{plan}_september_{year}",
        "food_plan": plan,
        "price_month": f"{year}-{month:02d}",
        "imputation": "none",
        "calculation_mode": "empirical_pinned",
    }
