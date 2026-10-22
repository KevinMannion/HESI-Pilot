"""Phase 4: non-wage error audit, BEA-sourced candidates, composition vs rates.

Does not publish a September 2026 adequacy share. Phase 3 gates remain locked.
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
from hashutil import sha256_file
from reconstruct_enriched import SOURCES, reconstruct_enriched

FROZEN_COST = 2894.90805340822
NATIONAL_R22_SHA = "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7"
REP = [f"WGTP{i}" for i in range(1, 81)]
COLA = {2022: 0.059, 2023: 0.087, 2024: 0.032}

LOCKED_EVAL = ("2022_to_2023", "2023_to_2024")
EXTRA_EVAL = ("2021_to_2022",)


def sdr_se(rep_vals, point):
    rep_vals = np.asarray(rep_vals, dtype=float)
    return float(np.sqrt((4.0 / 80.0) * ((rep_vals - point) ** 2).sum()))


def wmean(df, col):
    w = df.WGTP.to_numpy(dtype=float)
    return float((w * df[col].to_numpy(dtype=float)).sum() / w.sum())


def share_below(df, annual):
    w = df.WGTP.to_numpy(dtype=float)
    below = (annual / 12.0) < FROZEN_COST
    p = float((w * below).sum() / w.sum())
    reps = df[REP].to_numpy(dtype=float)
    pr = (reps * below[:, None]).sum(axis=0) / reps.sum(axis=0)
    return p, sdr_se(pr, p)


def wquant(df, col, qs=(0.1, 0.25, 0.5, 0.75, 0.9)):
    w = df.WGTP.to_numpy(dtype=float)
    v = df[col].to_numpy(dtype=float)
    order = np.argsort(v)
    v, w = v[order], w[order]
    cdf = np.cumsum(w) / w.sum()
    return {str(q): float(v[np.searchsorted(cdf, q, side="left").clip(0, len(v) - 1)]) for q in qs}


def flags(df):
    h = df.hincp_adj.to_numpy(dtype=float)
    den = np.maximum(np.abs(h), 1.0)
    zero_w = df.WAGP.to_numpy(dtype=float) <= 0
    ret_maj = (df.SSP + df.SSIP + df.RETP).to_numpy(dtype=float) / den >= 0.5
    any65 = df.n_65plus.to_numpy(dtype=float) >= 1
    np1 = df.NP.to_numpy(dtype=float) == 1
    return {
        "all": np.ones(len(df), dtype=bool),
        "positive_wages": ~zero_w,
        "zero_wages": zero_w,
        "retirement_majority": ret_maj,
        "not_retirement_majority": ~ret_maj,
        "any_age65plus": any65,
        "no_age65plus": ~any65,
        "single_person": np1,
        "multi_person": ~np1,
        "zero_wage_and_retirement_majority": zero_w & ret_maj,
        "zero_wage_not_retirement": zero_w & ~ret_maj,
    }


def cell_id(df):
    h = df.hincp_adj.to_numpy(dtype=float)
    den = np.maximum(np.abs(h), 1.0)
    z = (df.WAGP.to_numpy(dtype=float) <= 0).astype(int)
    r = ((df.SSP + df.SSIP + df.RETP).to_numpy(dtype=float) / den >= 0.5).astype(int)
    a = (df.n_65plus.to_numpy(dtype=float) >= 1).astype(int)
    return z * 4 + r * 2 + a


def kitagawa(origin, actual):
    """Cross-sectional Kitagawa split of mean HINCP change. Not individual trajectories."""
    oc, ac = cell_id(origin), cell_id(actual)
    rows = []
    comp = rate = inter = 0.0
    ow, aw = origin.WGTP.to_numpy(dtype=float), actual.WGTP.to_numpy(dtype=float)
    oh, ah = origin.hincp_adj.to_numpy(dtype=float), actual.hincp_adj.to_numpy(dtype=float)
    for c in range(8):
        om, amask = oc == c, ac == c
        w0 = float(ow[om].sum())
        w1 = float(aw[amask].sum())
        p0 = w0 / float(ow.sum())
        p1 = w1 / float(aw.sum())
        mu0 = float((ow[om] * oh[om]).sum() / w0) if w0 else np.nan
        mu1 = float((aw[amask] * ah[amask]).sum() / w1) if w1 else np.nan
        if w0 and w1:
            comp += (p1 - p0) * mu0
            rate += p0 * (mu1 - mu0)
            inter += (p1 - p0) * (mu1 - mu0)
        rows.append(
            {
                "cell": c,
                "zero_wage": bool(c // 4),
                "retirement_majority": bool((c // 2) % 2),
                "any_age65plus": bool(c % 2),
                "origin_weight_share": p0,
                "actual_weight_share": p1,
                "origin_mean_hincp": mu0,
                "actual_mean_hincp": mu1,
                "within_cell_pct_change": ((mu1 - mu0) / mu0) if (w0 and w1 and mu0) else None,
            }
        )
    return {
        "note": "Independent ACS samples. SERIALNO is not a panel id. Composition is cell-share change; rate is within-cell mean change. Interaction is the remainder.",
        "actual_minus_origin_mean_hincp": wmean(actual, "hincp_adj") - wmean(origin, "hincp_adj"),
        "composition_using_origin_cell_means": comp,
        "within_cell_using_origin_shares": rate,
        "interaction": inter,
        "cells": rows,
    }


def apply_models(df, bls, bea, cola):
    ahe, awe, cpi = bls["ahe_total_private"], bls["awe_total_private"], bls["cpi_u_nsa"]
    cola_f = 1.0 + cola
    prop = bea["proprietors_A041RC"]
    intp_f = bea["intp_interest_dividends_rental_bundle"]
    wagp = df.WAGP.to_numpy(dtype=float)
    semp = df.SEMP.to_numpy(dtype=float)
    intp = df.INTP.to_numpy(dtype=float)
    pos_w = wagp > 0
    pos_s = semp >= 0
    pos_i = intp >= 0

    def pack(name, **cols):
        out = df.copy()
        out["model"] = name
        for k, v in cols.items():
            out[k] = v
        if "hincp_adj" not in cols:
            out["hincp_adj"] = out[SOURCES].sum(axis=1) + out["residual"]
        return out

    m1 = pack("M1_freeze")
    m2 = df.copy()
    m2["model"] = "M2_uniform_cpi"
    for col in [*SOURCES, "residual", "hincp_adj"]:
        m2[col] = df[col] * cpi
    m4 = pack(
        "M4_source_specific",
        WAGP=np.where(pos_w, wagp * awe, wagp),
        SSP=df.SSP * cola_f,
        SSIP=df.SSIP * cola_f,
    )
    m5 = pack(
        "M5_m4_plus_bea_semp_intp",
        WAGP=np.where(pos_w, wagp * awe, wagp),
        SEMP=np.where(pos_s, semp * prop, semp),
        INTP=np.where(pos_i, intp * intp_f, intp),
        SSP=df.SSP * cola_f,
        SSIP=df.SSIP * cola_f,
    )
    m5b = pack(
        "M5b_m4_plus_bea_semp_only",
        WAGP=np.where(pos_w, wagp * awe, wagp),
        SEMP=np.where(pos_s, semp * prop, semp),
        SSP=df.SSP * cola_f,
        SSIP=df.SSIP * cola_f,
    )
    m6 = pack(
        "M6_m5_plus_cola_on_bundled_RETP",
        WAGP=np.where(pos_w, wagp * awe, wagp),
        SEMP=np.where(pos_s, semp * prop, semp),
        INTP=np.where(pos_i, intp * intp_f, intp),
        RETP=df.RETP * cola_f,
        SSP=df.SSP * cola_f,
        SSIP=df.SSIP * cola_f,
    )
    m6["assumption"] = "COLA on all ACS RETP is not a DB/DC split; sensitivity only"
    return {
        "M1_freeze": m1,
        "M2_uniform_cpi": m2,
        "M4_source_specific": m4,
        "M5_m4_plus_bea_semp_intp": m5,
        "M5b_m4_plus_bea_semp_only": m5b,
        "M6_m5_plus_cola_on_bundled_RETP": m6,
    }


def score(actual, pred, label):
    err = {}
    pct = {}
    for col in ["hincp_adj", *SOURCES]:
        a, p = wmean(actual, col), wmean(pred, col)
        err[col] = p - a
        pct[col] = (p - a) / a if a else None
    pa, sea = share_below(actual, actual.hincp_adj.to_numpy(dtype=float))
    pp, sep = share_below(pred, pred.hincp_adj.to_numpy(dtype=float))
    qa, qp = wquant(actual, "hincp_adj"), wquant(pred, "hincp_adj")
    fa, fp = flags(actual), flags(pred)
    sub = {}
    for name, mask in fa.items():
        da, dp = actual.loc[mask], pred.loc[fp[name]]
        if da.WGTP.sum() == 0 or dp.WGTP.sum() == 0:
            continue
        am, pm = wmean(da, "hincp_adj"), wmean(dp, "hincp_adj")
        sa, _ = share_below(da, da.hincp_adj.to_numpy(dtype=float))
        sp, _ = share_below(dp, dp.hincp_adj.to_numpy(dtype=float))
        src = {s: wmean(dp, s) - wmean(da, s) for s in SOURCES}
        sub[name] = {
            "actual_weight_share": float(da.WGTP.sum() / actual.WGTP.sum()),
            "pred_weight_share": float(dp.WGTP.sum() / pred.WGTP.sum()),
            "actual_mean_hincp": am,
            "pred_mean_hincp": pm,
            "pct_error_hincp": (pm - am) / am if am else None,
            "share_error": sp - sa,
            "source_mean_error": src,
        }
    contrib = {s: err[s] for s in SOURCES}
    contrib["residual"] = wmean(pred, "residual") - wmean(actual, "residual")
    return {
        "label": label,
        "pct_error": pct,
        "error_projected_minus_actual": err,
        "source_contribution_to_mean_hincp_error": contrib,
        "quantiles_actual": qa,
        "quantiles_projected": qp,
        "quantile_error": {k: qp[k] - qa[k] for k in qa},
        "diagnostic_share": {
            "actual_share": pa,
            "actual_sampling_se_sdr": sea,
            "projected_share": pp,
            "projected_sampling_se_sdr_factors_fixed": sep,
            "share_error_projected_minus_actual": pp - pa,
        },
        "subgroups": sub,
    }


def locked_gate_check(comparisons):
    def grab(year, model):
        return next(c for c in comparisons if c["year"] == year and c["model"] == model)

    g2, g3, g4, g5 = True, True, True, True
    detail = {}
    for yr in LOCKED_EVAL:
        m4, m1 = grab(yr, "M4_source_specific"), grab(yr, "M1_freeze")
        e_h, e_s, e_w = abs(m4["pct_error"]["hincp_adj"]), abs(m4["diagnostic_share"]["share_error_projected_minus_actual"]), abs(m4["pct_error"]["WAGP"])
        detail[yr] = {"hincp": e_h, "share": e_s, "wagp": e_w, "freeze_hincp": abs(m1["pct_error"]["hincp_adj"])}
        g2 = g2 and e_h <= 0.015
        g3 = g3 and e_s <= 0.005
        g4 = g4 and e_w <= 0.020
        g5 = g5 and e_h < abs(m1["pct_error"]["hincp_adj"])
    return {
        "protocol": "Phase 3 VALIDATION_GATES.json locked. Not relaxed. Candidate models are not used to rewrite PASS.",
        "G2_hincp_mean": {"pass": g2, "detail": {k: v["hincp"] for k, v in detail.items()}},
        "G3_share": {"pass": g3, "detail": {k: v["share"] for k, v in detail.items()}},
        "G4_wagp": {"pass": g4, "detail": {k: v["wagp"] for k, v in detail.items()}},
        "G5_beats_freeze": {"pass": g5, "detail": detail},
        "all_locked_eval_pass": g2 and g3 and g4 and g5,
    }


def asec_retirement_note(asec):
    m = asec["means"]
    pen, ann = m["pension"], m["annuity"]
    return {
        "kind": "national_asec_cy2025_observation_not_a_household_split",
        "HPENVAL_mean": pen,
        "HANNVAL_mean": ann,
        "pension_share_of_pension_plus_annuity": pen / (pen + ann),
        "cannot_map_onto_ACS_RETP": "ACS RETP bundles DB, DC, and related receipts. Applying the ASEC national pension/annuity mix to each ACS household would invent a household-level split the PUMS does not contain.",
    }


def bls_pair(bls_json, y0, y1):
    def r(sid):
        a = bls_json["series"][sid]["annual"][str(y0)]
        b = bls_json["series"][sid]["annual"][str(y1)]
        key = "complete_calendar_year" if "complete_calendar_year" in a else "complete"
        if not a[key] or not b[key]:
            raise SystemExit(f"incomplete {sid} {y0}-{y1}")
        return b["mean"] / a["mean"]

    return {
        "ahe_total_private": r("CES0500000003"),
        "awe_total_private": r("CES0500000011"),
        "weekly_hours_total_private": r("CES0500000007"),
        "cpi_u_nsa": r("CUUR0000SA0"),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cache", required=True)
    p.add_argument("--bls", required=True)
    p.add_argument("--bea", required=True)
    p.add_argument("--asec", required=True)
    p.add_argument("--national-r22", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--housing-2021", required=True)
    p.add_argument("--person-2021", required=True)
    p.add_argument("--housing-2022", required=True)
    p.add_argument("--person-2022", required=True)
    p.add_argument("--housing-2023", required=True)
    p.add_argument("--person-2023", required=True)
    p.add_argument("--housing-2024", required=True)
    p.add_argument("--person-2024-a", required=True)
    p.add_argument("--person-2024-b", required=True)
    a = p.parse_args()
    cache = Path(a.cache)
    cache.mkdir(parents=True, exist_ok=True)
    jobs = [
        (2021, a.housing_2021, [a.person_2021]),
        (2022, a.housing_2022, [a.person_2022]),
        (2023, a.housing_2023, [a.person_2023]),
        (2024, a.housing_2024, [a.person_2024_a, a.person_2024_b]),
    ]
    meta = {}
    for year, hus, pus in jobs:
        pk = cache / f"occupied_enriched_{year}.pkl"
        if pk.exists():
            print("reuse", pk, flush=True)
            meta[str(year)] = {"reused": True, "path": str(pk)}
        else:
            meta[str(year)] = reconstruct_enriched(hus, pus, pk)
    data = {y: pd.read_pickle(cache / f"occupied_enriched_{y}.pkl") for y in (2021, 2022, 2023, 2024)}
    bls = json.loads(Path(a.bls).read_text())
    bea = json.loads(Path(a.bea).read_text())
    asec = json.loads(Path(a.asec).read_text())
    comparisons = []
    decomps = {}
    pairs = [(2021, 2022), (2022, 2023), (2023, 2024)]
    for y0, y1 in pairs:
        key = f"{y0}_to_{y1}"
        origin, actual = data[y0], data[y1]
        decomps[key] = kitagawa(origin, actual)
        models = apply_models(origin, bls_pair(bls, y0, y1), bea["factors"][key], COLA[y1])
        for name, pred in models.items():
            row = score(actual, pred, f"ACS{y0}_{name}_vs_ACS{y1}_occupied")
            row["year"] = key
            row["model"] = name
            row["role"] = "locked_evaluation" if key in LOCKED_EVAL else "additional_untouched_evaluation"
            comparisons.append(row)
            d = row["diagnostic_share"]
            print(key, name, "hincp", row["pct_error"]["hincp_adj"], "share", d["share_error_projected_minus_actual"], flush=True)
    gates = locked_gate_check(comparisons)
    r22 = sha256_file(a.national_r22)
    report = {
        "national_2026_adequacy_share_published": False,
        "core_r24_18_9918_modified": False,
        "scientific_validation": False,
        "computational_reproduction": True,
        "phase3_gates_locked": True,
        "go_nogo": "NO-GO",
        "go_nogo_reason": "Phase 3 locked evaluation gates G2 and G3 remain failed on 2023→2024. BEA NIPA was acquired and used only in labeled candidate models. Candidate improvements are not retroactive PASS. Cross-section nowcasts are not household trajectories.",
        "locked_gates": gates,
        "prospective_protocol_future_untouched_years": {
            "do_not_apply_to_2022_2024": True,
            "future_year_example": "ACS 2024→2025 after 2025 PUMS exists, or a later pair never used to choose factors",
            "keep": ["G2 |HINCP%|<=1.5% both designated eval years", "G3 |share err|<=0.50pp", "G4 |WAGP%|<=2%", "G5 beat freeze", "no CPI production", "sampling SE separate"],
            "add": ["hashed BEA NipaDataM.txt or API vintage", "report Kitagawa composition vs within-cell on the eval year", "do not treat BEA INTP as household INTP without a predeclared mapping test"],
        },
        "cross_section_vs_trajectory": "ACS SERIALNO does not identify the same household across years. All scores compare two independent cross-sections. Kitagawa composition/rate splits describe cell-share vs cell-mean change, not individual income paths.",
        "kitagawa": decomps,
        "comparisons": comparisons,
        "asec_retirement": asec_retirement_note(asec),
        "bea_file_sha256": bea["source_sha256"],
        "bls_file_sha256": bls["source_sha256"],
        "national_R22_sha256": r22,
        "national_R22_ok": r22 == NATIONAL_R22_SHA,
        "reconstruction_meta": meta,
        "acs_2025_tables": {"status": "NOT_RELEASED", "scheduled": "2026-10-29"},
    }
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2) + "\n")
    print("GO_NOGO", report["go_nogo"], "locked_all_pass", gates["all_locked_eval_pass"])


if __name__ == "__main__":
    main()
