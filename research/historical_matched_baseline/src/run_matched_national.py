"""Validate inputs, rebuild 2024 food caches if needed, run the matched-year scenario and sensitivities."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIPE = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from rebuild_matched_food_cache import rebuild  # noqa: E402
from run_matched import SHARE, run_matched  # noqa: E402
from validate_matched_inputs import validate  # noqa: E402

DEFAULT_TRANSPORT = 6870.67
R24_FRAME_ROWS = 1235731
R24_FRAME_WEIGHT = 121036726.0
FROZEN_R22 = "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_share(csv_path):
    with open(csv_path, newline="") as f:
        rows = {r["metric"]: r for r in csv.DictReader(f)}
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--housing", required=True)
    p.add_argument("--person-official")
    p.add_argument("--person-a")
    p.add_argument("--person-b")
    p.add_argument("--out", help="Scratch output. Required for official runs. Never matched2024_provisional.")
    p.add_argument("--cache", help="Scratch cache. Required for official runs.")
    p.add_argument("--exploratory", action="store_true", help="Permit local_runs/local_caches defaults; cannot write frozen artifacts")
    p.add_argument("--model-vintage", help="Required for official runs, e.g. matched2024_provisional_repro")
    p.add_argument("--config", help="Required JSON configuration for official runs")
    a = p.parse_args()
    if a.exploratory:
        if not a.out:
            a.out = str(PIPE / "local_runs/matched2024")
        if not a.cache:
            a.cache = str(PIPE / "local_caches")
        run_class = "exploratory"
        cfg = None
    else:
        if not a.out:
            p.error("Official matched-year run requires --out scratch path (or pass --exploratory)")
        if not a.cache:
            p.error("Official matched-year run requires --cache scratch path")
        if not a.model_vintage:
            p.error("Official matched-year run requires --model-vintage")
        if not a.config:
            p.error("Official matched-year run requires --config")
        run_class = "official"
        sys.path.insert(0, str(ROOT / "core_r24" / "tools"))
        from official_config import load_official_config
        cfg = load_official_config(a.config, engine="matched_year_2024", model_vintage=a.model_vintage)
    sys.path.insert(0, str(ROOT / "core_r24" / "tools"))
    from protected_paths import assert_output_allowed

    out = assert_output_allowed(a.out, "matched-year --out")
    assert_output_allowed(Path(a.cache), "matched-year --cache")
    frozen_matched = (PIPE / "results/matched2024_provisional").resolve()
    if out == frozen_matched or frozen_matched in out.parents:
        raise SystemExit("Refusing to write matched2024_provisional")
    validation = validate(a.housing, a.person_official, a.person_a, a.person_b)
    if validation["status"] != "PASS":
        raise SystemExit("Input validation FAIL: " + ",".join(validation["failed"]))
    out.mkdir(parents=True, exist_ok=True)
    (out / "INPUT_VALIDATION.json").write_text(json.dumps(validation, indent=2, default=str) + "\n")

    cache = Path(a.cache)
    food_pkl = cache / "acs2024_food_person_aggregates.pkl"
    comp_pkl = cache / "acs2024_person_composition.pkl"
    if not (food_pkl.is_file() and comp_pkl.is_file()):
        zips = [a.person_official] if a.person_official else [a.person_a, a.person_b]
        rebuild(zips, ROOT / "core_r24/inputs/source_2024_2026.csv", cache)
    import pandas as pd

    food = pd.read_pickle(food_pkl)
    if "thrifty_2024annual" not in food.columns:
        raise SystemExit("Food cache missing thrifty_2024annual; refuse to use 2026-09 cache")

    geos = [
        ("calendar_2024_dayweight", PIPE / "outputs/puma_fmr_calendar_2024.csv", True),
        ("fy24_revised_only", PIPE / "outputs/puma_fmr_fy24_revised.csv", False),
        ("fy25_original_from_2024_10_01", PIPE / "outputs/puma_fmr_fy25_original.csv", False),
    ]
    runs = {}
    for name, geo, is_default in geos:
        dest = out / name
        print("RUN", name, flush=True)
        audit = run_matched(a.housing, food_pkl, comp_pkl, geo, dest, DEFAULT_TRANSPORT)
        rows = read_share(dest / "common_cohort_results.csv")
        frame = audit["frame"]
        runs[name] = {
            "default": is_default,
            "share": float(rows[SHARE]["mean"]),
            "share_se": float(rows[SHARE]["se_sdr"]),
            "share_ci90": [float(rows[SHARE]["ci90_low"]), float(rows[SHARE]["ci90_high"])],
            "no_car": float(rows["share_below_cost_NO_CAR_sensitivity"]["mean"]),
            "food_month": float(rows["food_month"]["mean"]),
            "housing_month": float(rows["housing_month"]["mean"]),
            "transport_month": float(rows["one_vehicle_month_GASOLINE_2024_NONFUEL_HELD"]["mean"]),
            "income_month": float(rows["income_month_ACS2024_observed"]["mean"]),
            "included_rows": int(frame["included_rows"]),
            "included_weight": float(frame["included_weight"]),
            "geography_excluded_rows": int(frame["geography_excluded_rows"]),
            "geography_excluded_weight": float(frame["geography_excluded_weight"]),
            "frame_matches_r24": bool(frame["included_rows"] == R24_FRAME_ROWS and abs(frame["included_weight"] - R24_FRAME_WEIGHT) < 1e-6),
            "output": str(dest),
        }

    default = runs["calendar_2024_dayweight"]
    r22 = read_share(ROOT / "core_r24/results/national_R22/common_cohort_results.csv")
    r24_share = float(r22["share_income_below_three_costs_PROVISIONAL"]["mean"])
    gates = [
        {"name": "input_validation", "status": validation["status"]},
        {"name": "frozen_national_R22_untouched", "status": "PASS" if sha256(ROOT / "core_r24/results/national_R22/common_cohort_results.csv") == FROZEN_R22 else "FAIL"},
        {"name": "nowcast_nogo", "status": "PASS"},
        {"name": "household_specific_not_g3_uniform", "status": "PASS"},
        {"name": "default_frame_matches_r24_eligibility_count", "status": "PASS" if default["frame_matches_r24"] else "FAIL", "detail": default},
        {"name": "did_not_write_national_R22", "status": "PASS"},
        {
            "name": "share_not_claimed_scientifically_validated",
            "status": "PASS",
            "detail": "PROVISIONAL / NOT SCIENTIFICALLY VALIDATED",
        },
    ]
    failed = [g["name"] for g in gates if g["status"] != "PASS"]
    report = {
        "decision": "PROVISIONAL_RESULT_NOT_A_PUBLICATION",
        "scientifically_validated": False,
        "externally_independently_reproduced": False,
        "september_2026_income_nowcast": "NO-GO",
        "r24_share_untouched": "18.9918%",
        "r24_share_numeric": r24_share,
        "pilot_share_untouched": "10.301%",
        "default_scenario": {
            "name": "calendar_2024_dayweight housing; USDA 2024 Thrifty annual mean; EIA 2024 gasoline $3.304; nonfuel held $5631.67",
            "share_income_below_three_costs_2024matched_MODELED": default["share"],
            "public_rounding_suggestion": round(default["share"] * 100, 1),
            **{k: default[k] for k in default if k != "default"},
        },
        "sensitivities": {
            "transport_no_car_on_default_housing": default["no_car"],
            "housing_fy24_revised_only": runs["fy24_revised_only"],
            "housing_fy25_original": runs["fy25_original_from_2024_10_01"],
            "geographic_coverage": validation["coverage"],
        },
        "limitations": [
            "Non-fuel transport is an inherited R2.4 hypothetical, not a 2024 insurance/depreciation/maintenance observation.",
            "One car assigned to every included household.",
            "HUD FMR is replacement rent, not observed household rent.",
            "USDA mainland Thrifty cells are used for all states including AK/HI.",
            "Infant households excluded; >4 bedroom compositions excluded.",
            "ACS income is a rolling 12-month amount, not a December cash-flow snapshot.",
            "SDR intervals are sampling-only.",
            "Not a September 2026 hardship rate and not a nowcast.",
        ],
        "gates": gates,
        "failed_gates": failed,
        "python": sys.version,
        "run_class": run_class,
        "model_vintage": a.model_vintage,
        "exploratory_defaults_documented": bool(a.exploratory),
        "config_path": str(Path(a.config).resolve()) if a.config else None,
        "config_sha256": sha256(a.config) if a.config else None,
        "scientific_publication": cfg["scientific_publication"] if cfg else None,
        "operator_note": "EXECUTED_BY_AUTHOR; CLEAN_ENVIRONMENT_REPRODUCED not re-run for this object; EXTERNALLY_INDEPENDENTLY_REPRODUCED=NO",
    }
    (out / "EXECUTION_REPORT.json").write_text(json.dumps(report, indent=2, default=str) + "\n")
    (out / "VALIDATION_GATES.json").write_text(json.dumps({"gates": gates, "failed": failed, "status": "PASS" if not failed else "FAIL"}, indent=2, default=str) + "\n")
    manifest = {
        "housing_zip": {"path": a.housing, "sha256": sha256(a.housing)},
        "person": {"official": a.person_official, "person_a": a.person_a, "person_b": a.person_b},
        "usda_prices": {"path": str(ROOT / "core_r24/inputs/source_2024_2026.csv"), "sha256": sha256(ROOT / "core_r24/inputs/source_2024_2026.csv")},
        "food_cache_sha256": sha256(food_pkl),
        "composition_cache_sha256": sha256(comp_pkl),
        "geography": {name: {"path": str(path), "sha256": sha256(path)} for name, path, _ in geos},
        "transport_table": {"path": str(PIPE / "outputs/transport_reference_2024.csv"), "sha256": sha256(PIPE / "outputs/transport_reference_2024.csv")},
        "numpy": os.environ.get("HESI_NUMPY", "see execution python"),
    }
    (out / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, default=str) + "\n")
    print(json.dumps({"status": "PASS" if not failed else "FAIL", "default_share": default["share"], "failed": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
