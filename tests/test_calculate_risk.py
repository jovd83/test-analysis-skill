from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import calculate_risk


class CalculateRiskTests(unittest.TestCase):
    def test_build_result_for_high_risk(self) -> None:
        result = calculate_risk.build_result(8, 3)
        self.assertEqual(result["score"], 24)
        self.assertEqual(result["category"], "High")

    def test_build_result_for_critical_risk(self) -> None:
        result = calculate_risk.build_result(16, 4)
        self.assertEqual(result["score"], 64)
        self.assertEqual(result["category"], "Critical")

    def test_invalid_scale_raises(self) -> None:
        with self.assertRaises(ValueError):
            calculate_risk.build_result(3, 2)


if __name__ == "__main__":
    unittest.main()
