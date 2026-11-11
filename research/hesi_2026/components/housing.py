from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


class HousingComponent(EssentialCostComponent):
    name = "housing"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        if "housing_annual_usd" not in household:
            return EssentialCostResult(
                component=self.name,
                source_vintage=context.get("housing_vintage"),
                geographic_applicability=str(household.get("puma_geoid", "unknown")),
                household_applicability="replacement_rent_normative",
                annual_usd=None,
                missing_status=MissingStatus.MISSING_DATA,
                policy_approved=False,
                notes="housing_annual_usd not supplied; no default rent invented",
            )
        return EssentialCostResult(
            component=self.name,
            source_vintage=str(context.get("housing_vintage", "explicit_fixture")),
            geographic_applicability=str(household.get("puma_geoid", "national")),
            household_applicability="replacement_rent_normative",
            annual_usd=float(household["housing_annual_usd"]),
            missing_status=MissingStatus.PRICED,
            policy_approved=bool(context.get("housing_policy_approved", False)),
            notes=str(context.get("housing_notes", "")),
        )
