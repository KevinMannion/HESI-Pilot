"""Geography-resolution policy interface (no imputation without approval)."""
from __future__ import annotations

from typing import Mapping

from policies import GeographyPolicy, UniversePolicies


def geography_allowed(puma_record: Mapping[str, str], policies: UniversePolicies) -> bool:
    policies.validate()
    status = str(puma_record.get("status", ""))
    if policies.geography_policy == GeographyPolicy.COMPLETE_UNAMBIGUOUS_ONLY:
        return status == "COMPLETE_UNAMBIGUOUS"
    if policies.geography_policy == GeographyPolicy.REJECT_PARTIAL:
        return status != "PARTIAL_NOT_APPROVED"
    raise NotImplementedError(policies.geography_policy.value)
