
from source_analyzer import analyze_python_source
from space_analyzer import analyze_space_source


def analyze_program(source: str) -> dict:
    """Return time and space estimates for supported Python code."""

    time_result = analyze_python_source(source)
    space_result = analyze_space_source(source)

    return {
        "language": "python",
        "time_complexity": time_result["complexity"],
        "time_expression": time_result["expression"],
        "space_complexity": space_result["space_complexity"],
        "limitations": [
            "Results are estimates for the supported Python subset.",
            "Recursive calls and complex function calls are not fully analyzed.",
            "Space analysis only recognizes selected list allocations.",
        ],
    }
