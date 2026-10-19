# HESI Food-Cost Integration Pilot — 2024

This release replaces arbitrary per-person food scenarios with published December 2024 **USDA Thrifty and Low-Cost Food Plan** estimates calibrated by individual age and sex. It applies USDA's official household-size adjustment to member costs and compares that annualized December 2024 food benchmark plus observed ACS rent/owner costs against gross ACS household income.

## Research Status — Pilot Results (v0.1)

The real-data pipeline successfully ingested all 3,422,888 person records, integrated official USDA food plans, and executed full 80-replicate-weight Successive Difference Replication (SDR) variance math across 1.32M unweighted households (representing 130.5M weighted households). Results are stored in `results.csv`. `run.py` is a candidate implementation, provided for peer review and methodological transparency.

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

1. Create a folder named `input_data` in the root directory.
2. Place `csv_hus.zip`, `HESI_Person_Part_1.zip`, and `HESI_Person_Part_2.zip` inside the `input_data/` folder.
3. Execute `python run.py`. 

The script processes large microdata volumes, applies official USDA food plans, computes 80-replicate-weight SDR variance, and generates `results.csv` alongside a cryptographic `manifest.json` file.

### Obtaining the Raw Data

HESI uses the **2024 American Community Survey (ACS) 1-Year Public Use Microdata Sample (PUMS)**, published by the U.S. Census Bureau.

Download the original files from the [Census Bureau's 2024 PUMS download page](https://www.census.gov/programs-surveys/acs/microdata/access/2024.html).

1. **Housing:** Download the nationwide housing CSV archive, `csv_hus.zip`.
2. **Persons:** Download the nationwide person CSV archive, `csv_pus.zip`.
3. **Organize inputs:** Create an `input_data/` directory in the repository root and place both ZIP files inside it. The script also supports the previously split archives, `HESI_Person_Part_1.zip` and `HESI_Person_Part_2.zip`, for backward compatibility. Splitting is no longer required.
4. **Verify integrity and reproducibility:** The repository's `manifest.json` records SHA-256 hashes from the original pilot run using split person archives. Running `run.py` with the original `csv_pus.zip` generates a new manifest containing hashes for the files used in that run. Different ZIP packaging can produce different hashes even when the underlying Census records are identical.

**Replication standard:** Researchers should verify the person-record counts, household matching, weighted household totals, and calculated estimates—including confidence intervals—against the published `results.csv`. Matching archive hashes alone is neither necessary nor sufficient to establish numerical replication.
