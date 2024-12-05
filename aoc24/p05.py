from collections import defaultdict
from io import StringIO
from pathlib import Path


def parse_input(filepath: Path | StringIO) -> tuple[dict[int, list[int]], dict[int, list[int]], list[list[int]]]:
    """Parse text file into page ordering rules and pages to produce in each update.

    Page ordering rules are two dictionaries. The first lists all pages that must come before the key.
    The second lists all pages that must come after the key (inverse of first).

    Each update (in the list of updates) is an ordered list of page numbers.
    """
    puzzle_input = filepath.read_text() if isinstance(filepath, Path) else filepath.read()
    rules, updates = puzzle_input.strip().split("\n\n")
    k_before_v = defaultdict(list)
    k_after_v = defaultdict(list)
    for line in rules.split("\n"):
        before, after = (int(x) for x in line.split("|"))
        k_before_v[before].append(after)
        k_after_v[after].append(before)
    updates = [[int(x) for x in line.split(",")] for line in updates.split("\n")]
    return k_before_v, k_after_v, updates


def is_ordered_correctly(update: list[int], k_before_v: dict[int, list[int]], k_after_v: dict[int, list[int]]) -> bool:
    """Check if the pages in `update` comply with the ordering rules in `k_before_v` and `k_after_v`."""
    for i, page in enumerate(update):
        for later_page in k_before_v[page]:
            if later_page in update[:i]:
                return False
        for earlier_page in k_after_v[page]:
            if earlier_page in update[i:]:
                return False
    return True


def p05a(filepath: Path | StringIO) -> int:
    """Sum the middle page of all correctly ordered updates."""
    k_before_v, k_after_v, updates = parse_input(filepath)
    total = 0
    for update in updates:
        if is_ordered_correctly(update, k_before_v, k_after_v):
            total += update[len(update) // 2]
    return total


def p05b(filepath: Path | StringIO) -> int:
    """Reorder the incorrectly ordered updates and sum the middle page from each."""
    k_before_v, k_after_v, updates = parse_input(filepath)
    total = 0
    for update in updates:
        if not is_ordered_correctly(update, k_before_v, k_after_v):
            new_update = []
            while update:
                for candidate_page in update:
                    for earlier_page in k_after_v[candidate_page]:
                        if earlier_page in update:
                            break
                    else:
                        new_update.append(candidate_page)
                        update.remove(candidate_page)
            total += new_update[len(new_update) // 2]
    return total
