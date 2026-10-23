
def validate_cost(cost: dict[int, float]) -> None:
    """Verify that a cost is a valid polynomial representation."""

    if not isinstance(cost, dict):
        raise TypeError("Cost must be a dictionary")

    for exponent, coefficient in cost.items():
        if type(exponent) is not int or exponent < 0:
            raise ValueError("Exponents must be non-negative integers")

        if not isinstance(coefficient, (int, float)):
            raise TypeError("Coefficients must be numbers")

        if coefficient < 0:
            raise ValueError("Cost coefficients must be non-negative")


def add_costs(
    first: dict[int, float],
    second: dict[int, float]
) -> dict[int, float]:
    """Add the costs of two sequential parts of an algorithm."""

    validate_cost(first)
    validate_cost(second)

    result = first.copy()

    for exponent, coefficient in second.items():
        result[exponent] = result.get(exponent, 0) + coefficient

    # Remove terms whose coefficients are zero.
    return {
        exponent: coefficient
        for exponent, coefficient in result.items()
        if coefficient != 0
    }


def multiply_by_n(cost: dict[int, float]) -> dict[int, float]:
    """Represent a cost repeated n times."""

    validate_cost(cost)

    # Multiplication by n increases every exponent by one.
    return {
        exponent + 1: coefficient
        for exponent, coefficient in cost.items()
        if coefficient != 0
    }


def scale_cost(
    cost: dict[int, float],
    factor: int
) -> dict[int, float]:
    """Multiply every polynomial coefficient by a non-negative constant."""

    validate_cost(cost)

    if type(factor) is not int or factor < 0:
        raise ValueError("Factor must be a non-negative integer")

    return {
        exponent: coefficient * factor
        for exponent, coefficient in cost.items()
        if coefficient != 0 and factor != 0
    }
