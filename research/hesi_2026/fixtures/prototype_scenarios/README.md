# Reviewer prototype scenarios (v0.1)

## Geography notes

- **`source_backed_al_family_2026.json`** uses Census **2020 PUMA `0101403`** (Birmingham City, Jefferson County) for HUD FMR and CMS crosswalk, and **county FIPS `01073`** for NDCP P4-C01 childcare. See `al_puma_0101403_jefferson_county_01073_mapping.json`.

- **`complete_provisional_al_family.json`** retains legacy PUMA **`0100100`** to preserve **`canonical_hashes_v0.1.json`** golden reproducibility. Under the 2020 PUMA vintage, `0100100` is **not** Jefferson County, Alabama. Do **not** treat that scenario as a geographically validated household example; use `source_backed_al_family_2026.json` for Jefferson-aligned integration review.
