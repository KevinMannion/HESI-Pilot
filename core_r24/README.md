# HESI Core R2.4 — Rebuilt from original Census microdata

## VERIFIED EXECUTION (October 21, 2026)

This code release repairs the disconnected person caches. We processed **both original 2024 ACS person PUMS ZIPs (3,422,888 records)** using `rebuild_raw_person_caches.py`, computed the household result using the original 2024 housing ZIP, and compared output against prior R2.2 reference CSVs. All headline metrics matched to floating-point precision, **all 80 replicate rows/columns matched**, and the eligible household/exclusion cascade matched exactly. This is an author-run raw-source-to-result replication, **not independently verified by an external researcher**. The 2024 PUMS files are original user-provided archives and are not redistributed in this smaller code package.

## Original input data: precise names and SHA-256

| Original file | Purpose | SHA-256 |
|---|---|---|
| `csv_hus (2).zip` | ACS2024 housing ZIP | `8281008e53de98f0ef81e7a2ee5a8725991dda1ecfd2713ead73246425e515d0` |
| `HESI_Person_Part_1(1).zip` | ACS2024 person a | `05a4bdcb84fa8af1f3cc3034d9776a0a96e4311907fbb497298ff31bd445e6d8` |
| `HESI_Person_Part_2(1).zip` | ACS2024 person b | `2a891e40a44dec1374b9885926e20bc275c5ee93d6a55a12d0386893d091712c` |
| `inputs/puma_fmr_screened.csv` | HUD/PUMA geography and modeled rent | `210a7ec6ae756ca8034cf3b7bff8afb3480d53186834cc7b304b913445f2a3ee` |
| `inputs/source_2024_2026.csv` | Correct raw USDA table schema | `90bc39d1a569073b9530ca0a78a4ccf19c781c4a42dd70c51a0bed9e1907602c` |

IMPORTANT: The earlier `inputs/usda_september_2026.csv` has a different schema and cannot be passed directly to `food_model.load_prices`. This corrected pipeline explicitly uses `inputs/source_2024_2026.csv`.

## Clean-machine reproduction

Install Python 3.10+; `python -m pip install numpy pandas`. Unzip this code release and place the three original Census ZIPs anywhere on disk, then run:

```bash
python -m unittest discover -s tests -v
python reproduce_from_raw.py \
  --housing '/path/to/csv_hus (2).zip' \
  --person-a '/path/to/HESI_Person_Part_1(1).zip' \
  --person-b '/path/to/HESI_Person_Part_2(1).zip' \
  --output '/path/to/hesi_reproduced'
```

The command fails closed on incorrect SHA-256 source bytes, derives its own food and composition caches from the raw person archives (using resumable per-archive checkpoints), runs all three components on identical household IDs, compares means and standard errors, validates **every SDR replicate column**, checks population/exclusion counts, and writes `REPRODUCTION_REPORT.json` on PASS. It does *not* use the historical cached person files in the calculation.

For checking an already-produced result without rerunning everything:

```bash
python reproduce_from_raw.py --check-existing /path/to/hesi_reproduced/national
```

## Published scenario, not a validated national hardship rate

Reproduced included weighted households **121,036,726** out of 132,737,145 occupied; mean food **$653.522289/mo**, housing **$1,635.994098/mo**, provisional assumed one-car **$605.391667/mo**, combined **$2,894.908053/mo**; share of covered households whose **2024 gross household income** fell below **September 2026** modeled three-cost scenario = **18.9918%**, 90% ACS sampling-only interval [18.9028%,19.0808%]. No-car boundary case: 14.0322%. These are NOT matched-year hardship estimates. No childcare, healthcare, essentials or income-tax allowance is included. Replacement rent is applied to homeowners. Household exclusions and geographic/price uncertainties are documented in the saved audits. A separately validated national mobility adequacy standard is still absent.

## Research provenance limitation

The national reexecution is demonstrably tied to exact original Census input bytes. The PUMA-to-HUD mapping and curated USDA source were supplied by earlier HESI research and are preserved byte-identically; the *upstream construction* of the PUMA mapping from HUD raw source and geography is **not regenerated in this release**. Thus this is raw-ACS-to-joint-result reproducibility conditional on the published mapping and USDA table, not a certified independently reproduced full HUD/USDA extraction pipeline. The external reproducibility gate remains false until a separate party runs the code. Keep this distinction when citing.
