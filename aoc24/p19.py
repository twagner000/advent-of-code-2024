import re
from collections import defaultdict
from functools import cache
from io import TextIOBase


def solve_p19(input_stream: TextIOBase, *, count_all_solutions_per_pattern: bool) -> int:
    """Arrange towels to form a desired pattern.

    If `count_all_solutions_per_pattern` is True, count how many ways the desired patterns can be formed from the
    available towels. Otherwise, count how many of the desired patterns can be formed from the available towels.
    """
    # parse input
    raw_avail, desired = input_stream.read().strip().split("\n\n")
    desired = [pattern[::-1] for pattern in desired.split("\n")]

    # make a dict of the available towels where the key is the length of the towel and the value is a set of towels
    # this allows us to index into the pattern by an exact number of characters and use the set's quick lookup
    avail = defaultdict(set)
    for towel in re.split(r",\s*", raw_avail):
        avail[len(towel)].add(towel[::-1])

    @cache
    def try_match(pattern: str) -> int:
        """Count ways of making a pattern by recursively trying to match the first portion against available towels.

        Memoizing the function is critical to achieving reasonable performance. Since `avail` never changes, `try_match`
        is an internal function to `solve_p19` so that the cache doesn't need to include `avail`.
        """
        arrangements = 0
        for size, towels in avail.items():
            if pattern[:size] in towels:
                remaining_pattern = pattern[size:]
                if not remaining_pattern:
                    arrangements += 1
                else:
                    arrangements += try_match(remaining_pattern)
        return arrangements

    if count_all_solutions_per_pattern:
        return sum(try_match(pattern) for pattern in desired)
    return sum(try_match(pattern) > 0 for pattern in desired)


def p19a(input_stream: TextIOBase) -> int:
    """Count how many of the desired patterns can be formed from the available towels."""
    return solve_p19(input_stream, count_all_solutions_per_pattern=False)


def p19b(input_stream: TextIOBase) -> int:
    """Count how many ways the desired patterns can be formed from the available towels."""
    return solve_p19(input_stream, count_all_solutions_per_pattern=True)
