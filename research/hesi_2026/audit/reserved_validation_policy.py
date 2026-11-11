"""Fail-closed CPS ASEC 2026 reserved validation / holdout access policy (local enforcement).

CPS ASEC 2026 is designated PRIOR_EXPOSURE — RESTRICTED VALIDATION. This module
blocks official modeling, calibration, and validation workflows from loading
reserved microdata, derived national-outcome JSON, or equivalent identifiers.
It does not delete or rewrite historical artifacts.
"""
from __future__ import annotations

import json
import re
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence

DESIGNATION_PRIOR_EXPOSURE = "PRIOR_EXPOSURE_RESTRICTED_VALIDATION"
LABEL_HISTORICAL_BENCHMARK = "HISTORICAL_DESCRIPTIVE_BENCHMARK"
POLICY_VERSION = "asec_2026_validation_integrity_r1"

# Known reserved identifiers (trace r1; no outcome values stored here).
RESERVED_PATH_FRAGMENT_RE = re.compile(
    r"(asecpub26|hhpub26|ffpub26|pppub26|asec_csv_repwgt_2026|"
    r"asec_2026_household_source_totals|asec_source_totals|"
    r"p60-289|p60_289|p60-286|p60_286|asec2026_ddl|asec2026_ddl_pub|"
    r"cpsmar26|cps_asec_2026|quarantine_owner_reserved)",
    re.IGNORECASE,
)
RESERVED_TOKEN_RE = re.compile(
    r"(asec_independent_benchmark|asec_vs_acs|"
    r"CPS_ASEC_2026_MICRODATA|fe819d0d2fc4470c|f4d61659cae9d669|"
    r"independent_benchmark_not_a_match)",
    re.IGNORECASE,
)
RESERVED_SHA256_EXACT = frozenset(
    {
        "fe819d0d2fc4470c282e76c247b8aa8b6054811619730307e9f2fe6186707d93",
        "f4d61659cae9d6698405b17e246abbac09ea65f8a3e4587e291ab4363af9ac85",
    }
)
RESERVED_SHA256_PREFIXES = frozenset({"fe819d0d", "f4d61659", "4ae3ab1a", "074b68df"})


class WorkflowKind(str, Enum):
    MODELING = "official_modeling"
    CALIBRATION = "official_calibration"
    VALIDATION = "official_validation"
    PIPELINE = "official_pipeline"


class ReservedValidationAccessError(RuntimeError):
    """Fail-closed: reserved CPS ASEC 2026 material requested in an official workflow."""


def historical_benchmark_label(*, artifact_kind: str, reference: str) -> dict[str, Any]:
    """Label frozen Track D / Phase 3 comparisons (no outcome values)."""
    return {
        "validation_designation": DESIGNATION_PRIOR_EXPOSURE,
        "benchmark_class": LABEL_HISTORICAL_BENCHMARK,
        "not_blind_independent_validation": True,
        "policy_version": POLICY_VERSION,
        "artifact_kind": artifact_kind,
        "reference": reference,
        "interpretation": (
            "Historical descriptive benchmark only; prior exposure disqualifies "
            "untouched independent validation for the same national estimands."
        ),
    }


def policy_status() -> dict[str, Any]:
    return {
        "designation": DESIGNATION_PRIOR_EXPOSURE,
        "enforcement": "fail_closed",
        "policy_version": POLICY_VERSION,
        "workflows_guarded": [w.value for w in WorkflowKind],
    }


def _normalize_text(value: str) -> str:
    return value.lower().replace("\\", "/")


def _hits_in_text(text: str) -> list[str]:
    hits: list[str] = []
    norm = _normalize_text(text)
    for m in RESERVED_PATH_FRAGMENT_RE.finditer(norm):
        hits.append(f"path_fragment:{m.group(0)}")
    for m in RESERVED_TOKEN_RE.finditer(norm):
        hits.append(f"token:{m.group(0)}")
    norm_sha = norm.replace("-", "")
    for exact in RESERVED_SHA256_EXACT:
        if exact in norm or exact.replace("-", "") in norm_sha:
            hits.append("sha256_exact:asec_reserved")
    for prefix in RESERVED_SHA256_PREFIXES:
        if re.search(rf"\b{re.escape(prefix)}[0-9a-f]{{0,56}}\b", norm):
            hits.append(f"sha256_prefix:{prefix}")
    return hits


def _flatten_context(obj: Any, *, _prefix: str = "") -> list[str]:
    out: list[str] = []
    if obj is None:
        return out
    if isinstance(obj, (str, Path)):
        out.extend(_hits_in_text(str(obj)))
        return out
    if isinstance(obj, (int, float, bool)):
        return out
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            out.extend(_hits_in_text(str(k)))
            out.extend(_flatten_context(v, _prefix=f"{_prefix}.{k}" if _prefix else str(k)))
        return out
    if isinstance(obj, (list, tuple, set)):
        for v in obj:
            out.extend(_flatten_context(v, _prefix=_prefix))
        return out
    out.extend(_hits_in_text(repr(obj)))
    return out


def collect_reserved_hits(context: Mapping[str, Any] | None) -> list[str]:
    if not context:
        return []
    hits = _flatten_context(dict(context))
    # de-dupe stable order
    seen: set[str] = set()
    unique: list[str] = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            unique.append(h)
    return unique


def assert_official_entry_allowed(
    *,
    workflow: WorkflowKind,
    context: Mapping[str, Any] | None = None,
    paths: Sequence[str | Path] | None = None,
) -> None:
    """Fail closed when reserved CPS ASEC 2026 material is referenced."""
    probe: dict[str, Any] = {"workflow": workflow.value}
    if context:
        probe["context"] = dict(context)
    if paths:
        probe["paths"] = [str(p) for p in paths]
    hits = collect_reserved_hits(probe)
    if hits:
        raise ReservedValidationAccessError(
            f"{DESIGNATION_PRIOR_EXPOSURE}: blocked {workflow.value}; "
            f"reserved CPS ASEC 2026 material detected ({', '.join(hits[:8])}"
            f"{'; …' if len(hits) > 8 else ''}). "
            "Use frozen historical artifacts with "
            f"{LABEL_HISTORICAL_BENCHMARK} labels only; preregister separate protocol for new statistics."
        )


def assert_path_resolution_allowed(local_path: str) -> None:
    """Guard data-root path resolution (direct and alias paths)."""
    assert_official_entry_allowed(
        workflow=WorkflowKind.PIPELINE,
        context={"register_local_path": local_path},
    )


def parse_json_object_without_reserved(content: str, *, source: str) -> Any:
    """Block validation workflows from loading reserved derived JSON by content/id."""
    hits = _hits_in_text(source) + _hits_in_text(content[:4096])
    if "observation_asec_calendar_2025" in content[:8192].lower():
        hits.append("json_kind:observation_asec_calendar_2025")
    if "asec_independent_benchmark" in content[:8192].lower():
        hits.append("json_section:asec_independent_benchmark")
    if hits:
        raise ReservedValidationAccessError(
            f"{DESIGNATION_PRIOR_EXPOSURE}: refused to parse reserved derived JSON from {source!r}"
        )
    return json.loads(content)
