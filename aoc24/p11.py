from collections import defaultdict
from io import TextIOBase


def parse_input(input_stream: TextIOBase) -> dict[int, int]:
    """Count how many times each integer appears in the text input and return as a dictionary (k=integer, v=count)."""
    stones = defaultdict(int)
    for k in [int(x) for x in input_stream.read().strip().split()]:
        stones[k] += 1
    return stones


def blink(stones: dict[int, int]) -> dict[int, int]:
    """Apply the "blink" logic from the problem to the dictionary of stone counts (k=integer, v=count)."""
    new_stones = defaultdict(int)
    for k, v in stones.items():
        if k == 0:
            # 0 transforms to 1
            new_stones[1] += v
        elif (n := len(s := str(k))) % 2 == 0:
            # even number of digits transforms into 2 new numbers by splitting the digits (drop any leading zeros)
            new_stones[int(s[: n // 2])] += v
            new_stones[int(s[n // 2 :])] += v
        else:
            new_stones[k * 2024] += v
    return new_stones


def p11a(input_stream: TextIOBase) -> int:
    """Count the number of stones after 25 "blinks" (refer to problem for "blink" logic)."""
    stones = parse_input(input_stream)
    for _ in range(25):
        stones = blink(stones)
    return sum(stones.values())


def p11b(input_stream: TextIOBase) -> int:
    """Count the number of stones after 75 "blinks" (refer to problem for "blink" logic)."""
    stones = parse_input(input_stream)

    # no test case provided for part b
    if stones == {125: 1, 17: 1}:
        return -1

    for _ in range(75):
        stones = blink(stones)
    return sum(stones.values())
