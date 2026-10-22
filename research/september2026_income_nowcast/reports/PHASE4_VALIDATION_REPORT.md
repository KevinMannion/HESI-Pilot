# Phase 4 validation — non-wage errors and composition

**Decision remains NO-GO.** No September 2026 national nowcast or adequacy share. Phase 3 gates were not relaxed. Candidate models are diagnostics, not a retroactive PASS.

Computational reproduction: yes. Scientific validation: no. `national_R22` hash `6778c312…` unchanged.

## Cross-section vs trajectory

ACS `SERIALNO` does not identify the same household across years. Every score compares two independent occupied cross-sections. Kitagawa composition/rate splits describe **cell-share vs cell-mean** change, not individual income paths.

## 2023→2024: composition is not the story

Actual occupied mean HINCP rose **$5,136**.

| Kitagawa piece | Dollars |
| --- | ---: |
| Composition (cell shares × origin cell means) | **+$106** |
| Within-cell means (origin shares) | **+$5,030** |
| Interaction | **+$1** |

Zero-wage × retirement-majority × age-65+ cell weight was 16.10% in 2023 and 16.21% in 2024. That cell’s **mean** rose 4.8% ($52,948 → $55,477). M4 only applied the 3.2% January 2024 COLA to SSP/SSIP and froze RETP/INTP/SEMP.

M4 2023→2024 source contributions to mean error (projected − actual dollars): INTP **−$715**, WAGP **−$373**, SSP **−$310**, RETP **−$248**, SEMP **−$133**. Zero-wage households: HINCP **−4.11%**, share error **+1.27 pp**. Retirement-majority: **−3.47%**, **+1.34 pp**. Weight shares of those groups match the next ACS year to ~0.1 pp, so the miss is within-cell income, not a changing mix of household types.

## BEA NIPA (acquired)

`https://apps.bea.gov/national/Release/TXT/NipaDataM.txt` (36,806,318 bytes, sha256 `bd202765…`). Units: millions of dollars, SAAR. Coverage through **2026M08** (September 2026 PI not in file). BEA JSON API without UserID returns `Invalid API UserId`. Prior zip URLs remain HTML stubs and were not reused as data.

Calendar-year SAAR ratios (not household money income):

| Transition | Proprietors A041RC | INTP bundle (interest+dividends+rental) |
| --- | ---: | ---: |
| 2021→2022 | 1.0267 | 1.0944 |
| 2022→2023 | 0.9860 | 1.1611 |
| 2023→2024 | 1.0398 | 1.0646 |

BEA 2022→2023 personal interest **+32%** while ACS occupied INTP did **not** rise with that NIPA series. Applying the bundle as a household INTP factor is an assumption, not an observation of ACS INTP.

## ACS RETP and ASEC

ACS RETP is bundled. CPS ASEC 2026 (calendar 2025) national means: pension $3,858, annuity $572 (87% pension of the pair). That mix is **not** mapped onto ACS households.

## Locked evaluation (2022→2023, 2023→2024)

| Year | Model | HINCP % | Share err pp | Notes |
| --- | --- | ---: | ---: | --- |
| 2022→2023 | M1 freeze | −3.207 | +1.245 | baseline |
| 2022→2023 | M2 CPI | +0.777 | +0.472 | control only |
| 2022→2023 | M4 AWE+COLA | +0.238 | +0.322 | locked production candidate |
| 2022→2023 | M5 M4+BEA SEMP/INTP | +0.963 | +0.255 | INTP overlay overshoots this year |
| 2022→2023 | M5b SEMP only | +0.172 | +0.329 | |
| 2022→2023 | M6 +COLA on all RETP | +1.566 | +0.064 | unsupported household RETP split |
| 2023→2024 | M1 freeze | −4.491 | +1.313 | |
| 2023→2024 | M2 CPI | −1.674 | +0.715 | |
| 2023→2024 | M4 | −1.646 | +0.668 | G2/G3 fail |
| 2023→2024 | M5 | −1.169 | +0.611 | helps INTP; G3 still fail |
| 2023→2024 | M5b | −1.467 | +0.635 | |
| 2023→2024 | M6 | −0.955 | +0.549 | still fails G3; not a DB/DC model |

Locked gates: G2 FAIL, G3 FAIL, G4 PASS, G5 PASS. Unchanged.

## Additional untouched year 2021→2022 (not used to choose a model)

M1 −7.30% / +1.88 pp. M2 CPI +0.12% / +0.17 pp. M4 −3.75% / +1.08 pp. High-inflation year: uniform CPI wins the mean and is still forbidden for production. M4 wage+COLA is not sufficient when non-wage and price-level shifts are large.

ACS 2021 PUMS hashes: hus `e1f4fb85…`, pus `e1e64f81…`.

## Prospective protocol (future untouched years only)

Do not apply to 2022–2024 after seeing these results. For a later pair (for example ACS 2024→2025 once 2025 PUMS exists): keep G2–G8; require hashed BEA NipaDataM (or API) vintage; predeclare whether BEA INTP is used; report Kitagawa composition vs within-cell; do not invent ACS DB/DC splits.

## Identifiability of September 2026 run rate

CES through 2026-09 (preliminary) is on disk. BEA monthly NIPA through **2026-08** only. Locked historical gates still fail. Still not identifiable as a publishable household nowcast.
