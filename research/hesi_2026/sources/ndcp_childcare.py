"""NDCP county childcare prices ingest (pinned register P4-C01 or bounded CSV fixture)."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any, Mapping

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import load_source_register, validate_required_source_pins_or_abort
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


def resolve_ndcp_source(*, use_register: bool = False) -> dict[str, Any]:
    """Return resolved path metadata. Default uses bounded fixture unless use_register=True."""
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


def load_ndcp_weekly_table(
    path: Path,
    *,
    study_year: int = 2022,
    care_setting: str = "market_center_median",
) -> dict[tuple[str, str], float]:
    if path.suffix.lower() == ".xlsx":
        from sources.ndcp_workbook import iter_ndcp_workbook_rows, parse_ndcp_price_cell
        from sources.ndcp_workbook import CARE_SETTING_COLUMNS, normalize_county_fips

        if care_setting not in CARE_SETTING_COLUMNS:
            raise ValueError(f"unknown ndcp care_setting {care_setting!r}")
        columns = CARE_SETTING_COLUMNS[care_setting]
        year_s = str(int(study_year))
        out: dict[tuple[str, str], float] = {}
        for _row_num, row in iter_ndcp_workbook_rows(path):
            if str(row.get("STUDYYEAR", "")).strip() != year_s:
                continue
            fips = normalize_county_fips(row.get("COUNTY_FIPS_CODE"))
            for care_type, (price_col, _flag_col) in columns.items():
                price = parse_ndcp_price_cell(row.get(price_col))
                if price is None:
                    continue
                out[(fips, care_type)] = price
        return out
    out = {}
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
    data_source: str = "fixture",
    study_year: int = 2022,
    care_setting: str = "market_center_median",
) -> dict[str, Any]:
    county = (county_fips or household.get("county_fips") or "").strip()
    if not county:
        raise ValueError("ndcp childcare requires county_fips")
    if data_source == "register":
        verified = validate_required_source_pins_or_abort([P4_C01_ID])
        src = resolve_ndcp_source(use_register=True)
        src["verified_sha256"] = verified[P4_C01_ID]
        src["fail_closed"] = True
    elif data_source == "fixture":
        src = resolve_ndcp_source(use_register=False)
    else:
        raise ValueError(f"unknown ndcp data_source {data_source!r}; use fixture or register")
    path_s = src.get("path")
    if not path_s:
        raise FileNotFoundError("NDCP source missing: register bytes absent and fixture missing")
    path = Path(path_s)
    if data_source == "register" and path.suffix.lower() == ".xlsx":
        from sources.ndcp_workbook import lookup_ndcp_weekly_prices, normalize_county_fips

        workbook_lookup = lookup_ndcp_weekly_prices(
            path,
            normalize_county_fips(county),
            study_year=study_year,
            care_setting=care_setting,
        )
        rates = {
            (workbook_lookup["county_fips"], care): wk
            for care, wk in workbook_lookup["weekly_usd_by_care_type"].items()
        }
        src["ndcp_workbook_row"] = workbook_lookup.get("workbook_row")
        src["ndcp_observed_records"] = workbook_lookup.get("records")
        src["ingest_mode"] = "register_xlsx_bounded_lookup"
    else:
        rates = load_ndcp_weekly_table(
            path, study_year=study_year, care_setting=care_setting
        )
        src["ingest_mode"] = "fixture_csv" if data_source == "fixture" else "register_csv"
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
        "source_vintage": f"NDCP_{int(study_year)}_county_weekly_observed_unapproved",
        "ndcp_study_year_observed": int(study_year),
        "ndcp_care_setting": care_setting,
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
