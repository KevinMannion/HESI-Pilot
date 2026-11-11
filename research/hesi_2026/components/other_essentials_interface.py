"""Other essentials (O) vector interface — Sprint 2E gated; engineering scaffold only."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from components.base import EssentialCostResult, MissingStatus

# HESI residual categories pending owner approval (Sprint 2E).
OTHER_ESSENTIALS_CATEGORIES: tuple[str, ...] = (
    "apparel",
    "personal_care",
    "housekeeping_supplies",
    "telephone",
    "home_internet",
)

SPRINT2E_BLOCKED_METHODS: tuple[str, ...] = (
    "bls_ce_second_quintile_residual",
    "proposed_internet_allowance",
    "cpi_aging_bridge_unapproved",
    "household_size_scaling_unapproved",
)


@dataclass(frozen=True)
class OtherEssentialsVectorSpec:
    """Declared coverage for component O; pricing not activated until Sprint 2E approval."""

    categories: tuple[str, ...] = OTHER_ESSENTIALS_CATEGORIES
    sprint2e_status: str = "pending_owner_decisions"
    activation_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "categories": list(self.categories),
            "sprint2e_status": self.sprint2e_status,
            "activation_allowed": self.activation_allowed,
            "blocked_methods": list(SPRINT2E_BLOCKED_METHODS),
        }


DEFAULT_OTHER_ESSENTIALS_SPEC = OtherEssentialsVectorSpec()


def price_other_essentials_o_unresolved(
    household: Mapping[str, Any],
    *,
    context: Mapping[str, Any] | None = None,
    spec: OtherEssentialsVectorSpec = DEFAULT_OTHER_ESSENTIALS_SPEC,
) -> EssentialCostResult:
    """
    Return unresolved O until Sprint 2E approves category mapping, internet allowance,
    CE quintile residual, CPI bridge, and household-size scaling.
    """
    _ = household
    ctx = dict(context or {})
    mode = str(ctx.get("other_necessities_calculation_mode", ctx.get("calculation_mode", "")))
    return EssentialCostResult(
        component="other_necessities",
        source_vintage=None,
        geographic_applicability=str(household.get("state_code", "unassigned")),
        household_applicability="other_essentials_O_vector",
        annual_usd=None,
        missing_status=MissingStatus.MISSING_UNAPPROVED_POLICY,
        policy_approved=False,
        notes=(
            "Other essentials O (apparel, personal care, housekeeping, telephone, internet) "
            "await Sprint 2E scientific decisions; CE second-quintile, internet allowance, "
            "CPI aging, and size scaling not activated."
        ),
        metadata={
            "calculation_mode": mode or "sprint2e_unresolved",
            "other_essentials_vector_spec": spec.to_dict(),
            "sprint2e_blockers": list(SPRINT2E_BLOCKED_METHODS),
        },
    )
