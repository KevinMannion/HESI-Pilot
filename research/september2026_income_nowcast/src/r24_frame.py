"""Rebuild the Core R2.4 eligibility frame without recomputing affordability shares.

Uses the same occupancy, geography, composition, bedroom, and infant rules as
core_r24/src/run_joint.py. Does not alter Food, Housing, or Transportation formulas.
"""
from pathlib import Path
import numpy as np
import pandas as pd

from hashutil import require_hash

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "core_r24"

HOUSING_HASH = "8281008e53de98f0ef81e7a2ee5a8725991dda1ecfd2713ead73246425e515d0"
GEO_HASH = "210a7ec6ae756ca8034cf3b7bff8afb3480d53186834cc7b304b913445f2a3ee"

REP_COLS = [f"WGTP{i}" for i in range(1, 81)]
HCOLS = ["SERIALNO", "STATE", "PUMA", "TYPEHUGQ", "NP", "WGTP", "HINCP", "ADJINC", "TEN"] + REP_COLS

PUBLISHED_FRAME = {
    "raw_rows": 1631969,
    "occupied_rows": 1348408,
    "occupied_weight": 132737145.0,
    "geography_excluded_rows": 64079,
    "geography_excluded_weight": 6271320.0,
    "composition_excluded_rows": 113,
    "composition_excluded_weight": 17463.0,
    "over4_excluded_rows": 23486,
    "over4_excluded_weight": 2591711.0,
    "infant_excluded_rows": 24999,
    "infant_excluded_weight": 2819925.0,
    "included_rows": 1235731,
    "included_weight": 121036726.0,
}


def load_person_table(path):
    path = Path(path)
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path, dtype={"SERIALNO": str})
        if "SERIALNO" in df.columns:
            df = df.set_index("SERIALNO")
        return df
    return pd.read_pickle(path)


def build_frame(housing_zip, food_cache, composition_cache, geography, out_path):
    require_hash(housing_zip, HOUSING_HASH, "housing")
    require_hash(geography, GEO_HASH, "geography")
    food = load_person_table(food_cache)[["thrifty_2026sep", "n_person", "n_infant"]]
    comp = load_person_table(composition_cache)
    geo = pd.read_csv(geography, dtype={"puma_geoid": str})
    geo = geo.loc[geo.status.eq("COMPLETE_UNAMBIGUOUS")].set_index("puma_geoid")
    if not food.index.is_unique or not comp.index.is_unique or not geo.index.is_unique:
        raise ValueError("Duplicate key in a lookup")
    totals = {k: 0 for k in PUBLISHED_FRAME}
    parts = []
    import zipfile

    with zipfile.ZipFile(housing_zip) as z:
        members = sorted(
            n
            for n in z.namelist()
            if n.lower().split("/")[-1].startswith("psam_hus") and n.lower().endswith(".csv")
        )
        for member in members:
            for h in pd.read_csv(
                z.open(member),
                usecols=HCOLS,
                dtype={"SERIALNO": str, "STATE": str, "PUMA": str},
                chunksize=100000,
            ):
                totals["raw_rows"] += len(h)
                h = h.loc[h.TYPEHUGQ.eq(1) & h.NP.gt(0) & h.WGTP.gt(0)].copy()
                totals["occupied_rows"] += len(h)
                totals["occupied_weight"] += float(h.WGTP.sum())
                h["puma_geoid"] = h.STATE.str.zfill(2) + h.PUMA.str.zfill(5)
                good = h.puma_geoid.isin(geo.index)
                totals["geography_excluded_rows"] += int((~good).sum())
                totals["geography_excluded_weight"] += float(h.loc[~good, "WGTP"].sum())
                h = h.loc[good].copy()
                if h.empty:
                    continue
                c = comp.reindex(h.SERIALNO)
                f = food.reindex(h.SERIALNO)
                valid = (
                    c[["adult", "child", "partner"]].notna().all(axis=1).to_numpy()
                    & f[["n_person", "n_infant", "thrifty_2026sep"]].notna().all(axis=1).to_numpy()
                )
                ad = c.adult.to_numpy()
                ch = c.child.to_numpy()
                pt = c.partner.to_numpy()
                valid &= (
                    ((ad + ch) == h.NP.to_numpy())
                    & (f.n_person.to_numpy() == h.NP.to_numpy())
                    & (pt <= ad)
                    & (ad >= 1)
                )
                totals["composition_excluded_rows"] += int((~valid).sum())
                totals["composition_excluded_weight"] += float(h.loc[~valid, "WGTP"].sum())
                h = h.loc[valid].copy()
                c = c.iloc[np.flatnonzero(valid)]
                f = f.iloc[np.flatnonzero(valid)]
                if h.empty:
                    continue
                br = (c.adult.to_numpy() - np.minimum(c.partner.to_numpy(), 1) + np.ceil(c.child.to_numpy() / 2)).astype(int)
                passbr = (br >= 1) & (br <= 4)
                totals["over4_excluded_rows"] += int((~passbr).sum())
                totals["over4_excluded_weight"] += float(h.loc[~passbr, "WGTP"].sum())
                h = h.iloc[np.flatnonzero(passbr)].copy()
                f = f.iloc[np.flatnonzero(passbr)]
                if h.empty:
                    continue
                notinf = f.n_infant.to_numpy() == 0
                totals["infant_excluded_rows"] += int((~notinf).sum())
                totals["infant_excluded_weight"] += float(h.loc[~notinf, "WGTP"].sum())
                h = h.iloc[np.flatnonzero(notinf)].copy()
                if h.empty:
                    continue
                totals["included_rows"] += len(h)
                totals["included_weight"] += float(h.WGTP.sum())
                parts.append(h)
                print("processed", member, "eligible so far", totals["included_rows"], flush=True)
    frame = pd.concat(parts, ignore_index=True)
    mismatches = {k: (totals[k], PUBLISHED_FRAME[k]) for k in PUBLISHED_FRAME if totals[k] != PUBLISHED_FRAME[k]}
    # float weights: allow tiny drift
    for k, (got, exp) in list(mismatches.items()):
        if isinstance(exp, float) and abs(got - exp) < 1e-6:
            mismatches.pop(k)
        elif got == exp:
            mismatches.pop(k)
    if mismatches:
        raise SystemExit(f"R2.4 eligibility frame mismatch: {mismatches}")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_pickle(out_path)
    return {"frame": totals, "rows_written": len(frame), "path": str(out_path)}
