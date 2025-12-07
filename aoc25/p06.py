from functools import reduce
from io import TextIOBase
from operator import add, mul

import numpy as np


def parse_input_a(input_stream: TextIOBase) -> tuple[np.ndarray, list]:
    """Parse the grid of numbers, plus the list of operations in the last row."""
    grid = np.array([x.split() for x in input_stream.read().strip().splitlines()])
    return grid[:-1, :].astype(int).T, [{"*": mul, "+": add}.get(x) for x in grid[-1, :]]


def p06a(input_stream: TextIOBase) -> int:
    """Sum the result of applying each operator to its set of values."""
    values, ops = parse_input_a(input_stream)
    return sum(reduce(op, v) for v, op in zip(values, ops, strict=False))


def parse_input_b(input_stream: TextIOBase) -> tuple[list[list[int]], list]:
    """Parse the grid of numbers in cephalopod form, plus the list of operations in the last row.

    In cephalopod form, each number is given in its own column, with the most significant digit at the top.

    Not all problems have the same number of inputs, so a list of lists is used instead of a 2D array.
    """
    grid = input_stream.read().splitlines()
    values = "\n".join(["".join(x).strip() for x in np.array([list(x) for x in grid[:-1]]).T])
    values = [[int(y) for y in x.splitlines() if y] for x in values.split("\n\n")]
    return values, [{"*": mul, "+": add}.get(x) for x in grid[-1].split()]


def p06b(input_stream: TextIOBase) -> int:
    """Sum the result of applying each operator to its set of values."""
    values, ops = parse_input_b(input_stream)
    return sum(reduce(op, v) for v, op in zip(values, ops, strict=False))
