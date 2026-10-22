# 2024 matched-year national scenario — PROVISIONAL — NOT SCIENTIFICALLY VALIDATED

Date: 2026-10-22. Not a measured national hardship rate. Not an official validated HESI finding. Not a September 2026 hardship rate. Not an income nowcast. External computational reproduction is pending.

Core R2.4 **18.9918%** (`national_R22` `6778c312…`) and the 2024 observed-housing pilot **10.301%** are unchanged. September 2026 income nowcast remains **NO-GO**.

This object uses **household-specific** modeled food + HUD replacement rent + one-car transport versus observed ACS 2024 income. It does **not** use the nowcast G3 uniform $2,894.91 threshold.

## Default result

Income: ACS 2024 `HINCP × ADJINC / 1e6 / 12` on the R2.4 eligibility frame (1,235,731 households; weighted **121,036,726**). Frame identity vs R2.4: PASS (same complete PUMA set of 2,350; geography-excluded 64,079 / 6,271,320).

| Component | Monthly mean |
| --- | ---: |
| Food (2024 Thrifty annual mean of 12 mainland months) | $625.425455 |
| Housing (calendar-2024 day-weight FY24 orig/rev + FY25 orig) | $1,528.922176 |
| Transport (EIA 2024 gasoline $3.304; **non-fuel $5,631.67 held**) | $572.555833 |
| Combined | $2,726.903465 |
| Observed ACS 2024 income | $9,325.244238 |

Share below household-specific combined cost: **0.17683956520767094**, displayed **17.6839565%**, about **17.7%**.  
Sampling-only 90% interval: 17.5966% to 17.7714% (ACS 80 SDR; costs held fixed).  
Economic-model uncertainty (housing clock, no-car, inherited non-fuel $5,631.67, one-car rule) is **outside** that interval. See `MODEL_VS_SAMPLING_UNCERTAINTY.md`.

## Sensitivities (same households)

| Scenario | Share | No-car share |
| --- | ---: | ---: |
| Default calendar-2024 housing | 17.68396% | 13.05558% |
| FY2024 revised FMR only | 17.54959% | 12.92492% |
| FY2025 original FMR (from 2024-10-01) | 18.12042% | 13.45400% |

R2.4 cross-vintage 18.9918% used September 2026 food/housing/gasoline on this same 2024 income frame.

## Input gates

`INPUT_VALIDATION.json`: PASS before the national run (frozen hashes, Census ZIP verification, 12 USDA 2024 months, PUMA complete-set identity, labeled transport).

`VALIDATION_GATES.json`: PASS after the run, including refusal to write `national_R22` and explicit non-validation status.

## Limitations

- Non-fuel transport is an inherited R2.4 hypothetical, not 2024 insurance, depreciation, maintenance, registration, or financing.
- One car is assigned to every included household.
- HUD FMR is replacement rent, not observed rent.
- Mainland Thrifty cells are used nationally, including AK/HI.
- Infants and >4-bedroom compositions are excluded.
- ACS income is rolling 12-month money income, not a December snapshot.
- SDR intervals are sampling-only.
- `EXTERNALLY_INDEPENDENTLY_REPRODUCED=NO`.

Machine-readable copies: `EXECUTION_REPORT.json`, `SOURCE_MANIFEST.json`, `calendar_2024_dayweight/common_cohort_results.csv`.
