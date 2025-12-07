from io import TextIOBase

import numpy as np


def parse_input(input_stream: TextIOBase) -> tuple[np.ndarray, np.ndarray, int]:
    """Parse the input into 2D numpy arrays of splitters and beam paths, plus the start row.

    The first array has 1 where there is a splitter ("^") and 0 elsewhere.

    The second array is a grid of zeros in the shape of the input,
    with a 1 at the start location ("S").
    """
    grid = np.array([list(row) for row in input_stream.read().strip().split()])
    splitters = 1 * (grid == "^")
    start = np.array(np.where(grid == "S")).flatten().tolist()
    beams = np.zeros_like(grid, dtype=int)
    beams[*start] = 1
    return splitters, beams, start[0]


def p07a(input_stream: TextIOBase) -> int:
    """Count the number of splitters activated by tachyon beams."""
    splitters, beams, start_i = parse_input(input_stream)

    used_splitters = np.zeros_like(splitters, dtype=int)
    for i in range(start_i + 1, beams.shape[0]):
        for j in np.array(np.where(beams[i - 1, :])).flatten():  # incoming beams
            if splitters[i - 1, j]:
                beams[i, j - 1] = 1
                beams[i, j + 1] = 1
                used_splitters[i - 1, j] = 1
            else:
                beams[i, j] = 1
    return used_splitters.sum()


def p07b(input_stream: TextIOBase) -> int:
    """Count the total number of paths a tachyon partical can take to reach the bottom row.

    This is analagous to the number of timelines in a many-worlds quantum interpretation.
    """
    splitters, beams, start_i = parse_input(input_stream)
    for i in range(start_i + 1, beams.shape[0]):
        for j in np.array(np.where(beams[i - 1, :])).flatten():  # incoming beams
            n = beams[i - 1, j]
            if splitters[i - 1, j]:
                beams[i, j - 1] += n
                beams[i, j + 1] += n
            else:
                beams[i, j] += n
    return beams[-1, :].sum()
