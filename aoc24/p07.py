from io import TextIOBase

import pandas as pd


def p07a(input_stream: TextIOBase) -> int:
    """TBD."""
    puzzle_input = pd.read_csv(input_stream, sep=r"\s+", names=["left", "right"], dtype=int)  # noqa: F841


def p07b(input_stream: TextIOBase) -> int:
    """TBD."""
    puzzle_input = pd.read_csv(input_stream, sep=r"\s+", names=["left", "right"], dtype=int)  # noqa: F841
