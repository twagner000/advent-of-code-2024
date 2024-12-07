from io import TextIOBase

import numpy as np

DIRECTION_SYMBOLS = "^>v<"
DIRECTION_MOVES = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def parse_puzzle_input(input_stream: TextIOBase) -> tuple[int, np.ndarray, tuple[int, int, int]]:
    """Parse text input to find grid size, binary array of obstacle locations, and starting position/direction."""
    puzzle_input = np.array([list(line.strip()) for line in input_stream])
    grid_size = puzzle_input.shape[0]
    assert grid_size == puzzle_input.shape[1]
    start_pos = [x.item() for x in np.where(np.isin(puzzle_input, list(DIRECTION_SYMBOLS)))]
    start_dir = DIRECTION_SYMBOLS.index(puzzle_input[*start_pos])
    return grid_size, (puzzle_input == "#").astype(int), (*start_pos, start_dir)


def visualize(obstacles: np.ndarray, visited: np.ndarray) -> str:
    """Visualize a grid with obstacles (#) and the spaces traveled by an agent (X)."""
    viz = obstacles.astype(str)
    viz = np.char.replace(np.char.replace(viz, "0", "."), "1", "#")
    viz[*visited[:, :2].T] = "X"
    return "\n".join("".join(row) for row in viz)


def try_move(row: int, col: int, direction: int) -> tuple[int, int, int]:
    """Use `direction` to return a tuple with row and column incremented (and direction unchanged)."""
    d_row, d_col = DIRECTION_MOVES[direction]
    return row + d_row, col + d_col, direction


def find_route(grid_size: int, obstacles: np.ndarray, previous: tuple) -> tuple[bool, list[tuple[int, int, int]]]:
    """Travel the route of an agent that turns right every time it hits an obstacle.

    Return a bool indicating whether the agent got stuck in a loop, and a set of tuples covered by the agent.
    Each tuple consists of (row, column, direction).
    """
    visited = {previous}  # using a set (instead of list) enables quicker checks for loops
    while True:
        row, col, direction = try_move(*previous)
        if row < 0 or col < 0 or row >= grid_size or col >= grid_size:
            break  # exiting grid
        if (row, col, direction) in visited:
            # have been in this position/direction before, entering a loop
            return True, visited
        if obstacles[row, col]:
            # obstacle reached, stay in place and change direction
            row, col, direction = previous
            direction += 1
            direction %= 4
        previous = (row, col, direction)
        visited.add(previous)
    return False, visited


def p06a(input_stream: TextIOBase) -> int:
    """Find number of spaces covered before exiting a grid, if an agent turns right every time it hits an obstacle."""
    grid_size, obstacles, start = parse_puzzle_input(input_stream)
    _, visited = find_route(grid_size, obstacles, start)
    visited = np.stack(list(visited))  # 2d array for ease of manipulation, now that length is known
    print(visualize(obstacles, visited))
    return np.unique(visited[:, :2], axis=0).shape[0]


def p06b(input_stream: TextIOBase) -> int:
    """Find how many times adding a single new obstacle to a grid traps an agent in a loop.

    The agent turns right every time it hits an obstacle.
    """
    grid_size, obstacles, start = parse_puzzle_input(input_stream)
    _, visited = find_route(grid_size, obstacles, start)

    loop_obstacles = set()
    for pre_obstacle_space in visited:
        obs_row, obs_col, _ = try_move(*pre_obstacle_space)
        if obs_row < 0 or obs_col < 0 or obs_row >= grid_size or obs_col >= grid_size:
            continue  # can't add an obstacle outside of the grid
        if not obstacles[obs_row, obs_col]:
            new_obstacles = obstacles.copy()
            new_obstacles[obs_row, obs_col] = 1
            entered_loop, _ = find_route(grid_size, new_obstacles, start)
            if entered_loop:
                loop_obstacles.add((obs_row, obs_col))
    return len(loop_obstacles)
