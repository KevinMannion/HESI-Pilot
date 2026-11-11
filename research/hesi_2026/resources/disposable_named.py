"""Fixture-only disposable resources with named tax/credit/benefit variables (no PE default units)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from resources.disposable import DisposableResourceResult

NAMED_VARIABLES = (
    "employment_income",
    "income_tax_before_refundable_credits",
    "fica_payroll_tax",
    "eitc",
    "refundable_ctc",
    "refundable_aotc",
    "state_income_tax",
    "local_income_tax",
    "snap_benefit",
    "tanf_benefit",
    "ssi_benefit",
    "housing_assistance",
    "childcare_assistance",
    "premium_tax_credit",
)


EXCLUDED_FROM_D = frozenset(
    {
        "premium_tax_credit",
        "housing_assistance",
        "childcare_assistance",
    }
)


@dataclass
class NamedDisposableFixture:
    variables: dict[str, float] = field(default_factory=dict)
    tax_year: str = "2026"
    policy_approved: bool = False
    notes: str = "fixture_named_variables_only"

    def validate(self) -> None:
        unknown = set(self.variables) - set(NAMED_VARIABLES)
        if unknown:
            raise ValueError(f"unknown disposable variables: {sorted(unknown)}")
        if "premium_tax_credit" in self.variables and self.variables["premium_tax_credit"] != 0:
            raise ValueError("premium_tax_credit must be zero in D fixture (excluded; belongs in M only)")


def compute_d_from_named(variables: Mapping[str, float]) -> float:
    fixture = NamedDisposableFixture(variables=dict(variables))
    fixture.validate()
    gross = float(variables.get("employment_income", 0.0))
    fed_before = float(variables.get("income_tax_before_refundable_credits", 0.0))
    fica = float(variables.get("fica_payroll_tax", 0.0))
    state = float(variables.get("state_income_tax", 0.0))
    local = float(variables.get("local_income_tax", 0.0))
    refcred = (
        float(variables.get("eitc", 0.0))
        + float(variables.get("refundable_ctc", 0.0))
        + float(variables.get("refundable_aotc", 0.0))
    )
    benefits_in_d = (
        float(variables.get("snap_benefit", 0.0))
        + float(variables.get("tanf_benefit", 0.0))
        + float(variables.get("ssi_benefit", 0.0))
    )
    taxes = fed_before + fica + state + local
    return round(gross - taxes + refcred + benefits_in_d, 2)


def disposable_from_named_fixture(household: Mapping[str, Any]) -> DisposableResourceResult:
    if household.get("use_policyengine_default_tax_unit"):
        raise ValueError("PolicyEngine default tax-unit construction is prohibited in HESI 2026 Sprint 2A")
    block = household.get("disposable_named_variables")
    if not isinstance(block, dict):
        return DisposableResourceResult(
            annual_pre_tax_income_usd=None,
            annual_disposable_usd=None,
            source="missing",
            tax_year="2026",
            policyengine_available=False,
            policy_approved=False,
            notes="disposable_named_variables dict required",
        )
    d = compute_d_from_named(block)
    gross = float(block.get("employment_income", 0.0))
    return DisposableResourceResult(
        annual_pre_tax_income_usd=gross,
        annual_disposable_usd=d,
        source="named_fixture",
        tax_year=str(household.get("tax_year", "2026")),
        policyengine_available=False,
        policy_approved=bool(household.get("disposable_fixture_approved", False)),
        notes="D from named variables; PTC excluded from D; PE default tax units prohibited",
    )
