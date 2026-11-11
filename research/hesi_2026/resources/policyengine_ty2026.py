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


def build_synthetic_household_ty2026(
    *,
    state_code: str,
    primary_adult_age: int,
    spouse_adult_age: int,
    child_ages: list[int],
    primary_employment_income: float,
    spouse_employment_income: float,
) -> dict[str, Any]:
    """Married couple + children TY2026 synthetic situation (hypothetical earnings only)."""
    if not child_ages:
        raise ValueError("child_ages required for household situation")
    people: dict[str, Any] = {
        "adult_primary": {
            "age": {TAX_YEAR: primary_adult_age},
            "employment_income": {TAX_YEAR: primary_employment_income},
        },
        "adult_spouse": {
            "age": {TAX_YEAR: spouse_adult_age},
            "employment_income": {TAX_YEAR: spouse_employment_income},
        },
    }
    members = ["adult_primary", "adult_spouse"]
    for i, age in enumerate(child_ages):
        pid = f"child_{i}"
        people[pid] = {"age": {TAX_YEAR: age}}
        members.append(pid)
    return {
        "people": people,
        "households": {"household": {"members": members, "state_code": {TAX_YEAR: state_code}}},
        "marital_units": {"marital_unit": {"members": ["adult_primary", "adult_spouse"]}},
        "tax_units": {"tax_unit": {"members": members}},
        "spm_units": {"spm_unit": {"members": members}},
    }


def calculate_ty2026_household(household: Mapping[str, Any]) -> dict[str, Any]:
    """Provisional TY2026 taxes; hypothetical inputs; benefits mostly unresolved."""
    try:
        from policyengine_us import Simulation
    except ImportError as e:
        raise RuntimeError(
            f"PolicyEngine not installed; use isolated venv with {POLICYENGINE_PIN}"
        ) from e

    spec = household.get("policyengine_synthetic") or {}
    primary_inc = float(spec.get("primary_employment_income", household.get("primary_employment_income", 0)))
    spouse_inc = float(spec.get("spouse_employment_income", household.get("spouse_employment_income", 0)))
    child_ages = [int(m["age"]) for m in household.get("members", []) if int(m.get("age", 99)) < 18]
    if len(child_ages) != 1:
        raise ValueError("prototype household situation expects exactly one child member for TY2026 probe")
    situation = build_synthetic_household_ty2026(
        state_code=str(household["state_code"]),
        primary_adult_age=int(spec.get("primary_adult_age", 35)),
        spouse_adult_age=int(spec.get("spouse_adult_age", 33)),
        child_ages=child_ages,
        primary_employment_income=primary_inc,
        spouse_employment_income=spouse_inc,
    )
    sim = Simulation(situation=situation)
    income_tax_federal = float(sim.calculate("income_tax", TAX_YEAR)[0])
    state_income_tax = float(sim.calculate("state_income_tax", TAX_YEAR)[0])
    employee_payroll_tax = float(sim.calculate("employee_payroll_tax", TAX_YEAR)[0])
    snap_observed = float(sim.calculate("snap", TAX_YEAR)[0])
    eitc_observed = float(sim.calculate("eitc", TAX_YEAR)[0])
    ptc_observed = float(sim.calculate("premium_tax_credit", TAX_YEAR)[0])
    gross = round(primary_inc + spouse_inc, 2)
    unresolved = {
        "snap_benefit": "computed_but_excluded_from_disposable_probe",
        "tanf_benefit": "unresolved_not_decomposed_in_probe",
        "premium_tax_credit_in_disposable": "excluded_by_design_no_double_count",
        "eitc_refundable_detail": "observed_not_applied_to_disposable_probe",
    }
    return {
        "employment_income_primary_usd": primary_inc,
        "employment_income_spouse_usd": spouse_inc,
        "employment_income_household_usd": gross,
        "income_tax_federal_household_usd": income_tax_federal,
        "income_tax_household_usd": income_tax_federal,
        "state_income_tax_household_usd": state_income_tax,
        "employee_payroll_tax_household_usd": employee_payroll_tax,
        "fica_payroll_tax_household_usd": employee_payroll_tax,
        "benefit_components_reported_not_applied": {
            "snap_usd": snap_observed,
            "eitc_usd": eitc_observed,
            "premium_tax_credit_usd": ptc_observed,
        },
        "package": POLICYENGINE_PIN,
        "tax_year": TAX_YEAR,
        "state_code": str(household["state_code"]),
        "inputs_labeled_hypothetical": True,
        "unresolved_components": unresolved,
        "disclaimer": "PolicyEngine TY2026 probe; not CPS/ACS observed income",
    }


def disposable_from_policyengine_household(household: Mapping[str, Any]):
    from resources.disposable import DisposableResourceResult

    pe = calculate_ty2026_household(household)
    gross = float(pe["employment_income_household_usd"])
    fed_tax = float(pe["income_tax_federal_household_usd"])
    state_tax = float(pe["state_income_tax_household_usd"])
    payroll = float(pe["employee_payroll_tax_household_usd"])
    subtract = fed_tax + state_tax + payroll
    disposable = round(gross - subtract, 2)
    return DisposableResourceResult(
        annual_pre_tax_income_usd=gross,
        annual_disposable_usd=disposable,
        source="policyengine_us_household_ty2026_probe",
        tax_year=TAX_YEAR,
        policyengine_available=True,
        policy_approved=False,
        notes="hypothetical earnings; federal+state+employee payroll only; SNAP/PTC excluded",
    ), pe


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
