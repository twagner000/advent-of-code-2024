from io import StringIO
from pathlib import Path

import numpy as np


def parse_input(filepath: Path | StringIO) -> np.array:
    """Parse the input into a numpy array of characters."""
    puzzle_input = filepath.read_text() if isinstance(filepath, Path) else filepath.read()
    return np.array([list(row) for row in puzzle_input.strip().split("\n")])


def diagonals_to_strings(window: np.array) -> list[str]:
    """Extract the diagonal and antidiagonal as strings from a square array of characters."""
    return [
        "".join(np.diagonal(window)),
        "".join(np.diagonal(np.fliplr(window))),
    ]


def p04a(filepath: Path | StringIO) -> int:
    """Count the number of times XMAS appears in the word search."""
    puzzle_input = parse_input(filepath)
    count = 0
    targets = ("XMAS", "SAMX")
    for shape in [(1, 4), (4, 1), (4, 4)]:
        for windows in np.lib.stride_tricks.sliding_window_view(puzzle_input, shape):
            for window in windows:
                if shape == (4, 4):
                    # search diagonals
                    for diag in diagonals_to_strings(window):
                        if diag in targets:
                            count += 1
                elif "".join(window.flatten()) in targets:
                    count += 1
    return count


def p04b(filepath: Path | StringIO) -> int:
    """Count the number of times an X-shape is formed by the word MAS (twice) in the word search.

    E.g.,

    ```
    M.S
    .A.
    M.S
    ```
    """
    puzzle_input = parse_input(filepath)
    count = 0
    for windows in np.lib.stride_tricks.sliding_window_view(puzzle_input, (3, 3)):
        for window in windows:
            if all(diag in ("MAS", "SAM") for diag in diagonals_to_strings(window)):
                count += 1
    return count
