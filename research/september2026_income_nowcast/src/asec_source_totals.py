"""National CPS ASEC 2026 household money-income source totals (calendar 2025).

Observation of ASEC microdata. Not ACS. Not a 2026 nowcast.
"""
import argparse, json, zipfile
from pathlib import Path
import pandas as pd

# Household record fields from hhldfmt.txt
# HTOTVAL total, HWSVAL wages, HSEVAL self-emp, HSSVAL SS, HSSIVAL SSI,
# HPENVAL+HANNVAL retirement-ish, HINTVAL+HDIVVAL+HRNTVAL investment-ish,
# HPAWVAL public assistance, HOIVAL other
FIELDS = {
    "HTOTVAL": "total",
    "HWSVAL": "wages",
    "HSEVAL": "self_employment",
    "HSSVAL": "social_security",
    "HSSIVAL": "ssi",
    "HPENVAL": "pension",
    "HANNVAL": "annuity",
    "HINTVAL": "interest",
    "HDIVVAL": "dividends",
    "HRNTVAL": "rent",
    "HPAWVAL": "public_assistance",
    "HOIVAL": "other",
    "HSUP_WGT": "weight_raw",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zip", required=True)
    p.add_argument("--report", required=True)
    a = p.parse_args()
    with zipfile.ZipFile(a.zip) as z:
        names = z.namelist()
        hhname = [n for n in names if "hh" in n.lower() and n.lower().endswith(".csv")]
        if not hhname:
            raise SystemExit("No household CSV in " + str(names))
        hh = pd.read_csv(z.open(hhname[0]), low_memory=False)
    cols = {c.upper(): c for c in hh.columns}
    wcol = cols.get("HSUP_WGT")
    if wcol is None:
        raise SystemExit("Missing HSUP_WGT; columns=" + str(list(hh.columns)[:40]))
    w = pd.to_numeric(hh[wcol], errors="coerce").fillna(0) / 100.0  # ASEC weights often x100
    out = {
        "file_in_zip": hhname[0],
        "rows": int(len(hh)),
        "weight_sum_after_div100": float(w.sum()),
        "weight_convention": "HSUP_WGT / 100 as Census ASEC household supplement weight",
        "kind": "observation_asec_calendar_2025",
        "means": {},
        "columns_present": {},
    }
    for field, lab in FIELDS.items():
        if field == "HSUP_WGT":
            continue
        c = cols.get(field)
        out["columns_present"][field] = c is not None
        if c is None:
            continue
        v = pd.to_numeric(hh[c], errors="coerce").fillna(0)
        out["means"][lab] = float((w * v).sum() / w.sum())
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("rows", "weight_sum_after_div100", "means")}, indent=2))


if __name__ == "__main__":
    main()
