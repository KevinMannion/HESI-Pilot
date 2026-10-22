import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import unittest
from pathlib import Path
from food_model import *
P=Path(__file__).resolve().parents[1]/'inputs/source_2024_2026.csv'
class TestFood(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data,cls.issues=load_prices(P)
 def test_reference_family_september_2026(self):
  people=[{'age':35,'sex':'Male'},{'age':35,'sex':'Female'},{'age':7},{'age':10}]
  self.assertAlmostEqual(monthly_cost(self.data,2026,9,'Thrifty',people),1024.0,delta=0.11)
 def test_2024_full_year_all_plans(self):
  people=[{'age':35,'sex':'Male'},{'age':35,'sex':'Female'},{'age':7},{'age':10}]
  for plan in ['Thrifty','Low-Cost','Moderate-Cost','Liberal']:
   self.assertEqual(len(period_cost(self.data,2024,range(1,13),plan,people)['monthly_costs']),12)
 def test_age_zero_rejected(self):
  with self.assertRaises(ValueError):monthly_cost(self.data,2024,1,'Thrifty',[{'age':0}])
 def test_missing_2026_december_rejected(self):
  with self.assertRaises(ValueError):monthly_cost(self.data,2026,12,'Liberal',[{'age':35,'sex':'Male'}])
 def test_household_adjustment(self):
  base=self.data[(2024,1,'thrifty','Male','20-50 years')]
  self.assertEqual(monthly_cost(self.data,2024,1,'Thrifty',[{'age':35,'sex':'Male'}]),round(base*1.2,2))
 def test_duplicate_months_rejected(self):
  with self.assertRaises(ValueError):period_cost(self.data,2024,[1,1],'Thrifty',[{'age':35,'sex':'Male'}])
 def test_age_boundary_distinction(self):
  self.assertEqual(age_key(19,'Male','thrifty'),('Male','14-19 years'))
  self.assertEqual(age_key(19,'Male','low-cost'),('Male','19-50 years'))
if __name__=='__main__':unittest.main()
