# Healthcare benchmark methodology audit (2026 bounded validation)

**Status:** research / bounded demonstration — **not** nationally approved.

## Benchmark definition

The essential-cost healthcare component uses the **Marketplace second-lowest-cost silver plan (SLCSP)** gross premium for an **unsubsidized** household:

1. Restrict to **silver** QHP rows with **no CSR plan variant** (CMS PUF: `Standard Silver On Exchange Plan` only in the bounded extract).
2. For each eligible silver plan in the household's **rating area**, compute **one household premium** as the sum of **age-specific `IndividualRate`** values for **all covered members on that same plan** (CMS non-tobacco individual-rate curve; child ages map to PUF key `0-14`).
3. The benchmark monthly premium is the **second-lowest** household total across qualifying silver plans (lowest if only one plan qualifies).

### Explicit non-method (rejected)

**Do not** sum independent single-member SLCSP amounts where each member could be assigned a different silver plan. That pattern is retained only as `anti_pattern_sum_individual_slcsp_monthly_usd` for regression tests.

## Geographic and vintage

| Input | Vintage | Coverage |
|-------|---------|----------|
| `cms2026_rate_puf_bounded_al_ra1.csv` | CMS **BusinessYear 2026** rate PUF extract | AL **Rating Area 1** (80 rows) |
| `puma_to_marketplace_rating_area_bounded_2026.csv` | Research crosswalk | PUMAs `0100100`, `0100200`, `0100300` → Rating Area 1 |

Full national rate PUF is **not** pinned in-repo; extract via `tools/extract_cms_rates_bounded.py` from local CMS zips.

## Household coverage assumptions (current code)

- All listed `members[].age` persons are treated as Marketplace-covered at gross premium.
- **No** employer-sponsored insurance offset.
- **No** Medicaid / Medicare eligibility screening.
- **No** advance premium tax credit (APTC) or cost-sharing reduction (CSR) applied.

## Age-rating assumptions

- **Non-tobacco** `IndividualRate` only (`Tobacco User/Non-Tobacco User` rows in source PUF).
- Ages **0–14** use PUF bucket `0-14`.

## Policy / release

`healthcare_policy_approved` remains **false** by default. `NATIONAL_HEADLINE_ENABLED` remains **false**.
