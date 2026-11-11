"""Empirical healthcare from pinned CMS Marketplace rate file + rating-area crosswalk."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping

from sources.cms_rates import load_cms_rate_rows, validate_rate_file
from sources.healthcare_benchmark import BenchmarkPremiumError, slcsp_monthly, validate_benchmark_constructible
from sources.pinned import PINNED_SOURCES

# Age 40 in AL_RA01 fixture: second-lowest silver = 475/mo (plans 450, 475, 500)
REF_FIXTURE_SLCSP_MONTHLY_AGE40 = 475.0


def _childcare_age_group(age: int) -> str:
    if age < 3:
        return "infant"
    if age < 6:
        return "preschool"
    if age < 13:
        return "school_age"
    return "none"


def _load_crosswalk(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            status = row.get("status", "COMPLETE_UNAMBIGUOUS")
            if status != "COMPLETE_UNAMBIGUOUS":
                continue
            rows[row["puma_geoid"]] = row
    return rows


def _household_member_ages(household: Mapping[str, Any]) -> list[int]:
    members = household.get("members")
    if members:
        ages = []
        for m in members:
            if "age" not in m:
                raise ValueError("member missing age")
            ages.append(int(m["age"]))
        return ages
    if "adults" in household or "children" in household:
        adults = int(household.get("adults", 0))
        children = int(household.get("children", 0))
        if adults + children <= 0:
            raise ValueError("household requires positive person count")
        # Composition-only households without ages: fail closed
        raise ValueError("healthcare empirical requires member ages or members[] with age")
    raise ValueError("healthcare empirical requires members with ages")


def price_healthcare_annual(
    household: Mapping[str, Any],
    *,
    rates_pin_key: str = "cms2026_marketplace_rates_sample",
    crosswalk_pin_key: str = "puma_to_marketplace_rating_area_sample",
    business_year: int = 2026,
    benchmark_rule: str = "second_lowest_silver",
) -> dict[str, Any]:
    rates_pin = PINNED_SOURCES[rates_pin_key]
    xwalk_pin = PINNED_SOURCES[crosswalk_pin_key]
    rates_pin.verify()
    xwalk_pin.verify()
    validate_rate_file(rates_pin.path, business_year=business_year)

    puma = str(household.get("puma_geoid", ""))
    if not puma:
        raise ValueError("healthcare empirical requires puma_geoid")
    xwalk = _load_crosswalk(xwalk_pin.path)
    if puma not in xwalk:
        raise ValueError(f"puma_geoid {puma} not in marketplace crosswalk")
    rating_area_id = xwalk[puma]["rating_area_id"]
    rows = load_cms_rate_rows(rates_pin.path, business_year=business_year)

    ages = _household_member_ages(household)
    per_person: list[dict[str, Any]] = []
    monthly_total = 0.0
    for age in ages:
        try:
            monthly = slcsp_monthly(
                rows,
                rating_area_id=rating_area_id,
                age=age,
                rule=benchmark_rule,  # type: ignore[arg-type]
            )
        except BenchmarkPremiumError as e:
            raise ValueError(f"no SLCSP for age {age} in {rating_area_id}") from e
        monthly_total += monthly
        per_person.append({"age": age, "slcsp_monthly_usd": monthly})

    annual = round(monthly_total * 12, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": round(monthly_total, 2),
        "rating_area_id": rating_area_id,
        "business_year": business_year,
        "benchmark_rule": benchmark_rule,
        "per_person": per_person,
        "source_vintage": rates_pin.source_vintage,
        "input_sha256_rates": rates_pin.sha256,
        "input_sha256_crosswalk": xwalk_pin.sha256,
        "geographic_applicability": f"marketplace_rating_area_{rating_area_id}",
        "household_applicability": "unsubsidized_slcsp_sum_all_members",
        "scientific_status": "research_benchmark_not_esi_adjusted",
        "limitations": [
            "Employer-sponsored insurance offsets not applied",
            "Medicaid/Medicare eligibility not modeled",
            "Uses pinned sample extract not full national CMS file",
        ],
    }


def verify_healthcare_sources(*, business_year: int = 2026) -> dict[str, object]:
    rates_pin = PINNED_SOURCES["cms2026_marketplace_rates_sample"]
    rates_pin.verify()
    rate_meta = validate_rate_file(rates_pin.path, business_year=business_year)
    bench = validate_benchmark_constructible(rates_pin.path, business_year=business_year)
    return {"rate_file": rate_meta, "benchmark_construction": bench}
