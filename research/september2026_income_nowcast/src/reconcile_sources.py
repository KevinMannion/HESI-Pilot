"""Household money-income source reconstruction from 2024 ACS PUMS.

Does not apply a uniform inflation factor and does not compute a 2026 affordability share.
"""
from pathlib import Path
import json
import zipfile
import numpy as np
import pandas as pd

from hashutil import require_hash

PERSON_A_HASH = "05a4bdcb84fa8af1f3cc3034d9776a0a96e4311907fbb497298ff31bd445e6d8"
PERSON_B_HASH = "2a891e40a44dec1374b9885926e20bc275c5ee93d6a55a12d0386893d091712c"

SOURCES = ["WAGP", "SEMP", "RETP", "SSP", "SSIP", "INTP", "PAP", "OIP"]
SOURCE_LABELS = {
    "WAGP": "wages",
    "SEMP": "self_employment",
    "RETP": "retirement",
    "SSP": "social_security",
    "SSIP": "ssi",
    "INTP": "investment",
    "PAP": "public_assistance",
    "OIP": "other",
}
PCOLS = ["SERIALNO", "AGEP", "ADJINC", "PINCP", "PERNP"] + SOURCES
REP_COLS = [f"WGTP{i}" for i in range(1, 81)]


def _adj(amount, adjinc):
    return amount.astype("float64") * adjinc.astype("float64") / 1e6


def aggregate_person_income(person_zips):
    require_hash(person_zips[0], PERSON_A_HASH, "person_a")
    require_hash(person_zips[1], PERSON_B_HASH, "person_b")
    parts = []
    n_person_rows = 0
    n_under15 = 0
    for zpath in person_zips:
        with zipfile.ZipFile(zpath) as z:
            members = [
                n
                for n in z.namelist()
                if Path(n).name.lower().startswith("psam_pus") and n.lower().endswith(".csv")
            ]
            if not members:
                raise ValueError("Missing person CSV in " + str(zpath))
            for member in members:
                for d in pd.read_csv(
                    z.open(member),
                    usecols=PCOLS,
                    dtype={"SERIALNO": str},
                    chunksize=175000,
                ):
                    n_person_rows += len(d)
                    n_under15 += int((d.AGEP < 15).sum())
                    adj = pd.to_numeric(d.ADJINC, errors="coerce")
                    age = d.AGEP.to_numpy()
                    adult = age >= 15
                    rec = {"SERIALNO": d.SERIALNO.to_numpy(), "n_person": np.ones(len(d), dtype="int16"), "n_age15plus": adult.astype("int16")}
                    for col in SOURCES + ["PINCP", "PERNP"]:
                        raw = pd.to_numeric(d[col], errors="coerce")
                        val = np.where(adult, _adj(raw.fillna(0), adj).to_numpy(), 0.0)
                        rec[col] = val
                        rec[col + "_missing_age15plus"] = (adult & raw.isna()).astype("int16")
                        rec[col + "_negative"] = (adult & (raw < 0)).astype("int16")
                    rec["WAGP_plus_SEMP"] = rec["WAGP"] + rec["SEMP"]
                    parts.append(pd.DataFrame(rec))
                    print("persons", zpath, member, "so far", n_person_rows, flush=True)
    allp = pd.concat(parts, ignore_index=True)
    g = allp.groupby("SERIALNO", sort=False)
    hh = g.agg({c: "sum" for c in ["n_person", "n_age15plus"] + SOURCES + ["PINCP", "PERNP", "WAGP_plus_SEMP"] + [c + "_missing_age15plus" for c in SOURCES + ["PINCP", "PERNP"]] + [c + "_negative" for c in SOURCES]})
    return hh, {"person_rows": n_person_rows, "person_rows_under15": n_under15, "households_with_persons": len(hh)}


