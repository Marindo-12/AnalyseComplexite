
def complexity_class(terms: dict[int, float]) -> str:
    """
    Determine the Big O class of a polynomial cost expression.

    terms maps:
        exponent -> coefficient

    Example:
        {0: 5, 1: 3, 2: 2}
        represents T(n) = 5 + 3n + 2n²
    """

    if not isinstance(terms, dict):
        raise TypeError("terms must be a dictionary")

    for exponent, coefficient in terms.items():
        if type(exponent) is not int or exponent < 0:
            raise ValueError("Exponents must be non-negative integers")

        if not isinstance(coefficient, (int, float)):
            raise TypeError("Coefficients must be numbers")

        if coefficient < 0:
            raise ValueError("Cost coefficients must be non-negative")

    # Keep only terms with non-zero coefficients.
    active_exponents = [
        exponent
        for exponent, coefficient in terms.items()
        if coefficient != 0
    ]

    # No growing term: the cost is constant (or zero).
    if not active_exponents:
        return "O(1)"

    # The highest exponent determines the polynomial's growth.
    degree = max(active_exponents)

    if degree == 0:
        return "O(1)"

    if degree == 1:
        return "O(n)"

    return f"O(n^{degree})"


def analyze_cost(cost: dict[int, float]) -> dict:
    """Return the polynomial cost and its Big O classification."""

    complexity = complexity_class(cost)

    # Build a readable polynomial representation.
    terms = []

    for exponent in sorted(cost):
        coefficient = cost[exponent]

        if coefficient == 0:
            continue

        if exponent == 0:
            terms.append(str(coefficient))
        elif exponent == 1:
            terms.append(f"{coefficient}n")
        else:
            terms.append(f"{coefficient}n^{exponent}")

    expression = " + ".join(terms) if terms else "0"

    return {
        "expression": expression,
        "complexity": complexity,
    }
