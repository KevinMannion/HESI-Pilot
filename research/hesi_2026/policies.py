"""Explicit configuration policies for universe accounting (no silent defaults)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class InfantPolicy(str, Enum):
    EXCLUDE_UNPRICED = "exclude_unpriced"
    REQUIRE_APPROVED_PRICING = "require_approved_pricing"


class BedroomPolicy(str, Enum):
    EXCLUDE_OVER_FOUR = "exclude_over_four"
    HUD_FOUR_BR_CAP_UNAPPROVED = "hud_four_br_cap_unapproved"
    FIVE_PLUS_FMR_UNAPPROVED = "five_plus_fmr_unapproved"


class GeographyPolicy(str, Enum):
    COMPLETE_UNAMBIGUOUS_ONLY = "complete_unambiguous_only"
    REJECT_PARTIAL = "reject_partial"
    IMPUTE_UNAPPROVED = "impute_unapproved"


@dataclass(frozen=True)
class UniversePolicies:
    infant_policy: InfantPolicy = InfantPolicy.EXCLUDE_UNPRICED
    bedroom_policy: BedroomPolicy = BedroomPolicy.EXCLUDE_OVER_FOUR
    geography_policy: GeographyPolicy = GeographyPolicy.COMPLETE_UNAMBIGUOUS_ONLY
    tenure_classes: tuple[str, ...] = ("owner", "renter", "rent_free", "other_tenure")

    def validate(self) -> None:
        if self.infant_policy == InfantPolicy.REQUIRE_APPROVED_PRICING:
            raise NotImplementedError(
                "REQUIRE_APPROVED_PRICING is not approved; set infant_policy to EXCLUDE_UNPRICED"
            )
        if self.bedroom_policy != BedroomPolicy.EXCLUDE_OVER_FOUR:
            raise NotImplementedError(f"Bedroom policy {self.bedroom_policy.value} is not approved")
        if self.geography_policy != GeographyPolicy.COMPLETE_UNAMBIGUOUS_ONLY:
            raise NotImplementedError(f"Geography policy {self.geography_policy.value} is not approved")


DEFAULT_UNIVERSE_POLICIES = UniversePolicies()
