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
}


def verify_all_pins() -> dict[str, str]:
    out = {}
    for key, src in PINNED_SOURCES.items():
        src.verify()
        out[key] = src.sha256
    return out
