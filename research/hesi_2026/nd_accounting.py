"""Synthetic-only ND (no double-count) guards for subsidy allocation checks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class DoubleCountError(ValueError):
    pass


@dataclass(frozen=True)
class SubsidyAllocationProbe:
    """Fixture-level deltas used to test ND invariants before full D/C engines exist."""

    ptc_applied_to_healthcare_cost_usd: float = 0.0
    ptc_applied_to_disposable_usd: float = 0.0
    snap_applied_to_disposable_usd: float = 0.0
    snap_applied_to_food_cost_usd: float = 0.0
    refundable_credits_applied_to_disposable_usd: float = 0.0
    refundable_credits_applied_to_costs_usd: float = 0.0
    employer_premium_charged_to_household_usd: float = 0.0

    @classmethod
    def from_mapping(cls, data: Mapping[str, float]) -> "SubsidyAllocationProbe":
        return cls(**{k: float(data.get(k, 0.0)) for k in cls.__dataclass_fields__})


def verify_nd_subsidy_invariants(probe: SubsidyAllocationProbe, *, atol: float = 1e-9) -> None:
    """Enforce dossier ND direction on a synthetic allocation probe."""
    if abs(probe.ptc_applied_to_disposable_usd) > atol:
        raise DoubleCountError("PTC must not enter disposable resources (cost side only)")
    if abs(probe.snap_applied_to_food_cost_usd) > atol:
        raise DoubleCountError("SNAP must not reduce food essential cost (D only)")
    if abs(probe.refundable_credits_applied_to_costs_usd) > atol:
        raise DoubleCountError("refundable tax credits must not enter essential costs")
    if abs(probe.employer_premium_charged_to_household_usd) > atol:
        raise DoubleCountError("employer-paid premium share must not be charged to household")


def assert_ptc_cost_only(probe: SubsidyAllocationProbe) -> None:
    if abs(probe.ptc_applied_to_disposable_usd) > 1e-9:
        raise DoubleCountError("PTC in disposable")


def assert_snap_disposable_only(probe: SubsidyAllocationProbe) -> None:
    if abs(probe.snap_applied_to_food_cost_usd) > 1e-9:
        raise DoubleCountError("SNAP in food cost")


def assert_refundable_resources_only(probe: SubsidyAllocationProbe) -> None:
    if abs(probe.refundable_credits_applied_to_costs_usd) > 1e-9:
        raise DoubleCountError("refundable credits in costs")
