"""Corrected FMR Q4 schedule (ER-1 / S-4) as versioned unapproved option; legacy lookup preserved."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

REPO = Path(__file__).resolve().parents[3]
SCHEDULE_FIXTURE = REPO / "research/hesi_2026/fixtures/fmr_q4_schedule_er1_2026.json"


@dataclass(frozen=True)
class FmrScheduleChoice:
    area_label: str
    calendar_month: int
    vintage: str
    policy_approved: bool = False


def load_schedule_fixture() -> dict[str, Any]:
    return json.loads(SCHEDULE_FIXTURE.read_text())


def q4_vintage_for_area(area_label: str, *, schedule: dict[str, Any] | None = None) -> str:
    schedule = schedule or load_schedule_fixture()
    holds = set(schedule.get("q4_fy26_revised_holdover_areas", []))
    fixtures = schedule.get("at5_fixture_areas", {})
    if area_label in fixtures:
        return str(fixtures[area_label])
    if area_label in holds:
        return "q4_fy26_rev"
    return "q4_fy27"


def select_fmr_vintage(area_label: str, calendar_month: int) -> FmrScheduleChoice:
    schedule = load_schedule_fixture()
    if calendar_month == 1 and "jan1_11" in schedule.get("weights", {}):
        jan_vintage = "fy25" if area_label == "san_jose" else "fy26_orig"
        return FmrScheduleChoice(area_label, calendar_month, jan_vintage, policy_approved=False)
    if 2 <= calendar_month <= 9:
        return FmrScheduleChoice(area_label, calendar_month, "fy26_rev", policy_approved=False)
    vintage = q4_vintage_for_area(area_label)
    return FmrScheduleChoice(area_label, calendar_month, vintage, policy_approved=False)


def price_housing_with_schedule_option(
    household: Mapping[str, Any],
    *,
    area_label: str = "general",
    calendar_month: int = 10,
    use_schedule: bool = False,
) -> dict[str, Any]:
    """When use_schedule=False, delegate to legacy empirical pinned FMR table unchanged."""
    from sources.housing_empirical import price_housing_annual

    legacy = price_housing_annual(household)
    legacy["fmr_schedule_option"] = "legacy_puma_fmr_screened_fy2026"
    legacy["policy_approved"] = False
    if not use_schedule:
        legacy["schedule_path"] = "legacy_only"
        return legacy
    choice = select_fmr_vintage(area_label, calendar_month)
    return {
        **legacy,
        "fmr_schedule_option": schedule_fixture_meta(),
        "schedule_vintage_selected": choice.vintage,
        "schedule_area_label": area_label,
        "calendar_month": calendar_month,
        "scientific_status": "er1_q4_schedule_unapproved_overlay",
        "policy_approved": False,
        "notes": "Legacy monthly rent unchanged in Sprint 2A; schedule records ER-1 vintage labels only",
    }


def schedule_fixture_meta() -> dict[str, Any]:
    data = load_schedule_fixture()
    return {
        "schedule_id": data.get("schedule_id"),
        "policy_approved": data.get("policy_approved", False),
        "register_pin": data.get("register_pin"),
    }
