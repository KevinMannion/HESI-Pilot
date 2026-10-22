# Official research-run configuration

These JSON files are the checked-in example methodology configurations for
**official** (non-exploratory) executions.

Official runs are refused unless the operator supplies:

1. `--output` / `--out` (scratch; never a frozen scientific directory)
2. `--model-vintage` matching the JSON `model_vintage`
3. `--config` pointing at one of these files
4. Authenticated Census housing and person archives on the CLI (`--housing`, `--person-official` or split person ZIPs)

Do **not** pass `--exploratory` for acceptance of official research runs.

Census microdata paths are **not** stored in the JSON. They remain operator-held and uncommitted.

## National R2.4 (frozen comparison)

```
python core_r24/reproduce_from_raw.py \
  --housing /PATH/csv_hus.zip \
  --person-official /PATH/csv_pus.zip \
  --output /PATH/scratch_official_national \
  --model-vintage r24_sep2026_costs_on_acs2024_income \
  --config core_r24/configs/official_r24_sep2026_on_acs2024.json
```

Expected: six national metrics and 80 SDR replicates match `core_r24/results/national_R22` at atol 1e-7. Frozen directories must be unmodified.

## Matched-year 2024 (provisional reproduction)

```
python research/historical_matched_baseline/src/run_matched_national.py \
  --housing /PATH/csv_hus.zip \
  --person-official /PATH/csv_pus.zip \
  --out /PATH/scratch_official_matched \
  --cache /PATH/scratch_official_matched_cache \
  --model-vintage matched2024_provisional_repro \
  --config research/historical_matched_baseline/configs/official_matched2024_provisional_repro.json
```

`--out` must not be `results/matched2024_provisional`.

Scientific publication stays **NO-GO**.
