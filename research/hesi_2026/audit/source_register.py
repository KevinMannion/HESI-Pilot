"""Ingest and validate SOURCE_PIN_REGISTER_r1.csv (recommendations; not approvals)."""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from audit.hesi_data_root import hesi_data_root, resolve_register_local_path

REGISTER_COLUMNS = (
    "source_id",
    "component",
    "title",
    "url",
    "publisher",
    "publication_date",
    "vintage",
    "coverage",
    "local_path",
    "sha256",
    "verification_status",
    "unresolved_gaps",
    "blocks",
    "limitations",
    "adjustment_2026",
    "origin",
)

DEFAULT_REGISTER = Path(__file__).resolve().parent / "source_pin_register_r1.csv"
S3_LIST = Path(__file__).resolve().parent / "s3_bounded_source_ids.json"


class SourceRegisterError(ValueError):
    pass


class SourceRegisterAbortError(SourceRegisterError):
    """Fail-closed: a required pinned source is missing or hash-mismatched."""


@dataclass
class SourceRegisterRow:
    source_id: str
    component: str
    title: str
    vintage: str
    local_path: str
    sha256: str
    verification_status: str
    resolved_path: Path | None = None
    sha256_match: bool | None = None
    file_missing: bool = False
    extra: dict[str, str] = field(default_factory=dict)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_source_register(register_path: Path | None = None) -> list[SourceRegisterRow]:
    register_path = Path(register_path or DEFAULT_REGISTER)
    if not register_path.is_file():
        raise SourceRegisterError(f"missing register: {register_path}")
    rows: list[SourceRegisterRow] = []
    with open(register_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise SourceRegisterError("register has no header row")
        missing_cols = [c for c in REGISTER_COLUMNS if c not in reader.fieldnames]
        if missing_cols:
            raise SourceRegisterError(f"register schema missing columns: {missing_cols}")
        for raw in reader:
            sid = (raw.get("source_id") or "").strip()
            if not sid:
                continue
            lp = (raw.get("local_path") or "").strip()
            want = (raw.get("sha256") or "").strip().lower()
            rows.append(
                SourceRegisterRow(
                    source_id=sid,
                    component=(raw.get("component") or "").strip(),
                    title=(raw.get("title") or "").strip(),
                    vintage=(raw.get("vintage") or "").strip(),
                    local_path=lp,
                    sha256=want,
                    verification_status=(raw.get("verification_status") or "").strip(),
                    extra={k: (raw.get(k) or "").strip() for k in raw if k not in REGISTER_COLUMNS},
                )
            )
    return rows


def _register_index(register_path: Path | None = None) -> dict[str, SourceRegisterRow]:
    rows = load_source_register(register_path)
    by_id = {r.source_id: r for r in rows}
    if len(by_id) != len(rows):
        raise SourceRegisterError("duplicate source_id in register")
    return by_id


def validate_required_source_pins_or_abort(
    source_ids: list[str],
    *,
    register_path: Path | None = None,
) -> dict[str, str]:
    """
    Fail closed: every listed source_id must exist on disk and match register sha256.
    Only the requested ids are checked (unrelated missing register rows do not block).
    """
    if not source_ids:
        raise SourceRegisterError("validate_required_source_pins_or_abort requires at least one source_id")
    by_id = _register_index(register_path)
    verified: dict[str, str] = {}
    for sid in source_ids:
        if sid not in by_id:
            raise SourceRegisterAbortError(f"required source_id not in register: {sid}")
        row = by_id[sid]
        if not row.sha256 or len(row.sha256) != 64:
            raise SourceRegisterAbortError(f"{sid}: required pin has no sha256 in register")
        if not row.local_path:
            raise SourceRegisterAbortError(f"{sid}: required pin missing local_path in register")
        resolved = resolve_register_local_path(row.local_path)
        if resolved is None or not resolved.is_file():
            raise SourceRegisterAbortError(
                f"{sid}: required source file missing; set HESI_DATA_ROOT "
                f"(register local_path={row.local_path!r})"
            )
        got = _sha256_file(resolved)
        want = row.sha256.lower()
        if got != want:
            raise SourceRegisterAbortError(
                f"{sid}: sha256 mismatch at {resolved} got={got} want={want}"
            )
        verified[sid] = got
    return verified


def validate_source_register_or_abort(
    source_ids: list[str],
    *,
    register_path: Path | None = None,
) -> dict[str, str]:
    """Alias for fail-closed validation of an explicit required-source subset."""
    return validate_required_source_pins_or_abort(source_ids, register_path=register_path)


def validate_source_register(
    register_path: Path | None = None,
    *,
    verify_bytes: bool = True,
) -> dict[str, Any]:
    """Validate register schema; verify paths and SHA-256 when files exist. Never invent bytes."""
    rows = load_source_register(register_path)
    by_id = {r.source_id: r for r in rows}
    if len(by_id) != len(rows):
        raise SourceRegisterError("duplicate source_id in register")

    verified: list[str] = []
    missing_path: list[str] = []
    no_hash_expected: list[str] = []
    hash_mismatch: list[dict[str, str]] = []
    unverified_no_bytes: list[str] = []

    for row in rows:
        if row.verification_status == "UNVERIFIED" and not row.sha256:
            unverified_no_bytes.append(row.source_id)
            row.file_missing = True
            continue
        if not row.local_path:
            if row.sha256:
                missing_path.append(row.source_id)
            else:
                no_hash_expected.append(row.source_id)
            row.file_missing = True
            continue
        resolved = resolve_register_local_path(row.local_path)
        row.resolved_path = resolved
        if resolved is None or not resolved.is_file():
            missing_path.append(row.source_id)
            row.file_missing = True
            continue
        if not row.sha256 or len(row.sha256) != 64:
            raise SourceRegisterError(f"{row.source_id}: sha256 missing or not 64 hex chars")
        if verify_bytes:
            got = _sha256_file(resolved)
            row.sha256_match = got == row.sha256
            if row.sha256_match:
                verified.append(row.source_id)
            else:
                hash_mismatch.append(
                    {"source_id": row.source_id, "got": got, "want": row.sha256, "path": str(resolved)}
                )
        else:
            verified.append(row.source_id)

    return {
        "register_path": str((register_path or DEFAULT_REGISTER).resolve()),
        "row_count": len(rows),
        "verified_on_disk": verified,
        "missing_files": sorted(missing_path),
        "unverified_no_bytes": sorted(unverified_no_bytes),
        "hash_mismatches": hash_mismatch,
        "status": "PASS" if not hash_mismatch else "HASH_MISMATCH",
    }


def load_s3_bounded_source_ids() -> list[str]:
    data = json.loads(S3_LIST.read_text())
    ids = data.get("source_ids")
    if not isinstance(ids, list) or not ids:
        raise SourceRegisterError("s3_bounded_source_ids.json invalid")
    return [str(x) for x in ids]


def validate_s3_bounded_pins(register_path: Path | None = None) -> dict[str, Any]:
    """Report S-3 allowlisted sources: present/missing on this host (no substitution)."""
    rows = {r.source_id: r for r in load_source_register(register_path)}
    want_ids = load_s3_bounded_source_ids()
    detail: list[dict[str, Any]] = []
    present: list[str] = []
    missing: list[str] = []
    for sid in want_ids:
        row = rows.get(sid)
        if row is None:
            missing.append(sid)
            detail.append({"source_id": sid, "error": "not_in_register"})
            continue
        resolved = resolve_register_local_path(row.local_path) if row.local_path else None
        if resolved and resolved.is_file() and row.sha256:
            got = _sha256_file(resolved)
            ok = got == row.sha256
            if ok:
                present.append(sid)
            else:
                missing.append(sid)
            detail.append(
                {
                    "source_id": sid,
                    "path": str(resolved),
                    "sha256_match": ok,
                    "want": row.sha256,
                    "got": got if not ok else row.sha256,
                }
            )
        else:
            missing.append(sid)
            detail.append(
                {
                    "source_id": sid,
                    "register_local_path": row.local_path,
                    "resolved": str(resolved) if resolved else None,
                    "missing": True,
                }
            )
    return {
        "s3_allowlist_count": len(want_ids),
        "present_verified": present,
        "missing_or_unverified": missing,
        "detail": detail,
        "hesi_data_root": str(hesi_data_root()) if hesi_data_root() else None,
    }


def coverage_by_component(register_path: Path | None = None) -> dict[str, dict[str, int]]:
    report = validate_source_register(register_path, verify_bytes=False)
    rows = load_source_register(register_path)
    out: dict[str, dict[str, int]] = {}
    missing_set = set(report["missing_files"])
    verified_set = set(report.get("verified_on_disk", []))
    for row in rows:
        comp = row.component or "unknown"
        bucket = out.setdefault(comp, {"rows": 0, "on_disk_verified": 0, "missing": 0, "unverified_no_bytes": 0})
        bucket["rows"] += 1
        if row.source_id in missing_set:
            bucket["missing"] += 1
        elif row.source_id in verified_set:
            bucket["on_disk_verified"] += 1
        elif row.verification_status == "UNVERIFIED" and not row.sha256:
            bucket["unverified_no_bytes"] += 1
    return out
