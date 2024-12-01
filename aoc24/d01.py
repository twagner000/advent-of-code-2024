from io import StringIO
from pathlib import Path

import pandas as pd


def p01a(filepath: Path | StringIO) -> int:
    """Independently sort 2 columns of integers and sum the differences."""
    puzzle_input = pd.read_csv(filepath, sep=r"\s+", names=["left", "right"], dtype=int)
    return (
        puzzle_input.assign(
            left=lambda df: df["left"].sort_values(ignore_index=True),
            right=lambda df: df["right"].sort_values(ignore_index=True),
            diff=lambda df: df["left"] - df["right"],
        )["diff"]
        .abs()
        .sum()
    )


def p01b(filepath: Path | StringIO) -> int:
    """Multiply each integer in the left column by the number of times it appears in the right column, then sum."""
    puzzle_input = pd.read_csv(filepath, sep=r"\s+", names=["left", "right"], dtype=int)
    counts = puzzle_input["right"].value_counts().to_dict()
    return puzzle_input.assign(product=lambda df: df["left"].apply(lambda x: x * counts.get(x, 0)))["product"].sum()
