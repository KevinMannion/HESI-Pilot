"""Extract annual CES/ECI/CPI factors from the hashed BLS Public API v1 JSON.

Does not call download.bls.gov. Does not invent missing BEA series.
"""
from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(HERE))
from hashutil import sha256_file


def monthly_annual_means(series):
    byy = defaultdict(list)
    notes = defaultdict(list)
    for row in series["data"]:
        period = row["period"]
        if not period.startswith("M"):
            continue
        month = int(period[1:])
        if month > 12:
            continue
        raw = row["value"]
        if raw in ("-", ""):
            notes[int(row["year"])].append({"month": month, "status": "missing"})
            continue
        byy[int(row["year"])].append(float(raw))
        fn = row.get("footnotes") or []
        for item in fn:
            if item.get("code"):
                notes[int(row["year"])].append({"month": month, "footnote": item})
    out = {}
    for year, vals in sorted(byy.items()):
        out[str(year)] = {
            "n_months": len(vals),
            "mean": sum(vals) / len(vals),
            "complete_calendar_year": len(vals) == 12,
            "notes": notes.get(year, []),
        }
    return out


def quarterly_annual_means(series):
    byy = defaultdict(list)
    for row in series["data"]:
        if not str(row["period"]).startswith("Q"):
            continue
        raw = row["value"]
        if raw in ("-", ""):
            continue
        byy[int(row["year"])].append(float(raw))
    out = {}
    for year, vals in sorted(byy.items()):
        out[str(year)] = {
            "n_quarters": len(vals),
            "mean": sum(vals) / len(vals),
            "complete": len(vals) == 4,
        }
    return out


def ratio(means, y0, y1):
    a = means[str(y0)]
    b = means[str(y1)]
    if not a["complete_calendar_year"] or not b.get("complete_calendar_year", b.get("complete")):
        return None
    return b["mean"] / a["mean"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bls-json", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    raw = Path(a.bls_json)
    bundle = json.loads(raw.read_text())
    series = {s["seriesID"]: s for s in bundle["Results"]["series"]}
    catalog = {
        "CES0500000003": {"title": "CES average hourly earnings, total private, SA", "unit": "dollars per hour", "sa": True, "agency": "BLS CES"},
        "CES0500000011": {"title": "CES average weekly earnings, total private, SA", "unit": "dollars per week", "sa": True, "agency": "BLS CES"},
        "CES0500000007": {"title": "CES average weekly hours, total private, SA", "unit": "hours", "sa": True, "agency": "BLS CES"},
        "CES0500000001": {"title": "CES all employees, total private, SA", "unit": "thousands of jobs", "sa": True, "agency": "BLS CES"},
        "CIS2020000000000I": {"title": "ECI wages and salaries, civilian workers, SA index", "unit": "index", "sa": True, "agency": "BLS ECI"},
        "CIS1010000000000I": {"title": "ECI total compensation, civilian workers, SA index", "unit": "index", "sa": True, "agency": "BLS ECI"},
        "CUUR0000SA0": {"title": "CPI-U all items, NSA", "unit": "index 1982-84=100", "sa": False, "agency": "BLS CPI"},
        "CUSR0000SA0": {"title": "CPI-U all items, SA", "unit": "index 1982-84=100", "sa": True, "agency": "BLS CPI"},
    }
    extracted = {}
    for sid, meta in catalog.items():
        s = series[sid]
        means = quarterly_annual_means(s) if sid.startswith("CIS") else monthly_annual_means(s)
        extracted[sid] = {**meta, "annual": means}
    pairs = [(2022, 2023), (2023, 2024)]
    factors = {}
    for y0, y1 in pairs:
        key = f"{y0}_to_{y1}"
        def r(sid):
            ann = extracted[sid]["annual"]
            if sid.startswith("CIS"):
                a, b = ann[str(y0)], ann[str(y1)]
                if not (a["complete"] and b["complete"]):
                    return None
                return b["mean"] / a["mean"]
            return ratio(ann, y0, y1)

        factors[key] = {
            "simulated_forecast_date": f"{y1+1}-01-31",
            "vintage_limitation": "BLS Public API v1 current vintage as of download; ALFRED historical vintages not acquired (FRED site maintenance). CES months through the API include later revisions relative to first print.",
            "ahe_total_private": r("CES0500000003"),
            "awe_total_private": r("CES0500000011"),
            "weekly_hours_total_private": r("CES0500000007"),
            "employment_total_private": r("CES0500000001"),
            "eci_wages_civilian": r("CIS2020000000000I"),
            "eci_compensation_civilian": r("CIS1010000000000I"),
            "cpi_u_nsa": r("CUUR0000SA0"),
            "cola_january_tplus1": {2023: 0.087, 2024: 0.032}[y1],
            "bea_proprietors": None,
            "bea_interest_dividends": None,
            "bea_status": "NOT_ACQUIRED: FRED/ALFRED maintenance; BEA NIPA zip/csv endpoints returned 28185-byte HTML stubs (sha256 prefix 9578ca8e). Not substituted.",
        }
    report = {
        "source_file": str(raw),
        "source_sha256": sha256_file(raw),
        "bls_api_status": bundle.get("status"),
        "endpoint": "https://api.bls.gov/publicAPI/v1/timeseries/data/",
        "download_timestamp_utc": (
            Path(os.environ.get("HESI_CLEANREPRO", str(Path.home() / "HESI-R25-CleanRepro")))
            / "income_nowcast/phase3/meta/download_timestamp.txt"
        ).read_text().strip()
        if (
            Path(os.environ.get("HESI_CLEANREPRO", str(Path.home() / "HESI-R25-CleanRepro")))
            / "income_nowcast/phase3/meta/download_timestamp.txt"
        ).exists()
        else None,
        "kind": "observation of BLS Public API JSON; annual means are computed transforms",
        "series": extracted,
        "factors": factors,
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in factors.items()}, indent=2))


if __name__ == "__main__":
    main()
