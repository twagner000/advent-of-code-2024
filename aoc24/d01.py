def p01a(puzzle_input: str) -> int:
    """Independently sort 2 columns of integers and sum the differences."""
    puzzle_input = [[int(x) for x in line.split()] for line in puzzle_input.split("\n")]
    total_diff = 0
    for a, b in zip(*[sorted(x) for x in zip(*puzzle_input, strict=False)], strict=False):
        total_diff += abs(a - b)
    return total_diff


def p01b(puzzle_input: str) -> int:
    """Multiply each integer in the left column by the number of times it appears in the right column, then sum."""
    puzzle_input = [[int(x) for x in line.split()] for line in puzzle_input.split("\n")]
    left, right = zip(*puzzle_input, strict=False)
    counts = {x: right.count(x) for x in set(left)}
    return sum(x * counts[x] for x in left)
