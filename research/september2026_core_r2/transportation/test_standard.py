import unittest,csv,subprocess,sys,hashlib
from pathlib import Path
from run_standard import compute_scenarios
B=Path(__file__).resolve().parent
LOCKED='19cc412e1d13662782ee57315f148f0a2187e1fd1613052c3aebd3397a687af6'
class StandardTests(unittest.TestCase):
 def test_exec(self):
  before=hashlib.sha256((B/'transport_reference_2026_09.csv').read_bytes()).hexdigest()
  subprocess.run([sys.executable,str(B/'run_standard.py')],check=True,capture_output=True)
  after=hashlib.sha256((B/'transport_reference_2026_09.csv').read_bytes()).hexdigest()
  self.assertEqual(before,after)
  self.assertEqual(after,LOCKED)
  self.assertEqual(len(compute_scenarios()),3)
 def test_baseline_mileage(self):
  with (B/'transport_reference_2026_09.csv').open() as f:r={x['scenario']:x for x in csv.DictReader(f)}
  self.assertEqual(int(r['reference']['annual_miles']),12000)
  self.assertAlmostEqual(float(r['reference']['fuel_annual']),1633.03,places=2)
 def test_sensitivity(self):
  with (B/'transport_reference_2026_09.csv').open() as f:r={x['scenario']:x for x in csv.DictReader(f)}
  self.assertLess(float(r['low_mileage']['annual']),float(r['reference']['annual']))
  self.assertLess(float(r['reference']['annual']),float(r['high_mileage']['annual']))
 def test_status(self):
  with (B/'transport_reference_2026_09.csv').open() as f:r=list(csv.DictReader(f))
  self.assertTrue(all(x['status']=='hypothetical_sensitivity_only' for x in r))
if __name__=='__main__':unittest.main()
