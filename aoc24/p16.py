import heapq
from collections import defaultdict
from io import TextIOBase

import numpy as np

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def dijkstra[T](graph: dict[T, dict[T, int]], start: T) -> dict[T:int]:
    """Use Dijkstra's algorithm to find the shortest path from a start node to all other nodes in a graph.

    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]  # priority queue of (distance, node)

    # stop after all reachable nodes have been explored
    # since default distance is inf, every reachable node will get pushed onto pq at some point,
    # and popped before we're done
    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                # we've found a new shortest path to this node (recall, default is inf)
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))

    return distances


def p16a(input_stream: TextIOBase) -> int:
    """Find the lowest score a reindeer can get navigating through the maze, as described by the puzzle."""
    grid = np.array([list(row) for row in input_stream.read().strip().split("\n")]).T  # transpose so that index is x,y
    size = grid.shape[0]
    assert size == grid.shape[1]
    sx, sy = (x.item() for x in np.where(grid == "S"))
    ex, ey = (x.item() for x in np.where(grid == "E"))

    graph = defaultdict(dict)
    for x, y in zip(*np.where(grid != "#"), strict=False):
        x, y = int(x), int(y)  # noqa: PLW2901
        for zi, (dx, dy) in enumerate(DIRECTIONS):
            # turn to a different direction
            graph[x, y, zi][x, y, (zi + 1) % 4] = 1000
            graph[x, y, zi][x, y, (zi + 2) % 4] = 2000
            graph[x, y, zi][x, y, (zi - 1) % 4] = 1000

            # move in current direction
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < size and ny < size and grid[nx, ny] != "#":
                graph[x, y, zi][nx, ny, zi] = 1
    distances = dijkstra(graph, (sx, sy, 0))  # always start facing east
    return min(distances[ex, ey, zi] for zi in range(4))


def p16b(input_stream: TextIOBase) -> int:
    """Count tiles that are part of a best path throught the maze, as described by the puzzle."""
    grid = np.array([list(row) for row in input_stream.read().strip().split("\n")]).T  # transpose so that index is x,y
    size = grid.shape[0]
    assert size == grid.shape[1]
    sx, sy = (x.item() for x in np.where(grid == "S"))
    ex, ey = (x.item() for x in np.where(grid == "E"))

    # to visualize grid, use `"\n".join("".join(r) for r in grid.T)`

    graph = defaultdict(dict)
    for x, y in zip(*np.where(grid != "#"), strict=False):
        x, y = int(x), int(y)  # noqa: PLW2901
        for zi, (dx, dy) in enumerate(DIRECTIONS):
            # turn to a different direction
            graph[x, y, zi][x, y, (zi + 1) % 4] = 1000
            graph[x, y, zi][x, y, (zi + 2) % 4] = 2000
            graph[x, y, zi][x, y, (zi - 1) % 4] = 1000

            # move in current direction
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < size and ny < size and grid[nx, ny] != "#":
                graph[x, y, zi][nx, ny, zi] = 1
    distances = dijkstra(graph, (sx, sy, 0))  # always start facing east
    dist2 = defaultdict(dict)
    for k, v in graph.items():
        for k2 in v:
            dist2[k2][k] = distances[k]
    dist2 = dict(dist2)

    prev_dist = min(distances[ex, ey, zi] for zi in range(4))
    ends = {((ex, ey, zi), prev_dist) for zi in range(4) if distances[ex, ey, zi] <= prev_dist}
    visited = ends.copy()
    while ends:
        new_ends = set()
        for xyz, d in ends:
            new_ends |= {(nxyz, nd) for nxyz, nd in dist2[xyz].items() if nd < d}
        print(new_ends)
        ends = new_ends - visited
        visited |= ends

    visited_xy = {(x, y) for (x, y, _), _ in visited}

    return len(visited_xy)
