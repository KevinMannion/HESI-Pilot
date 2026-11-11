"""Audit schema v2 (scratch outputs only)."""
from __future__ import annotations

AUDIT_SCHEMA_VERSION = "hesi_audit_v2"


def audit_v2_skeleton() -> dict:
    return {
        "audit_schema_version": AUDIT_SCHEMA_VERSION,
        "frame": {},
        "tenure_groups": {},
        "essential_costs": [],
        "disposable_resources": {},
        "adequacy": {},
        "policies": {},
        "provenance": {},
        "limitations": [],
        "status": "RESEARCH_ONLY",
    }
