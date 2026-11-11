"""Disposable resources: PolicyEngine TY2026 when available; explicit fixture income otherwise."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class DisposableResourceResult:
    annual_pre_tax_income_usd: float | None
    annual_disposable_usd: float | None
    source: str
    tax_year: str
    policyengine_available: bool
    policy_approved: bool
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "annual_pre_tax_income_usd": self.annual_pre_tax_income_usd,
            "annual_disposable_usd": self.annual_disposable_usd,
            "source": self.source,
            "tax_year": self.tax_year,
            "policyengine_available": self.policyengine_available,
            "policy_approved": self.policy_approved,
            "notes": self.notes,
        }


def disposable_from_fixture(household: Mapping[str, Any], *, tax_year: str = "2026") -> DisposableResourceResult:
    if "annual_gross_income_usd" not in household:
        return DisposableResourceResult(
            annual_pre_tax_income_usd=None,
            annual_disposable_usd=None,
            source="missing",
            tax_year=tax_year,
            policyengine_available=False,
            policy_approved=False,
            notes="annual_gross_income_usd required for fixture path",
        )
    gross = float(household["annual_gross_income_usd"])
    disposable = household.get("annual_disposable_usd")
    return DisposableResourceResult(
        annual_pre_tax_income_usd=gross,
        annual_disposable_usd=float(disposable) if disposable is not None else None,
        source="explicit_fixture",
        tax_year=tax_year,
        policyengine_available=False,
        policy_approved=bool(household.get("income_fixture_approved", False)),
        notes="fixture income; not measured 2026 household income",
    )
