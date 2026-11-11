from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


def _mode(context: Mapping[str, Any]) -> str:
    return str(context.get("calculation_mode", "fixture"))


class HealthcareComponent(EssentialCostComponent):
    name = "healthcare"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        mode = _mode(context)
        if mode == "empirical_pinned":
            try:
                from sources.healthcare_empirical import price_healthcare_annual

                detail = price_healthcare_annual(
                    household,
                    rates_pin_key=str(context.get("healthcare_rates_pin_key", "cms2026_marketplace_rates_sample")),
                    crosswalk_pin_key=str(
                        context.get("healthcare_crosswalk_pin_key", "puma_to_marketplace_rating_area_sample")
                    ),
                    business_year=int(context.get("healthcare_business_year", 2026)),
                    benchmark_rule=str(context.get("healthcare_benchmark_rule", "second_lowest_silver")),
                )
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability=str(household.get("puma_geoid", "unknown")),
                    household_applicability="marketplace_slcsp_benchmark",
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
                policy_approved=bool(context.get("healthcare_policy_approved", False)),
                notes="empirical_pinned CMS SLCSP; ESI/Medicaid not modeled",
                metadata=detail,
            )
        return EssentialCostResult(
            component=self.name,
            source_vintage=None,
            geographic_applicability="unassigned",
            household_applicability="marketplace_benchmark_unbuilt",
            annual_usd=None,
            missing_status=MissingStatus.NOT_IMPLEMENTED,
            policy_approved=False,
            notes="use calculation_mode=empirical_pinned for CMS benchmark path",
        )
