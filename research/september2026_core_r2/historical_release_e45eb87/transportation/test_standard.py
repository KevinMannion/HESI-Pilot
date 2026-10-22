import unittest,csv,subprocess,sys
from pathlib import Path
B=Path(__file__).resolve().parent
class StandardTests(unittest.TestCase):
 def test_exec(self):
  subprocess.run([sys.executable,str(B/'run_standard.py')],check=True,capture_output=True)
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
