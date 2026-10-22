# Income factor methodology (Phase 3)

Declared before scoring. Does not publish a September 2026 adequacy share.

## Clocks

| Clock | Object |
| --- | --- |
| ACS year T | Rolling 12-month money income, `ADJINC` to year-T dollars |
| CES/CPI/ECI | Monthly or quarterly *job* or price indices, calendar-year annual means |
| SSA COLA | Statutory percent payable in January of T+1 |
| Target (not computed) | Annualized September 2026 household money-income run rate, labeled NOWCAST |

ACS T→T+1 backtests overlay calendar-year T+1 / T index ratios on origin-year household sources. That is a coarse alignment, not a month-by-month reconstruction of each ACS interview window.

## Simulated forecast date

For ACS T→T+1: **31 January of T+2**. Series dated after December T+1 are not used. ACS T+1 PUMS is treated as unknown. BLS Public API values are the **current vintage** as of 2026-10-22T01:27:10Z. ALFRED first-print vintages were not acquired (FRED maintenance). Later CES revisions are a hindsight limitation.

## Models

| ID | Rule | Role |
| --- | --- | --- |
| M1 | All sources factor=1 | Baseline |
| M2 | `hincp_adj` × CPI-U NSA annual T+1/T | Diagnostic control. Forbidden for production. |
| M3 | CES AHE annual T+1/T applied only to `WAGP` of households with `WAGP>0`. Other sources frozen. Zero-wage households unchanged. | Aggregate wage-growth |
| M4 | `WAGP>0`: CES AWE annual T+1/T (rate × hours). `WAGP<=0`: freeze wages. `SSP`/`SSIP`: × (1+January COLA of T+1). `SEMP`, `INTP`, `RETP`, `PAP`, `OIP`, residual: freeze because BEA Table 2.6 was not acquired. Employment counts frozen (no new earners). Negative `SEMP`/`INTP` kept as observed (not multiplied). | Source-specific production candidate |

CES AHE is **not** applied to HINCP. CES employment growth is computed and stored but **not** multiplied into household wages (that would treat the extensive margin as a raise for people already earning WAGP).

ECI civilian wage and compensation annual means are a cross-check, not a household factor.

## Identity

Household reconstructed income remains `sum(WAGP, SEMP, RETP, SSP, SSIP, INTP, PAP, OIP) + residual` with `residual = HINCP×ADJINC/1e6 − component sum`. Residual is never given CES growth.

## What is not a 2026 nowcast

These backtests stay on the occupied ACS universe, not the R2.4 geography/bedroom/infant frame. Diagnostic share-below uses the frozen R2.4 three-cost monthly mean $2,894.91. That is not 18.9918%.
