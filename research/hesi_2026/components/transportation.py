from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


def _mode(context: Mapping[str, Any]) -> str:
    return str(context.get("calculation_mode", "fixture"))


class TransportationComponent(EssentialCostComponent):
    name = "transportation"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        mode = _mode(context)
        if mode == "normative_need_unapproved":
            try:
                from sources.transport_normative import price_transport_normative

                detail = price_transport_normative(
                    household,
                    access_class=str(context.get("transport_access_class", "LOW")),
                    use_veh_zero_rule=bool(context.get("use_veh_zero_rule", False)),
                    mobility_allowance_annual=float(context.get("mobility_allowance_annual", 0.0)),
                )
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability="national_scenario",
                    household_applicability="normative_mobility_unapproved",
                    annual_usd=None,
                    missing_status=MissingStatus.MISSING_DATA,
                    policy_approved=False,
                    notes=str(e),
                    metadata={"calculation_mode": mode},
                )
            return EssentialCostResult(
                component=self.name,
                source_vintage="normative_need_unapproved",
                geographic_applicability=detail["empirical_reference"]["geographic_applicability"],
                household_applicability=f"vehicles_{detail['vehicles_assigned']}",
                annual_usd=detail["annual_usd"],
                missing_status=MissingStatus.PRICED,
                policy_approved=False,
                notes=detail["scientific_status"],
                metadata=detail,
            )
        if mode == "empirical_pinned":
            try:
                from sources.transport_empirical import price_transport_annual

                scenario = str(context.get("transport_scenario", "reference"))
                detail = price_transport_annual(household, scenario=scenario)
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability="national_scenario",
                    household_applicability="one_vehicle_provisional",
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
                policy_approved=bool(context.get("transport_policy_approved", False)),
                notes=str(detail.get("scientific_status", "")),
                metadata=detail,
            )
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
                metadata={"calculation_mode": mode},
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
            metadata={"calculation_mode": "fixture"},
        )
