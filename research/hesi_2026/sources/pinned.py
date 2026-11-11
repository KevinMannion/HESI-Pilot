"""Pinned repository inputs for empirical component calculations (hash-verified)."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class PinnedSource:
    key: str
    rel_path: str
    sha256: str
    source_vintage: str
    geographic_applicability: str

    @property
    def path(self) -> Path:
        return REPO / self.rel_path

    def verify(self) -> None:
        if not self.path.is_file():
            raise FileNotFoundError(self.path)
        got = hashlib.sha256(self.path.read_bytes()).hexdigest()
        if got != self.sha256:
            raise ValueError(f"PINNED HASH MISMATCH {self.key}: {got} != {self.sha256}")


PINNED_SOURCES: dict[str, PinnedSource] = {
    "usda_prices_source_2024_2026": PinnedSource(
        key="usda_prices_source_2024_2026",
        rel_path="core_r24/inputs/source_2024_2026.csv",
        sha256="90bc39d1a569073b9530ca0a78a4ccf19c781c4a42dd70c51a0bed9e1907602c",
        source_vintage="USDA_monthly_Mainland_2026-09_Thrifty_via_source_2024_2026_csv",
        geographic_applicability="mainland_us_reference_not_ak_hi_individualized",
    ),
    "puma_fmr_screened_fy2026": PinnedSource(
        key="puma_fmr_screened_fy2026",
        rel_path="core_r24/inputs/puma_fmr_screened.csv",
        sha256="210a7ec6ae756ca8034cf3b7bff8afb3480d53186834cc7b304b913445f2a3ee",
        source_vintage="HUD_FY2026_revised_PUMA_occupancy_weighted",
        geographic_applicability="complete_unambiguous_pumas_only",
    ),
    "transport_reference_2026_09": PinnedSource(
        key="transport_reference_2026_09",
        rel_path="core_r24/inputs/transport_reference_2026_09.csv",
        sha256="19cc412e1d13662782ee57315f148f0a2187e1fd1613052c3aebd3397a687af6",
        source_vintage="EIA_Sept2026_gasoline_plus_hypothetical_nonfuel_12000mi_scenario",
        geographic_applicability="national_single_scenario_not_household_drawn",
    ),
    "synthetic_geography_fixture": PinnedSource(
        key="synthetic_geography_fixture",
        rel_path="core_r24/fixtures/synthetic_geography.csv",
        sha256="5c711e0dc6ccde795b283fc9ba6ee2bd3fb8c788af42f2b32e728bda977d1b54",
        source_vintage="synthetic_fixture_not_production",
        geographic_applicability="test_fixture_single_puma",
    ),
    "cms2026_marketplace_rates_sample": PinnedSource(
        key="cms2026_marketplace_rates_sample",
        rel_path="research/hesi_2026/fixtures/cms2026_marketplace_rates_sample.csv",
        sha256="84a9f1bd42ec6482ebc9c98a911917d72f738ca8252ed7137116de8205bc2a58",
        source_vintage="CMS_QHP_rate_extract_2026_sample_not_full_puf",
        geographic_applicability="sample_rating_areas_only",
    ),
    "cms2026_rate_puf_bounded_al_ra1": PinnedSource(
        key="cms2026_rate_puf_bounded_al_ra1",
        rel_path="research/hesi_2026/fixtures/inputs/cms2026_rate_puf_bounded_al_ra1.csv",
        sha256="9e028b54ced124b7d9bbdde9de14a129a132b437a41e0947242ae382f4640efe",
        source_vintage="CMS_2026_rate_puf_AL_Rating_Area_1_bounded_extract",
        geographic_applicability="alabama_rating_area_1_only",
    ),
    "puma_to_marketplace_rating_area_sample": PinnedSource(
        key="puma_to_marketplace_rating_area_sample",
        rel_path="research/hesi_2026/fixtures/puma_to_marketplace_rating_area_sample.csv",
        sha256="a92e8cd55329d470407fa39b2ffa3880b0d6f8c280dc591399cc19c93fea741f",
        source_vintage="ACS_PUMA_to_marketplace_rating_area_sample_crosswalk",
        geographic_applicability="sample_pumas_only",
    ),
    "puma_to_marketplace_rating_area_bounded_2026": PinnedSource(
        key="puma_to_marketplace_rating_area_bounded_2026",
        rel_path="research/hesi_2026/fixtures/puma_to_marketplace_rating_area_bounded_2026.csv",
        sha256="3eff2e8ecede77485e1b4735d444872c2f9681055938faca788366533bf0f6a5",
        source_vintage="ACS_PUMA_to_CMS_rating_area_bounded_2026",
        geographic_applicability="three_al_pumas_rating_area_1",
    ),
    "childcare_market_rates_sample": PinnedSource(
        key="childcare_market_rates_sample",
        rel_path="research/hesi_2026/fixtures/childcare_market_rates_sample.csv",
        sha256="904df49471acafe0fdeb55cd5e10bd36ea99f68f461c892fea5d8ca2a1e01308",
        source_vintage="CCDF_market_rate_research_fixture_2026",
        geographic_applicability="state_tables_sample_only",
    ),
    "ces_other_necessities_baseline_sample": PinnedSource(
        key="ces_other_necessities_baseline_sample",
        rel_path="research/hesi_2026/fixtures/ces_other_necessities_baseline_sample.csv",
        sha256="f37f33c5a6a2e088b8358b9c057f17071e1fa52ea1db4fa3ef17ec37515073cc",
        source_vintage="CES_residual_bundle_research_fixture_2026",
        geographic_applicability="national_index_fixture",
    ),
}


def verify_all_pins() -> dict[str, str]:
    out = {}
    for key, src in PINNED_SOURCES.items():
        src.verify()
        out[key] = src.sha256
    return out
