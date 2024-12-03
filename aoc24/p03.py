import re
from io import StringIO
from pathlib import Path


def p03a(filepath: Path | StringIO) -> int:
    """Find all valid mul(x,y) in the text, multiply x and y, and sum the results."""
    puzzle_input = filepath.read_text() if isinstance(filepath, Path) else filepath.read()
    instruction_regex = re.compile(r"mul\((\d+),(\d+)\)")
    return sum([int(x) * int(y) for x, y in instruction_regex.findall(puzzle_input)])


def p03b(filepath: Path | StringIO) -> int:
    """Find all valid mul(x,y) in the text, multiply x and y if ENABLED, and sum the results.

    The multiply operation starts enabled. Whenver do() or don't() is found in the text the operation is
    enabled or disabled, respectively.
    """
    puzzle_input = filepath.read_text() if isinstance(filepath, Path) else filepath.read()
    instruction_regex = re.compile(r"(?P<do_not>don't\(\))|(?P<do>do\(\))|(mul\((?P<mul_a>\d+),(?P<mul_b>\d+)\))")
    enabled = True
    total = 0
    for instruction in instruction_regex.findall(puzzle_input):
        match instruction:
            case ("don't()", *_):
                enabled = False
            case (_, "do()", *_):
                enabled = True
            case (_, _, _, x, y):
                if enabled:
                    total += int(x) * int(y)
    return total
