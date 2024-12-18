from collections import defaultdict
from io import TextIOBase

import numpy as np

from aoc24.p16 import DIRECTIONS, dijkstra


def p18a(input_stream: TextIOBase) -> int:
    """Find min steps to reach exit after some number of blocks have fallen."""
    blocks = np.array([line.strip().split(",") for line in input_stream], dtype=int)
    size = blocks.max() + 1
    n_bytes_fallen = 12 if size == 7 else 1024
    grid = np.zeros((size, size), dtype=int)
    grid[blocks[:n_bytes_fallen, 0], blocks[:n_bytes_fallen, 1]] = 1

    # use `"\n".join("".join([str(x) for x in r]).replace("0", ".").replace("1", "#") for r in grid.T)` to visualize

    # modifying/reusing code from p16
    graph = defaultdict(dict)
    for x, y in zip(*np.where(grid == 0), strict=False):
        x, y = int(x), int(y)  # noqa: PLW2901
        for dx, dy in DIRECTIONS:
            # move in current direction
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < size and ny < size and grid[nx, ny] == 0:
                graph[x, y][nx, ny] = 1

    distances = dijkstra(graph, (0, 0))
    return distances[size - 1, size - 1]


def p18b(input_stream: TextIOBase) -> str:
    """Find coords of first block to fall that prevents reaching the exit."""
    blocks = np.array([line.strip().split(",") for line in input_stream], dtype=int)
    size = blocks.max() + 1
    grid = np.zeros((size, size), dtype=int)

    # modifying/reusing code from p16
    # initial graph has all coords connected
    graph = defaultdict(dict)
    for x, y in zip(*np.where(grid == 0), strict=False):
        x, y = int(x), int(y)  # noqa: PLW2901
        for dx, dy in DIRECTIONS:
            # move in current direction
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < size and ny < size and grid[nx, ny] == 0:
                graph[x, y][nx, ny] = 1
    graph = dict(graph)  # defaultdict won't raise KeyError for nonexistent keys, so recast to dict

    for fx, fy in blocks:
        grid[fx, fy] = 1

        # remove connections to the fallen block from the graph
        for dx, dy in DIRECTIONS:
            nx, ny = fx + dx, fy + dy
            try:
                graph[nx, ny].pop((fx, fy))
                if not graph[nx, ny]:
                    graph.pop(nx, ny)
            except KeyError:
                pass

        distances = dijkstra(graph, (0, 0))
        # infinite distance to the exit means it's unreachable
        if distances[size - 1, size - 1] == float("inf"):
            return f"{fx},{fy}"
