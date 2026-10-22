"""Run live synthetic run_joint.py under two Python interpreters (NumPy 1.x and 2.x)."""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "tests" / "test_run_joint_synthetic.py"

def main():
    py126 = os.environ.get("HESI_PYTHON_NUMPY126", "/Users/kevinmannion/HESI-R25-CleanRepro/venv/bin/python")
    py2 = os.environ.get("HESI_PYTHON_NUMPY2", "/Users/kevinmannion/HESI-Pilot/.venv/bin/python")
    results = []
    for label, exe in [("numpy1", py126), ("numpy2", py2)]:
        if not Path(exe).exists():
            results.append({"label": label, "executable": exe, "status": "MISSING_INTERPRETER"})
            continue
        ver = subprocess.check_output([exe, "-c", "import numpy; print(numpy.__version__)"], text=True).strip()
        proc = subprocess.run([exe, "-m", "unittest", "tests.test_run_joint_synthetic", "-v"], cwd=ROOT)
        results.append({"label": label, "executable": exe, "numpy": ver, "returncode": proc.returncode, "status": "PASS" if proc.returncode == 0 else "FAIL"})
    print(json.dumps(results, indent=2))
    if any(r["status"] != "PASS" for r in results):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
