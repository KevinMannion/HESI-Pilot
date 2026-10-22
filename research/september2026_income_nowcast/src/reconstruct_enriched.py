"""Occupied reconstruction plus NP, max age, and age 65+ count.

Does not change source identity or R2.4 eligibility. New pickle schema for Phase 4.
"""
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd

SOURCES = ["WAGP", "SEMP", "RETP", "SSP", "SSIP", "INTP", "PAP", "OIP"]
PCOLS = ["SERIALNO", "AGEP", "ADJINC"] + SOURCES
HCOLS = ["SERIALNO", "TYPEHUGQ", "NP", "WGTP", "HINCP", "ADJINC"] + [f"WGTP{i}" for i in range(1, 81)]


def _adj(amount, adjinc):
    return amount.astype("float64") * adjinc.astype("float64") / 1e6


def _zip_members(z, prefix):
    return sorted(
        n
        for n in z.namelist()
        if Path(n).name.lower().startswith(prefix) and n.lower().endswith(".csv")
    )


def reconstruct_enriched(housing_zip, person_zips, out_pickle):
    person_parts = []
    demo_parts = []
    n_person = 0
    zips = person_zips if isinstance(person_zips, (list, tuple)) else [person_zips]
    for zp in zips:
        with zipfile.ZipFile(zp) as z:
            for member in _zip_members(z, "psam_pus"):
                for d in pd.read_csv(z.open(member), usecols=PCOLS, dtype={"SERIALNO": str}, chunksize=200000):
                    n_person += len(d)
                    adj = pd.to_numeric(d.ADJINC, errors="coerce")
                    age = pd.to_numeric(d.AGEP, errors="coerce").fillna(0)
                    adult = age.to_numpy() >= 15
                    rec = {"SERIALNO": d.SERIALNO.to_numpy()}
                    for col in SOURCES:
                        raw = pd.to_numeric(d[col], errors="coerce").fillna(0)
                        rec[col] = np.where(adult, _adj(raw, adj).to_numpy(), 0.0)
                    person_parts.append(pd.DataFrame(rec))
                    demo_parts.append(
                        pd.DataFrame(
                            {
                                "SERIALNO": d.SERIALNO.to_numpy(),
                                "max_age": age.to_numpy(),
                                "n_65plus": (age.to_numpy() >= 65).astype("float64"),
                                "n_adults": adult.astype("float64"),
                            }
                        )
                    )
                    print("persons", zp, member, n_person, flush=True)
    persons = pd.concat(person_parts, ignore_index=True).groupby("SERIALNO", sort=False)[SOURCES].sum()
    demo = pd.concat(demo_parts, ignore_index=True).groupby("SERIALNO", sort=False).agg(
        max_age=("max_age", "max"), n_65plus=("n_65plus", "sum"), n_adults=("n_adults", "sum")
    )
    hparts = []
    n_occ = 0
    with zipfile.ZipFile(housing_zip) as z:
        for member in _zip_members(z, "psam_hus"):
            header = pd.read_csv(z.open(member), nrows=0)
            cols = [c for c in HCOLS if c in header.columns]
            for h in pd.read_csv(z.open(member), usecols=cols, dtype={"SERIALNO": str}, chunksize=150000):
                h = h.loc[h.TYPEHUGQ.eq(1) & h.NP.gt(0) & h.WGTP.gt(0)].copy()
                n_occ += len(h)
                hparts.append(h)
                print("occupied housing", member, n_occ, flush=True)
    hh = pd.concat(hparts, ignore_index=True)
    p = persons.reindex(hh.SERIALNO)
    d = demo.reindex(hh.SERIALNO)
    hincp = _adj(pd.to_numeric(hh.HINCP, errors="coerce").fillna(0), pd.to_numeric(hh.ADJINC, errors="coerce"))
    out = hh[["SERIALNO", "NP", "WGTP"] + [c for c in hh.columns if c.startswith("WGTP") and c[4:].isdigit()]].copy()
    out["hincp_adj"] = hincp.to_numpy()
    for s in SOURCES:
        out[s] = p[s].fillna(0).to_numpy()
    out["max_age"] = d["max_age"].fillna(0).to_numpy()
    out["n_65plus"] = d["n_65plus"].fillna(0).to_numpy()
    out["n_adults"] = d["n_adults"].fillna(0).to_numpy()
    out["component_sum"] = sum(out[s] for s in SOURCES)
    out["residual"] = out["hincp_adj"] - out["component_sum"]
    Path(out_pickle).parent.mkdir(parents=True, exist_ok=True)
    out.to_pickle(out_pickle)
    return {"person_rows": n_person, "occupied_rows": len(out), "occupied_weight": float(out.WGTP.sum()), "path": str(out_pickle)}
