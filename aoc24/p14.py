import re
from io import TextIOBase
from math import prod

import numpy as np
from tqdm import tqdm

re_robot = re.compile(r"p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)")


def p14a(input_stream: TextIOBase, n_seconds: int = 100) -> int:
    """Find the product of robot counts in each quadrant after 100 seconds."""
    # parse robots from text input
    robots = [[int(x) for x in r] for r in re_robot.findall(input_stream.read())]
    grid_shape = [max(x) + 1 for x in list(zip(*robots, strict=False))[:2]]

    # move all robots forward by n_seconds using their velocities
    final_pos = [
        ((x + n_seconds * dx) % grid_shape[0], (y + n_seconds * dy) % grid_shape[1]) for x, y, dx, dy in robots
    ]

    # use a grid to count robots at each position
    grid = np.zeros(grid_shape[::-1], dtype=int)
    for x, y in final_pos:
        grid[y, x] += 1

    # divide the grid into quadrants and multiply the sums
    qx, qy = (x // 2 for x in grid_shape)
    quads = [grid[:qy, :qx], grid[-qy:, :qx], grid[:qy, -qx:], grid[-qy:, -qx:]]
    return prod(q.sum() for q in quads)


def p14b(input_stream: TextIOBase) -> int:
    """Find after how many seconds the robots form a Christmas tree shape."""
    # parse robots from text input
    robots = [[int(x) for x in r] for r in re_robot.findall(input_stream.read())]
    grid_shape = [max(x) + 1 for x in list(zip(*robots, strict=False))[:2]]

    # skip the test case for part b (not provided)
    if len(robots) == 12:
        return -1

    # move all robots one step at a time and

    for i in tqdm(range(1_000_000)):
        # move all robots one step
        robots = [((x + dx) % grid_shape[0], (y + dy) % grid_shape[1], dx, dy) for x, y, dx, dy in robots]

        # use a grid to count robots at each position
        grid = np.zeros(grid_shape[::-1], dtype=int)
        for x, y, _, _ in robots:
            grid[y, x] += 1

        # stop when a state is reached where no robots are in the same position
        # trial-and-error was used over a variety of "stop" states (e.g., mirrored in x) to find this one
        if grid.max() == 1:
            print(f"after **{i + 1}** seconds:")
            print("\n".join("".join(row) for row in np.char.replace(grid.astype(str), "0", ".")) + "\n")
            return i + 1
