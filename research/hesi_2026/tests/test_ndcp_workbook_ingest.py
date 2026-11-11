import hashlib
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit.source_register import SourceRegisterAbortError
from sources.ndcp_childcare import price_childcare_ndcp_county
from sources.ndcp_workbook import (
    NdcpWorkbookError,
    lookup_ndcp_county_row,
    lookup_ndcp_weekly_prices,
    normalize_county_fips,
    parse_ndcp_price_cell,
    records_from_county_row,
    resolve_p4_c01_workbook_path,
)

WESTCHESTER_FIPS = "36119"
WESTCHESTER_2022_MARKET_CENTER = {
    "infant": ("MCINFANT", 325.0),
    "toddler": ("MCTODDLER", 300.0),
    "preschool": ("MCPRESCHOOL", 293.0),
    "school_age": ("MCSA", 250.0),
}


def _p4_c01_mounted() -> bool:
    try:
        resolve_p4_c01_workbook_path(verify_pin=True)
        return True
    except (FileNotFoundError, SourceRegisterAbortError, NdcpWorkbookError):
        return False


def _write_minimal_ndcp_xlsx(
    path: Path,
    *,
    county_fips: str = "99999",
    study_year: int = 2022,
    prices: dict[str, float | None] | None = None,
) -> None:
    """Tiny NDCP-shaped workbook (single sheet) for parser unit tests."""
    prices = prices or {
        "MCINFANT": 100.0,
        "MCTODDLER": 90.0,
        "MCPRESCHOOL": 80.0,
        "MCSA": 70.0,
    }
    headers = [
        "STATE_NAME",
        "STATE_ABBREVIATION",
        "COUNTY_NAME",
        "COUNTY_FIPS_CODE",
        "STUDYYEAR",
        "MCINFANT",
        "MCInfant_flag",
        "MCTODDLER",
        "MCToddler_flag",
        "MCPRESCHOOL",
        "MCPreschool_flag",
        "MCSA",
    ]

    def sheet_xml() -> str:
        def cell(r: int, c: int, value, as_string: bool = False) -> str:
            ref = f"{chr(ord('A') + c)}{r}"
            if value is None or value == "":
                return ""
            if as_string:
                return f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>'
            if isinstance(value, float):
                return f'<c r="{ref}"><v>{value}</v></c>'
            return f'<c r="{ref}"><v>{value}</v></c>'

        rows = []
        r = 1
        cols = []
        for i, h in enumerate(headers):
            cols.append(cell(r, i, h, as_string=True))
        rows.append(f'<row r="{r}">{"".join(cols)}</row>')
        r = 2
        data = {
            "STATE_NAME": "Synthetic",
            "STATE_ABBREVIATION": "SY",
            "COUNTY_NAME": "Test County",
            "COUNTY_FIPS_CODE": county_fips,
            "STUDYYEAR": study_year,
            "MCINFANT": prices.get("MCINFANT"),
            "MCInfant_flag": "1",
            "MCTODDLER": prices.get("MCTODDLER"),
            "MCToddler_flag": "1",
            "MCPRESCHOOL": prices.get("MCPRESCHOOL"),
            "MCPreschool_flag": "1",
            "MCSA": prices.get("MCSA"),
        }
        cols = []
        for i, h in enumerate(headers):
            v = data.get(h)
            if h in ("STATE_NAME", "STATE_ABBREVIATION", "COUNTY_NAME"):
                cols.append(cell(r, i, v, as_string=True))
            elif v is None or v == "":
                continue
            else:
                cols.append(cell(r, i, v))
        rows.append(f'<row r="{r}">{"".join(cols)}</row>')
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f"<sheetData>{''.join(rows)}</sheetData></worksheet>"
        )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="County_LevelNDCP_v8_update2008_" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", wb_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", rels)
        zf.writestr("xl/sharedStrings.xml", (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="0" uniqueCount="0"/>'
        ))
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml())


