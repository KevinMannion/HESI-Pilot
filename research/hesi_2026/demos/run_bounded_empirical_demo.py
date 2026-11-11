"""Generate bounded six-component worked examples (not nationally representative)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from components.registry import default_six_component_registry
from components.base import MissingStatus
from gating import NATIONAL_HEADLINE_ENABLED, six_component_complete
from sources.pinned import PINNED_SOURCES

SCENARIOS = [
    {
        "scenario_id": "al_puma_0100100_couple_one_child",
        "label": "BOUNDED_DEMONSTRATION_NOT_NATIONAL",
        "household": {
            "puma_geoid": "0100100",
            "state_code": "AL",
            "adults": 2,
            "children": 1,
            "partners": 1,
            "np": 3,
            "members": [
                {"age": 35, "sex": "Male"},
                {"age": 33, "sex": "Female"},
                {"age": 4, "sex": "Male"},
            ],
        },
    },
    {
        "scenario_id": "al_puma_0100200_single_adult",
        "label": "BOUNDED_DEMONSTRATION_NOT_NATIONAL",
        "household": {
            "puma_geoid": "0100200",
            "state_code": "AL",
            "adults": 1,
            "children": 0,
            "partners": 0,
            "np": 1,
            "members": [{"age": 40, "sex": "Female"}],
        },
    },
]

CONTEXT = {
    "calculation_mode": "empirical_pinned",
    "geography_pin_key": "puma_fmr_screened_fy2026",
    "healthcare_rates_pin_key": "cms2026_rate_puf_bounded_al_ra1",
    "healthcare_crosswalk_pin_key": "puma_to_marketplace_rating_area_bounded_2026",
    "food_policy_approved": False,
    "housing_policy_approved": False,
    "transport_policy_approved": False,
    "healthcare_policy_approved": False,
    "childcare_policy_approved": False,
    "other_necessities_policy_approved": False,
}


def arithmetic_total(components: list[dict]) -> dict:
    lines = []
    total = 0.0
    for c in components:
        if c["missing_status"] != "priced" or c["annual_usd"] is None:
            lines.append({"component": c["component"], "annual_usd": None, "note": c["missing_status"]})
            continue
        lines.append(
            {
                "component": c["component"],
                "annual_usd": c["annual_usd"],
                "source_vintage": c.get("source_vintage"),
                "arithmetic": f"add {c['annual_usd']:.2f}",
            }
        )
        total += c["annual_usd"]
    return {"component_lines": lines, "sum_annual_usd": round(total, 2), "formula": "sum of priced component annual_usd (six-vector intended)"}


def main() -> None:
    verify_pins = {k: PINNED_SOURCES[k].sha256 for k in PINNED_SOURCES if k in {
        "usda_prices_source_2024_2026",
        "puma_fmr_screened_fy2026",
        "transport_reference_2026_09",
        "cms2026_rate_puf_bounded_al_ra1",
        "puma_to_marketplace_rating_area_bounded_2026",
        "childcare_market_rates_sample",
        "ces_other_necessities_baseline_sample",
    }}
    out_scenarios = []
    registry = default_six_component_registry()
    for spec in SCENARIOS:
        costs = [c.price(spec["household"], context=CONTEXT) for c in registry]
        dicts = [c.to_dict() for c in costs]
        complete, blockers = six_component_complete(dicts)
        out_scenarios.append(
            {
                **spec,
                "essential_costs": dicts,
                "total_arithmetic": arithmetic_total(dicts),
                "six_component_complete": complete,
                "six_component_blockers": blockers,
            }
        )
    payload = {
        "status": "BOUNDED_EMPIRICAL_DEMONSTRATION",
        "national_headline_enabled": NATIONAL_HEADLINE_ENABLED,
        "scientific_approval": False,
        "pinned_input_sha256": verify_pins,
        "methodology_refs": [
            "research/hesi_2026/audit/healthcare_benchmark_methodology_2026.md",
            "research/hesi_2026/audit/housing_verification_2026-11-11.json",
        ],
        "scenarios": out_scenarios,
    }
    out_path = ROOT / "demos" / "bounded_worked_examples_2026.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
