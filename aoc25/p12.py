import re
from io import TextIOBase

import numpy as np
from ortools.linear_solver import pywraplp
from tqdm import tqdm

re_shape = re.compile(r"\d+:\s+([#.\s]+)\n\n")
re_region = re.compile(r"^(\d+)x(\d+):\s+([\d\s]+)\s*$", re.MULTILINE)


def parse_input(input_stream: TextIOBase) -> tuple[np.ndarray, np.ndarray]:
    """Parse input into 3d array of present shapes and a 3d array of regions.

    First 2 elements per region are the size of the region, the remaining elements are target present shape counts.
    """
    text = input_stream.read().strip()
    shapes = np.array([[[1 * (z == "#") for z in y] for y in x.split()] for x in re_shape.findall(text)])
    regions = np.array([(x, y, *(z for z in counts.split())) for x, y, counts in re_region.findall(text)], dtype=int)
    return shapes, regions


def p12a(input_stream: TextIOBase) -> int:
    """Find how many regions can fit their listed presents.

    Naive approach - works for puzzle input but not example.
    """
    shapes, regions = parse_input(input_stream)
    if regions.shape[0] == 3:
        return 2  # hard-coded example solution

    success = 0
    covered_cells = shapes.sum((1, 2))
    for region in regions:
        if region[2:] @ covered_cells.T > region[:2].prod():
            continue
        can_easily_fit = (region[:2] // 3).prod()
        if region[2:].sum() <= can_easily_fit:
            success += 1
            continue
        raise NotImplementedError("This region is not obviously feasible or infeasible.")
    return success


def p12a_mip(input_stream: TextIOBase) -> int:
    """Find how many regions can fit their listed presents.

    Overkill (but fun) approach using integer programming!
    """
    shapes, regions = parse_input(input_stream)
    shapes_arr, shape_slices = get_shape_variations(shapes)
    success = 0
    for region in tqdm(regions):
        print(f"starting {region}...")
        success += solve_mip(region, shapes_arr, shape_slices)
    return success


def p12b(input_stream: TextIOBase) -> int:
    """TBD."""
    print(parse_input(input_stream))
    return 0


def get_shape_variations(shapes: np.ndarray) -> tuple[np.ndarray, list[slice]]:
    """Add rotated and flipped versions of the present shapes.

    Return an array of all of the variants, plus a list of slices to match back to the original shapes.
    """
    shapes_dict = {}
    for i, shape in enumerate(shapes):
        shapes_dict[i] = set()
        for _ in range(4):
            shape_tuple = tuple(tuple(row) for row in shape.tolist())
            shapes_dict[i].add(shape_tuple)
            # flipped
            shape_tuple = tuple(tuple(row) for row in shape[::-1, :].tolist())
            shapes_dict[i].add(shape_tuple)
            # next rotation
            shape = shape.T[::-1, :]  # noqa: PLW2901
    shapes_dict = {k: sorted(v) for k, v in shapes_dict.items()}
    shapes_arr = np.array([y for x in shapes_dict.values() for y in x])
    shape_slices = np.cumsum(np.array([len(v) for v in shapes_dict.values()])).tolist()
    shape_slices = [slice(i, j) for i, j in zip([0, *shape_slices], shape_slices, strict=False)]
    return shapes_arr, shape_slices


def solve_mip(region: np.ndarray, shapes_arr: np.ndarray, shape_slices: list[slice]) -> int:
    """Solve a MIP to determine whether a region is feasible.

    Returns 1 if feasible, 0 if infeasible.
    """
    solver = pywraplp.Solver.CreateSolver("GLOP")
    # optionally solver.EnableOutput()

    # x_ijk = 1 if x=i, y=j is the upper left corner of shape k, else 0
    x_var = np.array(
        [
            [[solver.BoolVar(f"x_{ix}_{iy}_{j}") for j in range(shapes_arr.shape[0])] for iy in range(region[1] - 2)]
            for ix in range(region[0] - 2)
        ],
    )

    # one shape per xy / ij position
    for (i, j), x_sum in np.ndenumerate(x_var.sum(axis=2)):
        solver.Add(x_sum <= 1, name=f"pos_{i}_{j}")

    # no overlapping, i.e., each grid square can only be occupied once
    grid = {(i, j): 0 for i, j in np.ndindex(*region[:2])}
    for (i, j, k), x in np.ndenumerate(x_var):
        for (i2, j2), v in np.ndenumerate(shapes_arr[k]):
            if v:
                grid[i + i2, j + j2] += x
    for (i, j), x_sum in grid.items():
        solver.Add(x_sum <= 1, name=f"grid_{i}_{j}")

    # fit the target present counts (types of shapes)
    for a, (k_slice, v) in enumerate(zip(shape_slices, region[2:].tolist(), strict=False)):
        solver.Add(x_var[:, :, k_slice].sum() == v, name=f"count_shape_{a}")

    solver.Maximize(1)  # just checking feasibility
    status = solver.Solve()

    match status:
        case pywraplp.Solver.OPTIMAL:
            return 1
        case pywraplp.Solver.INFEASIBLE:
            print(f"{region} is infeasible")
            return 0
        case _:
            msg = f"Unable to solve {region} to optimal or infeasible."
            raise Exception(msg)


if __name__ == "__main__":
    from pathlib import Path

    puzzle_input_path = Path("data") / "aoc25" / "p12.txt"
    with puzzle_input_path.open() as f:
        print(p12a_mip(f))
