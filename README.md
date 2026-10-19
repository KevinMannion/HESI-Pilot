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

Download the original data from the [Census Bureau's 2024 PUMS download page](https://www.census.gov/programs-surveys/acs/microdata/access/2024.html).

1. **Housing:** Download the nationwide housing CSV archive, `csv_hus.zip`.
2. **Persons:** Download the nationwide person CSV archive, `csv_pus.zip`.
3. **Prepare person files:** The current `run.py` expects two ZIP archives:
   - `HESI_Person_Part_1.zip`, containing `psam_pusa.csv`.
   - `HESI_Person_Part_2.zip`, containing `psam_pusb.csv`.

   Extract these two CSV members from `csv_pus.zip` and package each into its own ZIP using the expected filename.

4. **Organize inputs:** Create an `input_data/` directory in the repository root and place the housing ZIP and both person ZIPs inside it.
5. **Verify integrity:** The SHA-256 hashes in `manifest.json` describe the exact ZIP archives used in the original analysis. Repackaging ZIPs may produce different archive hashes even when their underlying CSV contents are identical. Therefore, checksum mismatches for independently repackaged person files do not necessarily indicate different Census data.

**Important:** This release has not yet established independently reproducible canonical hashes for the extracted Census CSV members. Successful reproduction should include verification of record counts, household matches, weighted totals and published results—not merely matching ZIP hashes.