class NdcpWorkbookParserUnit(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._xlsx = Path(self._tmp.name) / "ndcp_tiny.xlsx"

    def tearDown(self):
        self._tmp.cleanup()

    def test_parse_price_cell_sentinels(self):
        self.assertIsNone(parse_ndcp_price_cell(None))
        self.assertIsNone(parse_ndcp_price_cell("00011"))
        self.assertEqual(parse_ndcp_price_cell("325"), 325.0)
        self.assertEqual(parse_ndcp_price_cell(325.0), 325.0)

    def test_normalize_fips_padding(self):
        self.assertEqual(normalize_county_fips("1001"), "01001")
        self.assertEqual(normalize_county_fips(36119), "36119")

    def test_lookup_synthetic_workbook_matches_cells(self):
        _write_minimal_ndcp_xlsx(self._xlsx)
        hit = lookup_ndcp_county_row(self._xlsx, "99999", 2022)
        self.assertIsNotNone(hit)
        _row_num, row = hit
        records, gaps = records_from_county_row(row, study_year=2022, care_setting="market_center_median")
        self.assertEqual(gaps, [])
        by_type = {r.care_type: r for r in records}
        self.assertEqual(by_type["infant"].weekly_usd, float(row["MCINFANT"]))
        self.assertEqual(by_type["toddler"].weekly_usd, float(row["MCTODDLER"]))
        lookup = lookup_ndcp_weekly_prices(self._xlsx, "99999", study_year=2022)
        self.assertEqual(lookup["weekly_usd_by_care_type"]["infant"], 100.0)

    def test_missing_infant_price_fail_closed_lookup(self):
        _write_minimal_ndcp_xlsx(self._xlsx, prices={"MCINFANT": None, "MCTODDLER": 90.0, "MCPRESCHOOL": 80.0, "MCSA": 70.0})
        with self.assertRaises(NdcpWorkbookError):
            lookup_ndcp_weekly_prices(self._xlsx, "99999", study_year=2022)


@unittest.skipUnless(_p4_c01_mounted(), "P4-C01 workbook not available (HESI_DATA_ROOT)")
class NdcpP4C01RegisterIntegration(unittest.TestCase):
    def test_register_path_requires_verified_sha256(self):
        path = resolve_p4_c01_workbook_path(verify_pin=True)
        want = "6722a36474118c1ef3ec0313e610a476c57a880a35f380cb8599841a8d4cce62"
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(got, want)

    def test_westchester_2022_market_center_cells_match_workbook(self):
        path = resolve_p4_c01_workbook_path(verify_pin=True)
        hit = lookup_ndcp_county_row(path, WESTCHESTER_FIPS, 2022)
        self.assertIsNotNone(hit)
        row_num, row = hit
        self.assertIn("Westchester", str(row["COUNTY_NAME"]))
        records, gaps = records_from_county_row(
            row, study_year=2022, care_setting="market_center_median", excel_row=row_num
        )
        self.assertEqual(gaps, [], msg=f"missing care types: {gaps}")
        by_type = {r.care_type: r for r in records}
        for care_type, (col, expected) in WESTCHESTER_2022_MARKET_CENTER.items():
            self.assertEqual(float(row[col]), expected, f"workbook cell {col}")
            self.assertEqual(by_type[care_type].weekly_usd, expected)
            self.assertEqual(by_type[care_type].price_column, col)

    def test_price_childcare_register_observed_separate_from_cpi_bridge(self):
        hh = {"county_fips": WESTCHESTER_FIPS, "members": [{"age": 1}, {"age": 4}]}
        detail = price_childcare_ndcp_county(
            hh,
            data_source="register",
            cpi_bridge="owner_supplied_factor",
            cpi_factor=1.1,
            study_year=2022,
        )
        self.assertFalse(detail["policy_approved"])
        self.assertEqual(detail["ndcp_study_year_observed"], 2022)
        line0 = detail["lines"][0]
        self.assertEqual(line0["weekly_usd_2022"], 325.0)
        self.assertEqual(line0["weekly_usd_applied"], round(325.0 * 1.1, 4))
        self.assertEqual(detail["cpi_bridge"]["factor"], 1.1)
        self.assertIn("register_xlsx", detail["ndcp_source"]["ingest_mode"])


if __name__ == "__main__":
    unittest.main()
