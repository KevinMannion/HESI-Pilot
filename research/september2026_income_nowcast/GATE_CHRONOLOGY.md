# Validation-gate chronology (not preregistration)

`reports/VALIDATION_GATES.json` is **preserved**. This note only records what the git and file timestamps actually show.

## What is in git

Every file under `research/september2026_income_nowcast/` first appears in commit `fb58ddc` (2026-10-21 22:22:31 -0400), the public research-branch checkpoint. There is **no earlier git tag, commit, or OSF/GitHub deposit** of `VALIDATION_GATES.json` before Phase 2, 3, or 4 results.

Therefore this repository **does not support a claim of public preregistration**.

## Self-attested sequence (operator notes, not immutable)

| Claim | Evidence | Strength |
| --- | --- | --- |
| `declared_at`: 2026-10-21T21:26:00-04:00 | Field inside `VALIDATION_GATES.json` | Self-attested |
| `declared_before_phase3_model_comparisons`: true | Same file; comment in `run_phase3_validation.py` | Self-attested |
| BLS API download timestamp | `BLS_ANNUAL_FACTORS.json` `2026-10-22T01:27:10Z` (= 21:27 EDT) | One minute after the gates timestamp |
| Phase 2 occupied COLA/wage backtests | `reports/HISTORICAL_BACKTEST_REPORT_PHASE2.json` in the same commit as the gates | Exploratory results bundled with the gates |
| Phase 3/4 scored results | Same commit | Not a later sealed addendum |

Phase 2 occupied-universe backtests existed in the working tree **before** the Phase 3 four-model comparison code. The locked G2/G3 thresholds were written as a Phase 3 gate file. They were **not** posted to an independent registry before those scores were known to this operator.

## What remains locked

- Gate **rules and thresholds** in `VALIDATION_GATES.json` are not relaxed.
- Scored FAIL/PASS outcomes are not rewritten.
- Decision remains **NO-GO**.
- No September 2026 national adequacy estimate.

Use: “gates declared in-repo relative to Phase 3 code, with Phase 2 already exploratory” — not “preregistered.”
