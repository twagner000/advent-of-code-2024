from collections import defaultdict
from io import TextIOBase

import numpy as np

from aoc24.p16 import DIRECTIONS, dijkstra


def solve_p20(input_stream: TextIOBase, max_cheat_len: int) -> int:
    """Find the path through a maze, then find how many cheats of length <= max_cheat_len save a min number of steps.

    For the full solution, the minimum steps saved is 100. For the test case, I chose to define it as 50.

    While cheating, a racer may move through walls. However, a racer can only cheat once per race (up to max_cheat_len
    contiguous steps).
    """
    grid = np.array([list(row) for row in input_stream.read().strip().split("\n")]).T  # transpose so that index is x,y
    size = grid.shape[0]
    assert size == grid.shape[1]
    sx, sy = (x.item() for x in np.where(grid == "S"))
    ex, ey = (x.item() for x in np.where(grid == "E"))

    graph = defaultdict(dict)
    for x, y in zip(*np.where(grid != "#"), strict=False):
        x, y = int(x), int(y)  # noqa: PLW2901
        for dx, dy in DIRECTIONS:
            # move in current direction
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < size and ny < size and grid[nx, ny] != "#":
                graph[x, y][nx, ny] = 1
    distances = dijkstra(graph, (sx, sy))

    dist_delta = check_pairs(distances, max_cheat_len)
    min_savings = 50 if size == 15 else 100  # 10 for test case
    return sum(len(v) for k, v in dist_delta.items() if k >= min_savings)


def check_pairs(distances: dict, max_cheat_len: int) -> dict:
    """Take pairs of points along the race path and check for a feasible cheat between them.

    Return a dict where the key is the number of steps saved by cheating and the value is a list of pairs of points.
    """
    dist_delta = defaultdict(list)
    for (x1, y1), d1 in distances.items():
        for (x2, y2), d2 in distances.items():
            manh_dist = abs(x1 - x2) + abs(y1 - y2)
            if 0 < manh_dist <= max_cheat_len and d1 - d2 - manh_dist > 0:
                dist_delta[d1 - d2 - manh_dist].append((x1, y1, x2, y2))
    return dict(dist_delta)


def p20a(input_stream: TextIOBase) -> int:
    """Count how many cheats of length <=2 save a minimum number of steps in the race described by the puzzle."""
    return solve_p20(input_stream, 2)


def p20b(input_stream: TextIOBase) -> int:
    """Count how many cheats of length <=20 save a minimum number of steps in the race described by the puzzle."""
    return solve_p20(input_stream, 20)
