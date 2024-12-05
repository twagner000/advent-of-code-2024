from io import StringIO
from pathlib import Path

import pandas as pd


def p06a(filepath: Path | StringIO) -> int:
    """TBD."""
    puzzle_input = pd.read_csv(filepath, sep=r"\s+", names=["left", "right"], dtype=int)  # noqa: F841


def p06b(filepath: Path | StringIO) -> int:
    """TBD."""
    puzzle_input = pd.read_csv(filepath, sep=r"\s+", names=["left", "right"], dtype=int)  # noqa: F841
