"""CMS Individual QHP rate file ingestion and schema validation."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from sources.age_rating import member_age_key, normalize_puf_age

REQUIRED_COLUMNS = (
    "BusinessYear",
    "StateCode",
    "IssuerId",
    "PlanId",
    "MetalLevel",
    "CSRVariationType",
    "RatingAreaId",
    "Age",
    "IndividualRate",
)

_SILVER_CSR_OK = {"no", "0", "standard silver on exchange plan"}


@dataclass(frozen=True)
class RateRow:
    business_year: int
    state_code: str
    issuer_id: str
    plan_id: str
    metal_level: str
    csr_variation: str
    rating_area_id: str
    age_key: str
    individual_rate: float


class CmsRateFileError(ValueError):
    pass


def _parse_float(value: str, row_num: int, field: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as e:
        raise CmsRateFileError(f"row {row_num}: invalid {field}={value!r}") from e
    if out <= 0:
        raise CmsRateFileError(f"row {row_num}: {field} must be positive")
    return out


def _silver_row(row: RateRow) -> bool:
    if row.metal_level.lower() != "silver":
        return False
    return row.csr_variation.strip().lower() in _SILVER_CSR_OK


def load_cms_rate_rows(path: Path, *, business_year: int | None = None) -> list[RateRow]:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    rows: list[RateRow] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise CmsRateFileError("empty CSV")
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise CmsRateFileError(f"missing required columns: {missing}")
        for i, raw in enumerate(reader, start=2):
            try:
                year = int(raw["BusinessYear"])
            except (TypeError, ValueError) as e:
                raise CmsRateFileError(f"row {i}: invalid BusinessYear") from e
            if business_year is not None and year != business_year:
                continue
            csr = (raw.get("CSRVariationType") or "").strip()
            rows.append(
                RateRow(
                    business_year=year,
                    state_code=raw["StateCode"].strip(),
                    issuer_id=str(raw["IssuerId"]).strip(),
                    plan_id=str(raw["PlanId"]).strip(),
                    metal_level=raw["MetalLevel"].strip(),
                    csr_variation=csr or "No",
                    rating_area_id=raw["RatingAreaId"].strip(),
                    age_key=normalize_puf_age(raw["Age"]),
                    individual_rate=_parse_float(raw["IndividualRate"], i, "IndividualRate"),
                )
            )
    if not rows:
        raise CmsRateFileError("no rate rows loaded")
    return rows


def validate_rate_file(path: Path, *, business_year: int | None = None) -> dict[str, int | str]:
    rows = load_cms_rate_rows(path, business_year=business_year)
    silver = sum(1 for r in rows if _silver_row(r))
    areas = {r.rating_area_id for r in rows}
    ages = {r.age_key for r in rows}
    return {
        "row_count": len(rows),
        "silver_row_count": silver,
        "rating_area_count": len(areas),
        "distinct_age_keys": len(ages),
        "business_year": rows[0].business_year,
    }


def iter_silver_rates(rows: Iterable[RateRow], *, rating_area_id: str, member_age: int) -> list[float]:
    want = member_age_key(member_age)
    premiums: list[float] = []
    for r in rows:
        if r.rating_area_id != rating_area_id:
            continue
        if r.age_key != want:
            continue
        if not _silver_row(r):
            continue
        premiums.append(r.individual_rate)
    return sorted(premiums)
