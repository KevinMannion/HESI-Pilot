# NDCP P4-C01 source schema report (Sprint 2C Task 1)

**Source pin:** `P4-C01`  
**File:** `dol_NDCP2022.xlsx` (register path `/workspace/hesi-data/blocker_resolution_2026-11-11/files/dol_NDCP2022.xlsx`)  
**SHA-256:** `6722a36474118c1ef3ec0313e610a476c57a880a35f380cb8599841a8d4cce62`  
**Publisher / vintage:** U.S. DOL Women’s Bureau; county panel **2008–2022** (publication date 2024-11-15 on register row)

## Workbook structure

| Item | Observed value |
|------|----------------|
| Worksheets | **1** — `County_LevelNDCP_v8_update2008_` |
| Data extent | `A1:NF48309` (~48,309 rows × ~386 columns) |
| Grain | One row per **county × STUDYYEAR** |
| Shared strings | 2,453 |

Rows are **not** household-level; pricing uses county identifiers and NDCP age-band price columns.

## Geographic identifiers

| Column | Type / notes |
|--------|----------------|
| `STATE_NAME` | Text |
| `STATE_ABBREVIATION` | 2-letter |
| `COUNTY_NAME` | Text (includes “ County” suffix) |
| `COUNTY_FIPS_CODE` | Numeric or string; **must be zero-padded to 5 digits** (e.g. `1001` → `01001`) |
| `STATE_FIPS` | Present (state rollup block) |
| `STUDYYEAR` | Calendar year of NDCP price observation (2008–2022 in this file) |

## Childcare price columns (bounded parser supports)

### Market-center medians (default `care_setting=market_center_median`)

| HESI `care_type` | Price column | Flag column (when present) |
|------------------|--------------|----------------------------|
| `infant` | `MCINFANT` | `MCInfant_flag` |
| `toddler` | `MCTODDLER` | `MCToddler_flag` |
| `preschool` | `MCPRESCHOOL` | `MCPreschool_flag` |
| `school_age` | `MCSA` | *(none in workbook)* |

### Family child care medians (`care_setting=family_child_care_median`)

| HESI `care_type` | Price column | Flag column |
|------------------|--------------|-------------|
| `infant` | `MFCCINFANT` | `MFCCInfant_flag` |
| `toddler` | `MFCCTODDLER` | `MFCCToddler_flag` |
| `preschool` | `MFCCPRESCHOOL` | `MFCCPreschool_flag` |
| `school_age` | `MFCCSA` | *(none)* |

The workbook also contains **75th percentile** (`_75C*`, `_75FCC*`), finer age-bin columns (`MCBto5`, …), and **imputation indicator** columns (`iMC*`, `iMFCC*`). These are **not** used by the Sprint 2C bounded parser unless a future scientific decision selects them.

## Price units

- Observed childcare prices in `MC*` / `MFCC*` columns are **USD per week** (county-level medians for the stated `STUDYYEAR`).
- Parser output sets `unit="USD_per_week"` explicitly.
- **2026 CPI-adjusted** amounts are **not** stored in the workbook; HESI keeps them in `childcare_cpi_bridge` output only (`weekly_usd_applied` vs `weekly_usd_2022` in `ndcp_childcare`).

## Missing-value conventions

| Pattern | Parser behavior |
|---------|-----------------|
| Empty / absent cell | **Missing** — no price record emitted for that care type |
| String sentinels `00000`–`00011` (seen in some NDCP age-bin columns) | Treated as **missing** for median price columns (not coerced to numeric) |
| `MCInfant_flag` (and related) | **Documented only** (`1`, `2`, `3`, or blank). Blank often co-occurs with empty price cells; `3` can appear with numeric prices (imputation indicator — **requires DOL codebook / scientific sign-off before treating as observed vs imputed**) |

## Coverage snapshot (STUDYYEAR = 2022, `MCINFANT`)

| Metric | Count |
|--------|------:|
| County rows | 3,221 |
| Counties with numeric `MCINFANT` | 2,661 |
| Counties missing `MCINFANT` | 560 |

`MCInfant_flag` distribution (2022 rows): `1` → 965; `2` → 878; `3` → 821; blank → 557.

## Sample verified prices (market center, 2022)

See `fixtures/inputs/ndcp_p4_c01_verified_sample_records.json`. Westchester NY (`36119`) matches register narrative ($325 / $300 / $293 / $250 weekly).

## Implementation references

- **SHA-gated open:** `validate_required_source_pins_or_abort(["P4-C01"])` then `resolve_p4_c01_workbook_path()`
- **Bounded county lookup:** `sources/ndcp_workbook.lookup_ndcp_weekly_prices` (single county-year scan; no full-table materialization in pricing path)
- **Ingest wiring:** `sources/ndcp_childcare.price_childcare_ndcp_county(..., data_source="register")`

## Scientific blockers for defensible 2026 childcare estimates

1. **Care setting:** Market-center (`MC*`) vs family child care (`MFCC*`) vs 75th percentile — not approved in register.
2. **Study year vs 2026:** Latest `STUDYYEAR` is **2022** (3–4 year lag); bridging to 2026 requires explicit CPI methodology (`childcare_cpi_bridge` remains unapproved).
3. **Flag interpretation:** Imputation flags (`2`/`3`/blank) not mapped to include/exclude rules.
4. **Age mapping:** HESI ages map to NDCP aggregate care types (`infant` / `toddler` / `preschool` / `school_age`); finer bins (`MCBto5`, etc.) unused.
5. **Partial counties:** 560 counties lack `MCINFANT` for 2022 — household pricing must fail closed or use an approved fallback (none approved).
6. **Work / essential-hours rules:** Register lists unresolved gaps; not implemented.
7. **`policy_approved`:** Remains **False** for NDCP ingest path.
