
import unittest

from complexity import complexity_class


class TestComplexityClass(unittest.TestCase):

    def test_constant(self):
        self.assertEqual(complexity_class({0: 7}), "O(1)")

    def test_linear(self):
        self.assertEqual(complexity_class({0: 5, 1: 3}), "O(n)")

    def test_quadratic(self):
        self.assertEqual(
            complexity_class({0: 1, 1: 4, 2: 2}),
            "O(n^2)"
        )

    def test_cubic(self):
        self.assertEqual(
            complexity_class({1: 100, 2: 50, 3: 4}),
            "O(n^3)"
        )

    def test_zero_coefficient(self):
        self.assertEqual(
            complexity_class({0: 5, 1: 3, 3: 0}),
            "O(n)"
        )

    def test_all_zero(self):
        self.assertEqual(complexity_class({0: 0, 2: 0}), "O(1)")

    def test_negative_coefficient(self):
        with self.assertRaises(ValueError):
            complexity_class({1: -2})

    def test_invalid_exponent(self):
        with self.assertRaises(ValueError):
            complexity_class({-1: 5})


if __name__ == "__main__":
    unittest.main()
