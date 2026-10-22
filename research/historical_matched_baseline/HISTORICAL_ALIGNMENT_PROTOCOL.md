# Historical alignment protocol — calendar 2024

This protocol is for object B: observed ACS 2024 money income versus **2024 modeled** costs. It does not replace Core R2.4 (object A: 2024 income versus September 2026 costs = 18.9918%). It does not use the September 2026 income nowcast (NO-GO).

## Clocks

| Series | Clock | 2024 use |
| --- | --- | --- |
| ACS 1-year PUMS income | Rolling past 12 months; interviews in calendar 2024; `HINCP × ADJINC / 1e6 / 12`; ADJINC 1.015250 | Observed income. Not a January, September, or December snapshot. January interviews are mostly 2023 income; December interviews are mostly 2024 income. |
| USDA Thrifty Food Plan | Calendar month of publication | **Default:** unweighted mean of the 12 published 2024 monthly mainland individual cells, then the locked household-size factors. **Alternate (point-in-time):** a named month (e.g. December 2024). Do not use 2026-09. |
| HUD FMR | Federal fiscal year (1 Oct–30 Sep), with mid-year revisions | See housing schedules below. Do not use FY2026. |
| EIA regular gasoline | Calendar year / month / week as published | **Default:** EIA published **annual** 2024 value of series `EMM_EPMR_PTE_NUS_DPG`. **Alternates:** mean of 12 monthly values; mean of weekly 2024 observations; December 2024 monthly; last weekly 2024. |

## Housing schedules (must be labeled)

Leap year 2024 has 366 days.

1. **Default annual-average (calendar 2024 day-weight)**
   - 2024-01-01 through 2024-03-10 (70 days): FY2024 original county FMR (effective 2023-10-01).
   - 2024-03-11 through 2024-09-30 (204 days): FY2024 revised county FMR (Honolulu revision, 89 FR 9169, effective 2024-03-11). For every county except Honolulu County these two files are identical.
   - 2024-10-01 through 2024-12-31 (92 days): FY2025 original county FMR (effective 2024-10-01).
   - FY2025 **revised** Federal Register notice (90 FR 14158) is **effective 2025-04-28**. HUD USER labels the corresponding county/SAFMR workbooks “Effective April 27, 2025”. That April 27/28 labeling difference is a documentation error if treated as a single date; **neither date falls inside calendar 2024**, so the default day-weight does **not** use FY2025 revised. Frozen results are unchanged. See ERRATA E14.

2. **Alternate fiscal-year table:** FY2024 revised for all 12 months (labeled; not a calendar-year mix).

3. **Alternate point-in-time from 1 Oct 2024:** FY2025 original only.

Replacement rent, 0–4 bedroom mapping `adults − min(partners,1) + ceil(children/2)`, infant exclusion, and `COMPLETE_UNAMBIGUOUS` PUMA filter stay as in R2.4. Year-T geography may change the included weight. **Do not recode FIPS or force 121,036,726 households.**

## Transport

Mechanical formula held: 12,000 miles / 32 mpg × gasoline + non-fuel dollars. Only gasoline has a hashed 2024 EIA observation. Non-fuel dollars remain the R2.4 remainder $5,631.67 and are **not** 2024 insurance, depreciation, maintenance, or registration. See `TRANSPORT_LIMITATIONS.md`.

## What this is not

- Not “calendar-2024 cash-flow hardship.”
- Not a September 2026 hardship rate.
- Not a nowcast of 2026 income.
- Not observed rent, groceries, or vehicle outlays.
