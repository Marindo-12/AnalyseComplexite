
import unittest

from program_analyzer import analyze_program


class TestProgramAnalyzer(unittest.TestCase):

    def test_linear_time_and_linear_space(self):
        source = """
        def example(n):
            numbers = list(range(n))

            for i in range(n):
                print(numbers[i])

            return numbers
        """

        result = analyze_program(source)

        self.assertEqual(result["language"], "python")
        self.assertEqual(result["time_complexity"], "O(n)")
        self.assertEqual(result["space_complexity"], "O(n)")
        self.assertIn("time_expression", result)
        self.assertIn("limitations", result)

    def test_constant_space(self):
        source = """
        def example(n):
            total = 0

            for i in range(n):
                total += i

            return total
        """

        result = analyze_program(source)

        self.assertEqual(result["time_complexity"], "O(n)")
        self.assertEqual(result["space_complexity"], "O(1)")

    def test_invalid_python(self):
        source = "def example(:"

        with self.assertRaises(ValueError):
            analyze_program(source)


if __name__ == "__main__":
    unittest.main()
