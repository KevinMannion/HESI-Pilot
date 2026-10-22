# Income nowcast validation report (Phase 3)

**Decision: NO-GO** for a September 2026 national household income nowcast and for any new adequacy percentage.

Computational reproduction of these backtests: yes (hashed ACS 2022–2024 PUMS + hashed BLS API JSON). Scientific validation: no.

## Predeclared gates (not relaxed)

File: `VALIDATION_GATES.json` (timestamp 2026-10-21T21:26:00-04:00, before model comparisons).

| Gate | Result | Detail |
| --- | --- | --- |
| G1 series acquired | FAIL | CES AHE/AWE/hours/employment, ECI, CPI-U acquired. BEA proprietors and interest/dividends not acquired. ALFRED vintages not acquired. |
| G2 M4 \|HINCP % err\| ≤ 1.5% both years | FAIL | 2022→2023 0.238%; 2023→2024 **1.646%** |
| G3 M4 \|share err\| ≤ 0.50 pp both years | FAIL | 2022→2023 0.322 pp; 2023→2024 **0.668 pp** |
| G4 M4 \|WAGP % err\| ≤ 2.0% both years | PASS | 0.085%; 0.437% |
| G5 M4 beats M1 freeze on \|HINCP % err\| both years | PASS | 0.238 < 3.207; 1.646 < 4.491 |
| G6 no CPI production | PASS | M2 scored only |
| G7 sampling vs model separated | PASS | SDR SE ≠ share error |
| G8 national_R22 bytes | PASS | sha256 `6778c312…` |

## Attribution

- **Wage path:** National CES AWE applied only to ACS households with WAGP>0 recovered WAGP totals within 0.5% both years (G4). Rate vs hours: AWE/AHE hours ratios were 0.995 (2022→2023) and 0.997 (2023→2024); employment growth (+2.1%, +0.9%) was **not** applied to household wages.
- **2023→2024 residual miss:** M4 still understates occupied mean HINCP by 1.65%. Largest subgroup misses are zero-wage households (−4.11%) and retirement-majority households (−3.47%), consistent with frozen SEMP/INTP/RETP and a January COLA overlay that does not match ACS rolling SSP (SSP error −3.92%). Bottom tercile diagnostic share error +2.00 pp.
- **Composition vs within-household change:** Origin and target are independent ACS samples. Quantile errors (M4 median −$216 in 2022→2023; −$1,156 in 2023→2024) mix both. No panel identifier exists to separate them.
- **Hindsight:** CES/CPI/ECI are current API vintages, not first print.

## ASEC 2026 (calendar 2025) independent benchmark

Do not equate means. ACS 2024 occupied mean HINCP $114,375 (weight 132,737,145) vs ASEC HTOTVAL $126,664 (weight 137,123,797). Wage share of total 74.6% ACS vs 72.0% ASEC; SS share 6.9% vs 7.7%. Different frames, years, and taxonomies. ACS 2025 tables are not released (2026-10-29).

## September 2026 run-rate identifiability

CES through September 2026 is in the API (AHE $37.81, AWE $1,300.66, hours 33.8, private employment 135,717; preliminary). SSA COLA January 2026 is 2.8%. BEA source series through September 2026 are not on disk (August PI PDF only; September PI scheduled 2026-10-29). A complete source-specific household run rate therefore remains **not identifiable**. No national nowcast was coded.
