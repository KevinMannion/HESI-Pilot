"""Phase 3 four-model occupied ACS backtests. No 2026 national adequacy share.

Gates were declared in reports/VALIDATION_GATES.json before this comparison code ran.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from reconstruct_year import reconstruct, SOURCES
from hashutil import sha256_file

FROZEN_R24_THREE_COST_MONTH = 2894.90805340822
NATIONAL_R22_SHA = "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7"
REP = [f"WGTP{i}" for i in range(1, 81)]


def sdr_se(rep_vals, point):
    rep_vals = np.asarray(rep_vals, dtype=float)
    return float(np.sqrt((4.0 / 80.0) * ((rep_vals - point) ** 2).sum()))


def weighted_mean(df, col):
    w = df.WGTP.to_numpy(dtype=float)
    return float((w * df[col].to_numpy(dtype=float)).sum() / w.sum())


def weighted_means(df):
    out = {"weight": float(df.WGTP.sum()), "rows": int(len(df))}
    for col in ["hincp_adj", *SOURCES, "residual"]:
        out[col] = weighted_mean(df, col)
    return out


def share_below(df, annual_income):
    w = df.WGTP.to_numpy(dtype=float)
    below = (annual_income / 12.0) < FROZEN_R24_THREE_COST_MONTH
    p = float((w * below).sum() / w.sum())
    reps = df[REP].to_numpy(dtype=float)
    pr = (reps * below[:, None]).sum(axis=0) / reps.sum(axis=0)
    return p, sdr_se(pr, p)


def weighted_quantiles(df, col, qs=(0.1, 0.25, 0.5, 0.75, 0.9)):
    w = df.WGTP.to_numpy(dtype=float)
    v = df[col].to_numpy(dtype=float)
    order = np.argsort(v)
    v, w = v[order], w[order]
    cdf = np.cumsum(w) / w.sum()
    out = {}
    for q in qs:
        out[str(q)] = float(v[np.searchsorted(cdf, q, side="left").clip(0, len(v) - 1)])
    return out


def apply_models(df, fac):
    ahe = fac["ahe_total_private"]
    awe = fac["awe_total_private"]
    cpi = fac["cpi_u_nsa"]
    cola = 1.0 + fac["cola_january_tplus1"]
    wagp = df.WAGP.to_numpy(dtype=float)
    semp = df.SEMP.to_numpy(dtype=float)
    intp = df.INTP.to_numpy(dtype=float)
    pos_w = wagp > 0
    pos_s = semp >= 0
    pos_i = intp >= 0

    m1 = df.copy()
    m1["model"] = "M1_freeze"

    m2 = df.copy()
    m2["model"] = "M2_uniform_cpi"
    for col in [*SOURCES, "residual", "hincp_adj"]:
        m2[col] = df[col] * cpi

    m3 = df.copy()
    m3["model"] = "M3_aggregate_wage"
    m3["WAGP"] = np.where(pos_w, wagp * ahe, wagp)
    m3["hincp_adj"] = m3[SOURCES].sum(axis=1) + m3["residual"]

    m4 = df.copy()
    m4["model"] = "M4_source_specific"
    m4["WAGP"] = np.where(pos_w, wagp * awe, wagp)
    # BEA proprietors/interest not acquired: freeze SEMP and INTP (including negatives).
    m4["SEMP"] = semp
    m4["INTP"] = intp
    m4["SSP"] = df.SSP * cola
    m4["SSIP"] = df.SSIP * cola
    m4["hincp_adj"] = m4[SOURCES].sum(axis=1) + m4["residual"]
    return {"M1_freeze": m1, "M2_uniform_cpi": m2, "M3_aggregate_wage": m3, "M4_source_specific": m4}


def subgroup_masks(df):
    h = df.hincp_adj.to_numpy(dtype=float)
    denom = np.maximum(np.abs(h), 1.0)
    wage_share = df.WAGP.to_numpy(dtype=float) / denom
    ret_share = (df.SSP + df.SSIP + df.RETP).to_numpy(dtype=float) / denom
    w = df.WGTP.to_numpy(dtype=float)
    order = np.argsort(h)
    cdf = np.cumsum(w[order]) / w.sum()
    terc = np.empty(len(df), dtype=int)
    terc[order] = np.where(cdf <= 1 / 3, 1, np.where(cdf <= 2 / 3, 2, 3))
    return {
        "all": np.ones(len(df), dtype=bool),
        "positive_wages": df.WAGP.to_numpy(dtype=float) > 0,
        "zero_wages": df.WAGP.to_numpy(dtype=float) <= 0,
        "wage_majority": wage_share >= 0.5,
        "retirement_majority": ret_share >= 0.5,
        "income_tercile_1": terc == 1,
        "income_tercile_2": terc == 2,
        "income_tercile_3": terc == 3,
    }


def score(actual, pred, label):
    ma, mp = weighted_means(actual), weighted_means(pred)
    err = {k: mp[k] - ma[k] for k in ["hincp_adj", *SOURCES]}
    pct = {k: (err[k] / ma[k] if ma[k] else None) for k in err}
    p_act, se_act = share_below(actual, actual.hincp_adj.to_numpy(dtype=float))
    p_hat, se_hat = share_below(pred, pred.hincp_adj.to_numpy(dtype=float))
    q_act = weighted_quantiles(actual, "hincp_adj")
    q_hat = weighted_quantiles(pred, "hincp_adj")
    q_err = {k: q_hat[k] - q_act[k] for k in q_act}
    masks_a, masks_p = subgroup_masks(actual), subgroup_masks(pred)
    subgroups = {}
    for name in masks_a:
        da, dp = actual.loc[masks_a[name]], pred.loc[masks_p[name]]
        if len(da) == 0 or len(dp) == 0 or da.WGTP.sum() == 0 or dp.WGTP.sum() == 0:
            continue
        a_m, p_m = weighted_mean(da, "hincp_adj"), weighted_mean(dp, "hincp_adj")
        pa, _ = share_below(da, da.hincp_adj.to_numpy(dtype=float))
        pp, _ = share_below(dp, dp.hincp_adj.to_numpy(dtype=float))
        subgroups[name] = {
            "actual_rows": int(len(da)),
            "pred_rows": int(len(dp)),
            "actual_weight": float(da.WGTP.sum()),
            "pred_weight": float(dp.WGTP.sum()),
            "actual_mean_hincp": a_m,
            "pred_mean_hincp": p_m,
            "pct_error_hincp": (p_m - a_m) / a_m if a_m else None,
            "actual_share_below": pa,
            "pred_share_below": pp,
            "share_error": pp - pa,
        }
    return {
        "label": label,
        "actual_weighted_means_annual": ma,
        "projected_weighted_means_annual": mp,
        "error_projected_minus_actual": err,
        "pct_error": pct,
        "quantiles_actual": q_act,
        "quantiles_projected": q_hat,
        "quantile_error": q_err,
        "diagnostic_share": {
            "note": "NOT 18.9918%. Occupied households, frozen $2,894.91/mo three-cost mean.",
            "actual_share": p_act,
            "actual_sampling_se_sdr": se_act,
            "projected_share": p_hat,
            "projected_sampling_se_sdr_factors_fixed": se_hat,
            "share_error_projected_minus_actual": p_hat - p_act,
        },
        "subgroups": subgroups,
    }


def evaluate_gates(comparisons, series_ok, r22_ok):
    gates = json.loads((HERE.parent / "reports" / "VALIDATION_GATES.json").read_text())
    results = []

    def pair(year_label, model):
        return next(c for c in comparisons if c["year"] == year_label and c["model"] == model)

    g1 = {"id": "G1_series_acquired", "pass": series_ok["pass"], "detail": series_ok["detail"]}
    results.append(g1)
    g2_ok = True
    g2_detail = {}
    for yr in ("2022_to_2023", "2023_to_2024"):
        e = abs(pair(yr, "M4_source_specific")["pct_error"]["hincp_adj"])
        g2_detail[yr] = e
        g2_ok = g2_ok and e <= 0.015
    results.append({"id": "G2_hincp_mean", "pass": g2_ok, "abs_pct_error": g2_detail})
    g3_ok = True
    g3_detail = {}
    for yr in ("2022_to_2023", "2023_to_2024"):
        e = abs(pair(yr, "M4_source_specific")["diagnostic_share"]["share_error_projected_minus_actual"])
        g3_detail[yr] = e
        g3_ok = g3_ok and e <= 0.005
    results.append({"id": "G3_share", "pass": g3_ok, "abs_share_error": g3_detail})
    g4_ok = True
    g4_detail = {}
    for yr in ("2022_to_2023", "2023_to_2024"):
        e = abs(pair(yr, "M4_source_specific")["pct_error"]["WAGP"])
        g4_detail[yr] = e
        g4_ok = g4_ok and e <= 0.020
    results.append({"id": "G4_wagp", "pass": g4_ok, "abs_pct_error": g4_detail})
    g5_ok = True
    g5_detail = {}
    for yr in ("2022_to_2023", "2023_to_2024"):
        e4 = abs(pair(yr, "M4_source_specific")["pct_error"]["hincp_adj"])
        e1 = abs(pair(yr, "M1_freeze")["pct_error"]["hincp_adj"])
        g5_detail[yr] = {"M4": e4, "M1": e1, "beats_freeze": e4 < e1}
        g5_ok = g5_ok and e4 < e1
    results.append({"id": "G5_beats_freeze", "pass": g5_ok, "detail": g5_detail})
    results.append({"id": "G6_no_cpi_production", "pass": True, "detail": "M2 scored only; not selected"})
    results.append({"id": "G7_uncertainty_separated", "pass": True, "detail": "SDR SE and share error stored in separate fields"})
    results.append({"id": "G8_baselines_frozen", "pass": r22_ok, "national_R22_sha256": NATIONAL_R22_SHA})
    all_pass = all(g["pass"] for g in results)
    return {
        "declared_gates_file": "reports/VALIDATION_GATES.json",
        "declared_before_comparisons": gates["declared_before_phase3_model_comparisons"],
        "results": results,
        "all_pass": all_pass,
        "go_nogo": "GO" if all_pass else "NO-GO",
        "national_2026_adequacy_share_published": False,
    }


def asec_vs_acs(acs, asec):
    acs_w = float(acs.WGTP.sum())
    acs_means = {k: weighted_mean(acs, k) for k in ["hincp_adj", *SOURCES]}
    asec_means = asec["means"]
    acs_share = {k: acs_means[k] / acs_means["hincp_adj"] for k in SOURCES}
    asec_map = {
        "WAGP": "wages",
        "SEMP": "self_employment",
        "SSP": "social_security",
        "SSIP": "ssi",
        "RETP": "pension",
        "INTP": "interest",
        "PAP": "public_assistance",
        "OIP": "other",
    }
    asec_total = asec_means["total"]
    rows = {}
    for acs_k, asec_k in asec_map.items():
        am = asec_means.get(asec_k)
        rows[acs_k] = {
            "acs2024_occupied_mean": acs_means[acs_k],
            "acs2024_share_of_hincp": acs_share[acs_k],
            "asec2026_cy2025_mean": am,
            "asec2026_share_of_htotval": (am / asec_total) if am is not None else None,
        }
    return {
        "kind": "independent_benchmark_not_a_match",
        "do_not_equate_means": True,
        "acs_occupied_weight": acs_w,
        "asec_weight_sum_after_div100": asec["weight_sum_after_div100"],
        "acs_mean_hincp": acs_means["hincp_adj"],
        "asec_mean_htotval": asec_total,
        "source_shares": rows,
        "limitations": [
            "ACS 2024 occupied PUMS vs CPS ASEC 2026 calendar-year 2025 money income.",
            "Different sampling frames, weights, reference periods, and source taxonomies (ASEC splits pension/annuity/dividends/rent; ACS bundles RETP and INTP).",
            "Not a test of September 2026 nowcast accuracy.",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cache", required=True)
    p.add_argument("--factors", required=True)
    p.add_argument("--asec", required=True)
    p.add_argument("--housing-2022", required=True)
    p.add_argument("--person-2022", required=True)
    p.add_argument("--housing-2023", required=True)
    p.add_argument("--person-2023", required=True)
    p.add_argument("--housing-2024", required=True)
    p.add_argument("--person-2024-a", required=True)
    p.add_argument("--person-2024-b", required=True)
    p.add_argument("--national-r22", required=True)
    p.add_argument("--report", required=True)
    a = p.parse_args()
    cache = Path(a.cache)
    cache.mkdir(parents=True, exist_ok=True)
    meta = {}
    for year, hus, pus in [
        (2022, a.housing_2022, [a.person_2022]),
        (2023, a.housing_2023, [a.person_2023]),
        (2024, a.housing_2024, [a.person_2024_a, a.person_2024_b]),
    ]:
        pk = cache / f"occupied_sources_{year}.pkl"
        if pk.exists():
            print("reuse", pk, flush=True)
            meta[str(year)] = {"reused": True, "path": str(pk)}
        else:
            meta[str(year)] = reconstruct(hus, pus, pk)
    d22 = pd.read_pickle(cache / "occupied_sources_2022.pkl")
    d23 = pd.read_pickle(cache / "occupied_sources_2023.pkl")
    d24 = pd.read_pickle(cache / "occupied_sources_2024.pkl")
    facs = json.loads(Path(a.factors).read_text())
    comparisons = []
    for y0, y1, origin, actual in [("2022", "2023", d22, d23), ("2023", "2024", d23, d24)]:
        key = f"{y0}_to_{y1}"
        models = apply_models(origin, facs["factors"][key])
        for mname, pred in models.items():
            row = score(actual, pred, f"ACS{y0}_{mname}_vs_ACS{y1}_occupied")
            row["year"] = key
            row["model"] = mname
            row["factors_used"] = {
                k: facs["factors"][key][k]
                for k in (
                    "ahe_total_private",
                    "awe_total_private",
                    "cpi_u_nsa",
                    "cola_january_tplus1",
                    "bea_proprietors",
                    "bea_interest_dividends",
                    "simulated_forecast_date",
                    "vintage_limitation",
                )
            }
            comparisons.append(row)
            d = row["diagnostic_share"]
            print(key, mname, "hincp_pct", row["pct_error"]["hincp_adj"], "share_err", d["share_error_projected_minus_actual"], flush=True)
    r22_sha = sha256_file(a.national_r22)
    series_ok = {
        "pass": False,
        "detail": {
            "ces_ahe_awe_hours_employment": True,
            "eci": True,
            "cpi_u": True,
            "bea_proprietors": False,
            "bea_interest_dividends": False,
            "alfred_vintages": False,
        },
    }
    gates = evaluate_gates(comparisons, series_ok, r22_sha == NATIONAL_R22_SHA)
    asec = json.loads(Path(a.asec).read_text())
    report = {
        "national_2026_adequacy_share_published": False,
        "core_r24_18_9918_modified": False,
        "computational_reproduction": "Phase 3 backtests executed on hashed ACS PUMS and hashed BLS API JSON.",
        "scientific_validation": False,
        "go_nogo": gates["go_nogo"],
        "gates": gates,
        "comparisons": comparisons,
        "asec_independent_benchmark": asec_vs_acs(d24, asec),
        "acs_2025_tables": {"status": "NOT_RELEASED", "scheduled": "2026-10-29"},
        "reconstruction_meta": meta,
        "factor_file_sha256": sha256_file(a.factors),
        "bls_json_sha256": facs["source_sha256"],
        "national_R22_sha256": r22_sha,
        "error_attribution": [
            "M1 error is the ACS year-to-year change in occupied mean income plus composition change between independent samples.",
            "M3/M4 wage factors are national CES job-earnings indices applied only to ACS households with WAGP>0; they cannot capture occupation mix, hours of household earners, or new/lost jobs.",
            "M4 cannot grow SEMP/INTP because BEA Table 2.6 machine series were not acquired.",
            "Quantile and subgroup errors mix within-household income change with ACS sample composition change; the two cannot be separated without a panel.",
            "BLS API current vintage includes CES revisions; ALFRED first-print vintages were not acquired (FRED maintenance).",
        ],
    }
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2) + "\n")
    print("GO_NOGO", gates["go_nogo"], "all_pass", gates["all_pass"])


if __name__ == "__main__":
    main()
