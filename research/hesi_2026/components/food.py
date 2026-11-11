from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


def _mode(context: Mapping[str, Any]) -> str:
    return str(context.get("calculation_mode", "fixture"))


class FoodComponent(EssentialCostComponent):
    name = "food"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        mode = _mode(context)
        if mode == "empirical_pinned":
            try:
                from sources.food_empirical import price_food_annual

                plan = str(context.get("food_plan", "thrifty"))
                detail = price_food_annual(household, plan=plan)
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability="unknown",
                    household_applicability="thrifty_plan_household",
                    annual_usd=None,
                    missing_status=MissingStatus.MISSING_DATA,
                    policy_approved=False,
                    notes=str(e),
                    metadata={"calculation_mode": mode},
                )
            return EssentialCostResult(
                component=self.name,
                source_vintage=detail["source_vintage"],
                geographic_applicability=detail["geographic_applicability"],
                household_applicability=detail["household_applicability"],
                annual_usd=detail["annual_usd"],
                missing_status=MissingStatus.PRICED,
                policy_approved=bool(context.get("food_policy_approved", False)),
                notes="empirical_pinned; production approval separate",
                metadata=detail,
            )
        if "food_annual_usd" not in household:
            return EssentialCostResult(
                component=self.name,
                source_vintage=context.get("food_vintage"),
                geographic_applicability=str(context.get("food_geography", "mainland_usda_unapproved_ak_hi")),
                household_applicability="thrifty_plan_household",
                annual_usd=None,
                missing_status=MissingStatus.MISSING_DATA,
                policy_approved=False,
                notes="food_annual_usd not supplied; use calculation_mode=empirical_pinned",
                metadata={"calculation_mode": mode},
            )
        return EssentialCostResult(
            component=self.name,
            source_vintage=str(context.get("food_vintage", "explicit_fixture")),
            geographic_applicability=str(context.get("food_geography", "mainland_usda")),
            household_applicability="thrifty_plan_household",
            annual_usd=float(household["food_annual_usd"]),
            missing_status=MissingStatus.PRICED,
            policy_approved=bool(context.get("food_policy_approved", False)),
            metadata={"calculation_mode": "fixture"},
        )
