# Validation exposure register (r1)

**Designation:** `PRIOR_EXPOSURE_RESTRICTED_VALIDATION`  
**Policy:** `research/hesi_2026/audit/reserved_validation_policy.py`  
**Source trace:** `ASEC_2026_HISTORICAL_USAGE_TRACE_r1.txt` (inspected; no quarantined bytes opened for this register).

## Historical statistics examined (types only; values not repeated)

| Category | What was examined | Eligible for blind validation? |
|----------|-------------------|--------------------------------|
| ASEC 2026 PUF microdata (`asecpub26csv.zip` / `hhpub26.csv`) | National weighted household income **source means and shares** (HTOTVAL and listed source fields); frame row/weight counts | **No** — prior parse committed in Track D |
| Derived JSON (`ASEC_2026_HOUSEHOLD_SOURCE_TOTALS.json`) | Same national means/shares as microdata script output | **No** — derived national outcomes already in git record |
| Phase 3 validation (`run_phase3_validation.py` → `asec_independent_benchmark`) | ACS vs ASEC **national mean/share comparison** (explicitly not equated; not a gate input) | **No** for same estimands — `HISTORICAL_DESCRIPTIVE_BENCHMARK` |
| Official P60-289 / P60-286 published tables | **Median household money income** and related published aggregates quoted in METHOD, Data Scout findings, planning memos | **No** for those quoted aggregates |
| ASEC 2026 public-use dictionary PDF | Variable definitions / field inventory (possible read; hash on manifest only in trace) | Codebook use ≠ outcome validation; **outcome blind not restored** |
| Zip member / layout listings (`hhldfmt`, `persfmt`, header listings Nov 2026) | Structural metadata, member names, column names | Not outcome validation; prior exposure to field names |
| Income-source shares in Phase 4 restatement | Pension/annuity **national means** reused from totals JSON | **No** — same committed aggregates |

## Not examined in this implementation pass

- Quarantined directory contents (not entered).
- Any ACS 2025 holdout reserved under parallel rules.
- Statistics not listed in trace r1 (require **separate preregistered validation protocol** before use).

## Enforcement (local)

Official `hesi_2026` pipeline/prototype/data-root resolution and Track D loader/Phase3 `--asec` entry points call `reserved_validation_policy` **fail-closed**. Frozen reports and git history are unchanged.
