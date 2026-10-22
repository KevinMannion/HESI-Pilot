# Model sensitivity vs sampling uncertainty — 2024 matched-year

The 90% intervals on `common_cohort_results.csv` are **ACS successive-difference replicate (SDR) sampling intervals only**. They hold costs and model constants fixed.

## Inherited 2026 non-fuel transportation (not in the SDR interval)

R2.4 one-car total $7,264.70/year = September 2026 fuel $1,633.03 + remainder **$5,631.67**.

2024 matched-year default:

- Gasoline: EIA `EMM_EPMR_PTE_NUS_DPG` published annual 2024 **$3.304/gal** (hashed).
- Fuel: 12,000 miles / 32 mpg × 3.304 = **$1,239.00/year**.
- Remainder: **held at $5,631.67** (depreciation, insurance, maintenance, registration, financing). These dollars are the R2.4 hypothetical remainder, **not** 2024 prices.
- Labeled total: **$6,870.67/year** = $572.555833/month.

Transport `se_sdr` is ~1e-10 because every included household is assigned the same constant. That is **not** evidence that transport is measured precisely. It is evidence that the assignment does not vary across households.

Do not call $6,870.67 a 2024 AAA/IRS/NHTS cost of driving.

## Sampling (inside the published interval)

80 ACS household replicate weights `WGTP1`–`WGTP80`, variance factor 4/80, reconstructed on this execution to machine precision for the default share (`se_sdr` 0.0005312962315728786).

Food and housing `se_sdr` are nonzero because those costs vary by household composition and PUMA.

## Model sensitivity (outside the published interval)

| Lever | Default | Alternate on this execution | Share |
| --- | --- | --- | ---: |
| Housing clock | Calendar-2024 day-weight 70/204/92 | FY2024 revised only | 17.54959% |
| Housing clock | Calendar-2024 day-weight | FY2025 original from 2024-10-01 | 18.12042% |
| Transport | One car $6,870.67 | No car (food+housing only) | 13.05558% |
| Non-fuel dollars | $5,631.67 held | Not historically re-priced | n/a |

These alternatives are **not** folded into the 17.5966%–17.7714% sampling interval.
