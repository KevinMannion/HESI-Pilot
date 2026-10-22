"""SHA-256 plus key-sorted semantic comparison of CSV tables."""
import csv, hashlib, json
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _num(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return value

def compare_csv(reference, candidate, key_fields, numeric_fields, atol=1e-9):
    ref = Path(reference)
    cand = Path(candidate)
    report = {
        "reference": str(ref),
        "candidate": str(cand),
        "reference_sha256": sha256(ref),
        "candidate_sha256": sha256(cand),
        "hash_match": False,
        "row_count_reference": 0,
        "row_count_candidate": 0,
        "key_mismatches": [],
        "value_mismatches": [],
        "status": "FAIL",
    }
    report["hash_match"] = report["reference_sha256"] == report["candidate_sha256"]
    with ref.open(newline="") as f:
        ref_rows = list(csv.DictReader(f))
    with cand.open(newline="") as f:
        cand_rows = list(csv.DictReader(f))
    report["row_count_reference"] = len(ref_rows)
    report["row_count_candidate"] = len(cand_rows)
    def key(row):
        return tuple(str(row.get(k, "")) for k in key_fields)
    ref_map = {key(r): r for r in ref_rows}
    cand_map = {key(r): r for r in cand_rows}
    only_ref = sorted(set(ref_map) - set(cand_map))
    only_cand = sorted(set(cand_map) - set(ref_map))
    report["keys_only_in_reference"] = len(only_ref)
    report["keys_only_in_candidate"] = len(only_cand)
    report["key_mismatches"] = [
        {"where": "reference_only", "key": list(k)} for k in only_ref[:20]
    ] + [
        {"where": "candidate_only", "key": list(k)} for k in only_cand[:20]
    ]
    for k in sorted(set(ref_map) & set(cand_map)):
        a, b = ref_map[k], cand_map[k]
        for field in numeric_fields:
            av, bv = _num(a.get(field)), _num(b.get(field))
            if av is None and bv is None:
                continue
            if isinstance(av, float) and isinstance(bv, float):
                if abs(av - bv) > atol:
                    report["value_mismatches"].append(
                        {"key": list(k), "field": field, "reference": av, "candidate": bv, "diff": bv - av}
                    )
            elif av != bv:
                report["value_mismatches"].append(
                    {"key": list(k), "field": field, "reference": av, "candidate": bv}
                )
        if len(report["value_mismatches"]) >= 50:
            break
    material = only_ref or only_cand or report["value_mismatches"]
    report["status"] = "PASS" if not material else "FAIL"
    report["hash_mismatch_without_semantic_diff"] = report["hash_match"] is False and not material
    return report

def write_report(report, path):
    Path(path).write_text(json.dumps(report, indent=2) + "\n")
    return report