def reconcile(frame_path, person_income, out_path, report_json):
    frame = pd.read_pickle(frame_path)
    if frame.SERIALNO.duplicated().any():
        raise ValueError("Duplicate SERIALNO in eligibility frame")
    p = person_income.reindex(frame.SERIALNO)
    hincp_adj = _adj(pd.to_numeric(frame.HINCP, errors="coerce").fillna(0), pd.to_numeric(frame.ADJINC, errors="coerce"))
    component_sum = sum(p[s].fillna(0) for s in SOURCES)
    residual = hincp_adj.to_numpy() - component_sum.to_numpy()
    pincp_sum = p["PINCP"].fillna(0).to_numpy()
    pincp_vs_hincp = hincp_adj.to_numpy() - pincp_sum
    pernp_vs_earn = p["PERNP"].fillna(0).to_numpy() - p["WAGP_plus_SEMP"].fillna(0).to_numpy()
    out = frame.copy()
    out["hincp_adj_annual_2024"] = hincp_adj.to_numpy()
    out["hincp_month_2024_vintage"] = hincp_adj.to_numpy() / 12.0
    for s in SOURCES:
        out["src_" + SOURCE_LABELS[s]] = p[s].fillna(0).to_numpy()
        out["n_missing_" + SOURCE_LABELS[s]] = p[s + "_missing_age15plus"].fillna(0).to_numpy()
        out["n_negative_" + SOURCE_LABELS[s]] = p[s + "_negative"].fillna(0).to_numpy()
    out["component_sum_adj_annual"] = component_sum.to_numpy()
    out["residual_hincp_minus_components"] = residual
    out["abs_residual"] = np.abs(residual)
    out["pincp_sum_adj_annual"] = pincp_sum
    out["residual_hincp_minus_pincp"] = pincp_vs_hincp
    out["pernp_minus_wagp_semp"] = pernp_vs_earn
    out["n_person"] = p["n_person"].fillna(0).to_numpy()
    out["n_age15plus"] = p["n_age15plus"].fillna(0).to_numpy()
    out["person_table_missing"] = p["n_person"].isna().to_numpy()
    out["np_vs_n_person"] = out.NP.to_numpy() - out.n_person
    w = out.WGTP.to_numpy(dtype="float64")

    def wsum(mask):
        return float(w[mask].sum())

    abs_r = out.abs_residual.to_numpy()
    report = {
        "label": "ACS_2024_household_money_income_source_reconciliation",
        "not_a_2026_measurement": True,
        "national_affordability_nowcast_executed": False,
        "r24_frame_rows": int(len(out)),
        "r24_frame_weight": float(w.sum()),
        "person_table_missing_rows": int(out.person_table_missing.sum()),
        "person_table_missing_weight": wsum(out.person_table_missing.to_numpy()),
        "np_mismatch_rows": int((out.np_vs_n_person != 0).sum()),
        "hincp_negative_rows": int((out.hincp_adj_annual_2024 < 0).sum()),
        "hincp_negative_weight": wsum(out.hincp_adj_annual_2024.to_numpy() < 0),
        "hincp_zero_rows": int((out.hincp_adj_annual_2024 == 0).sum()),
        "residual_vs_components": {
            "mean_unweighted": float(np.mean(residual)),
            "mean_weighted": float((w * residual).sum() / w.sum()),
            "max_abs": float(np.max(abs_r)),
            "exact_zero_rows": int((abs_r == 0).sum()),
            "abs_lt_1_rows": int((abs_r < 1).sum()),
            "abs_lt_10_rows": int((abs_r < 10).sum()),
            "abs_ge_1_rows": int((abs_r >= 1).sum()),
            "abs_ge_1_weight": wsum(abs_r >= 1),
            "abs_ge_10_rows": int((abs_r >= 10).sum()),
            "abs_ge_10_weight": wsum(abs_r >= 10),
            "abs_ge_100_rows": int((abs_r >= 100).sum()),
            "abs_ge_100_weight": wsum(abs_r >= 100),
        },
        "residual_vs_pincp": {
            "mean_weighted": float((w * pincp_vs_hincp).sum() / w.sum()),
            "max_abs": float(np.max(np.abs(pincp_vs_hincp))),
            "abs_ge_1_rows": int((np.abs(pincp_vs_hincp) >= 1).sum()),
        },
        "pernp_vs_wagp_semp": {
            "mean_weighted": float((w * pernp_vs_earn).sum() / w.sum()),
            "max_abs": float(np.max(np.abs(pernp_vs_earn))),
            "abs_ge_1_rows": int((np.abs(pernp_vs_earn) >= 1).sum()),
        },
        "source_weighted_means_annual": {},
        "source_negative_households": {},
        "source_missing_age15plus_households": {},
        "source_zero_households": {},
        "largest_abs_residuals": [],
    }
    for s, lab in SOURCE_LABELS.items():
        col = out["src_" + lab].to_numpy()
        report["source_weighted_means_annual"][lab] = float((w * col).sum() / w.sum())
        report["source_negative_households"][lab] = {
            "rows": int((out["n_negative_" + lab] > 0).sum()),
            "weight": wsum(out["n_negative_" + lab].to_numpy() > 0),
        }
        report["source_missing_age15plus_households"][lab] = {
            "rows": int((out["n_missing_" + lab] > 0).sum()),
            "weight": wsum(out["n_missing_" + lab].to_numpy() > 0),
        }
        report["source_zero_households"][lab] = {
            "rows": int((col == 0).sum()),
            "weight": wsum(col == 0),
        }
    report["component_share_of_hincp_weighted"] = {}
    hpos = np.maximum(out.hincp_adj_annual_2024.to_numpy(), 0)
    hpos_w = w * (hpos > 0)
    denom = float((w * hpos).sum())
    for lab in SOURCE_LABELS.values():
        report["component_share_of_hincp_weighted"][lab] = float((w * out["src_" + lab].to_numpy()).sum() / denom) if denom else None
    report["component_share_of_hincp_weighted"]["residual"] = float((w * residual).sum() / denom) if denom else None
    top = out.nlargest(25, "abs_residual")[
        ["SERIALNO", "WGTP", "hincp_adj_annual_2024", "component_sum_adj_annual", "residual_hincp_minus_components"]
    ]
    report["largest_abs_residuals"] = json.loads(top.to_json(orient="records"))
    keep = [
        "SERIALNO",
        "STATE",
        "PUMA",
        "NP",
        "TEN",
        "WGTP",
        *REP_COLS,
        "hincp_adj_annual_2024",
        "hincp_month_2024_vintage",
        *[f"src_{SOURCE_LABELS[s]}" for s in SOURCES],
        "component_sum_adj_annual",
        "residual_hincp_minus_components",
        "pincp_sum_adj_annual",
        "residual_hincp_minus_pincp",
        "n_person",
        "n_age15plus",
        "person_table_missing",
    ]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    out[keep].to_pickle(out_path)
    Path(report_json).parent.mkdir(parents=True, exist_ok=True)
    Path(report_json).write_text(json.dumps(report, indent=2) + "\n")
    return report
