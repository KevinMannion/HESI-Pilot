# Household income reconciliation report (2024 ACS PUMS)

Executed 2026-10-21. This is **not** a September 2026 income measurement and **not** a new affordability rate.

Machine-readable twin: `HOUSEHOLD_INCOME_RECONCILIATION_REPORT.json`.

## Frame

R2.4 eligibility rebuilt from the same occupancy, geography, composition, bedroom, and infant rules as `core_r24/src/run_joint.py`, without recomputing three-cost shares.

| Count | Rows | Weight |
|---|---:|---:|
| Raw housing | 1,631,969 | — |
| Occupied | 1,348,408 | 132,737,145 |
| Geography excluded | 64,079 | 6,271,320 |
| Composition excluded | 113 | 17,463 |
| Over-4-bedroom excluded | 23,486 | 2,591,711 |
| Infant excluded | 24,999 | 2,819,925 |
| **R2.4 included** | **1,235,731** | **121,036,726** |

Exact match to `core_r24/results/national_R22/audit.json`. SERIALNO unique. WGTP and WGTP1–WGTP80 retained on the household source file (outside git: `$HESI_OPERATOR_HOME/HESI-R25-CleanRepro/income_nowcast/household_income_sources_r24_frame.pkl`).

Person files: 3,422,888 rows (510,098 under age 15). All R2.4 households matched a person aggregate (`person_table_missing_rows` = 0). NP vs person count mismatches: 0.

Published 18.9918% files were not modified (`national_R22/common_cohort_results.csv` SHA-256 `6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7`).

## Method

Person amounts (age ≥ 15) for WAGP, SEMP, RETP, SSP, SSIP, INTP, PAP, OIP, PINCP, PERNP inflated with `ADJINC/1e6` and summed to SERIALNO. Compared to household `HINCP × ADJINC / 1e6`. No uniform CPI. No CES factor.

## Residuals vs eight sources

| Residual | Households | Weight |
|---|---:|---:|
| Exact zero | 1,162,842 | — |
| \|r\| < $1 | 1,235,696 | — |
| \|r\| ≥ $1 | 35 | 3,354 |
| \|r\| ≥ $10 | 0 | 0 |

Weighted mean residual $0.000028. Maximum \|r\| = **$1.01525**, equal to the 2024 `ADJINC` factor times a $1 rounding remainder. Several of the 35 cases are HINCP = 1 (adjusted $1.01525) with zero person components.

PINCP vs HINCP: 1 household with \|r\| ≥ $1. PERNP vs WAGP+SEMP: 38 households with \|r\| ≥ $1; max also $1.01525.

## Source reconstruction (R2.4 frame, weighted)

Annual 2024-dollar means:

| Source | Weighted mean $ | Share of positive HINCP | Households with $0 | Households with a negative person amount |
|---|---:|---:|---:|---:|
| Wages (WAGP) | 82,630.52 | 73.84% | 373,453 | 0 |
| Self-employment (SEMP) | 5,106.63 | 4.56% | 1,099,205 | 7,076 (wt 619,687) |
| Retirement (RETP) | 8,052.57 | 7.20% | 858,280 | 0 |
| Social Security (SSP) | 8,035.80 | 7.18% | 751,280 | 0 |
| SSI (SSIP) | 540.68 | 0.48% | 1,173,534 | 0 |
| Investment (INTP) | 6,005.14 | 5.37% | 939,626 | 13,529 (wt 1,175,996) |
| Public assistance (PAP) | 80.03 | 0.07% | 1,209,638 | 0 |
| Other (OIP) | 1,451.56 | 1.30% | 1,121,972 | 0 |
| Residual | ~0 | ~0 | — | — |

HINCP negative: 589 households (weight 53,091). HINCP zero: 14,622. Age-15+ missing source cells: 0 on this frame (blanks treated as zero after numeric parse; no remaining NA among age 15+).

Wages dominate but are **not** household income. About 31.4 million weighted households have no wage dollars; applying CES AHE to HINCP would mis-state those households.

## Target (defined, not computed)

`annualized_september_2026_household_money_income_run_rate_NOWCAST` = reconstructed 2024 sources × **source-specific** versioned factors + frozen residual, labeled a nowcast. Monthly analog = annual / 12. **Not executed.** Sampling uncertainty (ACS SDR) remains separate from factor/employment-path uncertainty.

## Blockers for a national nowcast

See `DATA_SOURCE_ACQUISITION_REPORT.json` and `../HISTORICAL_BACKTESTING_PLAN.md`. Historical ACS 2019–2023 PUMS are not on disk; ASEC microdata, ECI, and BEA Table 2.6 series are not yet hashed; B2–B3 backtests have not run.
