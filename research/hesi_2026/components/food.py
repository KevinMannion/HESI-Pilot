from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


class FoodComponent(EssentialCostComponent):
    name = "food"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        if "food_annual_usd" not in household:
            return EssentialCostResult(
                component=self.name,
                source_vintage=context.get("food_vintage"),
                geographic_applicability=str(context.get("food_geography", "mainland_usda_unapproved_ak_hi")),
                household_applicability="thrifty_plan_household",
                annual_usd=None,
                missing_status=MissingStatus.MISSING_DATA,
                policy_approved=False,
                notes="food_annual_usd not supplied",
            )
        return EssentialCostResult(
            component=self.name,
            source_vintage=str(context.get("food_vintage", "explicit_fixture")),
            geographic_applicability=str(context.get("food_geography", "mainland_usda")),
            household_applicability="thrifty_plan_household",
            annual_usd=float(household["food_annual_usd"]),
            missing_status=MissingStatus.PRICED,
            policy_approved=bool(context.get("food_policy_approved", False)),
        )
