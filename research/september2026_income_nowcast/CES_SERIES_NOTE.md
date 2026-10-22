# CES series used in the income-nowcast factors

Locked BLS Public API v1 series (see `factor_sources/BLS_ANNUAL_FACTORS.json`):

| ID | BLS title in the extract | Role |
| --- | --- | --- |
| CES0500000003 | Average hourly earnings, total private, SA | M3 AHE |
| CES0500000011 | Average weekly earnings, total private, SA | Scored M4 wage factor |
| CES0500000007 | Average weekly hours, total private, SA | Stored; not multiplied into M4 |
| CES0500000001 | All employees, total private, SA | Stored; extensive margin **not** applied |

These are **all-employee, seasonally adjusted** CES series, not production-and-nonsupervisory earnings (e.g. CES0500000008) and not NSA.

M4 documentation that says “AWE (rate × hours)” is a **verbal motivation**. The scored factor is the **published AWE series ratio**, not the product of annual-mean AHE and annual-mean hours. Those two ratios differ (2023→2024 constructed AHE×hours vs published AWE). Using hours separately to reconstruct AWE would be a different model.
