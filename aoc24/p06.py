from io import TextIOBase

import numpy as np
from tqdm import tqdm

DIRECTION_SYMBOLS = "^>v<"
DIRECTION_MOVES = [
    np.array([-1, 0, 0]),
    np.array([0, 1, 0]),
    np.array([1, 0, 0]),
    np.array([0, -1, 0]),
]


def visualize(obstacles: np.ndarray, visited: np.ndarray) -> str:
    """Visualize a grid with obstacles (#) and the spaces traveled by an agent (X)."""
    viz = obstacles.astype(str)
    viz = np.char.replace(np.char.replace(viz, "0", "."), "1", "#")
    viz[*visited[:, :2].T] = "X"
    return "\n".join("".join(row) for row in viz)


def find_start(puzzle_input: np.ndarray) -> tuple[int, int, int]:
    """Parse the puzzle input to find the starting position and direction of agent."""
    position = [x.item() for x in np.where(np.isin(puzzle_input, list(DIRECTION_SYMBOLS)))]
    direction = DIRECTION_SYMBOLS.index(puzzle_input[*position])
    return (*position, direction)


def get_next_space(current_space: tuple[int, int, int]) -> np.ndarray:
    """Generate the next tuple (row, column direction) from `current_space`, assuming no obstacles are encountered."""
    return np.array(current_space) + DIRECTION_MOVES[current_space[2]]


def find_route(grid_size: int, obstacles: np.ndarray, visited: list[tuple]) -> tuple[bool, list[tuple[int, int, int]]]:
    """Travel the route of an agent that turns right every time it hits an obstacle.

    Return a bool indicating whether the agent got stuck in a loop, and a list of tuples covered by the agent.
    Each tuple consists of (row, column, direction).
    """
    visited = visited[::1]  # copy to avoid mutation issues
    while True:
        next_visit = get_next_space(visited[-1])
        if next_visit[:2].min() < 0 or next_visit[:2].max() >= grid_size:
            break  # exit grid
        if tuple(next_visit.tolist()) in visited:
            # have been in this position/orientation before, entering a loop
            return True, visited
        if obstacles[*next_visit[:2]]:
            # obstacle reached, stay in place and change direction
            next_visit = np.array(visited[-1])
            next_visit[2] += 1
            next_visit[2] %= 4
        visited.append(tuple(next_visit.tolist()))
    return False, visited


def p06a(input_stream: TextIOBase) -> int:
    """Find number of spaces covered before exiting a grid, if an agent turns right every time it hits an obstacle."""
    puzzle_input = np.array([list(line.strip()) for line in input_stream])
    grid_size = puzzle_input.shape[0]
    assert grid_size == puzzle_input.shape[1]
    obstacles = (puzzle_input == "#").astype(int)
    _, visited = find_route(grid_size, obstacles, [find_start(puzzle_input)])
    visited = np.stack(visited)  # 2d array for ease of manipulation, now that length is known
    print(visualize(obstacles, visited))
    return np.unique(visited[:, :2], axis=0).shape[0]


def p06b(input_stream: TextIOBase) -> int:
    """Find how many times adding a single new obstacle to a grid traps an agent in a loop.

    The agent turns right every time it hits an obstacle.

    TODO: inefficient naive implementation - can be improved.
    """
    puzzle_input = np.array([list(line.strip()) for line in input_stream])
    grid_size = puzzle_input.shape[0]
    assert grid_size == puzzle_input.shape[1]
    obstacles = (puzzle_input == "#").astype(int)
    start = find_start(puzzle_input)
    _, visited = find_route(grid_size, obstacles, [start])

    loop_obstacles = set()
    for candidate_turn in tqdm(visited[:-1]):
        new_obstacle = get_next_space(candidate_turn)[:2]
        if new_obstacle.min() >= 0 and new_obstacle.max() < grid_size and not obstacles[*new_obstacle]:
            new_obstacles = obstacles.copy()
            new_obstacles[*new_obstacle] = 1
            entered_loop, _ = find_route(grid_size, new_obstacles, [start])
            if entered_loop:
                loop_obstacles.add(tuple(new_obstacle.tolist()))
    return len(loop_obstacles)
