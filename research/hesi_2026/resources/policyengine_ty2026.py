"""Isolated PolicyEngine-US 2.x TY2026 household calculations (synthetic only)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

POLICYENGINE_PIN = "policyengine-us==2.116.17"
TAX_YEAR = "2026"


@dataclass(frozen=True)
class PolicyEngineTy2026Result:
    employment_income: float
    adjusted_gross_income_person: float
    income_tax: float
    package: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "employment_income": self.employment_income,
            "adjusted_gross_income_person": self.adjusted_gross_income_person,
            "income_tax": self.income_tax,
            "package": self.package,
            "tax_year": TAX_YEAR,
            "disclaimer": "computational probe only; not legal verification",
        }


def build_synthetic_situation(
    *,
    state_code: str,
    age: int,
    employment_income: float,
) -> dict[str, Any]:
    return {
        "people": {
            "person": {
                "age": {TAX_YEAR: age},
                "employment_income": {TAX_YEAR: employment_income},
            }
        },
        "households": {"household": {"members": ["person"], "state_code": {TAX_YEAR: state_code}}},
        "marital_units": {"marital_unit": {"members": ["person"]}},
        "tax_units": {"tax_unit": {"members": ["person"]}},
        "spm_units": {"spm_unit": {"members": ["person"]}},
    }


def calculate_ty2026_synthetic(
    household: Mapping[str, Any],
) -> PolicyEngineTy2026Result:
    try:
        from policyengine_us import Simulation
    except ImportError as e:
        raise RuntimeError(
            f"PolicyEngine not installed; use isolated venv with {POLICYENGINE_PIN}"
        ) from e

    state = str(household["state_code"])
    age = int(household.get("age", 35))
    emp = float(household["employment_income"])
    situation = build_synthetic_situation(state_code=state, age=age, employment_income=emp)
    sim = Simulation(situation=situation)
    emp_v = float(sim.calculate("employment_income", TAX_YEAR)[0])
    agi = float(sim.calculate("adjusted_gross_income_person", TAX_YEAR)[0])
    tax = float(sim.calculate("income_tax", TAX_YEAR)[0])
    return PolicyEngineTy2026Result(
        employment_income=emp_v,
        adjusted_gross_income_person=agi,
        income_tax=tax,
        package=POLICYENGINE_PIN,
    )


def disposable_from_policyengine(household: Mapping[str, Any]):
    from resources.disposable import DisposableResourceResult

    pe = calculate_ty2026_synthetic(household)
    gross = pe.employment_income
    disposable = gross - pe.income_tax
    return DisposableResourceResult(
        annual_pre_tax_income_usd=gross,
        annual_disposable_usd=disposable,
        source="policyengine_us",
        tax_year=TAX_YEAR,
        policyengine_available=True,
        policy_approved=False,
        notes="PolicyEngine synthetic TY2026; not PUMS-weighted national income",
    )
