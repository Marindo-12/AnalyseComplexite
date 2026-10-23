
import ast
import textwrap


def is_range_n(node: ast.AST) -> bool:
    """Return True only for the exact expression range(n)."""

    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "range"
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "n"
        and not node.keywords
    )


def analyze_space_source(source: str) -> dict:
    """
    Estimate auxiliary space for a limited subset of Python.

    Supported growing allocations:
    - list(range(n))
    - [expression for item in range(n)]
    """

    try:
        source = textwrap.dedent(source).strip()
        tree = ast.parse(source)
    except SyntaxError as error:
        raise ValueError(
            f"Invalid Python syntax: {error.msg}"
        ) from error

    for node in ast.walk(tree):
        # Example: numbers = list(range(n))
        if isinstance(node, ast.Call):
            is_list_call = (
                isinstance(node.func, ast.Name)
                and node.func.id == "list"
            )

            if is_list_call and (
                len(node.args) != 1 or node.keywords
            ):
                raise NotImplementedError(
                    "Only list(range(n)) is supported"
                )

            if is_list_call and is_range_n(node.args[0]):
                continue

            # Reject other list(...) calls instead of guessing their size.
            if is_list_call:
                raise NotImplementedError(
                    "Only list(range(n)) is supported"
                )

        # Example: numbers = [i for i in range(n)]
        if isinstance(node, ast.ListComp):
            supported_comprehension = (
                len(node.generators) == 1
                and is_range_n(node.generators[0].iter)
                and not node.generators[0].ifs
            )

            if not supported_comprehension:
                raise NotImplementedError(
                    "Only one-dimensional list comprehensions "
                    "over range(n), without filters, are supported"
                )

            continue

    grows_with_n = any(
        (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "list"
            and len(node.args) == 1
            and is_range_n(node.args[0])
        )
        or isinstance(node, ast.ListComp)
        for node in ast.walk(tree)
    )

    return {
        "space_complexity": "O(n)" if grows_with_n else "O(1)",
        "assumptions": [
            "n represents the input size",
            "only list(range(n)) and simple list comprehensions "
            "are recognized as growing allocations",
            "other supported statements are assumed to use constant "
            "additional space",
        ],
    }
