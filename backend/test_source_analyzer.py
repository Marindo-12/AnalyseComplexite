
import unittest

from source_analyzer import analyze_python_source


class TestSourceAnalyzer(unittest.TestCase):

    def test_constant_function(self):
        source = """
def example(n):
    return 10
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(1)")

    def test_linear_loop(self):
        source = """
def example(n):
    total = 0
    for i in range(n):
        total += i
    return total
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(n)")

    def test_nested_loops(self):
        source = """
def example(n):
    for i in range(n):
        for j in range(n):
            print(i, j)
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(n^2)")

    def test_invalid_syntax(self):
        with self.assertRaises(ValueError):
            analyze_python_source("def example(:\n    pass")

    def test_unsupported_if(self):
        source = """
def example(n):
    if n > 0:
        return n
"""
        with self.assertRaises(NotImplementedError):
            analyze_python_source(source)


if __name__ == "__main__":
    unittest.main()
