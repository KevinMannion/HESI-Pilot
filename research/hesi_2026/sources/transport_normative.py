"""Configurable normative transport need pathway (A r1 P1). Primary remains empirical_pinned."""
from __future__ import annotations

from typing import Any, Mapping

from sources.transport_empirical import price_transport_annual
from transport_vehicle_rules import validate_vehicle_assignment

RETIRED_FLAT_ANNUAL = 7264.7
PRIMARY_DEFINITION = "empirical_pinned_one_vehicle_provisional"


class NormativeTransportError(ValueError):
    pass


def count_normative_drivers(household: Mapping[str, Any], *, rule: str = "synthetic_proxy") -> int:
    if rule != "synthetic_proxy":
        raise NormativeTransportError(f"unsupported driver rule {rule!r}")
    if "normative_drivers" in household:
        return int(household["normative_drivers"])
    if "drivers" in household:
        return int(household["drivers"])
    if "adults" in household:
        return int(household["adults"])
    raise NormativeTransportError("normative pathway requires drivers or adults on synthetic household")


def normative_vehicle_count(
    household: Mapping[str, Any],
    *,
    access_class: str = "LOW",
    workers: int | None = None,
    use_veh_zero_rule: bool = False,
) -> int:
    """
    Normative need pathway (unapproved). use_veh_zero_rule defaults False so VEH=0 is NOT primary definition.
    """
    drv = count_normative_drivers(household)
    veh_obs = int(household.get("veh", household.get("VEH", household.get("vehicles_owned", 1))))
    if use_veh_zero_rule and veh_obs == 0:
        return 0
    if access_class.upper() == "HIGH":
        need = 0
    elif access_class.upper() == "MEDIUM":
        need = 1
    else:
        w = workers if workers is not None else int(household.get("workers", household.get("adults", 1)))
        need = 2 if drv >= 2 and w >= 2 else 1
    v = min(2, need, drv)
    hh = {**household, "vehicles_assigned": v, "drivers": drv}
    return validate_vehicle_assignment(hh)


def price_transport_normative(
    household: Mapping[str, Any],
    *,
    pvc_annual_per_vehicle: float | None = None,
    access_class: str = "LOW",
    use_veh_zero_rule: bool = False,
    mobility_allowance_annual: float = 0.0,
) -> dict[str, Any]:
    empirical = price_transport_annual(household, scenario="reference")
    if abs(float(empirical["annual_usd"]) - RETIRED_FLAT_ANNUAL) < 0.05:
        empirical["retired_primary_vector_flag"] = True
    v = normative_vehicle_count(
        household,
        access_class=access_class,
        use_veh_zero_rule=use_veh_zero_rule,
    )
    if pvc_annual_per_vehicle is None:
        pvc_annual_per_vehicle = float(empirical["annual_usd"])
    if v == 0 and use_veh_zero_rule and mobility_allowance_annual <= 0:
        annual = 0.0
    elif v == 0:
        annual = float(mobility_allowance_annual)
    else:
        annual = round(v * float(pvc_annual_per_vehicle), 2)
    if use_veh_zero_rule is False and int(household.get("veh", 1)) == 0 and v > 0:
        pass
    assert_primary_not_normative_only = PRIMARY_DEFINITION
    return {
        "annual_usd": annual,
        "monthly_usd": round(annual / 12, 2),
        "vehicles_assigned": v,
        "pvc_annual_per_vehicle": pvc_annual_per_vehicle,
        "access_class": access_class,
        "use_veh_zero_rule": use_veh_zero_rule,
        "primary_economic_security_definition": assert_primary_not_normative_only,
        "empirical_reference": empirical,
        "scientific_status": "normative_need_pathway_unapproved_not_primary",
        "policy_approved": False,
        "limitations": [
            "Access-class cutoffs and driver proxy are unapproved VALUE choices",
            "VEH=0 rule disabled by default (not primary economic-security definition)",
        ],
    }


def assert_not_retired_flat_primary(annual_usd: float) -> None:
    if abs(float(annual_usd) - RETIRED_FLAT_ANNUAL) < 0.05:
        raise NormativeTransportError(
            "transport value equals retired flat 7264.7; not permitted as normative primary vector"
        )
