"""NDCP county childcare prices ingest (pinned register P4-C01 or bounded CSV fixture)."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any, Mapping

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import load_source_register
from sources.childcare_cpi_bridge import apply_cpi_bridge, load_bridge_options

REPO = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURE = (
    REPO / "research/hesi_2026/fixtures/inputs/ndcp_county_prices_bounded_2022.csv"
)
P4_C01_ID = "P4-C01"

_AGE_TO_CARE = {
    "infant": (0, 2),
    "toddler": (2, 3),
    "preschool": (3, 6),
    "school_age": (6, 13),
}


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _register_row(source_id: str) -> tuple[str, str] | None:
    for row in load_source_register():
        if row.source_id == source_id:
            return row.local_path, row.sha256
    return None


def resolve_ndcp_source(*, use_register: bool = True) -> dict[str, Any]:
    """Return resolved path and verification metadata; missing register bytes are reported, not fabricated."""
    meta: dict[str, Any] = {"source_id": P4_C01_ID, "path": None, "sha256": None, "sha256_match": None}
    if use_register:
        reg = _register_row(P4_C01_ID)
        if reg:
            lp, want = reg
            resolved = resolve_register_local_path(lp)
            if resolved and resolved.is_file():
                got = _sha256_file(resolved)
                meta.update(
                    {
                        "path": str(resolved),
                        "sha256": got,
                        "sha256_match": got == want.lower(),
                        "register_sha256": want,
                    }
                )
                return meta
            meta["register_local_path"] = lp
            meta["missing_register_bytes"] = True
    if DEFAULT_FIXTURE.is_file():
        got = _sha256_file(DEFAULT_FIXTURE)
        meta.update(
            {
                "path": str(DEFAULT_FIXTURE),
                "sha256": got,
                "fixture_fallback": True,
                "scientific_status": "synthetic_bounded_extract_not_full_ndcp",
            }
        )
    else:
        meta["missing"] = True
    return meta


def _care_type(age: int) -> str:
    if age < 2:
        return "infant"
    if age < 3:
        return "toddler"
    if age < 6:
        return "preschool"
    if age < 13:
        return "school_age"
    return "none"


def load_ndcp_weekly_table(path: Path) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            fips = row["county_fips"].strip()
            care = row["care_type"].strip()
            out[(fips, care)] = float(row["weekly_usd"])
    return out


def price_childcare_ndcp_county(
    household: Mapping[str, Any],
    *,
    county_fips: str | None = None,
    weeks_per_year: int = 52,
    cpi_bridge: str = "none",
    cpi_factor: float | None = None,
) -> dict[str, Any]:
    county = (county_fips or household.get("county_fips") or "").strip()
    if not county:
        raise ValueError("ndcp childcare requires county_fips")
    src = resolve_ndcp_source()
    path_s = src.get("path")
    if not path_s:
        raise FileNotFoundError("NDCP source missing: register bytes absent and fixture missing")
    path = Path(path_s)
    rates = load_ndcp_weekly_table(path)
    bridge_opts = load_bridge_options()
    bridge_detail = apply_cpi_bridge(
        bridge_key=cpi_bridge,
        factor=cpi_factor,
        options=bridge_opts,
    )

    members = household.get("members") or []
    child_lines: list[dict[str, Any]] = []
    weekly = 0.0
    for m in members:
        age = int(m["age"])
        care = _care_type(age)
        if care == "none":
            continue
        key = (county, care)
        if key not in rates:
            raise ValueError(f"no NDCP weekly price for county {county} care_type {care}")
        wk = float(rates[key])
        wk_bridged = round(wk * float(bridge_detail["factor"]), 4)
        weekly += wk_bridged
        child_lines.append({"age": age, "care_type": care, "weekly_usd_2022": wk, "weekly_usd_applied": wk_bridged})

    annual = round(weekly * weeks_per_year, 2)
    return {
        "annual_usd": annual,
        "monthly_usd": round(annual / 12, 2),
        "county_fips": county,
        "covered_children": len(child_lines),
        "lines": child_lines,
        "weeks_per_year": weeks_per_year,
        "ndcp_source": src,
        "cpi_bridge": bridge_detail,
        "source_vintage": "NDCP_2022_county_weekly_unapproved",
        "geographic_applicability": f"county_{county}",
        "household_applicability": "center_based_mc_star_weekly_fixture_or_register",
        "scientific_status": "ndcp_ingest_unapproved_policy_gated",
        "policy_approved": False,
        "limitations": [
            "NDCP 2008-2022 county medians; 3-4 year lag",
            "CPI bridge not auto-approved",
            "Work/study need rule not implemented",
        ],
    }
