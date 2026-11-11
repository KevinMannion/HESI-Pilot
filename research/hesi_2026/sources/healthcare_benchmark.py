"""Second-lowest-cost silver plan (SLCSP) benchmark premium construction."""
from __future__ import annotations

from typing import Literal

from sources.age_rating import member_age_key
from sources.cms_rates import RateRow, _silver_row, iter_silver_rates, load_cms_rate_rows

BenchmarkRule = Literal["second_lowest_silver", "lowest_silver"]


class BenchmarkPremiumError(ValueError):
    pass


def second_lowest_silver_monthly(premiums: list[float], rule: BenchmarkRule = "second_lowest_silver") -> float:
    if not premiums:
        raise BenchmarkPremiumError("no silver premiums for rating area and age")
    uniq = sorted(set(premiums))
    if rule == "lowest_silver":
        return uniq[0]
    if len(uniq) == 1:
        return uniq[0]
    return uniq[1]


def slcsp_monthly(
    rows: list[RateRow],
    *,
    rating_area_id: str,
    age: int,
    rule: BenchmarkRule = "second_lowest_silver",
) -> float:
    """Single-adult SLCSP at a member age (one covered individual)."""
    premiums = iter_silver_rates(rows, rating_area_id=rating_area_id, member_age=age)
    return second_lowest_silver_monthly(premiums, rule=rule)


def _silver_plan_tables(rows: list[RateRow], *, rating_area_id: str) -> dict[tuple[str, str], dict[str, float]]:
    plans: dict[tuple[str, str], dict[str, float]] = {}
    for r in rows:
        if r.rating_area_id != rating_area_id:
            continue
        if not _silver_row(r):
            continue
        key = (r.issuer_id, r.plan_id)
        plans.setdefault(key, {})[r.age_key] = r.individual_rate
    return plans


def household_slcsp_monthly(
    rows: list[RateRow],
    *,
    rating_area_id: str,
    member_ages: list[int],
    rule: BenchmarkRule = "second_lowest_silver",
) -> tuple[float, dict[str, object]]:
    """Household SLCSP: one silver plan for all members; sum age-rated premiums; 2nd-lowest total.

    This matches Marketplace APTC benchmark logic (same plan covers all household members).
  It is NOT the sum of independent per-person SLCSP amounts from different plans.
    """
    if not member_ages:
        raise BenchmarkPremiumError("household must include at least one covered member age")
    age_keys = [member_age_key(a) for a in member_ages]
    plan_tables = _silver_plan_tables(rows, rating_area_id=rating_area_id)
    candidates: list[tuple[float, str, str]] = []
    for (issuer_id, plan_id), age_rates in plan_tables.items():
        try:
            total = sum(age_rates[k] for k in age_keys)
        except KeyError:
            continue
        candidates.append((total, issuer_id, plan_id))
    if not candidates:
        raise BenchmarkPremiumError("no silver plan rates all household member ages in rating area")
    totals = [c[0] for c in candidates]
    monthly = second_lowest_silver_monthly(totals, rule=rule)
    selected = next(c for c in sorted(candidates, key=lambda x: (x[0], x[1], x[2])) if c[0] == monthly)
    _, issuer_id, plan_id = selected
    return monthly, {
        "method": "single_plan_household_second_lowest_silver",
        "member_age_keys": age_keys,
        "candidate_plan_count": len(candidates),
        "selected_issuer_id": issuer_id,
        "selected_plan_id": plan_id,
    }


def sum_of_individual_slcsp_monthly(
    rows: list[RateRow],
    *,
    rating_area_id: str,
    member_ages: list[int],
    rule: BenchmarkRule = "second_lowest_silver",
) -> float:
    """Deprecated anti-pattern retained for negative tests only."""
    return sum(slcsp_monthly(rows, rating_area_id=rating_area_id, age=a, rule=rule) for a in member_ages)


def validate_benchmark_constructible(path, *, business_year: int = 2026) -> dict[str, object]:
    from pathlib import Path

    rows = load_cms_rate_rows(Path(path), business_year=business_year)
    areas = {r.rating_area_id for r in rows if _silver_row(r)}
    checks: list[dict[str, object]] = []
    for area in sorted(areas):
        for age_key in sorted({r.age_key for r in rows if r.rating_area_id == area and _silver_row(r)}):
            if age_key == "0-14":
                member_age = 10
            elif age_key == "64 and over":
                member_age = 64
            else:
                member_age = int(age_key)
            try:
                monthly = slcsp_monthly(rows, rating_area_id=area, age=member_age)
            except BenchmarkPremiumError as e:
                checks.append({"rating_area_id": area, "age_key": age_key, "ok": False, "error": str(e)})
            else:
                checks.append({"rating_area_id": area, "age_key": age_key, "ok": True, "slcsp_monthly": monthly})
    ok_count = sum(1 for c in checks if c["ok"])
    return {
        "business_year": business_year,
        "checks": checks,
        "constructible_pairs": ok_count,
        "total_pairs": len(checks),
    }
