"""Load and fail-closed-validate official research-run configuration JSON."""
from __future__ import annotations

import json
from pathlib import Path

REQUIRED_TOP = (
    "run_class",
    "engine",
    "model_vintage",
    "scientific_publication",
    "share_metric",
    "required_input_sha256",
    "transport_annual_usd",
    "forbidden_output_paths",
    "notes",
)


def load_official_config(path, *, engine, model_vintage):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"official --config missing: {path}")
    raw = path.read_text()
    if not raw.strip():
        raise ValueError(f"official --config is empty: {path}")
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"official --config is not JSON: {path}: {exc}") from exc
    if not isinstance(cfg, dict) or not cfg:
        raise ValueError(f"official --config must be a non-empty JSON object: {path}")
    missing = [k for k in REQUIRED_TOP if k not in cfg]
    if missing:
        raise ValueError(f"official --config missing keys {missing}: {path}")
    if cfg["run_class"] != "official":
        raise ValueError("official --config run_class must be 'official'")
    if cfg["engine"] != engine:
        raise ValueError(f"official --config engine {cfg['engine']!r} != {engine!r}")
    if cfg["model_vintage"] != model_vintage:
        raise ValueError(
            f"--model-vintage {model_vintage!r} does not match config {cfg['model_vintage']!r}"
        )
    if cfg["scientific_publication"] != "NO-GO":
        raise ValueError("official --config must keep scientific_publication=NO-GO")
    hashes = cfg["required_input_sha256"]
    if not isinstance(hashes, dict) or not hashes:
        raise ValueError("official --config required_input_sha256 must be a non-empty object")
    for key, value in hashes.items():
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError(f"official --config hash {key} is not lowercase sha256")
    if not isinstance(cfg["forbidden_output_paths"], list) or not cfg["forbidden_output_paths"]:
        raise ValueError("official --config forbidden_output_paths must be a non-empty list")
    return cfg
