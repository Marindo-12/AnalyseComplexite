
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

    def test_if_is_supported(self):
      source = """
  def example(n):
      if n > 0:
          return n
  """
      result = analyze_python_source(source)

      self.assertEqual(result["complexity"], "O(1)")
            
    
    def test_if_with_linear_branch(self):
        source = """
def example(n):
    if n > 0:
        for i in range(n):
            print(i)
    else:
        print("empty")
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(n)")

    def test_if_else_with_two_different_costs(self):
        source = """
def example(n):
    if n > 0:
        for i in range(n):
            for j in range(n):
                print(i, j)
    else:
        for i in range(n):
            print(i)
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(n^2)")

    def test_if_with_constant_branches(self):
        source = """
def example(n):
    if n > 0:
        print("positive")
    else:
        print("not positive")
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(1)")



if __name__ == "__main__":
    unittest.main()
    
    
    def test_range_with_constant_bound(self):
        source = """
def example(n):
    for i in range(100):
        print(i)
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(1)")

    def test_range_with_start_and_variable_stop(self):
        source = """
def example(n):
    for i in range(1, n):
        print(i)
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(n)")

    def test_range_with_step_two(self):
        source = """
def example(n):
    for i in range(0, n, 2):
        print(i)
"""
        result = analyze_python_source(source)
        self.assertEqual(result["complexity"], "O(n)")

    def test_range_with_invalid_step(self):
        source = """
def example(n):
    for i in range(0, n, 0):
        print(i)
"""
        with self.assertRaises(NotImplementedError):
            analyze_python_source(source)

