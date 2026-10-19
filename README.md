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
5. Data source ZIPs remain with the user; this release does not redistribute protected or large microdata files.

## Run

Place `csv_hus.zip`, `HESI_Person_Part_1.zip`, and `HESI_Person_Part_2.zip` at the paths defined in `run.py`, then execute `python run.py`. The script processes large microdata volumes and generates `results.csv` along with a cryptographic `manifest.json` file.
