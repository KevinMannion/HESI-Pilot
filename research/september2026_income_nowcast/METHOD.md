# R2.5 September 2026 household-income nowcast — design (no national estimate yet)

Status: research workstream only. National nowcast is **not coded**. Food, Housing, Transportation specifications and the published **18.9918%** 2024-income scenario are frozen.

Audit date: 2026-10-21.

## 1. What Core R2.4 actually uses

`core_r24/src/run_joint.py` converts observed ACS household money income to a monthly figure:

`HINCP * ADJINC / 1e6 / 12`

It labels the result `income_month_2024_vintage`. Person caches currently read only `SERIALNO`, `AGEP`, `SEX`, `RELSHIPP`. Wage, self-employment, Social Security, retirement, and other person-level amounts are **not** in the joint caches today.

The 18.9918% share is September 2026 modeled costs versus that 2024 income. It is not a 2026 hardship rate.

## 2. Available 2024 ACS PUMS income variables

Source: 2024 ACS 1-year PUMS Data Dictionary (16 October 2025). Amounts are past-12-months money income; apply `ADJINC` (2024 1-year factor 1.015250) to express 2024 dollars. Persons under 15 are N/A on person income fields.

### Household file (already in the joint housing ZIP)

| Variable | Role |
|---|---|
| HINCP | Household income, past 12 months. Bottom-coded at −$59,999. Used in R2.4. |
| FINCP | Family income. Not used in R2.4. Do not substitute for HINCP. |
| ADJINC | Income inflation factor (6 implied decimals). Used in R2.4. |
| GRPIP | Gross rent as percent of household income. Cost/income ratio, not an income source. |

### Person file (present in person ZIPs; not loaded by current caches)

| Variable | Source class for nowcast |
|---|---|
| WAGP | Wage and salary earnings |
| SEMP | Self-employment income (can be negative) |
| RETP | Retirement income (DB, DC, and related receipts are **bundled**) |
| SSP | Social Security (OASDI) |
| SSIP | SSI |
| INTP | Interest, dividends, and net rental (can be negative) |
| PAP | Public assistance |
| OIP | All other income |
| PERNP | Person earnings (WAGP+SEMP conceptually; still rounded/top-coded) |
| PINCP | Person total income |
| WKHP, WKWN, WKL, WRK, INDP, OCCP, COW | Labor supply and job class, needed so wage factors are not applied to non-workers |

Allocation flags (`FWAGP`, `FHINCP`, …) must be retained for sensitivity: allocated income should not silently drive nowcast error.

Identity check (document residual; do not force equality): household `HINCP` versus the sum of person `PINCP` (or source components) after rounding and top-coding.

## 3. Latest external vintages as of 2026-10-21

**CPS ASEC 2026** (income year **2025**). Public-use household/family/person files are posted. The official report *Income in the United States: 2025* was released 15 September 2026 (2026 ASEC). Real median household money income was reported as $87,460 in 2025. ASEC is a **calendar-year annual** supplement (Feb–Apr 2026 interviews about 2025), not a September 2026 household-income measurement. Useful person-source fields include wage/salary, self-employment, Social Security, SSI, retirement/annuity, interest, dividends, and other (API names such as `WSAL_VAL`, `SEMP_VAL`, `SS_VAL`, `SSI_VAL`, `RTM_VAL`, `ANN_VAL`, `INT_VAL`, `DIV_VAL`).

**BLS September 2026 Employment Situation** (USDL-26-1549, 2 October 2026; first print, preliminary):

- CES nonfarm payrolls +29,000; unemployment rate 4.2% (little changed)
- Private average hourly earnings $37.81; +0.1% month, +3.0% year
- Average weekly hours 34.4
- Average weekly earnings, all private, $1,300.66 (FRED table B-3)

These are **job** earnings and **labor-force** counts, not household money income.

**ACS 2025 1-year tables** public release is **29 October 2026**. 2025 PUMS release is **TBD**. Until PUMS exists, 2025 ACS can calibrate tables, not replace 2024 household microdata.

**SSA:** 2.8% COLA for OASDI/SSI payable January 2026 (CPI-W 2024 Q3 vs 2025 Q3). The 2025 COLA was 2.5%. These apply to **SSP/SSIP**, not to wages or HINCP as a whole.

**Not a household-income series:** uniform CPI-U/CPI-W on HINCP; CES AHE applied to total household income.

## 4. Proposed method (source-specific nowcast)

Hold 2024 ACS household composition, geography, and eligibility **fixed**. Nowcast income only. Output a separate object: `income_month_2026sep_NOWCAST`.

### Step A — decompose observed 2024 income

Re-read person PUMS. For each occupied household on the R2.4 frame:

1. Inflate each person source with `ADJINC`.
2. Aggregate `WAGP`, `SEMP`, `RETP`, `SSP`, `SSIP`, `INTP`, `PAP`, `OIP` to SERIALNO.
3. Store `residual = HINCP_adj − sum(components)` and `PINCP_gap`. Residual is a documented remainder (rounding/top-code/universe), not a ninth growth class to which CES is applied.

### Step B — map each source to a distinct index path (no uniform CPI)

