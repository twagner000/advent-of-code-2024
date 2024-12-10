from collections import defaultdict
from io import TextIOBase
from itertools import product

import numpy as np

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def parse_input(input_stream: TextIOBase) -> tuple[np.ndarray, int, list[tuple[int, int]]]:
    """Parse text to get grid of heights, grid size, and a list of trailheads (0-height points)."""
    grid = np.array([[int(x) for x in row.strip()] for row in input_stream])
    grid_size = grid.shape[0]
    assert grid_size == grid.shape[1]
    trailheads = list(zip(*np.stack(np.where(grid == 0)).tolist(), strict=False))
    return grid, grid_size, trailheads


def get_feasible(
    candidates: set[tuple[int, int]],
    grid_size: int,
    grid: np.ndarray,
    height: int,
) -> set[tuple[int, int]]:
    """Filter the points in candidates for feasibility (within the grid and appropriate height)."""
    return {
        (x, y) for x, y in candidates if x >= 0 and y >= 0 and x < grid_size and y < grid_size and grid[x, y] == height
    }


def p10a(input_stream: TextIOBase) -> int:
    """Sum the **scores** (number of reachable, distinct, 9-height positions) for all 0-height trailheads in the map.

    Trails move orthogonally and increase in height by 1 each step.
    """
    grid, grid_size, trailheads = parse_input(input_stream)
    total_scores = 0
    for trailhead in trailheads:
        feasible = {trailhead}
        for height in range(1, 10):
            candidates = {(a[0] + b[0], a[1] + b[1]) for a, b in product(feasible, DIRECTIONS)}
            feasible = get_feasible(candidates, grid_size, grid, height)
            if not feasible:
                break
        total_scores += len(feasible)
    return total_scores


def p10b(input_stream: TextIOBase) -> int:
    """Sum the **ratings** (number of distinct trails to 9-height positions) for all 0-height trailheads in the map.

    Trails move orthogonally and increase in height by 1 each step.
    """
    grid, grid_size, trailheads = parse_input(input_stream)
    total_ratings = 0
    for trailhead in trailheads:
        trails = {trailhead: [[trailhead]]}  # k=last point reached, v=list of trails (trail=list of tuples)
        for height in range(1, 10):
            new_trails = defaultdict(list)
            for prev, prev_trails in trails.items():
                candidates = {(prev[0] + x, prev[1] + y) for x, y in DIRECTIONS}
                for feasible in get_feasible(candidates, grid_size, grid, height):
                    new_trails[feasible] += [[*t, feasible] for t in prev_trails]
            trails = new_trails
        total_ratings += sum(len(v) for v in trails.values())
    return total_ratings
