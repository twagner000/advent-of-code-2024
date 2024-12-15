from io import TextIOBase

import numpy as np

DIRECTION_SYMBOLS = "^>v<"
DIRECTION_MOVES = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


def try_move(grid: np.ndarray, x: int, y: int, dx: int, dy: int) -> tuple[bool, np.ndarray]:
    """Try moving what's at (x,y) in the direction (dx,dy). If successful, return True plus the updated grid.

    If unsuccessful, return False plus the original grid, so that we can roll back from recursive calls.

    In the grid, "." represents an empty space, "#" represents a wall, "O" represents a movable box,
    and "[]" represents a movable wide box. Both halves of a wide box must be moved together as a unit.
    """
    nx, ny = (x + dx, y + dy)
    new_grid = grid.copy()
    match nv := grid[nx, ny]:
        case ".":
            # move into the empty space
            new_grid[x, y], new_grid[nx, ny] = new_grid[nx, ny], new_grid[x, y]
            return True, new_grid
        case "#":
            # can't move into a wall
            return False, grid
        case "O" | "[" | "]":
            # check if we can move the box
            success, new_grid = try_move(new_grid, nx, ny, dx, dy)
            if not success:
                return False, grid
            if nv != "O" and abs(dy):
                # if we're pushing a wide box ([]) up or down, we need to check the other half of the box too
                success, new_grid = try_move(new_grid, nx + (1 if nv == "[" else -1), ny, dx, dy)
                if not success:
                    return False, grid
            new_grid[x, y], new_grid[nx, ny] = new_grid[nx, ny], new_grid[x, y]
            return True, new_grid
        case _:
            raise NotImplementedError


def p15(input_stream: TextIOBase, *, wide_mode: bool = False) -> int:
    """Sum all boxes' GPS coordinates after the robot finishes moving.

    A box's GPS coordinate is 100x the distance from the top edge of the grid, plus 1x the distance from the left edge
    of the grid to the box's closest character.

    The robot ("@") will push boxes ("O", or wide box "[]") if they have free space (".") to move into. Walls ("#")
    stop both robot and boxes.

    `wide_mode` indicates whether the warehouse uses regular boxes ("O") or wide boxes ("[]"). If `wide_mode` is True,
    the text input is transformed per the following: `# -> ##`, `O -> []`, `. -> ..`, `@ -> @.`.
    """
    grid, moves = input_stream.read().split("\n\n")
    if wide_mode:
        grid = grid.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    grid = np.array([list(row) for row in grid.strip().split("\n")]).T  # transpose so that index is x,y
    x, y = (x.item() for x in np.where(grid == "@"))

    # execute all the robot's moves
    for move in moves.replace("\n", ""):
        dx, dy = DIRECTION_MOVES[DIRECTION_SYMBOLS.index(move)]
        success, grid = try_move(grid, x, y, dx, dy)
        if success:
            # update our tracker of the robot's coords, if it moved
            x, y = x + dx, y + dy
    print("\n".join("".join(r) for r in grid.T))

    # calculate and sum "GPS" coordinates for each box
    return sum(ox + 100 * oy for ox, oy in zip(*np.where(grid == ("[" if wide_mode else "O")), strict=False))


def p15a(input_stream: TextIOBase) -> int:
    """Sum all boxes' GPS coordinates after the robot finishes moving."""
    return p15(input_stream, wide_mode=False)


def p15b(input_stream: TextIOBase) -> int:
    """Sum all boxes' GPS coordinates after the robot finishes moving through the wide warehouse."""
    return p15(input_stream, wide_mode=True)
