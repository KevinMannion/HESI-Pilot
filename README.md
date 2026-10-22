# HESI Pilot — research development branch (`hesi/core-r25-integration`)

The Household Economic Security Index (HESI) is a **research** program. This branch publishes Core R2.5 development so reviewers can read the methods, code, tests, and status flags. **Pushing this branch is not scientific validation.**

The older public 2024 food-plus-observed-housing pilot remains on `main`. Do not merge this branch into `main` unless a separate review says to.

## Scientific status (this branch)

| Flag | Value |
| --- | --- |
| COMPUTATIONALLY_REPRODUCED | **YES**, for the specified Core R2.4 calculations on this operator’s clean environment |
| EXTERNALLY_INDEPENDENTLY_REPRODUCED | **NO** |
| SCIENTIFICALLY_VALIDATED | **NO** |
| SEPTEMBER_2026_INCOME_NOWCAST | **NO-GO** |

A GitHub copy does not change those flags.

## Do not mix these numbers

| Object | Housing | Food | Transport | Income | Eligible weighted HH | Share |
| --- | --- | --- | --- | --- | --- | --- |
| 2024 observed-housing pilot (`run.py`, `results.csv`) | ACS GRNTP / SMOCP | December 2024 USDA | none | 2024 ACS | 130,550,444 | 10.301% Thrifty |
| Core R2.4 three-pillar scenario (`core_r24/`) | FY2026 HUD FMR replacement rent | September 2026 Thrifty | one-car $7,264.70/year | 2024 ACS | 121,036,726 | **18.9918%** |
| September 2026 income nowcast | — | — | — | experimental | — | **not computed (NO-GO)** |
| 2024 matched-year three-component scenario (`research/historical_matched_baseline/`) | 2024 HUD calendar day-weight | 2024 Thrifty annual mean | 2024 EIA gasoline + **inherited hypothetical non-fuel $5,631.67**; one car per eligible HH | 2024 ACS observed | 121,036,726 | **17.6839565% (about 17.7%) — PROVISIONAL; NOT approved for formal publication; NOT SCIENTIFICALLY VALIDATED** |

18.9918% is a **cross-vintage modeled scenario** (2026 costs / 2024 gross income). It is not a measured September 2026 hardship rate.

Frozen R2.4 files (do not edit): `core_r24/results/national_R22/`. SHA-256 of `common_cohort_results.csv`: `6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7`. Computational share `0.18991790144753254`. For public prose, report **about 19.0%** (90% ACS sampling-only interval about 18.9% to 19.1%). One-car assignment is provisional; the **no-car sensitivity** on the same households is in `core_r24/results/rebuilt_from_raw/common_cohort_results.csv` (`0.14032179786488938`, **about 14.0%**). The frozen `national_R22` table does not include that row. See `ERRATA.txt` E5.

Dated methods errata: `ERRATA.txt`. Official Census `csv_pus.zip` is accepted only after **inner CSV** SHA-256 verification (`core_r24/PUMS_ARCHIVE_LOCK.json`).

## What is in this branch

1. **2024 observed-housing food pilot** (repository root; also on `main`).
2. **Core R2.4 joint engine** — `core_r24/reproduce_from_raw.py` → person-cache rebuild → `core_r24/src/run_joint.py`. Locked Food / Housing / Transportation specs: `research/september2026_core_r2/`.
3. **Income-nowcast research (Phases 1–4)** — `research/september2026_income_nowcast/`. Locked gates **fail**. Decision **NO-GO**. No September 2026 national adequacy estimate.
4. **Matched-year 2024 national engine** — `research/historical_matched_baseline/`. **PROVISIONAL — NOT approved for formal publication — NOT SCIENTIFICALLY VALIDATED.** Computational share `0.17683956520767094` (**17.6839565%**; about **17.7%**). Observed ACS 2024 income vs modeled 2024 USDA food, HUD housing, EIA gasoline, and inherited non-fuel transport. Sampling intervals are ACS SDR only; housing-year and no-car alternatives are model sensitivity. External computational reproduction is **pending**. Reproduction: `results/matched2024_provisional/REPRODUCER_HANDOFF.md`. This is **not** a measured national hardship rate. GitHub presence of these files is not publication approval (`research/GOVERNANCE_CORRECTION_2026-10-22.txt`).

