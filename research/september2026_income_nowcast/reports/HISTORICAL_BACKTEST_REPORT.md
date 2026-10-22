# Historical backtest report (Phase 3)

Universe: occupied ACS 1-year PUMS (TYPEHUGQ==1, NP>0, WGTP>0). Not the R2.4 eligibility frame. Diagnostic cost frozen at $2,894.91/month. **Not 18.9918%.**

Factors: BLS Public API current vintage (sha `bb68500e…`). BEA SEMP/INTP factors absent → frozen in M4. Simulated forecast date 31 January of T+2; ALFRED first-print not acquired.

| Transition | Model | HINCP % error | WAGP % error | SSP % error | Diagnostic share error (pp) |
| --- | --- | ---: | ---: | ---: | ---: |
| 2022→2023 | M1 freeze | −3.207 | −3.884 | −5.541 | +1.245 |
| 2022→2023 | M2 uniform CPI (control) | +0.777 | +0.073 | −1.653 | +0.472 |
| 2022→2023 | M3 aggregate AHE on WAGP>0 | +0.004 | +0.399 | −5.541 | +0.616 |
| 2022→2023 | M4 source-specific AWE+COLA | +0.238 | −0.085 | +2.677 | +0.322 |
| 2023→2024 | M1 freeze | −4.491 | −3.956 | −6.903 | +1.313 |
| 2023→2024 | M2 uniform CPI (control) | −1.674 | −1.124 | −4.157 | +0.715 |
| 2023→2024 | M3 aggregate AHE on WAGP>0 | −1.597 | −0.075 | −6.903 | +0.857 |
| 2023→2024 | M4 source-specific AWE+COLA | −1.646 | −0.437 | −3.924 | +0.668 |

M4 2022→2023 diagnostic share 0.22212 (SDR SE 0.00060) vs actual 0.21890 (SE 0.00052). Share error 0.32 pp ≫ sampling SE; the remainder is model/composition error, stored separately.

M4 2023→2024 share 0.21245 (SE 0.00052) vs actual 0.20578 (SE 0.00048); error 0.67 pp.

M3 is slightly better than M4 on 2023→2024 mean income and almost exact on 2022→2023 mean. M4 is better on diagnostic share both years. Neither passes the predeclared G2+G3 pair. M2 is not eligible for production.

Full machine output: `INCOME_NOWCAST_VALIDATION_REPORT.json` (also under `$HESI_OPERATOR_HOME/HESI-R25-CleanRepro/income_nowcast/phase3/`).
