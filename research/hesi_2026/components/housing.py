from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


def _mode(context: Mapping[str, Any]) -> str:
    return str(context.get("calculation_mode", "fixture"))


class HousingComponent(EssentialCostComponent):
    name = "housing"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        mode = _mode(context)
        if mode in ("empirical_pinned", "fmr_q4_schedule_unapproved"):
            try:
                if mode == "fmr_q4_schedule_unapproved":
                    from sources.housing_fmr_q4_schedule import price_housing_with_schedule_option

                    detail = price_housing_with_schedule_option(
                        household,
                        area_label=str(context.get("fmr_area_label", "general")),
                        calendar_month=int(context.get("calendar_month", 10)),
                        use_schedule=bool(context.get("use_er1_schedule", True)),
                    )
                else:
                    from sources.housing_empirical import price_housing_annual

                    pin_key = str(context.get("geography_pin_key", "puma_fmr_screened_fy2026"))
                    detail = price_housing_annual(household, geography_pin_key=pin_key)
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability=str(household.get("puma_geoid", "unknown")),
                    household_applicability="replacement_rent_normative",
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
                policy_approved=bool(context.get("housing_policy_approved", False)),
                notes="empirical_pinned FMR lookup",
                metadata=detail,
            )
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
                metadata={"calculation_mode": mode},
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
            metadata={"calculation_mode": "fixture"},
        )
