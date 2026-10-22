"""Verify provenance, source consistency and all pillar unit tests in release."""
import json,hashlib,pathlib,subprocess,sys
BASE=pathlib.Path(__file__).resolve().parent
checks=[('food', ['-m','unittest','-v','test_current_food.py']),('housing',['-m','unittest','-v','test_adequacy.py','test_reference.py']),('transportation',['-m','unittest','discover','-s','.','-p','test_*.py','-v'])]
results={}
for pillar,cmd in checks:
 p=subprocess.run([sys.executable,*cmd],cwd=BASE/pillar,capture_output=True,text=True,timeout=120)
 results[pillar]={'passed':p.returncode==0,'output_tail':(p.stdout+'\n'+p.stderr)[-3000:]}
 if p.returncode:print(f'FAILED {pillar}: {p.stderr}',file=sys.stderr)
lock=json.loads((BASE/'LOCK_REGISTER.json').read_text())
assert set(lock['pillars'])=={'food','housing','transportation'}
assert all(lock['pillars'][p]['specification_locked'] for p in lock['pillars'])
assert not any(lock['pillars'][p]['full_national_scientific_approval'] for p in lock['pillars'])
assert lock['pillars']['transportation']['reference_miles_per_year']==12000
results['release_register']={'passed':True}
print(json.dumps({k:v['passed'] for k,v in results.items()},indent=2))
if not all(v['passed'] for v in results.values()):sys.exit(1)
