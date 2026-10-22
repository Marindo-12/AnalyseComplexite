
import ast

from cost_model import add_costs, multiply_by_n
from complexity import analyze_cost


CONSTANT_COST = {0: 1}


def analyze_statements(statements: list[ast.stmt]) -> dict[int, float]:
    """Estimate the combined cost of a sequence of supported statements."""

    total_cost: dict[int, float] = {}

    for statement in statements:
        statement_cost = analyze_statement(statement)
        total_cost = add_costs(total_cost, statement_cost)

    return total_cost


def worst_case_cost(
    first: dict[int, float],
    second: dict[int, float]
) -> dict[int, float]:
    """Choose the branch with the greater polynomial cost."""

    exponents = sorted(set(first) | set(second), reverse=True)

    for exponent in exponents:
        first_coefficient = first.get(exponent, 0)
        second_coefficient = second.get(exponent, 0)

        if first_coefficient > second_coefficient:
            return first.copy()

        if second_coefficient > first_coefficient:
            return second.copy()

    return first.copy()



def analyze_statement(statement: ast.stmt) -> dict[int, float]:
    """Estimate the cost of one supported Python statement."""

    # A function definition is analyzed through its body.
    if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return analyze_statements(statement.body)

    # Simple statements are treated as constant-time operations.
    if isinstance(
        statement,
        (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Expr, ast.Return, ast.Pass),
    ):
        return CONSTANT_COST.copy()

    
    if isinstance(statement, ast.If):
        then_cost = analyze_statements(statement.body)
        else_cost = analyze_statements(statement.orelse)

        branch_cost = worst_case_cost(then_cost, else_cost)

        # The condition is assumed to take constant time.
        return add_costs(CONSTANT_COST, branch_cost)


    # Initially, support only: for i in range(n)
    if isinstance(statement, ast.For):
        iterator = statement.iter

        supported_loop = (
            isinstance(iterator, ast.Call)
            and isinstance(iterator.func, ast.Name)
            and iterator.func.id == "range"
            and len(iterator.args) == 1
            and isinstance(iterator.args[0], ast.Name)
            and iterator.args[0].id == "n"
            and not iterator.keywords
        )

        if not supported_loop:
            raise NotImplementedError(
                "Currently supported loop syntax: for i in range(n)"
            )

        body_cost = analyze_statements(statement.body)

        # Each iteration has an overhead, even if the body is empty.
        per_iteration_cost = add_costs(body_cost, CONSTANT_COST)

        # The loop repeats its body n times.
        repeated_cost = multiply_by_n(per_iteration_cost)

        # Add a constant cost for loop initialization/setup.
        return add_costs(CONSTANT_COST, repeated_cost)

    raise NotImplementedError(
        f"Unsupported Python statement: {type(statement).__name__}"
    )


def analyze_python_source(source: str) -> dict:
    """Parse Python source and estimate its polynomial time complexity."""

    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise ValueError(f"Invalid Python syntax: {error.msg}") from error

    cost = analyze_statements(tree.body)
    result = analyze_cost(cost)

    return {
        "expression": result["expression"],
        "complexity": result["complexity"],
        "cost_model": cost,
    }
