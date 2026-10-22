# September 2026 household-income nowcast (R2.5 research)

2024 ACS source reconciliation is implemented. Phase 4 acquired BEA monthly NIPA (`NipaDataM.txt`) and showed the 2023→2024 miss is within-cell, not composition. Locked Phase 3 gates still fail. Decision remains **NO-GO**. The September 2026 national income nowcast and a new affordability share are **not** computed.

The published Core R2.4 share **18.9918%** remains the immutable **2024-income** scenario: September 2026 modeled Food + Housing + one-car Transport versus 2024 ACS `HINCP` × `ADJINC`.

Read `METHOD.md`, `HISTORICAL_BACKTESTING_PLAN.md`, `reports/`, `SOURCE_REGISTER.json`, and `LOCK_DECISION.json` before any nowcast code.

Rules:

- Do not apply a uniform CPI factor to household income.
- Do not treat CES wage growth as household-income growth.
- Never label a nowcast as measured 2026 household income.
- Do not alter Food, Housing, or Transportation specifications or `core_r24/results/national_R22`.
