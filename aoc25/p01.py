from io import TextIOBase


def parse_instructions(input_stream: TextIOBase) -> list[int]:
    """Parse instructions to list of integers.

    Negative integer indicates left turn, positive indicates right.
    """
    return [int(x[1:]) * (-1 if x[0] == "L" else 1) for x in input_stream.read().strip().splitlines()]


def p01a(input_stream: TextIOBase) -> int:
    """Find how many instructions land on 0."""
    position = 50
    n_zeros = 0
    for instruction in parse_instructions(input_stream):
        position = (position + instruction) % 100
        if position == 0:
            n_zeros += 1
    return n_zeros


def p01b(input_stream: TextIOBase) -> int:
    """Find how many times we pass through 0."""
    position = 50
    n_zeros = 0
    for instruction in parse_instructions(input_stream):
        for i in range(-instruction, 0, -1) if instruction < 0 else range(1, instruction + 1):
            if (position + i) % 100 == 0:
                n_zeros += 1
        position = (position + instruction) % 100
    return n_zeros
