"""Import hesi_2026 reserved validation policy for Track D entry points."""
from __future__ import annotations

import sys
from pathlib import Path


def enforce_blocked(*, workflow: str, context: dict | None = None, paths: list | None = None) -> None:
    root = Path(__file__).resolve().parents[2] / "hesi_2026"
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from audit.reserved_validation_policy import (  # noqa: WPS433
        ReservedValidationAccessError,
        WorkflowKind,
        assert_official_entry_allowed,
    )

    kind = WorkflowKind(workflow)
    assert_official_entry_allowed(workflow=kind, context=context, paths=paths or None)


__all__ = ["enforce_blocked"]
