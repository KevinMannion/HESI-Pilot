import unittest
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parents[1]
class TestHousingMapping(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=pd.read_csv(P/'inputs/puma_fmr_screened.csv')
 def test_nonempty(self):self.assertGreater(len(self.d),100)
 def test_required_columns(self):
  for n in ['puma_geoid','status']+[f'monthly_{i}br_benchmark' for i in range(5)]:self.assertIn(n,self.d.columns)
 def test_unambiguous_price_nonnegative(self):
  x=self.d[self.d.status.eq('COMPLETE_UNAMBIGUOUS')]
  self.assertGreater(len(x),100)
  for i in range(5):self.assertTrue(x[f'monthly_{i}br_benchmark'].gt(0).all())
