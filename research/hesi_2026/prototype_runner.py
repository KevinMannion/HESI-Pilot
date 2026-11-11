"""Reviewer prototype v0.1: enrich pipeline output without weakening production gates."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Mapping

from components.base import MissingStatus
from gating import NATIONAL_HEADLINE_ENABLED
from pipeline import SIX_COMPONENT_NAMES, run_household_pipeline
from sources.pinned import PINNED_SOURCES

REVIEWER_PROTOTYPE_VERSION = "hesi_reviewer_prototype_v0.1"
PIN_CONTEXT_KEYS = (
    "geography_pin_key",
    "healthcare_rates_pin_key",
    "healthcare_crosswalk_pin_key",
    "childcare_rates_pin_key",
    "food_pin_key",
    "transport_pin_key",
    "other_necessities_pin_key",
)


def _git_head(repo_root: Path) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def collect_pin_provenance(cost_context: Mapping[str, Any]) -> tuple[dict[str, Any], list[str]]:
    pins: dict[str, Any] = {}
    warnings: list[str] = []
    for ctx_key in PIN_CONTEXT_KEYS:
        pin_key = cost_context.get(ctx_key)
        if not pin_key:
            continue
        src = PINNED_SOURCES.get(str(pin_key))
        if src is None:
            warnings.append(f"unknown pin key {pin_key!r} from {ctx_key}")
            continue
        try:
            src.verify()
            status = "verified"
        except (FileNotFoundError, ValueError) as e:
            status = "hash_or_path_failed"
            warnings.append(f"{pin_key}: {e}")
        pins[str(pin_key)] = {
            "context_field": ctx_key,
            "path": str(src.path),
            "sha256": src.sha256,
            "source_vintage": src.source_vintage,
            "geographic_applicability": src.geographic_applicability,
            "verification_status": status,
            "data_year_class": _classify_vintage(src.source_vintage),
        }
    return pins, warnings


def _classify_vintage(vintage: str) -> str:
    v = vintage.lower()
    if "synthetic" in v or "fixture" in v or "sample" in v or "bounded" in v:
        return "synthetic_or_bounded_fixture_not_national_empirical"
    if "2026" in v:
        return "observed_or_pinned_2026_vintage"
    if "2024" in v or "2022" in v or "2020" in v:
        return "older_source_vintage_may_require_bridge"
    return "unclassified_vintage_review_required"


def _component_year_class(cost: dict[str, Any]) -> str:
    vintage = (cost.get("source_vintage") or "").lower()
    meta = cost.get("metadata") or {}
    if meta.get("fixture_fallback") or "synthetic" in vintage or "fixture" in vintage:
        return "synthetic_fixture_literal"
    mode = str(meta.get("calculation_mode", cost.get("metadata", {}).get("calculation_mode", "")))
    if "ndcp_study_year_observed" in meta:
        return f"observed_ndcp_year_{meta['ndcp_study_year_observed']}_not_2026"
    if "cpi_bridge" in meta and (meta.get("cpi_bridge") or {}).get("factor") not in (None, 1, 1.0):
        return "older_observed_with_explicit_cpi_bridge"
    if "2026" in vintage:
        return "observed_or_modeled_2026_vintage"
    if mode == "empirical_pinned":
        return "empirical_pinned_check_source_vintage_field"
    return "unclassified"


def numeric_six_component_total(cost_dicts: list[dict[str, Any]]) -> tuple[float | None, list[str]]:
    total = 0.0
    missing: list[str] = []
    for name in SIX_COMPONENT_NAMES:
        row = next((c for c in cost_dicts if c["component"] == name), None)
        if row is None:
            missing.append(name)
            continue
        if row.get("missing_status") != MissingStatus.PRICED.value or row.get("annual_usd") is None:
            missing.append(name)
            continue
        total += float(row["annual_usd"])
    if missing:
        return None, missing
    return round(total, 2), []


def classify_reviewer_prototype(
    cost_dicts: list[dict[str, Any]],
    disposable: dict[str, Any],
) -> dict[str, Any]:
    six_total, missing = numeric_six_component_total(cost_dicts)
    d_annual = disposable.get("annual_disposable_usd")
    if six_total is not None and d_annual is not None:
        status = "COMPLETE_PROVISIONAL"
        provisional_ratio = round(float(d_annual) / six_total, 6) if six_total > 0 else None
    else:
        status = "PARTIAL_UNRESOLVED"
        provisional_ratio = None
    return {
        "reviewer_prototype_version": REVIEWER_PROTOTYPE_VERSION,
        "status": status,
        "approved_status": "APPROVED",
        "approved_status_enabled": False,
        "approved_hesi_economic_security_classification": None,
        "provisional_six_component_essential_annual_usd": six_total,
        "provisional_resources_to_essential_ratio": provisional_ratio,
        "unpriced_or_blocked_components": missing,
        "interpretation": (
            "COMPLETE_PROVISIONAL indicates numeric six-vector and D only; "
            "not scientifically approved HESI security."
        ),
    }


def build_canonical_calculation_payload(audit: Mapping[str, Any]) -> dict[str, Any]:
    adequacy = dict(audit.get("adequacy") or {})
    if isinstance(adequacy.get("blockers"), list):
        adequacy["blockers"] = sorted(adequacy["blockers"])
    release_gates = dict(audit.get("release_gates") or {})
    if isinstance(release_gates.get("six_component_blockers"), list):
        release_gates["six_component_blockers"] = sorted(release_gates["six_component_blockers"])
    reviewer = audit.get("reviewer_prototype") or {}
    if isinstance(reviewer.get("unpriced_or_blocked_components"), list):
        reviewer = dict(reviewer)
        reviewer["unpriced_or_blocked_components"] = sorted(reviewer["unpriced_or_blocked_components"])
    return {
        "audit_schema_version": audit.get("audit_schema_version"),
        "frame": audit.get("frame"),
        "essential_costs": audit.get("essential_costs"),
        "disposable_resources": audit.get("disposable_resources"),
        "adequacy": {
            k: adequacy.get(k)
            for k in (
                "essential_annual_usd",
                "disposable_annual_usd",
                "ratio",
                "partial_three_component_annual_usd",
                "partial_three_component_ratio",
                "blockers",
                "computable",
            )
        },
        "reviewer_prototype": reviewer,
        "source_pins": audit.get("source_pins"),
        "component_data_year_class": audit.get("component_data_year_class"),
        "release_gates": release_gates,
    }


def canonical_calculation_hash(audit: Mapping[str, Any]) -> str:
    payload = build_canonical_calculation_payload(audit)
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return _sha256_bytes(blob.encode("utf-8"))


def run_reviewer_prototype(
    scenario: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    from audit.reserved_validation_policy import WorkflowKind, assert_official_entry_allowed

    assert_official_entry_allowed(workflow=WorkflowKind.PIPELINE, context={"scenario": dict(scenario)})
    household = dict(scenario["household"])
    cost_context = dict(scenario.get("cost_context") or {})
    use_pe = bool(scenario.get("use_policyengine", False))
    scenario_id = str(scenario.get("scenario_id", "unspecified"))
    scenario_label = str(scenario.get("label", "SYNTHETIC_HOUSEHOLD_NOT_OBSERVED"))

    result = run_household_pipeline(household, cost_context=cost_context, use_policyengine=use_pe)
    audit = result["audit"]
    pins, pin_warnings = collect_pin_provenance(cost_context)

    component_years = {
        c["component"]: _component_year_class(c) for c in audit.get("essential_costs", [])
    }
    warnings = list(pin_warnings)
    warnings.extend(scenario.get("warnings") or [])
    if cost_context.get("calculation_mode") == "empirical_pinned":
        warnings.append(
            "empirical_pinned context uses repository pins/samples; "
            "not a claim of full national 2026 empirical HESI."
        )
    if scenario.get("scenario_kind") == "source_backed_provisional_2026":
        warnings.append("source_backed_provisional_2026: mixed vintages; not APPROVED HESI methodology")
    for reg_id in ("P4-C01", "P4-O01", "P4-O02"):
        if reg_id == "P4-C01" and cost_context.get("ndcp_data_source") == "register":
            try:
                from audit.source_register import validate_required_source_pins_or_abort

                verified = validate_required_source_pins_or_abort([reg_id])
                pins[reg_id] = {
                    "source_id": reg_id,
                    "sha256": verified[reg_id],
                    "data_year_class": "observed_ndcp_2022_not_2026",
                }
            except Exception as e:
                warnings.append(f"{reg_id} verification failed: {e}")
    if any(v == "synthetic_fixture_literal" for v in component_years.values()):
        warnings.append("one_or_more_components_use_synthetic_fixture_literals")

    reviewer = classify_reviewer_prototype(
        audit["essential_costs"],
        audit["disposable_resources"],
    )

    audit["reviewer_prototype"] = reviewer
    audit["source_pins"] = pins
    audit["component_data_year_class"] = component_years
    audit["warnings"] = warnings
    audit["scenario"] = {
        "scenario_id": scenario_id,
        "label": scenario_label,
        "synthetic_household": True,
        "national_representativeness": False,
    }
    audit["status"] = "REVIEWER_PROTOTYPE_v0.1"
    audit["limitations"] = [
        "Reviewer prototype only; not scientifically approved HESI.",
        "No approved economic security classification is emitted.",
        "National headline disabled; not a national prevalence estimate.",
        "Canonical hash excludes timestamps and git metadata.",
    ]
    audit["provenance"] = {
        **audit.get("provenance", {}),
        "runner": "research.hesi_2026.prototype_runner",
        "reviewer_prototype_version": REVIEWER_PROTOTYPE_VERSION,
        "national_headline_enabled": NATIONAL_HEADLINE_ENABLED,
        "pipeline_mode": cost_context.get("calculation_mode", "fixture"),
    }

    repo_root = repo_root or Path(__file__).resolve().parents[2]
    git_commit = _git_head(repo_root)

    canonical_hash = canonical_calculation_hash(audit)
    return {
        "audit": audit,
        "adequacy": result["adequacy"],
        "reviewer_prototype": reviewer,
        "canonical_calculation_sha256": canonical_hash,
        "git_commit": git_commit,
        "scenario_id": scenario_id,
    }


def write_reviewer_prototype_run(output_dir: Path, payload: dict[str, Any], *, run_id: str) -> dict[str, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    audit_path = output_dir / "audit.json"
    audit_path.write_text(json.dumps(payload["audit"], indent=2) + "\n")

    canonical_path = output_dir / "canonical_calculation.json"
    canonical_path.write_text(
        json.dumps(build_canonical_calculation_payload(payload["audit"]), indent=2) + "\n"
    )

    pipeline_path = output_dir / "pipeline_result.json"
    pipeline_path.write_text(
        json.dumps(
            {
                "scenario_id": payload["scenario_id"],
                "adequacy": payload["adequacy"],
                "reviewer_prototype": payload["reviewer_prototype"],
                "canonical_calculation_sha256": payload["canonical_calculation_sha256"],
                "audit_path": "audit.json",
            },
            indent=2,
        )
        + "\n"
    )

    manifest = {
        "run_id": run_id,
        "scenario_id": payload["scenario_id"],
        "reviewer_prototype_version": REVIEWER_PROTOTYPE_VERSION,
        "canonical_calculation_sha256": payload["canonical_calculation_sha256"],
        "git_commit": payload.get("git_commit"),
        "volatile_metadata_separated": True,
        "reproducibility_note": (
            "Compare canonical_calculation_sha256 only when scenario JSON, "
            "dependency pins, and repository inputs are identical; "
            "not byte-for-byte across environments."
        ),
        "files": {
            "audit.json": {"sha256": _sha256_file(audit_path)},
            "canonical_calculation.json": {"sha256": _sha256_file(canonical_path)},
            "pipeline_result.json": {"sha256": _sha256_file(pipeline_path)},
        },
    }
    manifest_path = output_dir / "PROTOTYPE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    return {
        "audit": audit_path,
        "canonical": canonical_path,
        "pipeline": pipeline_path,
        "manifest": manifest_path,
    }


def load_scenario_file(path: Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text())
    if "household" not in data:
        raise ValueError("scenario file must contain 'household'")
    return data
