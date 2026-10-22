# Grok Reproducer handoff — 2024 matched-year provisional

Reproduce the **computational** 2024 matched-year scenario. This is not scientific validation and not permission to publish 17.7%.

Branch: `hesi/core-r25-integration` (working tree as of this handoff; uncommitted until the operator approves).  
Do **not** write `core_r24/results/national_R22/`.  
Do **not** change `VALIDATION_GATES.json` nowcast thresholds.

## Software

- Python 3.13, `numpy>=1.22,<2`, `pandas>=1.4,<3` (author run: numpy 1.26.4 / pandas 2.3.3)
- `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`

Census microdata are **not** in git. Use official ACS 2024 1-year PUMS:

| File | SHA-256 |
| --- | --- |
| `csv_hus.zip` | `8281008e53de98f0ef81e7a2ee5a8725991dda1ecfd2713ead73246425e515d0` |
| `csv_pus.zip` (container) | `afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894` |
| inner `psam_pusa.csv` | `b1c2ba439cb7a65f85aa36821d18c1888ae4df77cfeec0facadc1c2cff74680c` |
| inner `psam_pusb.csv` | `b0ee65a88f8acf7e768ef94da2794bc7af2be81bfae8d2742b130f4fded13c88` |

Split person ZIPs `HESI_Person_Part_1/2` are accepted only if their **ZIP** SHA-256 match `core_r24/PUMS_ARCHIVE_LOCK.json`. Official `csv_pus.zip` is accepted only after **inner CSV** hashes match.

In-repo cost tables (already hashed in git):

| Path | SHA-256 |
| --- | --- |
| `core_r24/inputs/source_2024_2026.csv` | `90bc39d1a569073b9530ca0a78a4ccf19c781c4a42dd70c51a0bed9e1907602c` |
| `outputs/puma_fmr_calendar_2024.csv` | `1555b558629be1f730d4fb1a1d732120fdba2abd8e5ba9e860fc55c10e4ae9b0` |
| `outputs/puma_fmr_fy24_revised.csv` | `263d08a2c5b1140dfe88499d553c73851945eb80b4c7836ba47b43c84a344787` |
| `outputs/puma_fmr_fy25_original.csv` | `60c429d77a0acefc163e425088ba6148da3c5f7b97b3c6d0bc5dd0d19dea3c50` |
| `outputs/transport_reference_2024.csv` | `6db488816c775bb4cc8b8bfff097a683dea4b3c5f2a5d24b98d4ff56e0b08b55` |

Derived person caches are gitignored. Rebuild them. Author food-cache SHA-256 `911ef1f77071ecb026400e714b5ffeb8a7b5ec4677c19d950770274e3c3e1f72`; composition `4e7c8dbbbf6decb65bb5de0d0bb72260fd812f5c8e8f0604eefb00ffc2bf7e7d`.

## Commands

From the repository root, with Census ZIPs on disk:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1

python research/historical_matched_baseline/src/validate_matched_inputs.py \
  --housing /path/to/csv_hus.zip \
  --person-official /path/to/csv_pus.zip \
  --out /tmp/matched2024_repro/INPUT_VALIDATION.json

python research/historical_matched_baseline/src/run_matched_national.py \
  --housing /path/to/csv_hus.zip \
  --person-official /path/to/csv_pus.zip \
  --out /tmp/matched2024_repro \
  --cache /tmp/matched2024_repro/caches
```

Or split person archives instead of `--person-official`:

```bash
  --person-a /path/to/HESI_Person_Part_1.zip \
  --person-b /path/to/HESI_Person_Part_2.zip
```

## Acceptance

Compare `/tmp/matched2024_repro/calendar_2024_dayweight/` to
`research/historical_matched_baseline/results/matched2024_provisional/calendar_2024_dayweight/`.

| Check | Tolerance |
| --- | --- |
| `common_cohort_results.csv` every metric mean/se/ci | `atol=1e-7`, `rtol=0` |
| default share | `0.17683956520767094` |
| `replicate_results.csv` 80 rows, every column | `atol=1e-7` |
| `audit.json` `frame` | exact equality with R2.4 `national_R22` frame |
| included | 1,235,731 rows / 121,036,726 weight |
| `core_r24/results/national_R22/common_cohort_results.csv` | SHA-256 `6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7` |
| nowcast `GO_NOGO.json` | `NO-GO` |
| output path | must not be `core_r24/results/national_R22/` |

Hashes of the author outputs are in `ARTIFACT_LOCK.json`.

## What a PASS does not mean

Computational match ≠ scientific validation, ≠ permission to publish 17.7%, ≠ historically accurate non-fuel transport.
