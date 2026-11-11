from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


class TransportationComponent(EssentialCostComponent):
    name = "transportation"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        if "transport_annual_usd" not in household:
            return EssentialCostResult(
                component=self.name,
                source_vintage=context.get("transport_vintage"),
                geographic_applicability="national_scenario",
                household_applicability="one_vehicle_provisional",
                annual_usd=None,
                missing_status=MissingStatus.MISSING_DATA,
                policy_approved=False,
                notes="transport_annual_usd not supplied",
            )
        return EssentialCostResult(
            component=self.name,
            source_vintage=str(context.get("transport_vintage", "explicit_fixture")),
            geographic_applicability=str(context.get("transport_geography", "national")),
            household_applicability="one_vehicle_provisional",
            annual_usd=float(household["transport_annual_usd"]),
            missing_status=MissingStatus.PRICED,
            policy_approved=bool(context.get("transport_policy_approved", False)),
            notes=str(context.get("transport_notes", "provisional nonfuel held")),
        )
