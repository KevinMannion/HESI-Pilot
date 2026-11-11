"""Childcare essential cost from pinned state market-rate table (research fixture)."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping

from sources.pinned import PINNED_SOURCES


def _age_group(age: int) -> str:
    if age < 3:
        return "infant"
    if age < 6:
        return "preschool"
    if age < 13:
        return "school_age"
    return "none"


def _load_rates(path: Path) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            key = (row["state_code"].strip(), row["age_group"].strip())
            out[key] = float(row["weekly_rate_usd"])
    return out


def price_childcare_annual(
    household: Mapping[str, Any],
    *,
    rates_pin_key: str = "childcare_market_rates_sample",
    weeks_per_year: int = 52,
) -> dict[str, Any]:
    pin = PINNED_SOURCES[rates_pin_key]
    pin.verify()
    state = str(household.get("state_code", household.get("state", ""))).strip()
    if not state:
        raise ValueError("childcare empirical requires state_code")
    rates = _load_rates(pin.path)

    members = household.get("members") or []
    child_ages: list[int] = []
    if members:
        for m in members:
            age = int(m["age"])
            if _age_group(age) != "none":
                child_ages.append(age)
    else:
        children = int(household.get("children", 0))
        if children <= 0:
            return {
                "annual_usd": 0.0,
                "monthly_usd": 0.0,
                "covered_children": 0,
                "source_vintage": pin.source_vintage,
                "input_sha256": pin.sha256,
                "geographic_applicability": f"state_{state}",
                "household_applicability": "no_children_requiring_care",
                "scientific_status": "research_fixture_policy_gated",
            }
        raise ValueError("childcare empirical requires member ages when children present")

    weekly_total = 0.0
    lines: list[dict[str, Any]] = []
    for age in child_ages:
        grp = _age_group(age)
        key = (state, grp)
        if key not in rates:
            raise ValueError(f"no market rate for {state}/{grp}")
        wk = rates[key]
        weekly_total += wk
        lines.append({"age": age, "age_group": grp, "weekly_usd": wk})

    annual = round(weekly_total * weeks_per_year, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": round(annual / 12, 2),
        "covered_children": len(child_ages),
        "lines": lines,
        "weeks_per_year": weeks_per_year,
        "source_vintage": pin.source_vintage,
        "input_sha256": pin.sha256,
        "geographic_applicability": f"state_{state}",
        "household_applicability": "essential_hours_full_year_fixture",
        "scientific_status": "research_fixture_policy_gated",
        "limitations": ["Informal care not valued", "Parent work-hours gate not implemented"],
    }
