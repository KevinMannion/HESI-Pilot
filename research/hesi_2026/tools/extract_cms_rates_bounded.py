"""Extract a bounded CMS 2026 rate + plan-attribute subset for pinned empirical validation.

Reads local CMS PUF zips (not committed). Writes normalized CSV under fixtures/inputs/.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DEFAULT_OUT = REPO / "research/hesi_2026/fixtures/inputs/cms2026_rate_puf_bounded_al_ra1.csv"
DEFAULT_PLANS_OUT = REPO / "research/hesi_2026/fixtures/inputs/cms2026_plan_attributes_bounded_al.csv"

NORMALIZED_COLUMNS = [
    "BusinessYear",
    "StateCode",
    "IssuerId",
    "PlanId",
    "MetalLevel",
    "CSRVariationType",
    "RatingAreaId",
    "Age",
    "IndividualRate",
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _component_id(row: dict) -> str:
    comp = (row.get("StandardComponentId") or "").strip()
    if comp:
        return comp
    return str(row.get("PlanId", "")).split("-")[0].strip()


def load_al_silver_plan_ids(plan_zip: Path, *, business_year: int = 2026) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with zipfile.ZipFile(plan_zip) as z:
        name = [n for n in z.namelist() if n.endswith(".csv")][0]
        with z.open(name) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace")
            for row in csv.DictReader(text):
                if int(row["BusinessYear"]) != business_year:
                    continue
                if row["StateCode"] != "AL":
                    continue
                if row.get("DentalOnlyPlan", "").strip().lower() == "yes":
                    continue
                if (row.get("MarketCoverage") or "").strip().lower() != "individual":
                    continue
                metal = (row.get("MetalLevel") or "").strip()
                if metal.lower() != "silver":
                    continue
                csr = (row.get("CSRVariationType") or "").strip()
                if csr != "Standard Silver On Exchange Plan":
                    continue
                cid = _component_id(row)
                if cid:
                    out[cid] = {"MetalLevel": metal, "CSRVariationType": "No"}
    return out


def extract_rates(
    rate_zip: Path,
    plan_ids: set[str],
    *,
    business_year: int,
    rating_area: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with zipfile.ZipFile(rate_zip) as z:
        name = [n for n in z.namelist() if n.endswith(".csv")][0]
        with z.open(name) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace")
            for row in csv.DictReader(text):
                if int(row["BusinessYear"]) != business_year:
                    continue
                if row["StateCode"] != "AL":
                    continue
                if row["RatingAreaId"].strip() != rating_area:
                    continue
                pid = str(row.get("PlanId", "")).strip()
                if pid not in plan_ids:
                    continue
                age = row["Age"].strip()
                tobacco = (row.get("Tobacco") or "").strip().lower()
                if tobacco not in {
                    "",
                    "no preference",
                    "no",
                    "tobacco user/non-tobacco user",
                    "non-tobacco user",
                }:
                    continue
                rate = row.get("IndividualRate", "").strip()
                if not rate:
                    continue
                rows.append(
                    {
                        "BusinessYear": str(business_year),
                        "StateCode": "AL",
                        "IssuerId": row["IssuerId"].strip(),
                        "PlanId": pid,
                        "MetalLevel": "Silver",
                        "CSRVariationType": "No",
                        "RatingAreaId": rating_area,
                        "Age": age,
                        "IndividualRate": rate,
                    }
                )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate-zip", type=Path, required=True)
    ap.add_argument("--plan-zip", type=Path, required=True)
    ap.add_argument("--rating-area", default="Rating Area 1")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--business-year", type=int, default=2026)
    args = ap.parse_args()

    plan_meta = load_al_silver_plan_ids(args.plan_zip, business_year=args.business_year)
    plan_ids = set(plan_meta)
    extracted = extract_rates(
        args.rate_zip,
        plan_ids,
        business_year=args.business_year,
        rating_area=args.rating_area,
    )
    if not extracted:
        raise SystemExit("no rows extracted; check paths and filters")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=NORMALIZED_COLUMNS)
        w.writeheader()
        w.writerows(extracted)

    digest = _sha256(args.out)
    print(f"Wrote {args.out} rows={len(extracted)} sha256={digest}")


if __name__ == "__main__":
    main()
