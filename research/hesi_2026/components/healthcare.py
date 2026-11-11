from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


class HealthcareComponent(EssentialCostComponent):
    name = "healthcare"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        _ = household, context
        return EssentialCostResult(
            component=self.name,
            source_vintage=None,
            geographic_applicability="unassigned",
            household_applicability="marketplace_benchmark_unbuilt",
            annual_usd=None,
            missing_status=MissingStatus.NOT_IMPLEMENTED,
            policy_approved=False,
            notes="2026 Marketplace benchmark premium requires plan-level rate construction (not in repo)",
        )
