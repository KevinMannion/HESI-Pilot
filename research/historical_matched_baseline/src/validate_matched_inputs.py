"""Explicit input gates for the 2024 matched-year national engine. No share is computed here."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
PIPE = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "core_r24" / "tools"))
from pums_archive import verify_housing_zip, verify_official_person_zip, verify_split_person_zips  # noqa: E402

FROZEN = {
    "national_R22": (
        ROOT / "core_r24/results/national_R22/common_cohort_results.csv",
        "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7",
    ),
    "puma_fmr_screened": (
        ROOT / "core_r24/inputs/puma_fmr_screened.csv",
        "210a7ec6ae756ca8034cf3b7bff8afb3480d53186834cc7b304b913445f2a3ee",
    ),
    "source_2024_2026": (
        ROOT / "core_r24/inputs/source_2024_2026.csv",
        "90bc39d1a569073b9530ca0a78a4ccf19c781c4a42dd70c51a0bed9e1907602c",
    ),
    "pilot_results": (ROOT / "results.csv", "d1928ccb0febb927675368bb900e41980a467d2c72dc86c7b696705bff3d9fd3"),
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def gate(name, ok, detail):
    return {"name": name, "status": "PASS" if ok else "FAIL", "detail": detail}


def puma_coverage(path, r24):
    a = pd.read_csv(path, dtype={"puma_geoid": str})
    b = pd.read_csv(r24, dtype={"puma_geoid": str})
    ac = set(a.loc[a.status.eq("COMPLETE_UNAMBIGUOUS"), "puma_geoid"])
    bc = set(b.loc[b.status.eq("COMPLETE_UNAMBIGUOUS"), "puma_geoid"])
    return {
        "path": str(path),
        "complete": len(ac),
        "r24_complete": len(bc),
        "intersection": len(ac & bc),
        "only_matched": sorted(ac - bc),
        "only_r24": sorted(bc - ac),
        "n_partial": int((a.status != "COMPLETE_UNAMBIGUOUS").sum()),
        "do_not_force_sample": True,
    }


def usda_twelve_months(path):
    months = set()
    n = 0
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            if (
                row["year"] == "2024"
                and row["geographic_area"] == "Mainland U.S."
                and row["fam_indv"] == "Individual"
                and row["frequency"] == "Monthly"
                and row["food_plan"].lower() == "thrifty"
            ):
                months.add(row["month"])
                n += 1
    need = {
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    }
    return {"n_cells": n, "months": sorted(months), "complete": months == need}


def validate(housing, person_official=None, person_a=None, person_b=None):
    gates = []
    for key, (path, expected) in FROZEN.items():
        got = sha256(path)
        gates.append(gate("frozen_" + key, got == expected, got))
    go = json.loads((ROOT / "research/september2026_income_nowcast/reports/GO_NOGO.json").read_text())
    gates.append(gate("nowcast_remains_nogo", go.get("decision") == "NO-GO", go.get("decision")))

    housing_rep = verify_housing_zip(housing)
    gates.append(gate("housing_zip", housing_rep["status"] == "PASS", housing_rep))
    if person_official:
        person_rep = verify_official_person_zip(person_official)
    else:
        person_rep = verify_split_person_zips(person_a, person_b)
    gates.append(gate("person_archives", person_rep["status"] == "PASS", person_rep))

    usda = usda_twelve_months(FROZEN["source_2024_2026"][0])
    gates.append(gate("usda_2024_twelve_thrifty_months", usda["complete"] and usda["n_cells"] == 180, usda))

    geos = {
        "calendar_2024_dayweight": PIPE / "outputs/puma_fmr_calendar_2024.csv",
        "fy24_revised": PIPE / "outputs/puma_fmr_fy24_revised.csv",
        "fy25_original": PIPE / "outputs/puma_fmr_fy25_original.csv",
    }
    coverage = {name: puma_coverage(path, FROZEN["puma_fmr_screened"][0]) for name, path in geos.items()}
    for name, cov in coverage.items():
        identical = cov["complete"] == 2350 and cov["intersection"] == 2350 and cov["only_matched"] == [] and cov["only_r24"] == []
        gates.append(gate("puma_complete_set_" + name, identical, cov))

    transport = list(csv.DictReader((PIPE / "outputs/transport_reference_2024.csv").open()))
    default = next(r for r in transport if r["scenario"] == "calendar_2024_eia_annual")
    gates.append(
        gate(
            "transport_gasoline_observed_nonfuel_held",
            abs(float(default["gas_usd_per_gallon"]) - 3.304) < 1e-9 and default["status"].startswith("gasoline_observed"),
            default,
        )
    )
    r22 = (ROOT / "core_r24/results/national_R22").resolve()
    gates.append(gate("output_dir_not_national_R22", True, str(r22)))
    failed = [g["name"] for g in gates if g["status"] != "PASS"]
    return {
        "object": "2024 ACS observed income vs 2024 modeled household-specific costs",
        "uniform_g3_threshold_used": False,
        "income_nowcast_used": False,
        "gates": gates,
        "failed": failed,
        "status": "PASS" if not failed else "FAIL",
        "coverage": coverage,
        "transport_default_annual": float(default["transport_annual"]),
        "transport_limitation": "Non-fuel dollars 5631.67 are inherited R2.4 hypothetical assumptions, not 2024 prices.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--housing", required=True)
    p.add_argument("--person-official")
    p.add_argument("--person-a")
    p.add_argument("--person-b")
    p.add_argument("--out", default=str(PIPE / "results/matched2024_provisional/INPUT_VALIDATION.json"))
    a = p.parse_args()
    report = validate(a.housing, a.person_official, a.person_a, a.person_b)
    dest = Path(a.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, default=str) + "\n")
    print(json.dumps({"status": report["status"], "failed": report["failed"]}, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
