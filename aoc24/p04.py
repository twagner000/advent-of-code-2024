from io import TextIOBase

import numpy as np


def parse_input(input_stream: TextIOBase) -> np.array:
    """Parse the input into a numpy array of characters."""
    return np.array([list(row) for row in input_stream.read().strip().split("\n")])


def diagonals_to_strings(window: np.array) -> list[str]:
    """Extract the diagonal and antidiagonal as strings from a square array of characters."""
    return [
        "".join(np.diagonal(window)),
        "".join(np.diagonal(np.fliplr(window))),
    ]


def p04a(input_stream: TextIOBase) -> int:
    """Count the number of times XMAS appears in the word search."""
    puzzle_input = parse_input(input_stream)
    count = 0
    targets = ("XMAS", "SAMX")
    for shape in [(1, 4), (4, 1), (4, 4)]:  # horizontal, vertical, andor diagonal
        for window in np.lib.stride_tricks.sliding_window_view(puzzle_input, shape).reshape((-1, *shape)):
            if shape == (4, 4):
                count += sum(diag in targets for diag in diagonals_to_strings(window))
            elif "".join(window.flatten()) in targets:
                count += 1
    return count


def p04b(input_stream: TextIOBase) -> int:
    """Count the number of times an X-shape is formed by the word MAS (twice) in the word search.

    E.g.,

    ```
    M.S
    .A.
    M.S
    ```
    """
    puzzle_input = parse_input(input_stream)
    count = 0
    for window in np.lib.stride_tricks.sliding_window_view(puzzle_input, (3, 3)).reshape((-1, 3, 3)):
        if all(diag in ("MAS", "SAM") for diag in diagonals_to_strings(window)):
            count += 1
    return count
