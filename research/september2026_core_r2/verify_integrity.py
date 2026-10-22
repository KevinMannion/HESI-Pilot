"""Verify versioned integrity manifests against the tree they authenticate.

Never checks a historical manifest against current modified files.
A mismatch is an explicit FAIL.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
REGISTER = BASE / "MANIFEST_REGISTER.json"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_file(rel, overlay, root):
    """Historical overlays supply drifted files. Unchanged files may come from root.

    Never hash a drifted working-tree file under a historical expected hash.
    """
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
    man = json.loads(Path(manifest_path).read_text())
    files = man["files"] if "files" in man else man
    failed = []
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
    return json.loads(REGISTER.read_text())


def check_registered():
    reg = load_register()
    reports = []
    for entry in reg["manifests"]:
        overlay = (BASE / entry["overlay"]).resolve() if entry.get("overlay") else None
        root = (BASE / entry["root"]).resolve() if entry.get("root") else BASE
        reports.append(
            {
                **check_manifest(BASE / entry["path"], overlay, root),
                "id": entry["id"],
                "authenticates": entry["authenticates"],
            }
        )
    status = "PASS" if all(r["status"] == "PASS" for r in reports) else "FAIL"
    return {"status": status, "reports": reports}


def check_unapproved_locked_script_edits():
    """FAIL if a v1-locked file changed on disk without a v2 hash and register note."""
    reg = load_register()
    documented = {c["file"]: c for c in reg.get("documented_working_tree_changes", [])}
    v1 = json.loads((BASE / "INTEGRITY_MANIFEST.json").read_text())["files"]
    v2 = json.loads((BASE / "INTEGRITY_MANIFEST.v2.json").read_text())["files"]
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
