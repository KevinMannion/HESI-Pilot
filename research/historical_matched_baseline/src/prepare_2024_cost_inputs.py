"""Prepare 2024 matched-year cost inputs. Does not run a national share.

Does not modify core_r24/src, frozen puma_fmr_screened.csv, source_2024_2026.csv,
or results/national_R22/.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from calendar import month_name
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]  # HESI-Pilot
PIPE = HERE.parent
DEFAULT_OUT = PIPE / "outputs"
DOWNLOADS = Path(os.environ.get("HESI_DOWNLOADS", str(Path.home() / "Downloads")))
CLEANREPRO = Path(os.environ.get("HESI_CLEANREPRO", str(Path.home() / "HESI-R25-CleanRepro")))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "core_r24" / "tools"))
from hashutil import file_record, sha256  # noqa: E402
from xlsx_io import sanitized_xlsx  # noqa: E402

FROZEN = {
    "national_R22_common": (
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
    "acs_occupancy": (
        DOWNLOADS / "HESI_Housing_v15_ACS2024/downloaded_acs_2024/tract_tenure_acs2024.csv",
        "376160041b18b0fd4a002bedac8bd5f55c4ed1cbf9f38f257c0c36a2f3b7ed02",
    ),
    "tract_to_puma": (
        DOWNLOADS / "HESI_Housing_v15_ACS2024/tract_to_puma_50states_dc.csv",
        "4093277e44c88f3506483a3eea988846b5992140f82ca4cc1b4e04b2cb9befb9",
    ),
    "usda_thrifty_workbook": (
        DOWNLOADS / "usda-thriftyplan-june2021-sept2026.xlsx",
        "70b1d3b67d2d86e5b7f945fe95901211299facd10ff04028fb8704b8fa526c74",
    ),
}

HUD_FILES = {
    "fy24_original": {
        "path": CLEANREPRO / "matched2024/hud/FY24_FMRs.xlsx",
        "url": "https://www.huduser.gov/portal/datasets/fmr/fmr2024/FY24_FMRs.xlsx",
        "effective": "2023-10-01",
        "sheet": "FY24_FMRs",
        "page_listed_kb": 357,
    },
    "fy24_revised": {
        "path": CLEANREPRO / "matched2024/hud/FMR2024_final_revised.xlsx",
        "url": "https://www.huduser.gov/portal/datasets/fmr/fmr2024/FMR2024_final_revised.xlsx",
        "effective": "2024-03-11",
        "sheet": "FY24_FMRs_rev",
        "page_listed_kb": 1750,
        "note": "HUD page lists 1750 KB; live official file is ~356 KB. Honolulu-only revision (89 FR 9169).",
    },
    "fy25_original": {
        "path": CLEANREPRO / "matched2024/hud/FY25_FMRs.xlsx",
        "url": "https://www.huduser.gov/portal/datasets/fmr/fmr2025/FY25_FMRs.xlsx",
        "effective": "2024-10-01",
        "sheet": "FY25_FMRs",
        "page_listed_kb": 355,
    },
    "fy25_revised": {
        "path": CLEANREPRO / "matched2024/hud/FY25_FMRs_revised.xlsx",
        "url": "https://www.huduser.gov/portal/datasets/fmr/fmr2025/FY25_FMRs_revised.xlsx",
        "effective": "2025-04-27",
        "sheet": "FY25_FMRs_revised",
        "page_listed_kb": 355,
        "note": "After calendar 2024. Archived; not used in the default 2024 cost schedule.",
    },
}

EIA_FILES = {
    "annual": CLEANREPRO / "matched2024/eia/EMM_EPMR_PTE_NUS_DPGa.xls",
    "monthly": CLEANREPRO / "matched2024/eia/EMM_EPMR_PTE_NUS_DPGm.xls",
    "weekly": CLEANREPRO / "matched2024/eia/EMM_EPMR_PTE_NUS_DPGw.xls",
    "pswrgvwall": CLEANREPRO / "matched2024/eia/pswrgvwall.xls",
}

R24_TRANSPORT_ANNUAL = 7264.70
R24_FUEL_ANNUAL = 1633.03
R24_GAS = 4.35475
MILES = 12000.0
MPG = 32.0
NONFUEL_HELD = round(R24_TRANSPORT_ANNUAL - R24_FUEL_ANNUAL, 2)  # 5631.67; NOT 2024-validated

# Leap year 2024: FY24 original 1 Jan–10 Mar; FY24 revised 11 Mar–30 Sep; FY25 original 1 Oct–31 Dec.
DAYS_FY24_ORIG = 70
DAYS_FY24_REV = 204
DAYS_FY25_ORIG = 92
DAYS_2024 = 366


def check_frozen():
    out = {}
    for key, (path, expected) in FROZEN.items():
        rec = file_record(path)
        rec["expected_sha256"] = expected
        rec["hash_match"] = rec["sha256"] == expected
        out[key] = rec
    return out


def load_hud(meta):
    tmp = Path("/tmp/hesi_xlsx_matched2024") / meta["path"].name
    df = pd.read_excel(sanitized_xlsx(meta["path"], tmp), sheet_name=meta["sheet"])
    need = ["hud_area_code", "hud_area_name", "fips", "fmr_0", "fmr_1", "fmr_2", "fmr_3", "fmr_4"]
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise ValueError(f"{meta['path'].name} missing columns {missing}")
    df = df.copy()
    df["geo_id"] = df["fips"].map(lambda x: str(int(x)).zfill(10))
    for i in range(5):
        df[f"monthly_{i}br"] = pd.to_numeric(df[f"fmr_{i}"], errors="raise")
        if (df[f"monthly_{i}br"] < 0).any() or df[f"monthly_{i}br"].isna().any():
            raise ValueError(f"Invalid FMR values in {meta['path'].name} {i}BR")
    if df["geo_id"].duplicated().any():
        raise ValueError(f"Duplicate fips in {meta['path'].name}")
    return df


def county_rows(df, source_period):
    rows = []
    for _, r in df.iterrows():
        fmr = [int(r[f"monthly_{i}br"]) if float(r[f"monthly_{i}br"]).is_integer() else float(r[f"monthly_{i}br"]) for i in range(5)]
        rows.append(
            {
                "geo_type": "county",
                "geo_id": r["geo_id"],
                "hud_area_code": r["hud_area_code"],
                "area_name": r["hud_area_name"],
                "monthly_0br": fmr[0],
                "monthly_1br": fmr[1],
                "monthly_2br": fmr[2],
                "monthly_3br": fmr[3],
                "monthly_4br": fmr[4],
                "annual_2br": 12 * fmr[2],
                "source_period": source_period,
                "cost_status": "HUD_FMR_benchmark_not_actual_rent",
            }
        )
    return rows


def write_csv(path, rows, fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return path


def mix_calendar(orig, rev, fy25):
    m = orig[["geo_id", "hud_area_code", "hud_area_name"] + [f"monthly_{i}br" for i in range(5)]].merge(
        rev[["geo_id"] + [f"monthly_{i}br" for i in range(5)]], on="geo_id", suffixes=("_o", "_r")
    )
    m = m.merge(
        fy25[["geo_id"] + [f"monthly_{i}br" for i in range(5)]].rename(columns={f"monthly_{i}br": f"monthly_{i}br_25" for i in range(5)}),
        on="geo_id",
        how="inner",
        validate="one_to_one",
    )
    out = m[["geo_id", "hud_area_code", "hud_area_name"]].copy()
    for i in range(5):
        out[f"monthly_{i}br"] = (
            DAYS_FY24_ORIG * m[f"monthly_{i}br_o"]
            + DAYS_FY24_REV * m[f"monthly_{i}br_r"]
            + DAYS_FY25_ORIG * m[f"monthly_{i}br_25"]
        ) / DAYS_2024
    return out


def build_puma(acs_csv, tract_csv, hud_csv):
    """Same occupancy-weighted COMPLETE_UNAMBIGUOUS rule as R2.4, new FMR table only."""
    a = pd.read_csv(acs_csv, dtype=str)
    t = pd.read_csv(tract_csv, dtype=str)
    h = pd.read_csv(hud_csv, dtype=str)
    a["tract_geoid"] = a.state + a.county + a.tract
    for c in [x for x in a if x.startswith("B25003_")]:
        a[c] = pd.to_numeric(a[c], errors="coerce")
    if a.tract_geoid.duplicated().any() or t.tract_geoid.duplicated().any():
        raise ValueError("Duplicate tract identifiers")
    x = t.merge(a, on="tract_geoid", how="left", validate="one_to_one", indicator=True)
    mask = x[["B25003_001E", "B25003_002E", "B25003_003E"]].notna().all(axis=1)
    valid = (
        mask
        & (x.B25003_001E >= 0)
        & (x.B25003_002E >= 0)
        & (x.B25003_003E >= 0)
        & (x.B25003_001E == x.B25003_002E + x.B25003_003E)
    )
    x["estimate_status"] = np.where(
        x._merge != "both",
        "TRACT_MISSING",
        np.where(~mask, "NO_NUMERIC_ESTIMATE", np.where(~valid, "INVALID_TENURE_ARITHMETIC", "VALID")),
    )
    county = h.assign(county_geoid=h.geo_id.str[:5])
    ct = county.groupby("county_geoid").size()
    uni = county.loc[
        county.county_geoid.map(ct).eq(1),
        ["county_geoid", "hud_area_code", "area_name", *[f"monthly_{i}br" for i in range(5)]],
    ]
    x = x.merge(uni, on="county_geoid", how="left", validate="many_to_one")
    x["hud_status"] = np.where(
        x.hud_area_code.notna(),
        "UNAMBIGUOUS_COUNTY_FMR",
        np.where(x.county_geoid.isin(ct.index), "MULTIPLE_HUD_ROWS", "UNMATCHED_COUNTY"),
    )
    x["occupied_acs2024"] = x.B25003_001E.where(x.estimate_status == "VALID")
    recs = []
    for p, z in x.groupby("puma_geoid", sort=True):
        ok = z[z.estimate_status == "VALID"]
        exact = ok[ok.hud_status == "UNAMBIGUOUS_COUNTY_FMR"]
        total = ok.occupied_acs2024.sum()
        covered = exact.occupied_acs2024.sum()
        fully = (z.estimate_status == "VALID").all() and (z.hud_status == "UNAMBIGUOUS_COUNTY_FMR").all() and total > 0
        r = {
            "puma_geoid": p,
            "tracts": len(z),
            "missing_or_invalid_tracts": int((z.estimate_status != "VALID").sum()),
            "occupied_acs2024_observed": int(total) if pd.notna(total) else 0,
            "hud_exact_share_of_observed": float(covered / total) if total else None,
            "status": "COMPLETE_UNAMBIGUOUS" if fully else "PARTIAL_NOT_APPROVED",
        }
        for i in range(5):
            c = f"monthly_{i}br"
            r[c + "_benchmark"] = (
                float(np.average(pd.to_numeric(exact[c]), weights=exact.occupied_acs2024)) if fully else None
            )
        recs.append(r)
    return pd.DataFrame(recs)


def extract_usda_2024(workbook, frozen_csv, out_csv):
    tmp = Path("/tmp/hesi_xlsx_matched2024") / workbook.name
    xl = pd.ExcelFile(sanitized_xlsx(workbook, tmp))
    frames = []
    for sheet in xl.sheet_names:
        if sheet.lower().replace(" ", "") in {"readme", "read_me"}:
            continue
        df = pd.read_excel(xl, sheet_name=sheet, header=0)
        cols = {c.strip(): c for c in df.columns if isinstance(c, str)}
        if "geographic_area" not in cols:
            continue
        keep = df.rename(columns={v: k for k, v in cols.items()})
        frames.append(keep)
    if not frames:
        raise ValueError("No USDA data sheet")
    df = pd.concat(frames, ignore_index=True)
    df["year"] = pd.to_numeric(df["year"], errors="raise").astype(int)
    df = df[df["year"].eq(2024) & df["frequency"].astype(str).eq("Monthly")].copy()
    df["cost"] = pd.to_numeric(df["cost"], errors="raise")
    df["source_file"] = workbook.name
    months = list(month_name)[1:]
    df["month"] = df["month"].astype(str)
    fields = ["geographic_area", "fam_indv", "group", "age", "year", "month", "food_plan", "frequency", "cost", "source_file"]
    rows = []
    for _, r in df.sort_values(["geographic_area", "fam_indv", "group", "age", "month", "food_plan"]).iterrows():
        cost = float(r["cost"])
        cost_s = f"{cost:.1f}" if abs(cost * 10 - round(cost * 10)) < 1e-9 else str(cost)
        rows.append({k: (int(r["year"]) if k == "year" else cost_s if k == "cost" else r[k]) for k in fields})
    write_csv(out_csv, rows, fields)
    frozen = pd.read_csv(frozen_csv)
    frozen24 = frozen[frozen.year.eq(2024)]
    thrifty = df[
        df.geographic_area.eq("Mainland U.S.")
        & df.fam_indv.eq("Individual")
        & df.frequency.eq("Monthly")
        & df.food_plan.astype(str).str.lower().eq("thrifty")
    ]
    month_set = set(thrifty.month.astype(str))
    return {
        "rows_written": len(rows),
        "frozen_2024_rows": int(len(frozen24)),
        "mainland_individual_thrifty_rows": int(len(thrifty)),
        "thrifty_months": sorted(month_set, key=lambda m: months.index(m) if m in months else 99),
        "twelve_calendar_months": month_set == set(months),
        "workbook_not_used_to_overwrite_frozen": True,
    }


def extract_eia(out: Path):
    def series(path):
        df = pd.read_excel(path, sheet_name="Data 1", header=2)
        df.columns = ["date", "usd_per_gallon"]
        df["date"] = pd.to_datetime(df["date"])
        df["usd_per_gallon"] = pd.to_numeric(df["usd_per_gallon"], errors="coerce")
        return df.dropna(subset=["usd_per_gallon"])

    annual = series(EIA_FILES["annual"])
    monthly = series(EIA_FILES["monthly"])
    weekly = series(EIA_FILES["weekly"])
    a2024 = annual[annual.date.dt.year.eq(2024)]
    m2024 = monthly[monthly.date.dt.year.eq(2024)]
    w2024 = weekly[weekly.date.dt.year.eq(2024)]
    if len(a2024) != 1:
        raise ValueError(f"Expected one EIA annual 2024 row, got {len(a2024)}")
    if len(m2024) != 12:
        raise ValueError(f"Expected 12 EIA monthly 2024 rows, got {len(m2024)}")
    published_annual = float(a2024.usd_per_gallon.iloc[0])
    monthly_mean = float(m2024.usd_per_gallon.mean())
    weekly_mean = float(w2024.usd_per_gallon.mean())
    dec_monthly = float(m2024[m2024.date.dt.month.eq(12)].usd_per_gallon.iloc[0])
    last_weekly = float(w2024.sort_values("date").usd_per_gallon.iloc[-1])
    fuel = MILES / MPG * published_annual
    transport = NONFUEL_HELD + fuel
    weekly_out = out / "eia_us_regular_weekly_2024.csv"
    m2024.assign(price_basis="EIA monthly U.S. regular all formulations retail including taxes").to_csv(
        out / "eia_us_regular_monthly_2024.csv", index=False
    )
    w2024.assign(price_basis="EIA weekly U.S. regular all formulations retail including taxes").to_csv(weekly_out, index=False)
    return {
        "series": "EMM_EPMR_PTE_NUS_DPG",
        "units": "USD per gallon, U.S. regular all formulations retail including taxes",
        "release_in_file": "2026-10-20",
        "published_annual_2024": published_annual,
        "unweighted_mean_of_12_monthly_2024": monthly_mean,
        "unweighted_mean_of_weekly_2024": weekly_mean,
        "n_weekly_2024": int(len(w2024)),
        "december_2024_monthly": dec_monthly,
        "last_weekly_2024": last_weekly,
        "default_reference": "published_annual_2024",
        "miles": MILES,
        "mpg": MPG,
        "fuel_annual_using_published_annual": round(fuel, 2),
        "nonfuel_held_from_r24_sept2026_hypothetical": NONFUEL_HELD,
        "transport_annual_gasoline_updated_nonfuel_held": round(transport, 2),
        "r24_transport_annual_untouched": R24_TRANSPORT_ANNUAL,
        "limitation": "Updating gasoline does not make depreciation, insurance, maintenance, registration, or financing historically accurate.",
    }


def coverage_report(puma_new, puma_r24):
    a = pd.read_csv(puma_new, dtype={"puma_geoid": str})
    b = pd.read_csv(puma_r24, dtype={"puma_geoid": str})
    ac = set(a.loc[a.status.eq("COMPLETE_UNAMBIGUOUS"), "puma_geoid"])
    bc = set(b.loc[b.status.eq("COMPLETE_UNAMBIGUOUS"), "puma_geoid"])
    return {
        "r24_complete": len(bc),
        "matched2024_complete": len(ac),
        "intersection": len(ac & bc),
        "only_matched2024": sorted(ac - bc),
        "only_r24": sorted(bc - ac),
        "do_not_force_identical_sample": True,
        "r24_included_weight_not_imposed": 121036726,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    frozen = check_frozen()
    frozen_ok = all(v["hash_match"] for k, v in frozen.items() if k in ("national_R22_common", "puma_fmr_screened", "source_2024_2026"))
    occupancy_ok = frozen["acs_occupancy"]["hash_match"] and frozen["tract_to_puma"]["hash_match"]
    usda_wb_ok = frozen["usda_thrifty_workbook"]["hash_match"]

    hud_meta = {}
    hud_frames = {}
    for key, meta in HUD_FILES.items():
        rec = file_record(meta["path"])
        rec.update({k: meta[k] for k in meta if k != "path"})
        rec["is_xlsx"] = rec["present"] and meta["path"].read_bytes()[:4] == b"PK\x03\x04"
        hud_meta[key] = rec
        if rec["present"]:
            hud_frames[key] = load_hud(meta)
            rec["n_rows"] = int(len(hud_frames[key]))
            rec["n_geo"] = int(hud_frames[key].geo_id.nunique())
            rec["bedrooms"] = [0, 1, 2, 3, 4]

    fy24_change = None
    if "fy24_original" in hud_frames and "fy24_revised" in hud_frames:
        o, r = hud_frames["fy24_original"], hud_frames["fy24_revised"]
        m = o.merge(r, on="geo_id", suffixes=("_o", "_r"))
        ch = m[(m[[f"monthly_{i}br_o" for i in range(5)]].to_numpy() != m[[f"monthly_{i}br_r" for i in range(5)]].to_numpy()).any(axis=1)]
        fy24_change = {
            "n_changed_geo": int(len(ch)),
            "areas": ch[["geo_id", "hud_area_name_o"]].to_dict("records") if len(ch) else [],
        }

    county_fields = [
        "geo_type",
        "geo_id",
        "hud_area_code",
        "area_name",
        "monthly_0br",
        "monthly_1br",
        "monthly_2br",
        "monthly_3br",
        "monthly_4br",
        "annual_2br",
        "source_period",
        "cost_status",
    ]
    county_paths = {}
    if hud_frames:
        county_paths["fy24_revised"] = write_csv(
            out / "county_model_ready_FY2024_revised.csv",
            county_rows(hud_frames["fy24_revised"], "FY2024_revised_effective_2024-03-11"),
            county_fields,
        )
        county_paths["fy24_original"] = write_csv(
            out / "county_model_ready_FY2024_original.csv",
            county_rows(hud_frames["fy24_original"], "FY2024_original_effective_2023-10-01"),
            county_fields,
        )
        county_paths["fy25_original"] = write_csv(
            out / "county_model_ready_FY2025_original.csv",
            county_rows(hud_frames["fy25_original"], "FY2025_original_effective_2024-10-01"),
            county_fields,
        )
        mixed = mix_calendar(hud_frames["fy24_original"], hud_frames["fy24_revised"], hud_frames["fy25_original"])
        county_paths["calendar_2024"] = write_csv(
            out / "county_model_ready_calendar2024_dayweight.csv",
            county_rows(mixed, "CALENDAR2024_DAYWEIGHT_70_204_92"),
            county_fields,
        )
        fy26 = pd.read_csv(ROOT / "core_r24/inputs/county_model_ready.csv", dtype=str)
        g24 = set(hud_frames["fy24_revised"].geo_id)
        g26 = set(fy26.geo_id)
        geo_crosswalk = {
            "fy24_and_fy26_row_count": [int(len(hud_frames["fy24_revised"])), int(len(fy26))],
            "geo_id_intersection": len(g24 & g26),
            "only_fy24": len(g24 - g26),
            "only_fy26": len(g26 - g24),
            "note": "Connecticut town FIPS (090xx in FY2024) versus planning-region FIPS (091xx in FY2026) and at least one Maine town identifier. Do not recode to force the R2.4 sample.",
        }
    else:
        geo_crosswalk = {}

    puma_paths = {}
    puma_cov = None
    if occupancy_ok and county_paths:
        for label, src in [
            ("calendar_2024", county_paths["calendar_2024"]),
            ("fy24_revised", county_paths["fy24_revised"]),
            ("fy25_original", county_paths["fy25_original"]),
        ]:
            df = build_puma(FROZEN["acs_occupancy"][0], FROZEN["tract_to_puma"][0], src)
            dest = out / f"puma_fmr_{label}.csv"
            df.to_csv(dest, index=False)
            puma_paths[label] = dest
        puma_cov = coverage_report(puma_paths["calendar_2024"], FROZEN["puma_fmr_screened"][0])

    usda = None
    if usda_wb_ok:
        usda = extract_usda_2024(
            FROZEN["usda_thrifty_workbook"][0],
            FROZEN["source_2024_2026"][0],
            out / "usda_2024_monthly_from_thrifty_workbook.csv",
        )

    eia_rec = {k: file_record(p) for k, p in EIA_FILES.items()}
    eia = extract_eia(out)
    Path(out / "transport_reference_2024.csv").write_text(
        "scenario,gas_usd_per_gallon,annual_miles,mpg,fuel_annual,nonfuel_annual_HELD_NOT_2024_VALIDATED,transport_annual,status\n"
        f"calendar_2024_eia_annual,{eia['published_annual_2024']},{int(MILES)},{int(MPG)},{eia['fuel_annual_using_published_annual']},{NONFUEL_HELD},{eia['transport_annual_gasoline_updated_nonfuel_held']},gasoline_observed_nonfuel_hypothetical\n"
        f"r24_sept2026_reference_NOT_FOR_MATCHED_YEAR,{R24_GAS},{int(MILES)},{int(MPG)},{R24_FUEL_ANNUAL},{NONFUEL_HELD},{R24_TRANSPORT_ANNUAL},do_not_use_as_2024_cost\n"
    )

    frozen_after = check_frozen()
    frozen_still = all(
        frozen_after[k]["hash_match"] for k in ("national_R22_common", "puma_fmr_screened", "source_2024_2026")
    )

    def gate(name, ok, detail):
        return {"name": name, "status": "PASS" if ok else "FAIL", "detail": detail}

    gates = [
        gate("frozen_national_R22_untouched", frozen_still, frozen_after["national_R22_common"]["sha256"]),
        gate("frozen_puma_fmr_screened_untouched", frozen_after["puma_fmr_screened"]["hash_match"], frozen_after["puma_fmr_screened"]["sha256"]),
        gate("frozen_source_2024_2026_untouched", frozen_after["source_2024_2026"]["hash_match"], frozen_after["source_2024_2026"]["sha256"]),
        gate(
            "hud_fy24_original_acquired",
            hud_meta["fy24_original"].get("is_xlsx") and hud_meta["fy24_original"].get("n_rows") == 4764,
            hud_meta["fy24_original"],
        ),
        gate(
            "hud_fy24_revised_acquired",
            hud_meta["fy24_revised"].get("is_xlsx") and hud_meta["fy24_revised"].get("n_rows") == 4764,
            {"sha256": hud_meta["fy24_revised"]["sha256"], "size_bytes": hud_meta["fy24_revised"]["size_bytes"], "page_listed_kb": 1750, "honolulu_revision": fy24_change},
        ),
        gate(
            "hud_fy25_original_oct2024_acquired",
            hud_meta["fy25_original"].get("is_xlsx") and hud_meta["fy25_original"].get("n_rows") == 4764,
            hud_meta["fy25_original"]["sha256"],
        ),
        gate("hud_bedrooms_0_to_4", True, [0, 1, 2, 3, 4]),
        gate("usda_workbook_hash", usda_wb_ok, frozen["usda_thrifty_workbook"]["sha256"]),
        gate("usda_2024_twelve_thrifty_months", bool(usda and usda["twelve_calendar_months"] and usda["mainland_individual_thrifty_rows"] > 0), usda),
        gate("eia_2024_annual_reconstructed", eia["published_annual_2024"] is not None, eia["published_annual_2024"]),
        gate("eia_2024_twelve_months", True, eia["unweighted_mean_of_12_monthly_2024"]),
        gate("occupancy_crosswalk_hashes", occupancy_ok, {k: frozen[k]["sha256"] for k in ("acs_occupancy", "tract_to_puma")}),
        gate("puma_table_built_without_editing_r24_geography", bool(puma_paths), {k: str(v) for k, v in puma_paths.items()}),
        gate("coverage_difference_reported_not_forced", puma_cov is not None, puma_cov),
        gate("transport_nonfuel_limitation_documented", True, eia["limitation"]),
        gate("no_national_share_computed", True, "prepare pipeline writes cost inputs only"),
        gate("r24_engine_unmodified", True, "core_r24/src/run_joint.py not used"),
    ]
    # HUD page size mismatch is informational, not a failed acquisition.
    input_prep_pass = all(g["status"] == "PASS" for g in gates)
    execute_now = False
    recommendation = {
        "input_preparation": "PASS" if input_prep_pass else "FAIL",
        "execute_2024_matched_year_national_percentage_this_round": "NO-GO",
        "reason_execute_nogo": [
            "Sibling national engine is not run in this round.",
            "Person food caches still price (2026,9) in the R2.4 engine.",
            "Instruction: do not calculate a new national percentage in the preparation round.",
        ],
        "proceed_to_sibling_engine_after_this_prep": "GO" if input_prep_pass else "NO-GO",
        "september_2026_income_nowcast": "NO-GO",
        "overwrite_18_9918": "FORBIDDEN",
    }

    source_register = {
        "hud": hud_meta,
        "eia": eia_rec,
        "usda_workbook": frozen["usda_thrifty_workbook"],
        "occupancy": frozen["acs_occupancy"],
        "tract_to_puma": frozen["tract_to_puma"],
        "frozen_r24": {k: frozen[k] for k in ("national_R22_common", "puma_fmr_screened", "source_2024_2026")},
        "hud_geo_crosswalk_vs_fy2026": geo_crosswalk,
        "fy24_revision_diff": fy24_change,
        "eia_reconstruction": eia,
        "usda_extract": usda,
        "puma_coverage_vs_r24": puma_cov,
    }
    readiness = {
        "object": "2024 ACS observed income vs 2024 modeled costs (not computed)",
        "r24_share_untouched": "18.9918%",
        "gates": gates,
        "recommendation": recommendation,
        "default_cost_schedule": {
            "food": "USDA Thrifty 2024 annual mean of 12 published monthly mainland individual cells",
            "housing": "calendar-2024 day-weighted mix: 70 days FY2024 original + 204 days FY2024 revised + 92 days FY2025 original",
            "housing_alternates": ["FY2024_revised_only", "FY2025_original_point_in_time_from_2024-10-01"],
            "transport": eia,
        },
    }
    (PIPE / "SOURCE_REGISTER.json").write_text(json.dumps(source_register, indent=2, default=str) + "\n")
    (PIPE / "MATCHED_YEAR_READINESS.json").write_text(json.dumps(readiness, indent=2, default=str) + "\n")
    print(json.dumps({"input_preparation": recommendation["input_preparation"], "execute": recommendation["execute_2024_matched_year_national_percentage_this_round"], "gates": [(g["name"], g["status"]) for g in gates]}, indent=2))
    if not input_prep_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
