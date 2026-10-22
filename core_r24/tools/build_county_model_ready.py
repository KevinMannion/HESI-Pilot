"""Rebuild county_model_ready.csv from FY26_FMRs_revised.xlsx. Does not alter joint formulas."""
import argparse, csv, hashlib, json, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from xlsx_io import sanitized_xlsx
from compare_tables import compare_csv, sha256

REQUIRED = "0b130fd046c7bedbee5d206ab55654d390d27da423ff22e307e0698fbb56ad9c"

def build(workbook, out_csv):
    tmp = Path(out_csv).parent / "_tmp_FY26_FMRs_revised.xlsx"
    df = pd.read_excel(sanitized_xlsx(workbook, tmp), sheet_name="FY26_FMRs_revised")
    rows = []
    for _, r in df.iterrows():
        fips = str(int(r["fips"])).zfill(10)
        fmr = [int(r[f"fmr_{i}"]) for i in range(5)]
        rows.append(
            {
                "geo_type": "county",
                "geo_id": fips,
                "hud_area_code": r["hud_area_code"],
                "area_name": r["hud_area_name"],
                "monthly_0br": fmr[0],
                "monthly_1br": fmr[1],
                "monthly_2br": fmr[2],
                "monthly_3br": fmr[3],
                "monthly_4br": fmr[4],
                "annual_2br": 12 * fmr[2],
                "source_period": "FY2026",
                "cost_status": "HUD_FMR_benchmark_not_actual_rent",
            }
        )
    out_csv = Path(out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return len(rows)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workbook", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--reference", default=str(ROOT / "inputs" / "county_model_ready.csv"))
    p.add_argument("--report", required=True)
    a = p.parse_args()
    got = sha256(a.workbook)
    if got != REQUIRED:
        raise SystemExit(f"HUD FMR workbook hash mismatch: {got} != {REQUIRED}")
    n = build(a.workbook, a.out)
    report = compare_csv(
        a.reference,
        a.out,
        key_fields=["geo_id"],
        numeric_fields=["monthly_0br", "monthly_1br", "monthly_2br", "monthly_3br", "monthly_4br", "annual_2br"],
    )
    report["rows_written"] = n
    report["workbook_sha256"] = got
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "hash_match", "hash_mismatch_without_semantic_diff", "row_count_reference", "row_count_candidate")}, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
