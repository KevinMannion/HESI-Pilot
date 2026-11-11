from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


class OtherNecessitiesComponent(EssentialCostComponent):
    name = "other_necessities"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        _ = household, context
        return EssentialCostResult(
            component=self.name,
            source_vintage=None,
            geographic_applicability="unassigned",
            household_applicability="residual_essentials_unapproved",
            annual_usd=None,
            missing_status=MissingStatus.MISSING_UNAPPROVED_POLICY,
            policy_approved=False,
            notes="residual essentials vector not approved",
        )
