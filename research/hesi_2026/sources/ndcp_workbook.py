"""Bounded parser for DOL NDCP workbook (register pin P4-C01). Stdlib only; no Excel dependency."""
from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterator

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import load_source_register, validate_required_source_pins_or_abort

P4_C01_ID = "P4-C01"
NDCP_SHEET_NAME = "County_LevelNDCP_v8_update2008_"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

CARE_TYPES = ("infant", "toddler", "preschool", "school_age")

MARKET_CENTER_MEDIAN_COLUMNS: dict[str, tuple[str, str]] = {
    "infant": ("MCINFANT", "MCInfant_flag"),
    "toddler": ("MCTODDLER", "MCToddler_flag"),
    "preschool": ("MCPRESCHOOL", "MCPreschool_flag"),
    "school_age": ("MCSA", None),
}

FAMILY_CHILD_CARE_MEDIAN_COLUMNS: dict[str, tuple[str, str]] = {
    "infant": ("MFCCINFANT", "MFCCInfant_flag"),
    "toddler": ("MFCCTODDLER", "MFCCToddler_flag"),
    "preschool": ("MFCCPRESCHOOL", "MFCCPreschool_flag"),
    "school_age": ("MFCCSA", None),
}

CARE_SETTING_COLUMNS = {
    "market_center_median": MARKET_CENTER_MEDIAN_COLUMNS,
    "family_child_care_median": FAMILY_CHILD_CARE_MEDIAN_COLUMNS,
}

IDENTITY_COLUMNS = (
    "STATE_NAME",
    "STATE_ABBREVIATION",
    "COUNTY_NAME",
    "COUNTY_FIPS_CODE",
    "STUDYYEAR",
)


class NdcpWorkbookError(ValueError):
    pass


@dataclass(frozen=True)
class NdcpChildcarePriceRecord:
    state_name: str
    state_abbreviation: str
    county_name: str
    county_fips: str
    study_year: int
    care_setting: str
    care_type: str
    weekly_usd: float
    unit: str
    source_id: str
    workbook_sheet: str
    price_column: str
    flag_column: str | None
    flag_value: str | None
    provenance: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _col_to_num(col: str) -> int:
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _num_to_col(n: int) -> str:
    n += 1
    out: list[str] = []
    while n:
        n, rem = divmod(n - 1, 26)
        out.append(chr(65 + rem))
    return "".join(reversed(out))


def normalize_county_fips(raw: Any) -> str:
    if raw is None or raw == "":
        raise NdcpWorkbookError("COUNTY_FIPS_CODE missing")
    s = str(raw).strip()
    if s.endswith(".0") and s[:-2].isdigit():
        s = s[:-2]
    if not s.isdigit():
        raise NdcpWorkbookError(f"COUNTY_FIPS_CODE not numeric: {raw!r}")
    return s.zfill(5)


def parse_ndcp_price_cell(raw: Any) -> float | None:
    """Return weekly USD or None. Does not coerce NDCP suppression sentinels."""
    if raw is None or raw == "":
        return None
    s = str(raw).strip()
    if s.startswith("0000") or (len(s) == 5 and s.isdigit() and s.startswith("000")):
        return None
    try:
        return float(s)
    except ValueError as e:
        raise NdcpWorkbookError(f"non-numeric price cell: {raw!r}") from e


def resolve_p4_c01_workbook_path(*, verify_pin: bool = True) -> Path:
    if verify_pin:
        validate_required_source_pins_or_abort([P4_C01_ID])
    for row in load_source_register():
        if row.source_id != P4_C01_ID:
            continue
        if not row.local_path:
            break
        resolved = resolve_register_local_path(row.local_path)
        if resolved is None or not resolved.is_file():
            raise FileNotFoundError(
                "P4-C01 register bytes missing; set HESI_DATA_ROOT to dol_NDCP2022.xlsx"
            )
        if resolved.suffix.lower() != ".xlsx":
            raise NdcpWorkbookError(f"P4-C01 expected .xlsx, got {resolved}")
        return resolved
    raise NdcpWorkbookError("P4-C01 not found in source register")


