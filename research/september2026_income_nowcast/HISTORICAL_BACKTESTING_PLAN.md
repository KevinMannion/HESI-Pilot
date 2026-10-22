# Historical backtesting and calibration plan

Status: **partially executed 2026-10-21**. B1 pass (prior). B2 occupied ACS 2022→2023 and 2023→2024 ran with hashed PUMS but **wage/proprietors factors frozen** (CES/ECI/BEA series not acquired) — production gate **FAIL**. B3 ASEC 2026 microdata hashed and national means observed; factor calibration **not** completed. B4/B5 not run. September 2026 national income nowcast remains **blocked**. See `reports/HISTORICAL_BACKTEST_REPORT.json` and `reports/IDENTIFIABILITY_ASSESSMENT.md`.

This plan tests whether source-specific factors recover later *observed* ACS/ASEC money-income totals. It does not produce a 2026 affordability share.

## Target definition (when a nowcast is later allowed)

`income_annual_YYYY_NOWCAST` = sum over sources of (ACS base-year household source amount × source-specific factor) + frozen residual.

Label as a nowcast. Never as measured household income of the target year.

Sampling uncertainty: ACS 80 SDR replicates on the **base-year household frame**, holding factors fixed.

Nowcast-model uncertainty: variation of factors, employment path, residual treatment, and allocated-income inclusion, holding the base-year replicate draw fixed. Report the two intervals separately. Do not add them into one number without an explicit combination rule.

## Why it cannot run yet

The R2.4 distribution contains ACS **2024** housing and person ZIPs only. Backtests need ACS 1-year PUMS for 2019–2023 (housing + person) and contemporaneous CES/ASEC/SSA/BEA vintages. Those PUMS files are **not on disk**.

## Experiments (execute in order)

### B1. Identity / rounding (2024, this round)

Already required of the reconciliation pipeline: household sum of WAGP, SEMP, RETP, SSP, SSIP, INTP, PAP, OIP versus `HINCP × ADJINC / 1e6` on the R2.4 frame. Pass if residuals are documented and not treated as a ninth CES-wage class.

### B2. One-year ACS-to-ACS source nowcast

For each origin year T in {2019, 2020, 2021, 2022, 2023}:

1. Reconstruct household sources on year-T PUMS using this pipeline.
2. Build source factors from CES/ECI (wages), BEA proprietors (SEMP), SSA COLA (SSP/SSIP), BEA interest/dividends (INTP), freeze PAP/OIP/residual unless a program path is documented. Factors use **only information available at the end of T+1**.
3. Predict year T+1 ACS source totals and mean household income.
4. Compare to observed ACS T+1 PUMS (same occupancy definition; do not force the R2.4 2024 geography exclusions onto other years without a documented analog).

Scores: weighted mean error by source; residual share; Kolmogorov–Smirnov on log income for households with wages; error in a *frozen-cost* share-below using **year T+1 costs held out** — this last score is a nowcast diagnostic, not a published HESI affordability rate.

### B3. ACS-to-ASEC calibration

Using ACS 2024 sources, apply 2024→2025 factors and compare national source *shares and totals* to CPS ASEC 2026 (income year 2025). ASEC is not PUMA-coded like ACS; this is a national/state calibration, not a household match.

After 29 October 2026, also compare to ACS 2025 1-year tables. Do not wait for 2025 PUMS to run table-level calibration.

### B4. Employment-path vs rate-path

On B2, run three wage variants: (i) CES AHE only, hours and employment frozen; (ii) AHE × hours; (iii) AHE × hours × employment-population. Record which variant wins on non-wage sources (it should not “win” by leaking wage growth into SEMP/SSP).

### B5. Forbidden-control

A uniform CPI-U factor on HINCP must be scored as a **control that is not used**. If it beats source-specific factors on total income, still reject it for publication; report the comparison so the restriction is empirical, not rhetorical.

## Pass / fail before any September 2026 national nowcast

1. B1 complete on 2024 R2.4 frame (this engineering round).
2. At least B2 for T=2022→2023 and T=2023→2024 with hashed PUMS.
3. B3 ASEC 2025 calibration with hashed microdata or published totals.
4. Factor files SHA-256 frozen; no uniform CPI applied to production path.
5. Sampling vs model uncertainty documented on the backtest years.
6. `core_r24/results/national_R22` bytes unchanged; 18.9918% not rewritten.

## Exact files to acquire for B2–B3

- ACS 1-year PUMS housing + person ZIPs: 2019, 2020, 2021, 2022, 2023 (2024 already hashed).
- Matching PUMS dictionaries.
- CPS ASEC 2023–2026 public-use files (income years 2022–2025).
- CES AHE/AWE/hours monthly, ECI quarterly, BEA Table 2.6, SSA COLA FR notices for each year.
- After 2026-10-29: ACS 2025 1-year income tables.

Do not invent geographic weights or ACS files that are not on disk.
