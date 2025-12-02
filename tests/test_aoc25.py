from io import StringIO
from pathlib import Path

import pytest
import yaml

import aoc25

DATA_PATH = Path("data")

with Path("tests/aoc25_examples.yaml").open() as f:
    EXAMPLES = yaml.safe_load(f)
EXAMPLE_KEYS = [(k, k2) for k, v in EXAMPLES.items() for k2 in v if len(k2) == 1]


@pytest.mark.parametrize(("puzzle", "part"), EXAMPLE_KEYS)
def test_aoc25(puzzle: str, part: str):
    puzzle_func = getattr(aoc25, puzzle + part)
    with StringIO(EXAMPLES[puzzle]["input"]) as f:
        assert puzzle_func(f) == EXAMPLES[puzzle][part]
    if EXAMPLES[puzzle].get("print_full_solutions"):
        puzzle_input_path = DATA_PATH / f"{puzzle}.txt"
        with puzzle_input_path.open() as f:
            full_solution = f"{puzzle_func(f)} is the full solution."
            raise Exception(full_solution)
