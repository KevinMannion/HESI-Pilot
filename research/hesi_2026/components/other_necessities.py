from __future__ import annotations

from typing import Any, Mapping

from components.base import EssentialCostComponent, EssentialCostResult, MissingStatus


def _mode(context: Mapping[str, Any]) -> str:
    return str(context.get("calculation_mode", "fixture"))


class OtherNecessitiesComponent(EssentialCostComponent):
    name = "other_necessities"

    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        context = context or {}
        mode = _mode(context)
        per_component_mode = str(context.get("other_necessities_calculation_mode") or mode)
        if per_component_mode == "bls_ce_register":
            try:
                from sources.bls_ce_workbook import price_other_ce_register_or_unresolved

                price_other_ce_register_or_unresolved(dict(household))
            except (ValueError, FileNotFoundError) as e:
                from sources.bls_ce_workbook import extract_ce_observed_national_means

                meta: dict[str, object] = {}
                try:
                    meta = extract_ce_observed_national_means()
                except (ValueError, FileNotFoundError):
                    meta = {"register_unavailable": True}
                return EssentialCostResult(
                    component=self.name,
                    source_vintage="BLS_CE_CY2025_register_observed_unresolved",
                    geographic_applicability="national",
                    household_applicability="residual_essentials",
                    annual_usd=None,
                    missing_status=MissingStatus.MISSING_DATA,
                    policy_approved=False,
                    notes=str(e),
                    metadata={"calculation_mode": per_component_mode, "observed_ce_register": meta},
                )
        if mode == "bls_ce_fallback":
            try:
                from sources.bls_ce_other import price_other_ce_fallback

                detail = price_other_ce_fallback(
                    household,
                    use_fallback=bool(context.get("use_ce_fallback", True)),
                )
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability="national",
                    household_applicability="residual_essentials",
                    annual_usd=None,
                    missing_status=MissingStatus.MISSING_DATA,
                    policy_approved=False,
                    notes=str(e),
                    metadata={"calculation_mode": mode},
                )
            return EssentialCostResult(
                component=self.name,
                source_vintage="BLS_CE_fallback_unapproved",
                geographic_applicability="national",
                household_applicability=detail["method"],
                annual_usd=detail["annual_usd"],
                missing_status=MissingStatus.PRICED,
                policy_approved=False,
                notes=detail["scientific_status"],
                metadata=detail,
            )
        if mode == "empirical_pinned":
            try:
                from sources.other_necessities_empirical import price_other_necessities_annual

                detail = price_other_necessities_annual(
                    household,
                    bundle_pin_key=str(context.get("other_necessities_pin_key", "ces_other_necessities_baseline_sample")),
                )
            except (ValueError, FileNotFoundError) as e:
                return EssentialCostResult(
                    component=self.name,
                    source_vintage=None,
                    geographic_applicability="unknown",
                    household_applicability="residual_essentials",
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
                policy_approved=bool(context.get("other_necessities_policy_approved", False)),
                notes="empirical_pinned CES residual bundle; category policy gated",
                metadata=detail,
            )
        return EssentialCostResult(
            component=self.name,
            source_vintage=None,
            geographic_applicability="unassigned",
            household_applicability="residual_essentials_unapproved",
            annual_usd=None,
            missing_status=MissingStatus.MISSING_UNAPPROVED_POLICY,
            policy_approved=False,
            notes="residual essentials vector not approved; use calculation_mode=empirical_pinned for research pricing",
        )
