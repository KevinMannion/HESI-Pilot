"""2024 matched-year national engine. Sibling of core_r24/src/run_joint.py.

Writes only under a caller-supplied directory. Refuses national_R22.
Household-specific food+housing+transport vs observed ACS income.
Not the income-nowcast G3 uniform threshold. Not a September 2026 nowcast.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "core_r24" / "src"))
from run_joint import run  # noqa: E402

COST_LABELS = [
    "food_month",
    "housing_month",
    "one_vehicle_month_GASOLINE_2024_NONFUEL_HELD",
    "total_month_PROVISIONAL",
    "income_month_ACS2024_observed",
]
SHARE = "share_income_below_three_costs_2024matched_MODELED"
LABEL = (
    "PROVISIONAL / NOT SCIENTIFICALLY VALIDATED. "
    "2024 ACS observed income vs 2024 modeled USDA Thrifty annual-mean food, "
    "HUD FMR (named housing table), EIA 2024 gasoline $3.304/gal with non-fuel "
    "transport dollars inherited from the R2.4 hypothetical ($5,631.67). "
    "Household-specific costs; not G3 uniform $2,894.91."
)


def run_matched(housing_zip, food_cache, composition_cache, geography, out, transport_annual=6870.67):
    return run(
        housing_zip,
        food_cache,
        composition_cache,
        geography,
        out,
        transport_annual=transport_annual,
        food_column="thrifty_2024annual",
        cost_labels=COST_LABELS,
        share_metric=SHARE,
        scenario_label=LABEL,
        audit_status="PROVISIONAL_NOT_SCIENTIFICALLY_VALIDATED",
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--housing-zip", required=True)
    p.add_argument("--food-cache", required=True)
    p.add_argument("--composition-cache", required=True)
    p.add_argument("--geography", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--transport-annual", type=float, default=6870.67)
    a = p.parse_args()
    run_matched(a.housing_zip, a.food_cache, a.composition_cache, a.geography, a.out, a.transport_annual)


if __name__ == "__main__":
    main()
