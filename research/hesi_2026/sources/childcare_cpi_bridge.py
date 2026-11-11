"""Configurable CPI bridge for NDCP vintage prices (never auto-approved)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
OPTIONS_PATH = REPO / "research/hesi_2026/fixtures/inputs/cpi_childcare_bridge_options.json"


def load_bridge_options() -> dict[str, Any]:
    return json.loads(OPTIONS_PATH.read_text())


def apply_cpi_bridge(
    *,
    bridge_key: str,
    factor: float | None,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    options = options or load_bridge_options()
    if bridge_key == "none":
        return {
            "bridge_key": "none",
            "factor": 1.0,
            "policy_approved": False,
            "scientific_status": options.get("scientific_status"),
            "approved": False,
            "notes": "NDCP weekly prices without bridge",
        }
    if bridge_key == "owner_supplied_factor":
        if factor is None or factor <= 0:
            raise ValueError("owner_supplied_factor requires explicit positive cpi_factor in context")
        return {
            "bridge_key": bridge_key,
            "factor": float(factor),
            "policy_approved": False,
            "scientific_status": options.get("scientific_status"),
            "approved": False,
            "notes": "Owner-supplied bridge factor; not scientifically approved",
        }
    raise ValueError(f"unknown cpi_bridge {bridge_key!r}")
