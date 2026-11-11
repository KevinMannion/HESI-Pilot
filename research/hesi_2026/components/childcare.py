from __future__ import annotations

from typing import Any, Mapping

from audit.source_register import SourceRegisterAbortError
from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


def _mode(context: Mapping[str, Any]) -> str:
    return str(context.get("calculation_mode", "fixture"))


class ChildcareComponent(EssentialCostComponent):
    name = "childcare"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        mode = str(context.get("childcare_calculation_mode") or _mode(context))
        if mode in ("empirical_pinned", "ndcp_county"):
            try:
                if mode == "ndcp_county":
                    from sources.ndcp_childcare import price_childcare_ndcp_county

                    detail = price_childcare_ndcp_county(
                        household,
                        county_fips=context.get("county_fips") or household.get("county_fips"),
                        cpi_bridge=str(context.get("cpi_bridge", "none")),
                        cpi_factor=context.get("cpi_factor"),
                        data_source=str(context.get("ndcp_data_source", "fixture")),
                        study_year=int(context.get("study_year", context.get("ndcp_study_year", 2022))),
                    )
                else:
                    from sources.childcare_empirical import price_childcare_annual

                    detail = price_childcare_annual(
                        household,
                        rates_pin_key=str(context.get("childcare_rates_pin_key", "childcare_market_rates_sample")),
                    )
            except SourceRegisterAbortError:
                raise
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability=str(household.get("state_code", "unknown")),
                    household_applicability="childcare_essential",
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
                policy_approved=bool(context.get("childcare_policy_approved", False)),
                notes="empirical_pinned market rates; essential-hours policy gated",
                metadata=detail,
            )
        return EssentialCostResult(
            component=self.name,
            source_vintage=None,
            geographic_applicability="unassigned",
            household_applicability="childcare_essential_unapproved",
            annual_usd=None,
            missing_status=MissingStatus.MISSING_UNAPPROVED_POLICY,
            policy_approved=False,
            notes="childcare essential-cost policy not approved; use calculation_mode=empirical_pinned for research pricing",
        )
