# Methods review remediation, round 1 (2026-10-22)

Paused new features and national calculations. Frozen `national_R22` / 18.9918% not rewritten. Nowcast remains **NO-GO**. Closed as a local checkpoint; not pushed.

## Issue-by-issue

### 1. Reproduction inputs — confirmed
ZIP SHA-256 of Census `csv_pus.zip` (`afdc6d90…`) differs from split `HESI_Person_Part_*` because of container layout (two CSVs + README) and compression. Uncompressed `psam_pusa.csv` / `psam_pusb.csv` SHA-256 are **identical**. Added `PUMS_ARCHIVE_LOCK.json`, `tools/pums_archive.py`, and `reproduce_from_raw.py --person-official` which still requires inner-CSV checksums.

### 2. Validation protocol — confirmed, not preregistered
All nowcast files first appear in `fb58ddc`. `VALIDATION_GATES.json` is preserved. Chronology documented in `GATE_CHRONOLOGY.md`. Reports no longer call this public preregistration.

### 3. M4 specification — confirmed mismatch, results unchanged
Gate text includes BEA SEMP/INTP. Scored Phase 3 M4 freezes them. Phase 4 M5 applied BEA and still failed G3. See `M4_SPEC_VS_SCORED.md`.

### 4. G3 adequacy — confirmed proxy
G3 uses one frozen monthly mean. Household-specific backtest **designed** and fixture-tested; **not** run nationally; **not** a 2026 nowcast.

### 5. Reporting — recommended rounding + no-car
Computational 18.9918% locked. Public prose ~19.0%. No-car ~14.0% (computational 14.0322%) already in `common_cohort_results.csv`.

### 6. Pilot tenure labels — confirmed
206,820 “unsupported_tenure” = 183,206 GQ (TYPEHUGQ≠1, TEN missing) + 23,614 rent-free (TEN=4). `run.py` does not read TYPEHUGQ. Pilot `results.csv` unchanged.

### 7. CES series — confirmed
M4 uses all-employee SA AWE `CES0500000011`, not AHE×hours and not production/nonsupervisory AHE.

### 8. ERRATA.txt
Also records partnership rule, infant/food split, eight ACS sources vs BEA bundles, HUD FY2026 original vs 2026-05-21 revision.

## Tests run (this round)
See ITERATION_NOTES. No national nowcast. Local checkpoint only; no push/merge/PR. Pause before household-specific ACS validation.
