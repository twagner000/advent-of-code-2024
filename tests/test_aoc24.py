from io import StringIO
from pathlib import Path

import pytest
import yaml

import aoc24

DATA_PATH = Path("data")

with Path("tests/examples.yaml").open() as f:
    EXAMPLES = yaml.safe_load(f)
EXAMPLE_KEYS = [(k, k2) for k, v in EXAMPLES.items() for k2 in v if k2 != "input"]


@pytest.mark.parametrize(("puzzle", "part"), EXAMPLE_KEYS)
def test_aoc24(puzzle: str, part: str):
    puzzle_func = getattr(aoc24, puzzle + part)
    with StringIO() as example_input:
        example_input.write(EXAMPLES[puzzle]["input"])
        example_input.seek(0)
        assert puzzle_func(example_input) == EXAMPLES[puzzle][part]["solution"]
    if not EXAMPLES[puzzle][part].get("completed"):
        full_solution = f"The full solution is {puzzle_func(DATA_PATH / 'puzzle.txt')}"
        raise Exception(full_solution)