| ACS source | Index path to September 2026 | Forbidden shortcut |
|---|---|---|
| WAGP | Split rate vs hours vs employment. Rate: CES AHE or ECI by industry (`INDP`) and class of worker. Hours: CES/CPS weekly hours vs ACS `WKHP`/`WKWN`. Employment: CPS employment-population and unemployment vs 2024 ACS work status; do not raise wages of non-earners. Two-stage: ACS 2024 → ASEC 2025 wage totals, then CES/ECI January–September 2026. | Apply 3.0% CES AHE to HINCP |
| SEMP | BEA nonfarm (and farm, if rural) proprietors’ income; not CES payroll earnings. Optional IRS SOI lag as a diagnostic only. | Treat SEMP as wages |
| SSP, SSIP | Statutory COLA sequence through the ACS rolling year into January 2026; hold benefit **receipt** at 2024 ACS unless a separately specified take-up model is added | COLA on total income |
| RETP | Split if possible using ASEC retirement vs annuity. Public/DB: COLA or public-plan rules. DC/drawdown: not CPI; use a labeled capital-income path or freeze with wide sensitivity | One CPI factor |
| INTP | BEA personal interest and dividend receipts, or freeze + rate-path sensitivity. Rental net is mixed in ACS INTP | CES wages |
| PAP, OIP | Program/rule path if documented; otherwise freeze amounts and vary in sensitivity | Inflate with CPI-U |
| Residual | Freeze; report share of HINCP | Assign wage growth |

### Step C — vintage alignment

ACS 2024 income is a **rolling 12-month** amount across 2024 interviews, then `ADJINC`-shifted to 2024 dollars. ASEC is **calendar 2025**. CES is **monthly jobs**. The nowcast must state three clocks and not pretend they are one September 2026 household survey.

Proposed clocks:

1. **Observed:** 2024 ACS (R2.4).
2. **Annual calibration:** CPS ASEC 2026 / income year 2025, plus ACS 2025 1-year tables after 29 October 2026.
3. **Within-2026 labor/transfer path:** CES, CPS monthly, SSA COLA, BEA PI from January 2026 through September 2026 (CES Sept 2026 currently preliminary).

### Step D — construct household nowcast

`Y_2026sep_hh = sum_s (Y_2024_hh,s * F_s) + residual_2024_hh`

where `F_s` is the source-specific factor, possibly interacted with industry, work status, and receipt flags. Negative `SEMP`/`INTP` keep sign; do not apply a positive wage factor to losses without an explicit rule.

Monthly nowcast = annual nowcast / 12, parallel to R2.4, and labeled modeled.

## 5. Validation (required before any national share is published)

1. **Provenance:** SHA-256 every input; record series IDs, seasonal adjustment, and revision vintage (CES first print vs later).
2. **Vintage gate:** refuse to mix ASEC 2025 medians with ACS 2024 microdata without the two-stage documentation above.
3. **Historical backtest:** using ACS 2019–2023 PUMS and contemporaneous CES/ASEC/SSA, predict the next ACS 1-year household income **by source**, not only the mean. Score MAE/RMSE on source totals and on the share-below a frozen cost index.
4. **Calibration:** national (and state, if cell sizes allow) nowcast of 2025 ACS/ASEC source totals must be compared with published 2025 ASEC and, after 29 October 2026, ACS 2025 tables. Recalibrate factors only with a versioned change log.
5. **Uncertainty:** interval the nowcast from (a) ACS SDR 80 replicates on 2024 composition, (b) CES/ECI/BEA revision ranges, (c) employment-path alternatives, (d) freeze vs grow residual. Sampling-only ACS intervals are **not** nowcast uncertainty.
6. **Sensitivity:** wage-only vs full source mix; hours held vs hours updated; COLA-only transfers; investment freeze vs BEA path; allocated-income dropped.

Pass/fail for a later coding round: backtests and calibration reports exist; metric names remain distinct from `income_month_2024_vintage`; 18.9918% file bytes unchanged.

## 6. Data gaps (do not invent)

- No September 2026 ACS or CPS **household income** microdata.
- 2025 ACS PUMS not released as of 2026-10-21.
- ACS `RETP` and `INTP` mix unlike instruments; ASEC is richer but not PUMA-coded like ACS.
- ACS/CES industry crosswalk and top-coding bias at the right tail.
- Self-employment and capital income have no CES equivalent.
- CES September 2026 earnings are preliminary.
- QCEW lags; Q3 2026 QCEW will not support a September freeze.
- Benefit take-up, job loss, and household formation between 2024 and September 2026 are **not** observed; holding 2024 households is a scenario, not a panel.

## 7. Exact sources still needed on disk (hashed) before coding the national estimate

1. CPS ASEC 2026 CSV/SAS microdata + dictionary (`cpsmar26.pdf`).
2. CES/CPS September 2026 Employment Situation tables B-2, B-3, B-8 and series IDs (and the October revision when used).
3. Latest ECI quarter available at freeze.
4. BEA monthly personal income by source through the latest 2026 month.
5. SSA COLA 2025 and 2026 Federal Register notices (already identified).
6. 2024 ACS person files with `WAGP SEMP RETP SSP SSIP INTP PAP OIP PINCP PERNP WKHP WKWN INDP COW` plus allocation flags (same ZIPs already hashed; new column list only).
7. After 29 October 2026: ACS 2025 1-year income tables; PUMS if/when posted.

## 8. Implementation boundary

Do not edit `core_r24/src/run_joint.py` formulas, eligibility, or `results/national_R22`. A future nowcast runner must live under `research/september2026_income_nowcast/` and write separate outputs.
