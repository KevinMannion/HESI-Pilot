import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import policyengine_us  # noqa: F401

    HAS_PE = True
except ImportError:
    HAS_PE = False


@unittest.skipUnless(HAS_PE, "policyengine-us not installed in this environment")
class PolicyEngineTy2026(unittest.TestCase):
    def test_synthetic_ca_ty2026(self):
        from resources.policyengine_ty2026 import calculate_ty2026_synthetic

        out = calculate_ty2026_synthetic(
            {"state_code": "CA", "age": 35, "employment_income": 50000}
        )
        self.assertEqual(out.employment_income, 50000.0)
        self.assertGreater(out.income_tax, 0)
        self.assertGreaterEqual(out.adjusted_gross_income_person, out.employment_income - 1)


class PolicyEngineImportGuard(unittest.TestCase):
    def test_module_import_without_policyengine(self):
        spec = importlib.util.find_spec("resources.policyengine_ty2026")
        self.assertIsNotNone(spec)


if __name__ == "__main__":
    unittest.main()
