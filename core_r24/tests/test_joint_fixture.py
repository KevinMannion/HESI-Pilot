import json,unittest
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parents[1]
class SyntheticEndToEnd(unittest.TestCase):
 def test_coverage_and_arithmetic(self):
  a=json.loads((P/'results/synthetic/audit.json').read_text())['frame']
  self.assertEqual(a['included_rows'],3)
  self.assertEqual(a['over4_excluded_rows'],1)
  self.assertEqual(a['infant_excluded_rows'],1)
  self.assertEqual(a['geography_excluded_rows'],1)
  self.assertEqual(a['composition_excluded_rows'],1)
  self.assertAlmostEqual(a['occupied_weight'],sum(a[k+'_weight'] for k in ['included','geography_excluded','composition_excluded','over4_excluded','infant_excluded']))
  r=pd.read_csv(P/'results/synthetic/common_cohort_results.csv').set_index('metric')
  self.assertAlmostEqual(r.loc['total_month_PROVISIONAL','mean'],r.loc['food_month','mean']+r.loc['housing_month','mean']+r.loc['one_vehicle_month_PROVISIONAL','mean'])
  self.assertTrue(r['se_sdr'].notna().all())