def _load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    data = zf.read("xl/sharedStrings.xml")
    root = ET.fromstring(data)
    strings: list[str] = []
    for si in root.findall(".//m:si", NS):
        texts = [t.text or "" for t in si.findall(".//m:t", NS)]
        strings.append("".join(texts))
    return strings


def _sheet_path(zf: zipfile.ZipFile) -> str:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    sheets = wb.findall(".//m:sheet", NS)
    if len(sheets) != 1:
        raise NdcpWorkbookError(f"expected 1 worksheet, found {len(sheets)}")
    name = sheets[0].attrib.get("name")
    if name != NDCP_SHEET_NAME:
        raise NdcpWorkbookError(
            f"unexpected sheet name {name!r}; want {NDCP_SHEET_NAME!r}"
        )
    rid = sheets[0].attrib.get(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    )
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    for rel in rels:
        if rel.attrib.get("Id") == rid:
            target = rel.attrib["Target"].lstrip("/")
            return target if target.startswith("xl/") else f"xl/{target}"
    raise NdcpWorkbookError("workbook relationship for sheet1 missing")


def iter_ndcp_workbook_rows(workbook_path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    """Yield (1-based Excel row number, column_name -> cell value) for data rows after header."""
    with zipfile.ZipFile(workbook_path) as zf:
        strings = _load_shared_strings(zf)
        sheet_xml = _sheet_path(zf)
        root = ET.fromstring(zf.read(sheet_xml))
        header: list[str | None] | None = None
        for row in root.findall(".//m:sheetData/m:row", NS):
            row_num = int(row.attrib.get("r", "0"))
            max_idx = -1
            for cell in row.findall("m:c", NS):
                ref = cell.attrib.get("r", "")
                col = "".join(ch for ch in ref if ch.isalpha())
                max_idx = max(max_idx, _col_to_num(col))
            values: list[Any] = [None] * (max_idx + 1)
            for cell in row.findall("m:c", NS):
                ref = cell.attrib.get("r", "")
                col = "".join(ch for ch in ref if ch.isalpha())
                idx = _col_to_num(col)
                v_el = cell.find("m:v", NS)
                if v_el is not None and v_el.text is not None:
                    val: Any = v_el.text
                    if cell.attrib.get("t") == "s":
                        val = strings[int(val)]
                    values[idx] = val
                    continue
                is_el = cell.find("m:is", NS)
                if is_el is not None:
                    texts = [t.text or "" for t in is_el.findall(".//m:t", NS)]
                    values[idx] = "".join(texts)
            if header is None:
                header = [str(h) if h is not None else None for h in values]
                continue
            record = {
                header[i]: values[i]
                for i in range(len(header))
                if header[i] is not None
            }
            yield row_num, record


def lookup_ndcp_county_row(
    workbook_path: Path,
    county_fips: str,
    study_year: int,
) -> tuple[int, dict[str, Any]] | None:
    want_fips = normalize_county_fips(county_fips)
    year_s = str(int(study_year))
    for row_num, row in iter_ndcp_workbook_rows(workbook_path):
        if str(row.get("STUDYYEAR", "")).strip() != year_s:
            continue
        try:
            got = normalize_county_fips(row.get("COUNTY_FIPS_CODE"))
        except NdcpWorkbookError:
            continue
        if got == want_fips:
            return row_num, row
    return None


def records_from_county_row(
    row: dict[str, Any],
    *,
    study_year: int,
    care_setting: str,
    excel_row: int | None = None,
) -> tuple[list[NdcpChildcarePriceRecord], list[dict[str, str]]]:
    if care_setting not in CARE_SETTING_COLUMNS:
        raise NdcpWorkbookError(f"unknown care_setting {care_setting!r}")
    columns = CARE_SETTING_COLUMNS[care_setting]
    fips = normalize_county_fips(row.get("COUNTY_FIPS_CODE"))
    if str(row.get("STUDYYEAR", "")).strip() != str(int(study_year)):
        raise NdcpWorkbookError("row STUDYYEAR does not match requested study_year")

    records: list[NdcpChildcarePriceRecord] = []
    gaps: list[dict[str, str]] = []
    state_name = str(row.get("STATE_NAME", ""))
    state_abbrev = str(row.get("STATE_ABBREVIATION", ""))
    county_name = str(row.get("COUNTY_NAME", ""))

    for care_type in CARE_TYPES:
        price_col, flag_col = columns[care_type]
        raw_price = row.get(price_col)
        price = parse_ndcp_price_cell(raw_price)
        flag_val = str(row.get(flag_col, "")).strip() if flag_col else None
        if price is None:
            gaps.append(
                {
                    "county_fips": fips,
                    "care_type": care_type,
                    "price_column": price_col,
                    "raw_cell": "" if raw_price is None else str(raw_price),
                    "flag_column": flag_col or "",
                    "flag_value": flag_val or "",
                }
            )
            continue
        prov = f"P4-C01:{NDCP_SHEET_NAME}:{price_col}"
        if excel_row is not None:
            prov += f":row{excel_row}"
        records.append(
            NdcpChildcarePriceRecord(
                state_name=state_name,
                state_abbreviation=state_abbrev,
                county_name=county_name,
                county_fips=fips,
                study_year=int(study_year),
                care_setting=care_setting,
                care_type=care_type,
                weekly_usd=price,
                unit="USD_per_week",
                source_id=P4_C01_ID,
                workbook_sheet=NDCP_SHEET_NAME,
                price_column=price_col,
                flag_column=flag_col,
                flag_value=flag_val,
                provenance=prov,
            )
        )
    return records, gaps


def lookup_ndcp_weekly_prices(
    workbook_path: Path,
    county_fips: str,
    *,
    study_year: int = 2022,
    care_setting: str = "market_center_median",
) -> dict[str, Any]:
    hit = lookup_ndcp_county_row(workbook_path, county_fips, study_year)
    if hit is None:
        raise NdcpWorkbookError(
            f"no NDCP row for county_fips={county_fips!r} study_year={study_year}"
        )
    row_num, row = hit
    records, gaps = records_from_county_row(
        row, study_year=study_year, care_setting=care_setting, excel_row=row_num
    )
    if gaps:
        missing = ", ".join(f"{g['care_type']}({g['price_column']})" for g in gaps)
        raise NdcpWorkbookError(
            f"NDCP prices missing for county {county_fips} year {study_year}: {missing}"
        )
    weekly = {r.care_type: r.weekly_usd for r in records}
    return {
        "county_fips": normalize_county_fips(county_fips),
        "study_year": int(study_year),
        "care_setting": care_setting,
        "weekly_usd_by_care_type": weekly,
        "records": [r.to_dict() for r in records],
        "workbook_row": row_num,
        "source_id": P4_C01_ID,
        "observed_vintage_label": f"NDCP_{study_year}_county_weekly_observed",
    }


def summarize_ndcp_study_year(
    workbook_path: Path,
    study_year: int,
    *,
    care_setting: str = "market_center_median",
    price_care_type: str = "infant",
) -> dict[str, Any]:
    """Scan workbook once; report coverage without imputing missing prices."""
    if care_setting not in CARE_SETTING_COLUMNS:
        raise NdcpWorkbookError(f"unknown care_setting {care_setting!r}")
    price_col, _ = CARE_SETTING_COLUMNS[care_setting][price_care_type]
    year_s = str(int(study_year))
    counties = 0
    with_price = 0
    missing = 0
    flag_col = CARE_SETTING_COLUMNS[care_setting][price_care_type][1]
    flag_counts: dict[str, int] = {}
    for _row_num, row in iter_ndcp_workbook_rows(workbook_path):
        if str(row.get("STUDYYEAR", "")).strip() != year_s:
            continue
        counties += 1
        price = parse_ndcp_price_cell(row.get(price_col))
        if price is None:
            missing += 1
        else:
            with_price += 1
        if flag_col:
            fv = str(row.get(flag_col, "")).strip() or "(blank)"
            flag_counts[fv] = flag_counts.get(fv, 0) + 1
    return {
        "study_year": int(study_year),
        "care_setting": care_setting,
        "price_column": price_col,
        "county_row_count": counties,
        "counties_with_observed_price": with_price,
        "counties_missing_price": missing,
        "flag_value_counts": flag_counts,
    }