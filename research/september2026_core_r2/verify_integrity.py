"""Verify versioned integrity manifests against the tree they authenticate.

Never checks a historical manifest against current modified files.
A mismatch, missing/empty/malformed manifest, or empty register is FAIL.
No environment variable can skip these checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
REGISTER = BASE / "MANIFEST_REGISTER.json"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
BYPASS_ENV = ("HESI_SKIP_INTEGRITY", "HESI_SKIP_HASH", "HESI_ALLOW_MANIFEST_BYPASS")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def refuse_bypass():
    hits = [k for k in BYPASS_ENV if os.environ.get(k)]
    if hits:
        raise SystemExit("INTEGRITY FAIL: unauthorized bypass environment set: " + ",".join(hits))


def load_json_object(path, label):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"MISSING {label}: {path}")
    raw = path.read_text()
    if not raw.strip():
        raise ValueError(f"EMPTY {label}: {path}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"MALFORMED {label}: {path}: {exc}") from exc
    if not isinstance(data, dict) or not data:
        raise ValueError(f"EMPTY OR NON-OBJECT {label}: {path}")
    return data


def file_map(man):
    files = man["files"] if "files" in man else man
    if not isinstance(files, dict) or not files:
        raise ValueError("manifest files map is empty")
    skip_keys = {"authenticates", "manifest_id", "historical_predecessor", "note", "title", "original_packages"}
    out = {}
    for rel, want in files.items():
        if rel in skip_keys or not isinstance(want, str):
            continue
        if not HASH_RE.match(want):
            raise ValueError(f"malformed hash for {rel}: {want!r}")
        out[rel] = want
    if not out:
        raise ValueError("manifest contains no file hashes")
    return out


def resolve_file(rel, overlay, root):
    tree = Path(root) / rel
    if overlay:
        snapped = Path(overlay) / rel
        if snapped.is_file():
            return snapped, "overlay"
        if tree.is_file():
            return tree, "working_tree_unchanged_candidate"
        return snapped, "missing"
    if tree.is_file():
        return tree, "working_tree"
    return tree, "missing"


def check_manifest(manifest_path, overlay=None, root=None):
    root = Path(root) if root else BASE
    failed = []
    try:
        man = load_json_object(manifest_path, "manifest")
        files = file_map(man)
    except ValueError as exc:
        return {
            "manifest": str(Path(manifest_path).name),
            "overlay": str(overlay) if overlay else "working_tree",
            "root": str(root),
            "checked": 0,
            "failed": [{"file": str(manifest_path), "error": str(exc)}],
            "status": "FAIL",
        }
    checked = 0
    for rel, want in files.items():
        path, source = resolve_file(rel, overlay, root)
        if source == "missing" or not path.is_file():
            failed.append({"file": rel, "error": "MISSING", "path": str(path)})
            continue
        got = sha256(path)
        if source == "working_tree_unchanged_candidate" and got != want:
            failed.append(
                {
                    "file": rel,
                    "error": "DRIFTED FILE NOT IN HISTORICAL OVERLAY",
                    "expected": want,
                    "got": got,
                    "path": str(path),
                }
            )
            continue
        checked += 1
        if got != want:
            failed.append({"file": rel, "error": "HASH MISMATCH", "expected": want, "got": got, "path": str(path), "source": source})
    return {
        "manifest": str(Path(manifest_path).name),
        "overlay": str(overlay) if overlay else "working_tree",
        "root": str(root),
        "checked": checked,
        "failed": failed,
        "status": "FAIL" if failed else "PASS",
    }


def load_register():
    return load_json_object(REGISTER, "MANIFEST_REGISTER.json")


def check_registered():
    try:
        reg = load_register()
    except ValueError as exc:
        return {"status": "FAIL", "reports": [{"id": "register", "status": "FAIL", "failed": [{"error": str(exc)}]}]}
    manifests = reg.get("manifests")
    if not isinstance(manifests, list) or not manifests:
        return {"status": "FAIL", "reports": [{"id": "register", "status": "FAIL", "failed": [{"error": "manifests list missing or empty"}]}]}
    reports = []
    for entry in manifests:
        overlay = (BASE / entry["overlay"]).resolve() if entry.get("overlay") else None
        root = (BASE / entry["root"]).resolve() if entry.get("root") else BASE
        reports.append(
            {
                **check_manifest(BASE / entry["path"], overlay, root),
                "id": entry.get("id"),
                "authenticates": entry.get("authenticates"),
            }
        )
    status = "PASS" if all(r["status"] == "PASS" for r in reports) else "FAIL"
    return {"status": status, "reports": reports}


def check_unapproved_locked_script_edits():
    try:
        reg = load_register()
        v1 = file_map(load_json_object(BASE / "INTEGRITY_MANIFEST.json", "INTEGRITY_MANIFEST.json"))
        v2 = file_map(load_json_object(BASE / "INTEGRITY_MANIFEST.v2.json", "INTEGRITY_MANIFEST.v2.json"))
    except ValueError as exc:
        return {"status": "FAIL", "problems": [{"error": str(exc)}]}
    documented = {c["file"]: c for c in reg.get("documented_working_tree_changes", [])}
    problems = []
    for rel, old in v1.items():
        current = sha256(BASE / rel)
        if current == old:
            continue
        if rel not in documented:
            problems.append({"file": rel, "error": "modified without MANIFEST_REGISTER documented_working_tree_changes"})
            continue
        if v2.get(rel) != current:
            problems.append({"file": rel, "error": "working tree hash is not INTEGRITY_MANIFEST.v2.json", "got": current, "v2": v2.get(rel)})
    return {"status": "FAIL" if problems else "PASS", "problems": problems}


def main():
    refuse_bypass()
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true")
    a = p.parse_args()
    if not a.all:
        a.all = True
    body = check_registered()
    edits = check_unapproved_locked_script_edits()
    out = {"registered_manifests": body, "unapproved_locked_edits": edits}
    print(json.dumps(out, indent=2))
    if body["status"] != "PASS" or edits["status"] != "PASS":
        raise SystemExit("INTEGRITY FAIL")
    print("PASS: all registered integrity manifests and locked-script policy")


if __name__ == "__main__":
    main()
