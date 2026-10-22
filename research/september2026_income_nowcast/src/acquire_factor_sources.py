"""Download and SHA-256 versioned nowcast factor sources. Does not apply them to ACS income."""
import argparse
import json
import ssl
import urllib.request
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from hashutil import sha256_file

# Independent public files used as *factor inputs*, not as household income.
SOURCES = [
    {
        "id": "BLS_EMPSIT_2026M09_HTML",
        "url": "https://www.bls.gov/news.release/empsit.htm",
        "filename": "bls_empsit_2026m09.htm",
        "vintage": "USDL-26-1549 Employment Situation September 2026, posted page retrieved at acquisition time",
        "role": "CES/CPS September 2026 employment, hours, and earnings (job series, not household income)",
    },
    {
        "id": "SSA_COLA_2026_PRESS",
        "url": "https://www.ssa.gov/news/en/press/releases/2025-10-24.html",
        "filename": "ssa_cola_2026_press.html",
        "vintage": "SSA press release 2025-10-24 announcing 2.8 percent 2026 COLA",
        "role": "Statutory OASDI/SSI factor only",
    },
    {
        "id": "SSA_COLA_2026_FR",
        "url": "https://www.federalregister.gov/documents/2025/11/03/2025-19763/cost-of-living-increase-and-other-determinations-for-2026",
        "filename": "ssa_cola_2026_federal_register.html",
        "vintage": "Federal Register 2025-11-03 COLA and other 2026 determinations",
        "role": "Statutory OASDI/SSI factor only",
    },
    {
        "id": "CENSUS_ASEC_2026_DATASET_PAGE",
        "url": "https://www.census.gov/data/datasets/2026/demo/cps/cps-asec-2026.html",
        "filename": "census_cps_asec_2026_dataset_page.html",
        "vintage": "CPS ASEC 2026 public-use landing page (income year 2025)",
        "role": "Annual calibration catalog; microdata file not downloaded here because of size",
    },
    {
        "id": "CENSUS_PUMS_DICTIONARY_2024",
        "url": "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.txt",
        "filename": "PUMS_Data_Dictionary_2024.txt",
        "vintage": "2024 ACS 1-year PUMS data dictionary",
        "role": "Income field definitions",
    },
    {
        "id": "FRED_CES_AHE_ALL_PRIVATE_CES0500000003",
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CES0500000003",
        "filename": "fred_CES0500000003_ahe_all_private.csv",
        "vintage": "FRED extract of BLS CES average hourly earnings, all private employees, retrieved at acquisition time",
        "role": "Wage *rate* index only; must not be applied to HINCP",
    },
    {
        "id": "FRED_CES_AWE_ALL_PRIVATE_CES0500000011",
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CES0500000011",
        "filename": "fred_CES0500000011_awe_all_private.csv",
        "vintage": "FRED extract of BLS CES average weekly earnings, all private, retrieved at acquisition time",
        "role": "Wage earnings *job* index; not household income",
    },
    {
        "id": "FRED_UNRATE",
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE",
        "filename": "fred_UNRATE.csv",
        "vintage": "FRED extract of BLS CPS unemployment rate, retrieved at acquisition time",
        "role": "Employment-path sensitivity, not an income factor for non-earners",
    },
]


def fetch(url, dest):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "HESI-research-nowcast/R2.5"})
    with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
        dest.write_bytes(r.read())
    return dest


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    a = p.parse_args()
    out = Path(a.out)
    raw = out / "raw"
    records = []
    for spec in SOURCES:
        dest = raw / spec["filename"]
        rec = dict(spec)
        rec["status"] = "FAIL"
        rec["path"] = str(dest)
        try:
            fetch(spec["url"], dest)
            rec["bytes"] = dest.stat().st_size
            rec["sha256"] = sha256_file(dest)
            rec["status"] = "ACQUIRED"
        except Exception as e:
            rec["error"] = repr(e)
        records.append(rec)
        print(rec["id"], rec["status"], rec.get("sha256", rec.get("error")), flush=True)
    missing = [
        {
            "id": "CPS_ASEC_2026_MICRODATA_CSV",
            "url": "https://www.census.gov/data/datasets/2026/demo/cps/cps-asec-2026.html",
            "status": "NOT_DOWNLOADED",
            "reason": "Large public-use CSV (~132 MB). Catalog page acquired; microdata download deferred until backtest execution.",
        },
        {
            "id": "BEA_PERSONAL_INCOME_TABLE_2_6",
            "status": "NOT_DOWNLOADED",
            "reason": "Need BEA monthly personal income by source through latest 2026 month as a separate NIPA extract.",
        },
        {
            "id": "BLS_ECI_LATEST_QUARTER",
            "status": "NOT_DOWNLOADED",
            "reason": "Quarterly ECI file not fetched this round; required before wage-rate nowcast.",
        },
        {
            "id": "ACS_PUMS_2019_2023",
            "status": "NOT_ON_DISK",
            "reason": "Historical 1-year PUMS housing/person files are required for backtests and were not present in the R2.4 Census ZIP set.",
        },
        {
            "id": "ACS_2025_1YEAR_TABLES_AND_PUMS",
            "status": "NOT_RELEASED_OR_NOT_FETCHED",
            "reason": "1-year tables scheduled 2026-10-29; PUMS TBD as of 2026-10-21.",
        },
    ]
    report = {
        "acquired_at_local": "2026-10-21",
        "note": "Hashes are of retrieved bytes at acquisition time. HTML news pages can change; freeze copies are the hashed files.",
        "uniform_cpi_applied_to_hincp": False,
        "factors_applied_to_acs_income": False,
        "national_nowcast_executed": False,
        "records": records,
        "still_required": missing,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "DATA_SOURCE_ACQUISITION_REPORT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"acquired": sum(r["status"] == "ACQUIRED" for r in records), "failed": sum(r["status"] != "ACQUIRED" for r in records), "still_required": len(missing)}, indent=2))


if __name__ == "__main__":
    main()
