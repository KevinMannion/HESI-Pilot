# HESI Science v5.2 — September 2026 Food, current-price primary

**Primary measurement date: September 2026.** All current food calculations use the published USDA September 2026 mainland monthly costs. Never represent this as an annual 2026 observation. Historical 2024 ACS households can be used as the demographic reference **only when prominently labeled**. Their age distribution, weights, and household structure are not measured in September 2026.

## Run

`python current_food.py`

`python -m unittest -v test_current_food.py`

All 60 prices in `usda_september_2026.csv` are imported from the seven previously supplied USDA workbooks via the audited HESI v4.8 monthly archive. Refer to the original September 2026 USDA Thrifty and Other Plans PDFs for primary verification. Each row contains the plan, original USDA age/sex group, and monthly price. The age 19 boundary differs between Thrifty and the other plans. All reported costs are modeled home-prepared food budgets, **not observed household spending or a complete measure of food security**.

## Executed cross-checks

- National reference family (adult male 20–50, adult female 20–50, child 6–8, child 9–11): Thrifty $1,023.90 from rounded group costs, versus published $1,024.00 (rounding).
- Low-Cost $1,126.90; Moderate-Cost $1,389.20; Liberal $1,681.80 from household age-specific component schedules.
- `national_sdr_2026_reference.csv` contains the **previously executed** 2024 ACS survey-weighted September 2026 scenario estimates and 90% sampling intervals, **not new 2026 sampling data**. Only eligible age 1+ households were included, and mainland rates were applied nationally.
- `geography_sensitivity_2026.csv` reproduces previous v5.1 hypothetical regional-ratio sensitivity; do not call these individualized Alaska/Hawaii observed food costs.

## Scientific boundaries and acceptance

**Approved for controlled September 2026 mainland scenario use** for all household members aged one or above. Not approved as a complete national food adequacy standard. Infant feeding pathway is unobserved by ACS; do not substitute zero or age-one as a verified cost. Separate Anchorage/Hawaii reference-family costs cannot be used uncritically for all household compositions. Regional food availability and household food access require further evidence; USDA's meal-at-home basket is a monetary standard, not directly observed nutrition or financial hardship. Source publication-vintage provenance and independent replication remain requirements of final freeze.

## Next: September 2026 housing science

Use **2026 market rent benchmarks** and a separate current-occupancy housing-cost lens. Specify bedroom adequacy, utilities, rent geography/crosswalk, and ownership costs before coding an economic-security classification. Match 2024 ACS households to 2026 prices only as labeled *2026 costs on 2024 composition*. Establish source-vintage and 2026 publication checks for FY2026 HUD FMR, and compare ACS observed rents to modeled replacement housing costs without treating them as equivalent. No housing source input is yet included in this release.
