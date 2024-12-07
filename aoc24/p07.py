from collections.abc import Callable
from io import TextIOBase
from itertools import product
from operator import add, mul


def parse_input(input_stream: TextIOBase) -> list[int, tuple[int]]:
    """Return a list with each line parsed as a tuple of target value and series of integer terms."""
    equations = [line.strip().split(": ") for line in input_stream]
    return [(int(x), tuple(int(z) for z in y.split())) for x, y in equations]


def sum_solvable_equations(input_stream: TextIOBase, valid_operators: list[Callable[[int, int], int]]) -> int:
    """Sum all target values that can be calculated from their terms using `valid_operators`.

    Operators are evaluated left-to-right, NOT according to traditional precedence rules.

    Any order of operators may be used, one operator between each pair of terms. The integer terms cannot be rearranged.
    """
    result = 0
    for target, terms in parse_input(input_stream):
        for operators in product(valid_operators, repeat=len(terms) - 1):
            total = terms[0]
            for op, term in zip(operators, terms[1:], strict=False):
                total = op(total, term)
            if total == target:
                result += target
                break
    return result


def concat(a: int, b: int) -> int:
    """Concatenate the digits of `b` to the end of `a` and return as an integer.

    Custom operator for solving part two of the problem.
    """
    return int(str(a) + str(b))


def p07a(input_stream: TextIOBase) -> int:
    """Sum all target values that can be calculated from their terms using add and multiply operators."""
    return sum_solvable_equations(input_stream, [add, mul])


def p07b(input_stream: TextIOBase) -> int:
    """Sum all target values that can be calculated from their terms using add, multiply, and concat operators."""
    return sum_solvable_equations(input_stream, [add, mul, concat])
