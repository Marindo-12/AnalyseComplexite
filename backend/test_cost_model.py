
import unittest

from cost_model import add_costs, multiply_by_n


class TestCostModel(unittest.TestCase):

    def test_add_costs(self):
        first = {0: 3, 1: 2}
        second = {0: 5, 1: 4}

        self.assertEqual(
            add_costs(first, second),
            {0: 8, 1: 6}
        )

    def test_add_different_exponents(self):
        self.assertEqual(
            add_costs({0: 1, 2: 3}, {1: 2}),
            {0: 1, 2: 3, 1: 2}
        )

    def test_multiply_by_n(self):
        self.assertEqual(
            multiply_by_n({0: 5, 1: 3}),
            {1: 5, 2: 3}
        )

    def test_multiply_constant_by_n(self):
        self.assertEqual(
            multiply_by_n({0: 7}),
            {1: 7}
        )

    def test_zero_cost(self):
        self.assertEqual(multiply_by_n({0: 0}), {})

    def test_negative_coefficient(self):
        with self.assertRaises(ValueError):
            add_costs({1: -2}, {0: 1})


if __name__ == "__main__":
    unittest.main()
