
import unittest

from space_analyzer import analyze_space_source


class TestSpaceAnalyzer(unittest.TestCase):

    def test_constant_auxiliary_space(self):
        source = """
def example(n):
    total = 0
    for i in range(n):
        total += i
    return total
"""
        result = analyze_space_source(source)
        self.assertEqual(result["space_complexity"], "O(1)")

    def test_list_range_n(self):
        source = """
def example(n):
    numbers = list(range(n))
    return numbers
"""
        result = analyze_space_source(source)
        self.assertEqual(result["space_complexity"], "O(n)")

    def test_list_comprehension(self):
        source = """
def example(n):
    numbers = [i for i in range(n)]
    return numbers
"""
        result = analyze_space_source(source)
        self.assertEqual(result["space_complexity"], "O(n)")

    def test_invalid_syntax(self):
        with self.assertRaises(ValueError):
            analyze_space_source("def example(:\n    pass")

    def test_unsupported_list_call(self):
        source = """
def example(n):
    numbers = list(get_values(n))
    return numbers
"""
        with self.assertRaises(NotImplementedError):
            analyze_space_source(source)


if __name__ == "__main__":
    unittest.main()
