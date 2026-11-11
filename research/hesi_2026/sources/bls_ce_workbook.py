"""Bounded BLS CE Table 1101 / 1400 ingest (register P4-O01, P4-O02). Stdlib xlsx only."""
from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import load_source_register, validate_required_source_pins_or_abort

BLS_CE_REGISTER_IDS = ("P4-O01", "P4-O02")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
SECTION_AVERAGE_ANNUAL_EXP = "Average annual expenditures"
# Table 1101: column index for Second 20 percent mean (0=label, 1=All CU, 2=Lowest, 3=Second)
Q2_MEAN_COL = 3
# Table 1400: column index for Two or more people mean (0=label, 1=All, 2=One person, 3=Two or more)
TWO_OR_MORE_MEAN_COL = 3


class BlsCeWorkbookError(ValueError):
    pass


def _col_to_num(col: str) -> int:
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _read_xlsx_rows(path: Path) -> list[list[Any]]:
    with zipfile.ZipFile(path) as zf:
        strings = [
            "".join(t.text or "" for t in si.findall(".//m:t", NS))
            for si in ET.fromstring(zf.read("xl/sharedStrings.xml")).findall(".//m:si", NS)
        ]
        root = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
        rows: list[list[Any]] = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            max_idx = -1
            for cell in row.findall("m:c", NS):
                col = "".join(ch for ch in cell.attrib.get("r", "") if ch.isalpha())
                max_idx = max(max_idx, _col_to_num(col))
            values: list[Any] = [None] * (max_idx + 1)
            for cell in row.findall("m:c", NS):
                col = "".join(ch for ch in cell.attrib.get("r", "") if ch.isalpha())
                idx = _col_to_num(col)
                v_el = cell.find("m:v", NS)
                if v_el is None or v_el.text is None:
                    continue
                val: Any = v_el.text
                if cell.attrib.get("t") == "s":
                    val = strings[int(val)]
                values[idx] = val
            rows.append(values)
        return rows


def _mean_after_section(rows: list[list[Any]], col_index: int) -> float:
    for i, vals in enumerate(rows):
        if any(v == SECTION_AVERAGE_ANNUAL_EXP for v in vals if v):
            if i + 1 >= len(rows):
                break
            mean_row = rows[i + 1]
            if mean_row[0] != "Mean":
                raise BlsCeWorkbookError("expected Mean row after Average annual expenditures")
            raw = mean_row[col_index]
            if raw is None:
                raise BlsCeWorkbookError(f"missing mean at column {col_index}")
            return float(raw)
    raise BlsCeWorkbookError(f"section {SECTION_AVERAGE_ANNUAL_EXP!r} not found")


def resolve_bls_ce_workbook(source_id: str) -> Path:
    for row in load_source_register():
        if row.source_id == source_id:
            resolved = resolve_register_local_path(row.local_path) if row.local_path else None
            if resolved is None or not resolved.is_file():
                raise FileNotFoundError(f"{source_id} register bytes missing (HESI_DATA_ROOT)")
            return resolved
    raise BlsCeWorkbookError(f"{source_id} not in register")


def extract_ce_observed_national_means(*, verify_pins: bool = True) -> dict[str, Any]:
    """Parse CY2025 national observed means only; not an HESI essential-cost standard."""
    if verify_pins:
        verified = validate_required_source_pins_or_abort(list(BLS_CE_REGISTER_IDS))
    else:
        verified = {}
    p_o01 = resolve_bls_ce_workbook("P4-O01")
    p_o02 = resolve_bls_ce_workbook("P4-O02")
    q2 = _mean_after_section(_read_xlsx_rows(p_o01), Q2_MEAN_COL)
    two_plus = _mean_after_section(_read_xlsx_rows(p_o02), TWO_OR_MORE_MEAN_COL)
    return {
        "source_ids": list(BLS_CE_REGISTER_IDS),
        "verified_sha256": verified,
        "paths": {"P4-O01": str(p_o01), "P4-O02": str(p_o02)},
        "observation_vintage": "BLS_CE_CY2025",
        "table_1101_second_quintile_mean_annual_usd": q2,
        "table_1400_two_or_more_people_mean_annual_usd": two_plus,
        "internet_component": "unresolved_register_gap_no_approved_line_item",
        "residual_category_map": "unresolved_other_necessities_vector_not_defined_from_total_ce",
        "scientific_status": "observed_national_spending_only_not_normative_hesi_other_necessities",
        "policy_approved": False,
    }


def price_other_ce_register_or_unresolved(
    household: dict[str, Any],
) -> dict[str, Any]:
    """
    Fail closed on essential-cost assignment: register tables verified and parsed,
    but HESI residual 'other necessities' cannot be asserted from total CE spending alone.
    """
    _ = household
    observed = extract_ce_observed_national_means()
    raise BlsCeWorkbookError(
        "BLS CE P4-O01/P4-O02 parsed (CY2025 observed national means) but other_necessities "
        "essential-cost category mapping is unapproved; total average expenditures are observed "
        "spending, not the HESI residual normative standard. "
        f"q2_mean={observed['table_1101_second_quintile_mean_annual_usd']}, "
        f"two_plus_mean={observed['table_1400_two_or_more_people_mean_annual_usd']}. "
        "Internet/subcategory lines remain unresolved per register gaps."
    )
