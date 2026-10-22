"""Verify provenance, source consistency, versioned integrity manifests, and pillar unit tests."""
import json,pathlib,subprocess,sys
BASE=pathlib.Path(__file__).resolve().parent
integrity=subprocess.run([sys.executable,str(BASE/'verify_integrity.py'),'--all'],cwd=BASE,capture_output=True,text=True,timeout=60)
print(integrity.stdout)
if integrity.returncode:
 print('FAILED integrity manifests',integrity.stderr,file=sys.stderr)
 sys.exit(1)
checks=[('integrity_versioning',['-m','unittest','-v','test_integrity_versioning.py']),('food', ['-m','unittest','-v','test_current_food.py']),('housing',['-m','unittest','-v','test_adequacy.py','test_reference.py']),('transportation',['-m','unittest','discover','-s','.','-p','test_*.py','-v'])]
results={'integrity_manifests':{'passed':True}}
for pillar,cmd in checks:
 cwd=BASE if pillar=='integrity_versioning' else BASE/pillar
 p=subprocess.run([sys.executable,*cmd],cwd=cwd,capture_output=True,text=True,timeout=120)
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
