"""Verify current package hashes, frozen scientific results vs historical lock, and pillar integrity."""
from pathlib import Path
import hashlib,json,subprocess,sys,os
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent

def digest(path):
 return hashlib.sha256(Path(path).read_bytes()).hexdigest()

files=json.loads((ROOT/'RELEASE_FILE_HASHES.json').read_text())
for rel,want in files.items():
 path=ROOT/rel
 if not path.is_file():raise SystemExit('MISSING FILE '+rel)
 got=digest(path)
 if got!=want:raise SystemExit('HASH MISMATCH '+rel+' (current package lock)')
print('PASS: all',len(files),'source/result package files match current RELEASE_FILE_HASHES.json')

historical=json.loads((ROOT/'historical_release_e45eb87/RELEASE_FILE_HASHES.json').read_text())
frozen_keys=[k for k in historical if k.startswith('results/') or k.startswith('inputs/')]
for rel in frozen_keys:
 want=historical[rel]
 got=digest(ROOT/rel)
 if got!=want:raise SystemExit('FROZEN SCIENTIFIC HASH DRIFT '+rel+' vs historical e45eb87 lock')
print('PASS: frozen inputs/results still match historical e45eb87 RELEASE_FILE_HASHES.json')

env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
integrity=subprocess.run([sys.executable,str(REPO/'research/september2026_core_r2/verify_integrity.py'),'--all'],cwd=REPO/'research/september2026_core_r2',env=env,capture_output=True,text=True)
print(integrity.stdout)
if integrity.returncode:raise SystemExit('PILLAR INTEGRITY FAIL\n'+integrity.stderr)
print('PASS: versioned pillar integrity manifests')
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-q'],cwd=ROOT,env=env,check=True)
subprocess.run([sys.executable,'reproduce_from_raw.py','--check-existing','results/rebuilt_from_raw'],cwd=ROOT,env=env,check=True)
print('PASS: regression tests and reproduced national results')
