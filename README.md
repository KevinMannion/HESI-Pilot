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
