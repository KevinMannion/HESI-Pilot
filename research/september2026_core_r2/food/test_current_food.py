import unittest
from current_food import load,calculate,key
F=[{'age':35,'sex':'Male'},{'age':35,'sex':'Female'},{'age':7,'sex':'Male'},{'age':10,'sex':'Female'}]
class TestCurrent(unittest.TestCase):
 def test_complete(self):self.assertEqual(len(load()),60)
 def test_september_thrifty(self):self.assertAlmostEqual(calculate(F,'Thrifty')['cost_usd_monthly'],1023.90)
 def test_source_levels(self):
  expected={'Low-Cost':1126.90,'Moderate-Cost':1389.20,'Liberal':1681.80}
  for plan,x in expected.items():self.assertAlmostEqual(calculate(F,plan)['cost_usd_monthly'],x)
 def test_infant(self):
  with self.assertRaises(ValueError):calculate([{'age':0,'sex':'Female'}])
 def test_unsupported(self):
  with self.assertRaises(ValueError):calculate(F,'Undefined')
 def test_size(self):self.assertAlmostEqual(calculate([{'age':35,'sex':'Male'}],'Thrifty')['cost_usd_monthly'],382.8)
 def test_age19(self):self.assertEqual(key(19,'Male','Thrifty'),('Male','14-19 years'));self.assertEqual(key(19,'Male','Low-Cost'),('Male','19-50 years'))
if __name__=='__main__':unittest.main()
