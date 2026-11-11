"""Empirical healthcare from pinned CMS Marketplace rate file + rating-area crosswalk."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping

from sources.age_rating import member_age_key
from sources.cms_rates import load_cms_rate_rows, validate_rate_file
from sources.healthcare_benchmark import (
    BenchmarkPremiumError,
    household_slcsp_monthly,
    slcsp_monthly,
    sum_of_individual_slcsp_monthly,
    validate_benchmark_constructible,
)
from sources.pinned import PINNED_SOURCES


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
        raise ValueError("healthcare empirical requires members[] with age (composition-only insufficient)")
    raise ValueError("healthcare empirical requires members with ages")


def price_healthcare_annual(
    household: Mapping[str, Any],
    *,
    rates_pin_key: str = "cms2026_rate_puf_bounded_al_ra1",
    crosswalk_pin_key: str = "puma_to_marketplace_rating_area_bounded_2026",
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
    try:
        monthly, bench_detail = household_slcsp_monthly(
            rows,
            rating_area_id=rating_area_id,
            member_ages=ages,
            rule=benchmark_rule,  # type: ignore[arg-type]
        )
    except BenchmarkPremiumError as e:
        raise ValueError(f"household SLCSP not constructible in {rating_area_id}") from e

    per_person_reference = [
        {
            "age": age,
            "age_key": member_age_key(age),
            "single_member_slcsp_monthly_usd": slcsp_monthly(
                rows, rating_area_id=rating_area_id, age=age, rule=benchmark_rule  # type: ignore[arg-type]
            ),
        }
        for age in ages
    ]

    annual = round(monthly * 12, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": round(monthly, 2),
        "rating_area_id": rating_area_id,
        "business_year": business_year,
        "benchmark_rule": benchmark_rule,
        "benchmark_construction": bench_detail,
        "per_person_single_member_slcsp_reference": per_person_reference,
        "anti_pattern_sum_individual_slcsp_monthly_usd": round(
            sum_of_individual_slcsp_monthly(
                rows,
                rating_area_id=rating_area_id,
                member_ages=ages,
                rule=benchmark_rule,  # type: ignore[arg-type]
            ),
            2,
        ),
        "source_vintage": rates_pin.source_vintage,
        "input_sha256_rates": rates_pin.sha256,
        "input_sha256_crosswalk": xwalk_pin.sha256,
        "geographic_applicability": f"marketplace_rating_area_{rating_area_id}",
        "household_applicability": "all_members_one_silver_plan_unsubsidized",
        "scientific_status": "bounded_empirical_demonstration_not_nationally_approved",
        "coverage_assumptions": {
            "marketplace_unsubsidized_gross_premium": True,
            "employer_coverage_offset": False,
            "medicaid_medicare_triple_lock": False,
            "pediatric_dental_embedded": "as_in_qhp_medical_premium",
        },
        "subsidy_assumptions": {
            "advance_premium_tax_credit_applied": False,
            "cost_sharing_reduction_plan_variants_included": False,
        },
        "age_rating_assumptions": {
            "tobacco_surcharge": False,
            "uses_cms_puf_age_keys_non_tobacco_individual_rate": True,
        },
        "limitations": [
            "Bounded AL Rating Area 1 extract only; not national representativeness",
            "Household SLCSP uses one silver plan for all members (not sum of per-person plan picks)",
        ],
    }


def verify_healthcare_sources(
    *,
    business_year: int = 2026,
    rates_pin_key: str = "cms2026_rate_puf_bounded_al_ra1",
) -> dict[str, object]:
    rates_pin = PINNED_SOURCES[rates_pin_key]
    rates_pin.verify()
    rate_meta = validate_rate_file(rates_pin.path, business_year=business_year)
    bench = validate_benchmark_constructible(rates_pin.path, business_year=business_year)
    return {"rate_file": rate_meta, "benchmark_construction": bench}
