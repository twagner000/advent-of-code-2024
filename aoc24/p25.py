from io import TextIOBase

import numpy as np


def p25a(input_stream: TextIOBase) -> int:
    """TBD."""
    schematics = [
        (np.array([list(y) for y in x.strip().split("\n")]).T == "#").astype(int)
        for x in input_stream.read().split("\n\n")
    ]
    locks = [a.sum(axis=1) - 1 for a in schematics if a[:, 0].sum() == 5]
    keys = [a.sum(axis=1) - 1 for a in schematics if a[:, -1].sum() == 5]
    count = 0
    for lock in locks:
        for key in keys:
            if (lock + key).max() <= 5:
                count += 1
    return count


def p25b(input_stream: TextIOBase) -> int:
    """TBD."""
    return input_stream
