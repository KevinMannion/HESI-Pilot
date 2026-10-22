# HESI Housing — September 2026 controlled normative standard v1.0

## Lock decision: DEFINED-SCOPE SPECIFICATION LOCKED; NATIONAL SCIENTIFIC APPROVAL PENDING

### What the benchmark measures
The modeled cost of obtaining **adequate rental housing** in a local HUD rental market in September 2026; it is **not** the rent a household actually pays, a guarantee of availability, a mortgage cost, or an independently established minimum level of housing quality.

### Locked policy and price rules
* Prices: HUD's **revised FY2026 FMR schedule applicable September 2026** (effective May 21, 2026). Do not substitute FY2027 rents or 2024 observed rents. Standard HUD FMR is gross rent including utilities; prohibit generic additional utility allowance.
* Adults **age >=18**: one bedroom per adult, except a **verified couple** shares one bedroom. Every identified couple subtracts one from individual adult bedrooms. Each adult can belong to at most one identified couple.
* Children **age <18**: maximum two children per bedroom regardless of sex. Count ceil(children/2). Age 18 transitions to an adult room.
* Formula for a household with at least one adult: `B = adults - distinct_identified_couples + ceil(children_under_18/2)`.
* No fixed child-sex separation and no forced sharing of rooms between unrelated adults.
* Only bedrooms **1–4** in this population output. Households requiring 5+ bedrooms are **excluded and tabulated**, never capped at 4 or assigned invented prices.
* Disability, medical and accessibility accommodation needs are not identifiable for all ACS households; model reports this limitation and does not falsely assume a household never needs more room.
* Partner/couple identification: the executed national research model confirms only spouse/partner of the household reference person; it **cannot certify all couples within complex households**. The normative formula is locked but practical person coding is a residual measurement uncertainty.
* PUMA geographic expected values use occupied-housing-unit-based weights and FY2026 HUD area rents; these represent **area-weighted estimates**, not the specific location of an ACS household. Never silently impute blocked areas. Correct SAFMR applicability remains a separate policy check.

### Verified national execution (historical cohort priced at September 2026 levels)
The earlier September 2026 execution used **2024 ACS household compositions** and the geographically screened PUMA-level cost model:

* Canonical occupied ACS frame: **132,737,145 weighted** households / 1,348,408 unweighted.
* HESI chosen bedroom policy, *its own supported cohort*: **123,872,733 weighted** households (**93.3218%**) and a mean **$1,641.533003 per month**. This is the appropriate *candidate baseline* if publishing the baseline rule's own eligible cohort, still requiring its own sampling-uncertainty computation.
* Precisely *matched-population* three-way sensitivity cohort: **123,297,823 weighted** households (92.8887%) and **$1,636.794844 per month** for the chosen policy, versus **$1,550.886873** for two-persons-per-room and **$1,661.399304** for children grouped by sex. The $1,636.79 figure is a **comparison-cohort result, not the stand-alone chosen-policy baseline**.
* Seven compositional anomalies rejected in the screened sample; exclusions include geographic ambiguity and >4-bedroom need. Full, mutually exclusive weighted exclusion accounting by specific reason is not yet published.

These are *reference-price research estimates*, not observed September 2026 household expenditures or directly observed September 2026 demographic composition. The historical ACS dataset also introduces geographic and population-vintage limitations.

### Acceptance gates
| Gate | Decision |
|---|---|
| September 2026 HUD source and formula | PASS — locked exact-area lookup |
| Explicit normative bedroom definition and boundary tests | PASS — user-adopted policy, not HUD's universal rule |
| Full national composition execution and canonical denominator checks | PASS |
| Own-eligible cohort candidate estimate | COMPUTED, conditional |
| New scenario's 80-replicate ACS sampling CI | PENDING |
| Matched geography and final exclusion audit | PARTIAL; unresolved HUD / Connecticut and PUMA cases |
| Independent rent/bedroom validation and geography-model sensitivity | PENDING |
| Scientifically approved national index statistic | NOT YET |

**Locked** here means a versioned policy and computational standard with its scope and exceptions frozen. It does **not** assert the empirical mean is externally validated or nationally complete. Reviewers can recommend changing a normative housing standard, but any change requires a named new version and quantified effect; existing versions must remain reproducible.

### Verify
From the extracted folder: `python3 verify.py` and `python3 -m unittest -v test_adequacy test_reference`. The reference tests need `pandas`. Dataset table and identifiers are included. New scenarios' replicate-weight uncertainty is not claimed, since it has not been run.

### Release repository status
This ZIP is a proposed integration artifact; it has **not been committed to github.com/KevinMannion/HESI-Pilot**. The GitHub pilot independently measures reported housing expenditures, and should remain as the historical series alongside this replacement-cost standard.
