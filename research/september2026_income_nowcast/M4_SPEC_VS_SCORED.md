# M4: declared gate text vs scored implementation

Do not rewrite `VALIDATION_GATES.json` or Phase 3/4 numeric reports.

## Three objects

1. **Gate-file M4** (`VALIDATION_GATES.json` `models.M4_source_specific`): WAGP>0 × CES AWE; SSP/SSIP × January COLA; **SEMP × BEA proprietors**; **INTP × BEA interest+dividends**; RETP/PAP/OIP/residual frozen.
2. **Phase 3 scored M4** (`src/run_phase3_validation.py` `apply_models`): WAGP>0 × CES AWE; SSP/SSIP × COLA; **SEMP and INTP frozen** because BEA Table 2.6 had not been acquired. Comment in code: “BEA proprietors/interest not acquired.”
3. **Phase 4 M5 experiment**: applies BEA SEMP+INTP factors after NipaDataM.txt was acquired. **Not** scored as a retroactive replacement of M4. G3 still fails (share error 0.611 pp on 2023→2024).

`INCOME_FACTOR_METHODOLOGY.md` describes object 2 (the scored fallback). The gate file describes object 1 (the intended production specification). G1 failed because object 1’s BEA series were missing at Phase 3 scoring.

## Status language

Say: “Phase 3 M4 is the AWE+COLA implementation with non-wage sources frozen; it is not the full BEA M4 written in the gate file. Phase 4 M5 tested the BEA terms and still did not pass locked G3.”

Do not say: “M4 included BEA non-wage factors in the published backtest.”
