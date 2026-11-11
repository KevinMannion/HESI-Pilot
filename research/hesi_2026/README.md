# HESI 2026 engineering framework (development)

Greenfield modules for household-universe accounting, six-component essential costs,
disposable resources, and versioned audit provenance. Does **not** replace or overwrite
frozen `core_r24/results/national_R22/` artifacts.

Synthetic-fixture tests demonstrate wiring only; they do **not** validate a national 2026 estimate.

## Reviewer prototype v0.1 (single synthetic household)

From repository root, after checkout of `dev/hesi-2026-framework`:

```bash
cd research/hesi_2026

# Full unit/integration suite (no HESI_DATA_ROOT required for core checks)
env -u HESI_DATA_ROOT -u HESI_SCRATCH_ROOT \
  python3 -m unittest discover -s tests -p 'test_*.py' -v

# Runnable reviewer demo — synthetic scenarios only
python3 demos/run_prototype_household.py \
  --scenario fixtures/prototype_scenarios/complete_provisional_al_family.json \
  --out /tmp/hesi_reviewer_run

# Inspect outputs: audit.json, canonical_calculation.json, PROTOTYPE_MANIFEST.json
```

Statuses: `COMPLETE_PROVISIONAL` (numeric six-vector + disposable, policies still provisional) or `PARTIAL_UNRESOLVED`. No approved economic-security classification is emitted (`NATIONAL_HEADLINE_ENABLED=False`).
