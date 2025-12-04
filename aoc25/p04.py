from io import TextIOBase

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def parse_input(input_stream: TextIOBase) -> np.ndarray:
    """Parse the input into a 2D numpy array where "@" is 1 and "." is 0."""
    return np.array([[1 if cell == "@" else 0 for cell in row] for row in input_stream.read().strip().split()])


def p04a(input_stream: TextIOBase) -> int:
    """Count the number of accessible rolls of paper in the warehouse.

    A roll is accessible if there are fewer than 4 rolls of paper in the 8 adjacent positions.
    """
    # pad the array with zeros around the edges to simplify indexing
    padded = np.pad(parse_input(input_stream), 1, constant_values=0)
    accessible = 0
    for window in np.reshape(sliding_window_view(padded, (3, 3)), (-1, 3, 3)):
        # center of the 3x3 window must contain a roll, and there can't be too many adjacent rolls
        if window[1, 1] == 1 and np.sum(window) - 1 < 4:
            accessible += 1
    return accessible


def p04b(input_stream: TextIOBase) -> int:
    """Count the total number of accessible rolls of paper in the warehouse where rolls are successively removed.

    A roll is accessible if there are fewer than 4 rolls of paper in the 8 adjacent positions.

    Each round, all accessible rolls are removed.
    """
    parsed = parse_input(input_stream)
    removed = 0
    while True:
        # pad the array with zeros around the edges to simplify window indexing
        padded = np.pad(parsed, 1, constant_values=0)
        accessible = []
        for index in np.ndindex(parsed.shape):
            # since we've padded the array, the indices from `parsed` map to the upper left corner of a 3x3 window
            window = padded[index[0] : index[0] + 3, index[1] : index[1] + 3]
            # center of the 3x3 window must contain a roll, and there can't be too many adjacent rolls
            if window[1, 1] == 1 and np.sum(window) - 1 < 4:
                accessible.append(index)
        if not accessible:  # stop if there are no more accessible rolls
            break
        # remove all rolls that were accessible this round
        parsed[*zip(*accessible, strict=False)] = 0
        removed += len(accessible)
    return removed
