from io import TextIOBase
from itertools import product

import numpy as np

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def explore_region(x: int, y: int, grid_size: int, grid: np.array, regions: np.ndarray) -> dict:
    """Explore outward from `x, y` in `grid` to find an orthogonally continuous region of the same plant type.

    Returns a dictionary of information about the region that includes the following:

    - plant_type: the character used in `grid` to indicate the type of all plants in this region.
    - plots: a set of x-y coordinates representing the grid spaces / plots in the region.
    - all_edges: all edges touching the region, represented as a pair of x-y coordinates.
      The second coordinate in the pair is outwards in the direction of exploration.
      Includes both internal and external edges.
    - internal_edges: edges that fall between two plots within the region.
    - regions: the updated `regions` array with the addition of the new region using n+1 for an ID.
    """
    region = {}
    region["plant_type"] = grid[y, x]
    region["plots"] = {(x, y)}
    region["all_edges"] = set()
    region["internal_edges"] = set()
    previous_area = 0
    while len(region["plots"]) > previous_area:
        previous_area = len(region["plots"])
        for (px, py), (dx, dy) in product(region["plots"], DIRECTIONS):
            nx, ny = (px + dx, py + dy)
            edge = ((px, py), (nx, ny))  # edge is always stored from current region outwards
            region["all_edges"].add(edge)
            if nx >= 0 and ny >= 0 and nx < grid_size and ny < grid_size and grid[ny, nx] == region["plant_type"]:
                region["plots"].add((nx, ny))
                region["internal_edges"].add(edge)
    region["regions"] = regions.copy()
    region["regions"][*reversed(list(zip(*region["plots"], strict=False)))] = regions.max() + 1
    return region


def get_area_perimeter_cost(region_info: dict) -> int:
    """Calculate the cost to fence a region (area * perimeter) using `region_info`."""
    area = len(region_info["plots"])
    perimeter = area * 4 - len(region_info["internal_edges"])
    return area * perimeter


def get_area_n_sides_cost(region_info: dict) -> int:
    """Calculate the cost to fence a region (area * number of sides) using `region_info`."""
    external_edges = region_info["all_edges"] - region_info["internal_edges"]
    n_sides = 0
    while external_edges:
        edge = external_edges.pop()
        n_sides += 1

        # remove all other external edges that are part of the same side, so that we only count the side once
        traverse_dim = 1 * (edge[0][1] == edge[1][1])
        for traverse_dir in (-1, 1):
            nv = edge[0][traverse_dim] + traverse_dir
            try:
                while True:  # rely on KeyError to terminate loop
                    next_edge = tuple(tuple(nv if i == traverse_dim else v for i, v in enumerate(pt)) for pt in edge)
                    external_edges.remove(next_edge)
                    nv += traverse_dir
            except KeyError:
                pass

    return len(region_info["plots"]) * n_sides


def p12(input_stream: TextIOBase, *, n_sides_cost: bool) -> int:
    """Sum the cost to fence all regions in the map/grid. `n_sides_cost` indicates the costing method."""
    grid = np.array([list(line.strip()) for line in input_stream])
    grid_size = int(grid.shape[0])
    assert grid_size == grid.shape[1]
    regions = np.zeros_like(grid, dtype=int)
    total_cost = 0
    while regions.min() == 0:
        i = int(regions.argmin())
        x, y = i % grid_size, i // grid_size
        region_info = explore_region(x, y, grid_size, grid, regions)
        regions = region_info["regions"]
        total_cost += (get_area_n_sides_cost if n_sides_cost else get_area_perimeter_cost)(region_info)
    return total_cost


def p12a(input_stream: TextIOBase) -> int:
    """Sum the cost to fence all regions in the map/grid using area * perimeter."""
    return p12(input_stream, n_sides_cost=False)


def p12b(input_stream: TextIOBase) -> int:
    """Sum the cost to fence all regions in the map/grid using area * number of sides."""
    return p12(input_stream, n_sides_cost=True)
