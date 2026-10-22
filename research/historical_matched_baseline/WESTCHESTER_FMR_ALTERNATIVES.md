# Westchester FMR alternatives (not selected)

This note records **unresolved HUD geography alternatives** for Westchester County, New York. It does **not** choose a methodology and does **not** rewrite `puma_fmr_calendar_2024.csv`, FY24/FY25 county tables, or any frozen national/matched-year result.

The calendar-2024 matched-year run used the published HUD county FMR cells as ingested into `outputs/county_model_ready_*.csv` and occupancy-weighted to 2020 PUMAs. That is a **labeled provisional choice**, not an approved correction.

## Alternatives (none adopted here)

1. **Published county FMR as ingested** (current provisional tables). HUD county workbook cell for Westchester / associated NY metro mapping as read by `prepare_2024_cost_inputs.py`.
2. **HUD 50th-percentile rent series** for the affected FMR area, where HUD publishes 50th-percentile rents separately from 40th-percentile FMRs.
3. **Small Area FMR (SAFMR)** ZIP-code rents, occupancy-weighted, instead of the county mean.
4. **Exception payment standard / PHA payment-standard schedule** actually used by local administrators, which can differ from the published FMR.

Do not substitute (2), (3), or (4) into the locked 17.6839565% calculation without a separate scientific-methods approval. Do not recode FIPS to force the R2.4 included weight.

Frozen numerical results are unchanged.
