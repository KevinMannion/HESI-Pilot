"""Rebuild puma_fmr_screened.csv from ACS tract occupancy, tract-to-PUMA, and county HUD FMR.

Does not invent occupancy weights. Fails if any required hashed source is missing.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_tables import compare_csv, sha256

HASHES = {
    "acs_occupancy": "376160041b18b0fd4a002bedac8bd5f55c4ed1cbf9f38f257c0c36a2f3b7ed02",
    "tract_to_puma": "4093277e44c88f3506483a3eea988846b5992140f82ca4cc1b4e04b2cb9befb9",
    "county_model_ready": "f121cf328b3c71d7e84fe2073c50d3efe413b07ae2f335623ee5a4a20491dc8e",
}

def require(path, key):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"MISSING REQUIRED SOURCE {key}: {path}")
    got = sha256(path)
    if got != HASHES[key]:
        raise SystemExit(f"HASH MISMATCH {key}: {got} != {HASHES[key]}")
    return path

def build(acs_csv, tract_csv, hud_csv, out_csv):
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
    out = pd.DataFrame(recs)
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_csv, index=False)
    return {"pumas": len(out), "complete": int((out.status == "COMPLETE_UNAMBIGUOUS").sum())}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--acs-occupancy", required=True, help="tract_tenure_acs2024.csv from ACS 5-year B25003")
    p.add_argument("--tract-to-puma", required=True)
    p.add_argument("--county-model-ready", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--reference", default=str(ROOT / "inputs" / "puma_fmr_screened.csv"))
    p.add_argument("--report", required=True)
    a = p.parse_args()
    acs = require(a.acs_occupancy, "acs_occupancy")
    tr = require(a.tract_to_puma, "tract_to_puma")
    hud = require(a.county_model_ready, "county_model_ready")
    summary = build(acs, tr, hud, a.out)
    report = compare_csv(
        a.reference,
        a.out,
        key_fields=["puma_geoid"],
        numeric_fields=[
            "tracts",
            "missing_or_invalid_tracts",
            "occupied_acs2024_observed",
            "hud_exact_share_of_observed",
            "monthly_0br_benchmark",
            "monthly_1br_benchmark",
            "monthly_2br_benchmark",
            "monthly_3br_benchmark",
            "monthly_4br_benchmark",
        ],
        atol=1e-9,
    )
    report["build_summary"] = summary
    report["source_hashes_verified"] = HASHES
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "hash_match", "hash_mismatch_without_semantic_diff", "row_count_reference", "row_count_candidate")}, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