Iteration history: `STATUS.txt`, `ITERATION_NOTES.txt`, `ITERATION_REGISTER.txt`.

## Three-pillar reference calculation (R2.4)

On a common 2024 ACS occupied-household frame, after geography, composition, >4-bedroom, and infant exclusions:

- Food: USDA Thrifty, September 2026 mainland individual cells, USDA household-size factors.
- Housing: HUD FY2026 revised FMR, occupancy-weighted to 2020 PUMAs, bedroom rule `adults − min(partners,1) + ceil(children/2)`, 1–4 BR only.
- Transport: one assumed 12,000-mile / 32 mpg vehicle; September 2026 EIA gasoline plus **hypothetical** non-fuel dollars.
- Income: `HINCP × ADJINC / 1e6 / 12` (rolling past-12-months ACS money income, not a September snapshot).

Sampling uncertainty uses 80 ACS successive-difference replicates (4/80). That interval is **not** model, price, or geography uncertainty.

## Income-modeling research

See `research/september2026_income_nowcast/README.md` and `reports/GO_NOGO.json`.

- 2024 ACS source identity on the R2.4 frame was reconstructed.
- Historical backtests (M1–M6) vs locked gates: **G2 and G3 fail** on 2023→2024.
- BEA monthly NIPA through **2026-08** only; September 2026 household run-rate is not identifiable from those files.
- **Do not** apply a uniform CPI factor to `HINCP`. **Do not** treat CES wage growth as household-income growth.

## Limitations (all tracks)

- Not a six-pillar HESI (no childcare, health care, taxes, residual essentials, or assets).
- Replacement rent is assigned to owners; it is not observed housing cost.
- One car is assigned to every included household.
- Mainland USDA prices are used nationally, including Alaska and Hawaii.
- Infants and households needing more than four bedrooms are excluded.
- Nowcast remains NO-GO. The 17.6839565% matched-year figure is provisional computational output only and is **not approved for formal publication**.
- Operator local paths appear in some already-recorded reproduction logs. Those logs locate files on one machine; they are not Census microdata.

## Third-party sources

Census ACS PUMS, HUD FMR, USDA Food Plans, EIA gasoline, BLS, BEA, and SSA COLA are U.S. government publications. This repository **does not** redistribute raw ACS microdata or the original HUD/USDA/EIA workbooks. Derived small CSV extracts and SHA-256 manifests are included so reviewers can check tables against official files they download themselves.

Code and original HESI documentation in this repository are copyright Kevin Mannion (see `LICENSE`). Government source data remain public U.S. government works.

## Reproducibility (R2.4)

