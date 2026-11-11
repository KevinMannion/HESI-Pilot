"""Essential-cost component contract."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class MissingStatus(str, Enum):
    PRICED = "priced"
    MISSING_DATA = "missing_data"
    MISSING_UNAPPROVED_POLICY = "missing_unapproved_policy"
    NOT_IMPLEMENTED = "not_implemented"


@dataclass(frozen=True)
class EssentialCostResult:
    component: str
    source_vintage: str | None
    geographic_applicability: str
    household_applicability: str
    annual_usd: float | None
    missing_status: MissingStatus
    policy_approved: bool
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "component": self.component,
            "source_vintage": self.source_vintage,
            "geographic_applicability": self.geographic_applicability,
            "household_applicability": self.household_applicability,
            "annual_usd": self.annual_usd,
            "missing_status": self.missing_status.value,
            "policy_approved": self.policy_approved,
            "notes": self.notes,
            "metadata": self.metadata,
        }


class EssentialCostComponent(ABC):
    name: str

    @abstractmethod
    def price(self, household: Mapping[str, Any], *, context: Mapping[str, Any] | None = None) -> EssentialCostResult:
        raise NotImplementedError
