"""Verify all packaged files and tests. For full raw replication run reproduce_from_raw.py."""
from pathlib import Path
import hashlib,json,subprocess,sys,os
ROOT=Path(__file__).resolve().parent
files=json.loads((ROOT/'RELEASE_FILE_HASHES.json').read_text())
for rel,want in files.items():
 path=ROOT/rel
 if not path.is_file():raise SystemExit('MISSING FILE '+rel)
 got=hashlib.sha256(path.read_bytes()).hexdigest()
 if got!=want:raise SystemExit('HASH MISMATCH '+rel)
print('PASS: all',len(files),'source/result package files match release hashes')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-q'],cwd=ROOT,env=env,check=True)
subprocess.run([sys.executable,'reproduce_from_raw.py','--check-existing','results/rebuilt_from_raw'],cwd=ROOT,env=env,check=True)
print('PASS: regression tests and reproduced national results')
