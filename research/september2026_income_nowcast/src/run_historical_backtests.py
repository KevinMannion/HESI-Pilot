"""Historical backtests on acquired ACS PUMS. No 2026 national adequacy share.

Wage/SEMP/investment factors are frozen (factor=1) because CES/ECI/BEA time series
downloads failed (HTTP 403 / HTML stubs). SS/SSI uses statutory January COLA of T+1.

Diagnostic share-below uses the published R2.4 three-cost monthly mean as a frozen
cost index. That is NOT the Core R2.4 18.9918% result.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from reconstruct_year import reconstruct, SOURCES

# Statutory OASDI/SSI COLA payable in January of the calendar year (Federal Register).
# Kind: observation of a legal notice, not an ACS measurement.
COLA_JANUARY = {
    2023: 0.087,  # 87 FR 64296 / FR Doc 2022-23073
    2024: 0.032,  # 88 FR / FR Doc 2023-23317
    2025: 0.025,  # FR Doc 2024-24871
    2026: 0.028,  # 90 FR / FR Doc 2025-19763
}

# Published R2.4 three-cost monthly mean. Frozen diagnostic cost, not a 2026 nowcast.
FROZEN_R24_THREE_COST_MONTH = 2894.90805340822

REP = [f"WGTP{i}" for i in range(1, 81)]


def sdr_se(rep_vals, point):
    rep_vals = np.asarray(rep_vals, dtype=float)
    return float(np.sqrt((4 / 80) * ((rep_vals - point) ** 2).sum()))


def weighted_means(df):
    w = df.WGTP.to_numpy(dtype=float)
    out = {"weight": float(w.sum()), "rows": int(len(df))}
    for col in ["hincp_adj", *SOURCES, "residual"]:
        out[col] = float((w * df[col].to_numpy(dtype=float)).sum() / w.sum())
    return out


def share_below(df, annual_income, monthly_cost):
    w = df.WGTP.to_numpy(dtype=float)
    below = (annual_income / 12.0) < monthly_cost
    p = float((w * below).sum() / w.sum())
    if all(c in df.columns for c in REP):
        reps = df[REP].to_numpy(dtype=float)
        pr = (reps * below[:, None]).sum(axis=0) / reps.sum(axis=0)
        se = sdr_se(pr, p)
    else:
        se = None
    return p, se


def project(df, cola_tplus1):
    """Source-specific projection. Non-SS sources FROZEN (assumption, not CES)."""
    pred = df.copy()
    pred["WAGP"] = df.WAGP  # frozen: CES series not acquired
    pred["SEMP"] = df.SEMP  # frozen: BEA Table 2.6 series not acquired
    pred["RETP"] = df.RETP
    pred["INTP"] = df.INTP
    pred["PAP"] = df.PAP
    pred["OIP"] = df.OIP
    pred["residual"] = df.residual
    pred["SSP"] = df.SSP * (1.0 + cola_tplus1)
    pred["SSIP"] = df.SSIP * (1.0 + cola_tplus1)
    pred["hincp_adj"] = pred[SOURCES].sum(axis=1) + pred["residual"]
    return pred


def compare(actual, pred, freeze, label, cola_tplus1):
    wa = actual.WGTP.to_numpy(dtype=float)
    ma = weighted_means(actual)
    mp = weighted_means(pred)
    err = {k: mp[k] - ma[k] for k in ["hincp_adj", *SOURCES] if k in ma and k in mp}
    pct = {k: (err[k] / ma[k] if ma[k] else None) for k in err}
    p_act, se_act = share_below(actual, actual.hincp_adj.to_numpy(dtype=float), FROZEN_R24_THREE_COST_MONTH)
    p_hat, se_hat = share_below(pred, pred.hincp_adj.to_numpy(dtype=float), FROZEN_R24_THREE_COST_MONTH)
    p_fr, se_fr = share_below(freeze, freeze.hincp_adj.to_numpy(dtype=float), FROZEN_R24_THREE_COST_MONTH)
    return {
        "label": label,
        "actual_weighted_means_annual": ma,
        "projected_weighted_means_annual": mp,
        "error_projected_minus_actual": err,
        "pct_error": pct,
        "diagnostic_share_below_frozen_r24_three_cost_mean": {
            "note": "NOT the published 18.9918% HESI share. Occupied households, frozen $2,894.91/mo cost.",
            "actual_share": p_act,
            "actual_sampling_se_sdr": se_act,
            "projected_share": p_hat,
            "projected_sampling_se_sdr_factors_fixed": se_hat,
            "share_error_projected_minus_actual": p_hat - p_act,
            "freeze_all_sources_share": p_fr,
            "nowcast_model_delta_cola_minus_freeze": p_hat - p_fr,
            "freeze_sampling_se_sdr_factors_fixed": se_fr,
        },
        "factor_roles": {
            "SSP_SSIP": {"kind": "projection", "rule": "multiply by (1+January COLA of T+1)", "cola": cola_tplus1},
            "WAGP_SEMP_RETP_INTP_PAP_OIP_residual": {"kind": "assumption", "rule": "frozen factor=1 because CES/ECI/BEA series were not acquired"},
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cache", required=True)
    p.add_argument("--housing-2022", required=True)
    p.add_argument("--person-2022", required=True)
    p.add_argument("--housing-2023", required=True)
    p.add_argument("--person-2023", required=True)
    p.add_argument("--housing-2024", required=True)
    p.add_argument("--person-2024-a", required=True)
    p.add_argument("--person-2024-b", required=True)
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
    pred23 = project(d22, COLA_JANUARY[2023])
    freeze23 = project(d22, 0.0)
    pred24 = project(d23, COLA_JANUARY[2024])
    freeze24 = project(d23, 0.0)
    report = {
        "national_2026_adequacy_share_published": False,
        "core_r24_18_9918_modified": False,
        "b1_2024_identity": "executed in prior reconciliation round on R2.4 frame",
        "b2_acs_to_acs": [
            compare(d23, pred23, freeze23, "ACS2022_sources_x_COLA2023_vs_ACS2023_occupied", COLA_JANUARY[2023]),
            compare(d24, pred24, freeze24, "ACS2023_sources_x_COLA2024_vs_ACS2024_occupied", COLA_JANUARY[2024]),
        ],
        "reconstruction_meta": meta,
        "limitations": [
            "Occupied-household universe, not the R2.4 geography/bedroom/infant frame.",
            "CES/ECI time series: HTTP 403 from download.bls.gov; wage factors frozen.",
            "BEA Table 2.6 monthly series file not acquired (landing HTML stubs); SEMP frozen.",
            "January COLA is a coarse calendar overlay on ACS rolling 12-month income; labeled assumption.",
            "Diagnostic share uses frozen R2.4 mean three-cost, not household-specific FY2026 rents.",
            "ACS 2019-2021 PUMS not downloaded this round.",
        ],
    }
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2) + "\n")
    for row in report["b2_acs_to_acs"]:
        d = row["diagnostic_share_below_frozen_r24_three_cost_mean"]
        print(row["label"], "hincp_pct_err", row["pct_error"]["hincp_adj"], "share_err", d["share_error_projected_minus_actual"])


if __name__ == "__main__":
    main()
