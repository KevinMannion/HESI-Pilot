"""Second-lowest-cost silver plan (SLCSP) benchmark premium construction."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from sources.cms_rates import CmsRateFileError, RateRow, iter_silver_rates, load_cms_rate_rows

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
    premiums = iter_silver_rates(rows, rating_area_id=rating_area_id, age=age)
    return second_lowest_silver_monthly(premiums, rule=rule)


def build_rating_area_index(rows: list[RateRow]) -> dict[str, set[int]]:
    out: dict[str, set[int]] = {}
    for r in rows:
        out.setdefault(r.rating_area_id, set()).add(r.age)
    return out


def validate_benchmark_constructible(path: Path, *, business_year: int = 2026) -> dict[str, object]:
    rows = load_cms_rate_rows(path, business_year=business_year)
    index = build_rating_area_index(rows)
    checks: list[dict[str, object]] = []
    for area, ages in sorted(index.items()):
        for age in sorted(ages):
            try:
                monthly = slcsp_monthly(rows, rating_area_id=area, age=age)
            except (BenchmarkPremiumError, CmsRateFileError) as e:
                checks.append({"rating_area_id": area, "age": age, "ok": False, "error": str(e)})
            else:
                checks.append({"rating_area_id": area, "age": age, "ok": True, "slcsp_monthly": monthly})
    ok_count = sum(1 for c in checks if c["ok"])
    return {
        "business_year": business_year,
        "checks": checks,
        "constructible_pairs": ok_count,
        "total_pairs": len(checks),
    }
