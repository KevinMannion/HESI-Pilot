from __future__ import annotations

from components.childcare import ChildcareComponent
from components.food import FoodComponent
from components.healthcare import HealthcareComponent
from components.housing import HousingComponent
from components.other_necessities import OtherNecessitiesComponent
from components.transportation import TransportationComponent
from components.base import EssentialCostComponent


def default_six_component_registry() -> list[EssentialCostComponent]:
    return [
        HousingComponent(),
        FoodComponent(),
        TransportationComponent(),
        HealthcareComponent(),
        ChildcareComponent(),
        OtherNecessitiesComponent(),
    ]
