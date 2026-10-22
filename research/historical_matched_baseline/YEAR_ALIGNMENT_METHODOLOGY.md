# Year-alignment methodology (design only)

This document does not compute a national share. It does not alter Core R2.4.

## Two incommensurable objects

| Object | Income | Costs | Status |
| --- | --- | --- | --- |
| A. Published R2.4 | Observed 2024 ACS money income | September 2026 modeled Food + FY2026 HUD rent + Sept 2026 one-car | Immutable 18.9918% |
| B. Proposed matched-year baseline | Observed ACS year T money income | Modeled costs whose **published reference period** is year T | Not computed |

A is a cross-vintage scenario. B is a historically aligned scenario. They answer different questions. Do not overwrite A with B.

The income-nowcast workstream is a third experimental object. Its NO-GO and failed gates stay on file. Do not feed nowcasted 2026 income into B.

## Observed income vs modeled costs

- **Observed:** ACS `HINCP × ADJINC / 1e6 / 12` on that year’s PUMS. Survey-weighted. Rolling past-12-months money income.
- **Modeled:** USDA Thrifty schedule, HUD FMR replacement rent with the locked bedroom rule, one-car transport formula. None of these is the household’s reported grocery bill, rent, or car outlay.

ACS rolling-period limit: interviews in year T mix income from T−1 and T. `ADJINC` puts amounts in year-T dollars; it does not make income a December or September snapshot. Matched-year costs should be labeled the same way: **year-T modeled schedules vs year-T ACS rolling income**, not “calendar-T cash-flow hardship.”

## Proposed clocks for object B, year T ∈ {2022, 2023, 2024}

1. **Households and income:** ACS 1-year PUMS for year T. Occupied `TYPEHUGQ==1`, `NP>0`, `WGTP>0`, then the same bedroom/infant/completeness exclusions, applied to **that year’s** geography table. Do not reuse the 2024 included set of 121,036,726 as the 2022 or 2023 denominator.
2. **Food:** Mainland USDA Thrifty **monthly** cells for year T, aggregated to an **annual mean of the 12 published months**, then the same household-size factors as R2.4. Alternative (sensitivity, not default): a single named month. Do not use September 2026 prices.
3. **Housing:** HUD FMR for the fiscal year that contains the chosen cost month, occupancy-weighted to 2020 PUMAs with **year-T or documented contemporaneous** occupied counts. Default proposal for “calendar year T costs”: FMR **FY T** (October T−1–September T) for January–September alignment, with FY T+1 as a predeclared October–December sensitivity — or a single FY T table labeled as such. Do not mix FY2026 rents into B.
4. **Transport:** Same mechanical formula as the pillar (miles, mpg, component sum). Replace only series that have a hashed year-T observation (EIA gasoline). Hold unverified non-fuel dollars as **named assumptions** and vary them in a model-uncertainty table. Do not silently keep $7,264.70.
5. **Geography:** 2022–2024 ACS share 2020 PUMAs and may share a PUMA universe. 2021 ACS uses 2010 PUMAs and is out of scope for this series unless a separate 2010-PUMA FMR crosswalk is built.

## What must not be mixed

- 2024 ACS composition with 2022 USDA prices.
- FY2026 rents with a “2024 cost” label.
- 2020-PUMA FMR table with 2021 PUMS.
- Nowcast income with matched-year costs.
- Occupied-universe nowcast backtests with the R2.4 eligibility frame, or vice versa.

## Uncertainty

- **Sampling:** ACS 80 successive difference replicates, 4/80 formula, costs and model constants held fixed. Same method as R2.4.
- **Model assumptions (separate):** food annual-mean vs December; FY T vs FY T+1 housing; transport non-fuel dollars; mainland food on AK/HI; replacement rent on owners; one-car assignment. Report these as a table of alternatives, not added into the SDR interval.

## Engine architecture (when later approved to code)

Keep `core_r24/src/run_joint.py` as the September 2026 / 2024-income calculator.

Add a sibling path, for example `research/historical_matched_baseline/src/run_matched.py`, that:

- parameterizes food catalog `(year, month or annual mean)` instead of hard-coded `(2026, 9)`;
- takes a year-specific `puma_fmr_*.csv` and `transport_annual`;
- writes to a new output directory;
- refuses to write `core_r24/results/national_R22/`.

Person caches must be rebuilt per ACS year (composition and food prices both depend on T).
