from io import StringIO
from pathlib import Path

import pytest
import yaml

import aoc24

with Path("tests/examples.yaml").open() as f:
    EXAMPLES = yaml.safe_load(f)


@pytest.mark.parametrize("puzzle", EXAMPLES.keys())
def test_aoc24(puzzle: str):
    puzzle_func = getattr(aoc24, puzzle)
    with StringIO() as example_input:
        example_input.write(EXAMPLES[puzzle]["input"])
        example_input.seek(0)
        assert puzzle_func(example_input) == EXAMPLES[puzzle]["solution"]
    if fpath := EXAMPLES[puzzle].get("full_problem"):
        full_solution = f"The full solution is {puzzle_func(fpath)}"
        raise Exception(full_solution)
