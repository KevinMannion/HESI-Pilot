# Identifiability of a September 2026 household money-income run rate

Date: 2026-10-21. Phase 2. No national nowcast executed. No 18.9918% rewrite.

## Question

Is an `annualized_september_2026_household_money_income_run_rate_NOWCAST` identifiable from sources actually on disk, with observations, interpolations, projections, and assumptions labeled separately?

## Answer

**No.** A complete source-specific September 2026 household money-income run rate is **not identifiable** from the acquired machine-readable files. CES/ECI monthly-quarterly series and BEA Table 2.6 through September 2026 are missing. Historical gates that must pass before any national adequacy share **did not pass**.

## What is observed

| Object | Kind | Limit |
| --- | --- | --- |
| ACS 2022, 2023, 2024 1-year PUMS (hashed) | Observation of survey microdata | Rolling 12-month money income, not a September snapshot |
| CPS ASEC 2026 CSV (hashed) | Observation of calendar-year **2025** household money income | Not 2026; not ACS; not PUMA |
| SSA COLA 2023–2026 GovInfo FR HTML | Observation of statute | January payable rate, not ACS SSP |
| BEA `pi0826.pdf` | Observation of August 2026 NIPA publication | PDF, not Table 2.6 monthly machine series; September 2026 PI scheduled 2026-10-29 |
| CES Table B-3 extract (Sept 2026 first print) | Observation of a job-earnings snapshot | Private AHE $37.81 vs Sept 2025 $36.70; **not** household WAGP; preliminary |

## What was interpolated

None. Missing CES/BEA months were **not** interpolated.

## What was projected / assumed in the backtest only

- SSP and SSIP: multiply by (1 + January COLA of T+1). Application of a January statutory rate to ACS rolling-year SSP is a **projection/assumption**, not an ACS observation.
- WAGP, SEMP, RETP, INTP, PAP, OIP, residual: **frozen factor = 1** because CES/ECI/BEA series acquisition **failed**. This is an assumption, not a nowcast of wage or proprietors’ income.

## Historical validation (occupied ACS universe; not R2.4 frame)

Diagnostic share uses frozen R2.4 mean three-cost **$2,894.91/month**. It is **not** 18.9918% and is **not** a HESI adequacy estimate.

### B2 2022 → 2023 (COLA 8.7% on SS/SSI; other sources frozen)

- Occupied mean HINCP actual $109,238.72 vs projected $106,387.07 (**−2.6105%**)
- WAGP error **−3.884%** (dominant); SSP error **+2.677%**
- Diagnostic share actual 0.218904 (SDR SE 0.000521) vs projected 0.225906 (SE 0.000598); share error **+0.700 pp**
- Origin-year model contrast (COLA vs freeze, same 2022 sample): −0.545 pp
- Share error ≫ sampling SE; the gap is nowcast-model / composition error, reported separately from SDR

### B2 2023 → 2024 (COLA 3.2% on SS/SSI; other sources frozen)

- Occupied mean HINCP actual $114,375.09 vs projected $109,491.37 (**−4.270%**)
- WAGP error **−3.956%**; INTP error **−12.001%**; SSP error **−3.924%**
- Diagnostic share actual 0.205775 (SE 0.000483) vs projected 0.216777 (SE 0.000512); share error **+1.100 pp**
- Origin-year COLA vs freeze: −0.213 pp

B2 compares **two independent ACS samples**, so error mixes source-growth miss, household-composition change, and sampling. Wage freeze is the main source of understated income and overstated diagnostic hardship.

### B3 ASEC 2026 (calendar 2025) — observation only

- Household rows 88,026; HSUP_WGT/100 sums to 137,123,796.5
- Weighted mean HTOTVAL **$126,664.22**; wages $91,140.00; SS $9,802.57
- ACS occupied 2024 mean HINCP $114,375 is a **different universe and concept**. No ACS-to-ASEC factor calibration was run.

## Predefined gates for a national 2026 nowcast

| Gate | Result |
| --- | --- |
| B1 2024 identity on R2.4 frame | PASS (prior round) |
| B2 T=2022→2023 and 2023→2024 with hashed PUMS **and CES/ECI/BEA factors** | FAIL (PUMS hashed; wage/proprietors factors not acquired) |
| B3 ASEC 2025 calibration | INCOMPLETE (microdata hashed; calibration not run) |
| B4 employment vs rate path | NOT RUN |
| B5 uniform-CPI control | NOT RUN (CPI 403); forbidden for production regardless |
| Factor hashes frozen | PARTIAL |
| Sampling vs model documented | YES; not added |
| `national_R22` hash `6778c312…` | UNCHANGED |
| Publish September 2026 household adequacy | **NO** |

## Remaining limitations

1. download.bls.gov CES/ECI/CPI/CPS-LN: HTTP 403; wage nowcast path blocked.
2. BEA NipaDataM.zip / Section2 xls: 28,185-byte HTML stubs (sha `9578ca8e…`); not NIPA data.
3. `cpsmar26.pdf`: 247-byte WAF page, not the codebook PDF.
4. ACS 2019–2021 PUMS not downloaded.
5. ACS 2025 tables not released until 2026-10-29.
6. Backtests use occupied households, not the R2.4 geography/bedroom/infant eligibility frame.
7. January COLA is a coarse overlay on ACS rolling income.
8. CES Table B-3 is first-print preliminary and will revise; it is not a household-income index.

Until CES/ECI/BEA machine series are acquired and B2/B3 pass with those factors, do not code or publish a national September 2026 household adequacy rate.
