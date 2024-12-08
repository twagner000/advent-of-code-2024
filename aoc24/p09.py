from io import TextIOBase

import pandas as pd


def p09a(input_stream: TextIOBase) -> int:
    """TBD."""
    puzzle_input = pd.read_csv(input_stream, sep=r"\s+", names=["left", "right"], dtype=int)  # noqa: F841


def p09b(input_stream: TextIOBase) -> int:
    """TBD."""
    puzzle_input = pd.read_csv(input_stream, sep=r"\s+", names=["left", "right"], dtype=int)  # noqa: F841
