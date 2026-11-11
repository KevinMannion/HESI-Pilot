"""CMS Marketplace PUF ingest hooks (schema / zip boundary checks only)."""
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path
from typing import Any

from audit.hesi_data_root import resolve_register_local_path
from audit.source_register import load_source_register, validate_required_source_pins_or_abort

REGISTER_IDS = ("P4-HC01", "P4-HC02", "P4-HC03")


def _row(source_id: str):
    for r in load_source_register():
        if r.source_id == source_id:
            return r
    return None


def resolve_cms_puf(source_id: str) -> dict[str, Any]:
    row = _row(source_id)
    if row is None:
        return {"source_id": source_id, "error": "not_in_register"}
    resolved = resolve_register_local_path(row.local_path) if row.local_path else None
    meta: dict[str, Any] = {
        "source_id": source_id,
        "register_local_path": row.local_path,
        "verification_status": row.verification_status,
    }
    if resolved and resolved.is_file() and row.sha256:
        got = hashlib.sha256(resolved.read_bytes()).hexdigest()
        meta["path"] = str(resolved)
        meta["sha256_match"] = got == row.sha256.lower()
    else:
        meta["missing"] = True
    return meta


def inspect_rate_puf_zip(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.suffix.lower() != ".zip":
        raise ValueError("CMS rate PUF register entry must be a zip archive")
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        csvs = [n for n in names if n.lower().endswith(".csv")]
    return {
        "archive": str(path),
        "member_count": len(names),
        "csv_members": csvs,
        "scientific_status": "schema_boundary_inspection_only",
    }


def verify_cms_marketplace_register() -> dict[str, Any]:
    """Bounded real-source CMS PUF inspection; aborts if any required pin is missing or mismatched."""
    verified = validate_required_source_pins_or_abort(list(REGISTER_IDS))
    out = {
        sid: {
            **resolve_cms_puf(sid),
            "verified_sha256": verified[sid],
            "fail_closed": True,
        }
        for sid in REGISTER_IDS
    }
    row = _row(REGISTER_IDS[0])
    assert row is not None
    rate_path = resolve_register_local_path(row.local_path)
    assert rate_path is not None
    inspection = None
    if rate_path.suffix.lower() == ".zip":
        inspection = inspect_rate_puf_zip(rate_path)
    return {"sources": out, "rate_puf_inspection": inspection, "verified_pins": verified}
