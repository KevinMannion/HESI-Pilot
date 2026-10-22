"""Rebuild source_2024_2026.csv from original USDA Excel workbooks."""
import argparse, csv, json, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from xlsx_io import sanitized_xlsx
from compare_tables import compare_csv, sha256

WORKBOOKS = {
    "usda-alaska-june2023-sept2026.xlsx": "d8961448541b65e982a886b08d847f34a8d6929c278922a04e765bc20329de53",
    "usda-hawaii-june2023-sept2026.xlsx": "5b1d3a2117e0b5d693f7a11b182bf8726b6a0444436aff8f61e75af64fbb50ca",
    "usda-liberalplan-sept2007-sept2026.xlsx": "46981fa32031112303b399d821270886905e810f98c4c1332034a457aafc40d1",
    "usda-lowcostplan-sept2007-sept2026.xlsx": "78b963a5ba18052d7f8e29d5ebe9db8f340451dc2ee2e38fce597eb3e3405b03",
    "usda-moderatecostplan-sept2007-sept2026.xlsx": "3dea00a2eecbeab389f02ed2dff8015116c53c6db4cc7ed2421b53bdc8911bd6",
    "usda-thriftyplan-june2021-sept2026.xlsx": "70b1d3b67d2d86e5b7f945fe95901211299facd10ff04028fb8704b8fa526c74",
}
FIELDS = ["geographic_area", "fam_indv", "group", "age", "year", "month", "food_plan", "frequency", "cost", "source_file"]

def read_workbook(path):
    tmp = Path("/tmp/hesi_xlsx") / path.name
    xl = pd.ExcelFile(sanitized_xlsx(path, tmp))
    frames = []
    for sheet in xl.sheet_names:
        if sheet.lower().replace(" ", "") in {"readme", "read_me"}:
            continue
        df = pd.read_excel(xl, sheet_name=sheet, header=0)
        cols = {c.strip(): c for c in df.columns if isinstance(c, str)}
        if "geographic_area" not in cols:
            continue
        keep = df.rename(columns={v: k for k, v in cols.items()})
        frames.append(keep)
    if not frames:
        raise ValueError(f"No data sheet in {path.name}")
    out = pd.concat(frames, ignore_index=True)
    out["source_file"] = path.name
    return out

def build(workbook_dir, out_csv):
    workbook_dir = Path(workbook_dir)
    parts = []
    for name, digest in WORKBOOKS.items():
        path = workbook_dir / name
        if not path.is_file():
            raise FileNotFoundError(f"MISSING USDA WORKBOOK {name} under {workbook_dir}")
        got = sha256(path)
        if got != digest:
            raise SystemExit(f"HASH MISMATCH {name}: {got} != {digest}")
        parts.append(read_workbook(path))
    df = pd.concat(parts, ignore_index=True)
    df["year"] = pd.to_numeric(df["year"], errors="raise").astype(int)
    df = df[df["year"].isin([2024, 2026]) & df["frequency"].astype(str).eq("Monthly")].copy()
    df["cost"] = pd.to_numeric(df["cost"], errors="raise")
    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December",
    ]
    df["month"] = df["month"].astype(str)
    df["_m"] = df["month"].map({m: i for i, m in enumerate(month_order)})
    df = df.sort_values(["geographic_area", "fam_indv", "group", "age", "year", "_m", "food_plan", "source_file"])
    rows = []
    for _, r in df.iterrows():
        cost = float(r["cost"])
        cost_s = f"{cost:.1f}" if abs(cost * 10 - round(cost * 10)) < 1e-9 else str(cost)
        rows.append({k: r[k] if k != "cost" else cost_s for k in FIELDS})
        rows[-1]["year"] = int(r["year"])
    out_csv = Path(out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    return len(rows)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workbook-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--reference", default=str(ROOT / "inputs" / "source_2024_2026.csv"))
    p.add_argument("--report", required=True)
    a = p.parse_args()
    n = build(a.workbook_dir, a.out)
    report = compare_csv(
        a.reference,
        a.out,
        key_fields=["geographic_area", "fam_indv", "group", "age", "year", "month", "food_plan", "frequency", "source_file"],
        numeric_fields=["cost"],
        atol=1e-9,
    )
    report["rows_written"] = n
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "hash_match", "hash_mismatch_without_semantic_diff", "row_count_reference", "row_count_candidate", "rows_written")}, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
