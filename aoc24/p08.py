from io import TextIOBase
from itertools import combinations

import numpy as np


def parse_input(input_stream: TextIOBase) -> tuple[dict[str, list[tuple[int, int]]], int]:
    """Parse text to return dict of antennas (key=frequency, value=list of xy coords) and the grid size."""
    puzzle_input = np.array([list(line.strip()) for line in input_stream])
    antennas = {}
    for y, row in enumerate(puzzle_input):
        for x, v in enumerate(row):
            if v != ".":
                antennas.setdefault(str(v), []).append((x, y))
    grid_size = puzzle_input.shape[0]
    assert grid_size == puzzle_input.shape[1]
    return antennas, grid_size


def is_within_grid(point: tuple[int, int], grid_size: int) -> bool:
    """Check if point falls within the bounds of a square grid of size `grid_size`."""
    return point[0] >= 0 and point[1] >= 0 and point[0] < grid_size and point[1] < grid_size


def p08a(input_stream: TextIOBase) -> int:
    """Count the unique antinodes that occur within the grid when two antennas of the same frequency "resonate".

    This occurs when two antennas of the same frequency are in line, and one is twice as far away as the other.
    """
    antennas, grid_size = parse_input(input_stream)
    antinode_grid = np.zeros((grid_size, grid_size), dtype=int)

    for antennas_for_freq in antennas.values():
        for a, b in combinations(antennas_for_freq, 2):
            d = a[0] - b[0], a[1] - b[1]  # xy distances between the pair of antennas
            for antinode in [(a[0] + d[0], a[1] + d[1]), (b[0] - d[0], b[1] - d[1])]:
                if is_within_grid(antinode, grid_size):
                    antinode_grid[*antinode] = 1

    return antinode_grid.sum()


def p08b(input_stream: TextIOBase) -> int:
    """Count the unique antinodes that occur within the grid when two antennas of the same frequency are in line.

    The distance restriction is dropped for this version of antinodes.
    """
    antennas, grid_size = parse_input(input_stream)
    antinode_grid = np.zeros((grid_size, grid_size), dtype=int)

    for antennas_for_freq in antennas.values():
        for a, b in combinations(antennas_for_freq, 2):
            d = a[0] - b[0], a[1] - b[1]  # xy distances between the pair of antennas
            for sign in (1, -1):
                antinode = a
                while is_within_grid(antinode, grid_size):
                    antinode_grid[*antinode] = 1
                    antinode = antinode[0] + sign * d[0], antinode[1] + sign * d[1]

    return antinode_grid.sum()
