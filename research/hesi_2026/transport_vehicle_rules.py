"""Synthetic transport vehicle eligibility (not a final mobility cost model)."""
from __future__ import annotations

from typing import Any, Mapping

MAX_VEHICLES = 2


class VehicleEligibilityError(ValueError):
    pass


def count_eligible_drivers(household: Mapping[str, Any]) -> int:
    if "drivers" in household:
        drivers = int(household["drivers"])
    elif "adults" in household:
        drivers = int(household["adults"])
    else:
        raise VehicleEligibilityError("household requires drivers or adults for eligibility check")
    if drivers < 0:
        raise VehicleEligibilityError("drivers must be non-negative")
    return drivers


def assigned_vehicle_count(household: Mapping[str, Any]) -> int:
    if "vehicles_assigned" in household:
        return int(household["vehicles_assigned"])
    if "transport_vehicles" in household:
        return int(household["transport_vehicles"])
    return 0


def validate_vehicle_assignment(household: Mapping[str, Any]) -> int:
    """Return assigned vehicles after enforcing V <= drivers and V <= 2."""
    drivers = count_eligible_drivers(household)
    vehicles = assigned_vehicle_count(household)
    if vehicles < 0:
        raise VehicleEligibilityError("vehicles_assigned must be non-negative")
    if vehicles > MAX_VEHICLES:
        raise VehicleEligibilityError(f"vehicles_assigned {vehicles} exceeds cap {MAX_VEHICLES}")
    if vehicles > drivers:
        raise VehicleEligibilityError(f"vehicles_assigned {vehicles} exceeds drivers {drivers}")
    return vehicles
