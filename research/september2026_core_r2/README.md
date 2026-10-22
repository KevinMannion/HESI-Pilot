# HESI September 2026 Core R2 — Three Pillars

**This is the authoritative consolidated September 2026 development distribution for Food, Housing, and Transportation.** R2 preserves existing working code and source files from Core R1 and Transportation v1.0 without changing their formulas; it adds a unified lock register, rerun tests, and source integrity inventory.

## Pillar scope and limitations

- **Food:** September 2026 USDA mainland model; all household members aged 1+. 2024 ACS sample is a *demographic reference*, not a survey of 2026 households. Infant prices, individualized Alaska/Hawaii costs and independent replication remain outstanding.
- **Housing:** revised FY2026 HUD gross FMR, September 2026 reference; one bedroom per adult except a verified cohabiting couple sharing one; two minors under 18 per bedroom; requirements above four bedrooms excluded. Results are an estimated *adequate replacement-rent* benchmark, not actual rents or guaranteed unit availability. The candidate $1,641.53/month mean covers 123,872,733 weighted households from 2024 ACS, not the entire current U.S. population. Geographic coverage, survey interval for chosen policy, and independent validation are still incomplete.
- **Transportation:** economical used compact reference, 12,000 miles/year and 32 MPG reference assumption; September 2026 national gasoline $4.35475/gallon. Annualized economic ownership equation excludes loan principal when depreciation is counted. Approximately $605.39/month is a **provisional scenario only**; several nonfuel cost inputs remain hypothetical, and the national household/transit assignment has not been executed.

## Scientific truth-in-labeling

All three **reference specifications are frozen for their stated scopes**. None is independently certified as a full nationwide September 2026 economic-security pillar. Do not add $672.45 food + $1,641.53 housing + $605.39 transport and label it a national HESI budget: food and housing estimates have different eligibility populations; transport is not a household-weighted national estimate. A joint three-pillar calculation requires matched household keys, common eligibility, explicit transit/vehicle assignment and reconciled ACS sampling uncertainty.

## How to verify

From this root: `python3 verify_release.py`. Dependencies: Python 3, NumPy, Pandas. Existing individual test scripts are retained under each pillar. The machine-readable `LOCK_REGISTER.json` is the release status authority. Source file checksums are in `INTEGRITY_MANIFEST.json`. `INTEGRATION_TEST_REPORT.json` gives results from the consolidation test run.

## GitHub

This package is a portable release artifact. It **has not been committed** to https://github.com/KevinMannion/HESI-Pilot. To integrate, commit the extracted source in a new tracked release directory and preserve the historical original pilot.