Census microdata are **not** in git. Download 2024 ACS 1-year PUMS housing and person archives from the [Census PUMS page](https://www.census.gov/programs-surveys/acs/microdata/access/2024.html). Required SHA-256 values are in `core_r24/README.md` and `STATUS.txt`.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python core_r24/verify_package.py          # packaged hashes + synthetic tests
# National run (large; writes caches outside git):
python core_r24/reproduce_from_raw.py \
  --housing /path/to/csv_hus.zip \
  --person-a /path/to/person_part_1.zip \
  --person-b /path/to/person_part_2.zip \
  --output /path/to/empty_output_dir
```

Matching `national_R22` within `atol=1e-7` is computational reproduction of the published scenario. It is not independent external replication and not scientific validation.

### 2024 observed-housing pilot

Create `input_data/`, place `csv_hus.zip` and `csv_pus.zip` there, then `python run.py`. See the household audit below.

---

# HESI Food-Cost Integration Pilot — 2024

This release replaces arbitrary per-person food scenarios with published December 2024 **USDA Thrifty and Low-Cost Food Plan** estimates calibrated by individual age and sex. It applies USDA's official household-size adjustment to member costs and compares that annualized December 2024 food benchmark plus observed ACS rent/owner costs against gross ACS household income.

## Research Status — Pilot Results (v0.1)

The real-data pipeline successfully ingested all 3,422,888 person records, integrated official USDA food plans, and executed full 80-replicate-weight Successive Difference Replication (SDR) variance math across 1.32M unweighted households (representing 130.5M weighted households). Results are stored in `results.csv`. `run.py` is a candidate implementation, provided for peer review and methodological transparency.

## National Replication and Household Audit — October 2026

The updated 2024 ACS PUMS pipeline was executed against the original nationwide Census person and housing archives. All six published estimates in `results.csv`, including weighted household counts and 95% confidence interval bounds, reproduced exactly when compared with the previously published CSV.

The automated test suite also passed all five tests, including USDA food-cost checks and synthetic end-to-end pipeline tests.

### Household Accounting

| Audit measure | Unweighted records |
|---|---:|
| Person records processed | 3,422,888 |
| Housing records processed | 1,631,969 |
| Occupied households with positive person counts | 1,531,614 |
| Successfully matched occupied households | 1,531,614 |
| Unmatched occupied households | 0 |
| Person-count mismatches | 0 |
| Nonoccupied or zero-person housing records excluded | 100,355 |
| Unsupported-tenure records excluded | 206,820 |
| Other recorded exclusions | 0 |
| **Eligible households analyzed** | **1,324,794** |

The final eligible sample represents **130,550,444 weighted households**.

The reported percentages refer to this eligible analytical population, not every household in the United States. Unsupported tenure includes housing records outside the owner's and cash-renter tenure codes accepted by the pilot. The exclusion categories are assigned according to the pipeline's ordered filtering rules.

The full audit is published in `audit.json`, and source archive fingerprints are recorded in `manifest.json`.

These findings establish reproducibility of the implemented pilot calculations, but do not constitute independent external validation of the economic assumptions or a complete household economic stress index.

## USDA Source and Frozen Inputs

* Thrifty Food Plan, December 2024: https://fns-prod.azureedge.us/sites/default/files/resource-files/Cost_Of_Food_Thrifty_Food_Plan_December_2024.pdf
* Low-Cost Food Plan, December 2024: https://fns-prod.azureedge.us/sites/default/files/resource-files/Cost_Of_Food_Low_Moderate_Liberal_Food_Plans_December_2024.pdf
* Size multipliers: 1 person 1.20, 2 people 1.10, 3 people 1.05, 4 people 1.00, 5–6 people 0.95, 7+ 0.90.

## Important Caveats

1. USDA's December 2024 food prices are **not 2024 annual-average prices**. Applying them against annual 2024 incomes is a late-2024 illustrative snapshot, not a valid full-year deprivation statistic.
2. All meals/snacks are assumed prepared at home. The age-1 rate is provisionally assigned to 0-year-olds; this must be sensitivity-tested.
3. ACS housing expenses and incomes are observational household variables; food is a modeled allowance. Taxes, childcare, health care, transport, emergency savings, and assets are omitted.
4. 80 ACS housing replicate weights estimate sampling uncertainty conditional on model assumptions, not uncertainty in food costs.
5. The original Census PUMS microdata files are publicly available. This repository does not host the large source archives due to file size limits; researchers can download them directly from the U.S. Census Bureau.

## Run

1. Create an `input_data/` folder in the repository root.
2. Download `csv_hus.zip` and `csv_pus.zip` from the U.S. Census Bureau and place both files inside `input_data/`.
3. Install dependencies using `pip install -r requirements.txt`.
4. Execute `python run.py`.

The script also supports the previously split person ZIP archives for backward compatibility.

### Obtaining the Raw Data

HESI uses the **2024 American Community Survey (ACS) 1-Year Public Use Microdata Sample (PUMS)**, published by the U.S. Census Bureau.

Download the original files from the [Census Bureau's 2024 PUMS download page](https://www.census.gov/programs-surveys/acs/microdata/access/2024.html).

1. **Housing:** Download the nationwide housing CSV archive, `csv_hus.zip`.
2. **Persons:** Download the nationwide person CSV archive, `csv_pus.zip`.
3. **Organize inputs:** Create an `input_data/` directory in the repository root and place both ZIP files inside it. The script also supports the previously split archives, `HESI_Person_Part_1.zip` and `HESI_Person_Part_2.zip`, for backward compatibility. Splitting is no longer required.
4. **Verify integrity and reproducibility:** The repository's current `manifest.json` records SHA-256 hashes for the original Census `csv_pus.zip` and `csv_hus.zip` archives used in the October 2026 replication. Researchers using differently packaged archives should expect different file hashes and should compare the underlying record counts, audit results, estimates, and confidence intervals.

**Replication standard:** Researchers should verify the person-record counts, household matching, weighted household totals, and calculated estimates—including confidence intervals—against the published `results.csv`. Matching archive hashes alone is neither necessary nor sufficient to establish numerical replication.
