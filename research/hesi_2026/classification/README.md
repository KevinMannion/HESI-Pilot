# Provisional five-tier classification (engineering)

**Status:** Not scientifically approved. **Not** national-headline eligible (`NATIONAL_HEADLINE_ENABLED` remains `False`).

## What works

- `classify_provisional_five_tier()` — six costs **H, F, T, M, K, O** plus disposable **D**; surplus **D−C**; ratio **R=D/C** when **C>0**.
- Fail-closed on missing, invalid, or unresolved costs (no imputed zeros).
- Optional tier labels (1–5) when caller supplies explicit `ProvisionalTierThresholds` (`policy_approved` must stay `False`).
- `classification/sensitivity.py` — household tier flips and **R=1** affordability-boundary crossings under assumption variants (no national weights or CIs).
- `components/other_essentials_interface.py` — **O** vector spec (apparel, personal care, housekeeping, telephone, internet) with Sprint 2E **unresolved** pricing.
- Optional pipeline flag: `cost_context.include_provisional_five_tier=True` (default **off**; does not affect canonical prototype hashes).

## Blocked (Sprint 2E owner decisions)

- BLS CE second-quintile residual for **O**
- Proposed home internet allowance
- CPI aging to 2026 for **O**
- Household-size scaling for **O**
- Scientific tier boundaries (use **test-only** thresholds in unit tests)

## Reproduce tests

```bash
cd research/hesi_2026
python3 -m unittest tests.test_provisional_five_tier tests.test_prototype_reproducibility -v
python3 -m unittest discover -s tests -p 'test_*.py'
```

With data bundle (source-backed scenarios):

```bash
export HESI_DATA_ROOT=/path/to/hesi-data
export HESI_SCRATCH_ROOT=/path/to/scratch
python3 -m unittest discover -s tests -p 'test_*.py'
```
