
import unittest

from cost_model import add_costs, multiply_by_n
from complexity import analyze_cost


class TestComplexityEngine(unittest.TestCase):

    def test_linear_algorithm(self):
        first = {0: 3, 1: 2}
        loop = multiply_by_n({0: 4})

        total = add_costs(first, loop)
        result = analyze_cost(total)

        self.assertEqual(result["expression"], "3 + 6n")
        self.assertEqual(result["complexity"], "O(n)")

    def test_nested_loops(self):
        outer_loop = multiply_by_n({0: 1})
        nested_loop = multiply_by_n(outer_loop)

        result = analyze_cost(nested_loop)

        self.assertEqual(result["complexity"], "O(n^2)")


if __name__ == "__main__":
    unittest.main()
