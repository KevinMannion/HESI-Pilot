"""Annual T+1/T ratios from official BEA NipaDataM.txt (monthly NIPA).

Values are seasonally adjusted annual rates, millions of dollars.
HTML stubs from prior zip URLs are not used.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(HERE))
from hashutil import sha256_file

# Table 2.6 Personal Income and Its Disposition (monthly), BEA series codes.
SERIES = {
    "A041RC": {"title": "Proprietors' income with IVA and CCAdj", "use": "SEMP_positive"},
    "A064RC": {"title": "Personal interest income", "use": "INTP_component"},
    "B703RC": {"title": "Personal dividend income", "use": "INTP_component"},
    "A048RC": {"title": "Rental income of persons with CCAdj", "use": "INTP_component"},
    "A033RC": {"title": "Wage and salary disbursements", "use": "crosscheck_not_household_WAGP"},
    "A065RC": {"title": "Personal income", "use": "crosscheck_not_HINCP"},
}


def parse_value(s):
    return float(s.strip().strip('"').replace(",", ""))


def load_monthly(path, codes):
    by = {c: [] for c in codes}
    with open(path) as f:
        header = f.readline()
        if "SeriesCode" not in header:
            raise SystemExit("unexpected header: " + header[:80])
        for line in f:
            code, rest = line.split(",", 1)
            if code not in by:
                continue
            period, val = rest.split(",", 1)
            period = period.strip()
            if len(period) != 7 or period[4] != "M":
                continue
            year = int(period[:4])
            month = int(period[5:7])
            if month > 12:
                continue
            by[code].append((year, month, parse_value(val)))
    return by


def annual_means(obs):
    byy = defaultdict(list)
    for y, m, v in obs:
        byy[y].append(v)
    out = {}
    for y, vals in sorted(byy.items()):
        out[str(y)] = {
            "n_months": len(vals),
            "mean_saar_millions": sum(vals) / len(vals),
            "complete_calendar_year": len(vals) == 12,
        }
    return out


def ratio(ann, y0, y1):
    a, b = ann[str(y0)], ann[str(y1)]
    if not a["complete_calendar_year"] or not b["complete_calendar_year"]:
        return None
    return b["mean_saar_millions"] / a["mean_saar_millions"]


def intp_bundle_ratio(extracted, y0, y1):
    parts = []
    for code in ("A064RC", "B703RC", "A048RC"):
        a = extracted[code]["annual"][str(y0)]
        b = extracted[code]["annual"][str(y1)]
        if not a["complete_calendar_year"] or not b["complete_calendar_year"]:
            return None
        parts.append((a["mean_saar_millions"], b["mean_saar_millions"]))
    s0 = sum(p[0] for p in parts)
    s1 = sum(p[1] for p in parts)
    return s1 / s0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nipa-txt", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    raw = Path(a.nipa_txt)
    monthly = load_monthly(raw, SERIES)
    extracted = {}
    for code, meta in SERIES.items():
        extracted[code] = {**meta, "annual": annual_means(monthly[code]), "n_obs": len(monthly[code]), "last": monthly[code][-1] if monthly[code] else None}
    factors = {}
    for y0, y1 in [(2021, 2022), (2022, 2023), (2023, 2024)]:
        factors[f"{y0}_to_{y1}"] = {
            "proprietors_A041RC": ratio(extracted["A041RC"]["annual"], y0, y1),
            "interest_A064RC": ratio(extracted["A064RC"]["annual"], y0, y1),
            "dividends_B703RC": ratio(extracted["B703RC"]["annual"], y0, y1),
            "rental_A048RC": ratio(extracted["A048RC"]["annual"], y0, y1),
            "intp_interest_dividends_rental_bundle": intp_bundle_ratio(extracted, y0, y1),
            "nipa_wages_A033RC_crosscheck": ratio(extracted["A033RC"]["annual"], y0, y1),
            "kind": "computed annual-mean SAAR ratio from BEA monthly NIPA; not ACS household money income",
        }
    report = {
        "source_url": "https://apps.bea.gov/national/Release/TXT/NipaDataM.txt",
        "source_file": str(raw),
        "source_sha256": sha256_file(raw),
        "bytes": raw.stat().st_size,
        "units": "millions of dollars, seasonally adjusted annual rate",
        "coverage_note": "File ends 2026M08. September 2026 monthly PI is not in this vintage.",
        "vintage_limitation": "Current BEA release vintage as of download, not a frozen historical vintage.",
        "series": extracted,
        "factors": factors,
        "bea_api": "GetDataSetList without UserID returns Invalid API UserId. Machine file NipaDataM.txt used instead of the HTML-stub zip endpoints.",
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(factors, indent=2))


if __name__ == "__main__":
    main()
