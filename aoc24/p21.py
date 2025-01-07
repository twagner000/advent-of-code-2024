from functools import cache
from io import TextIOBase
from itertools import pairwise, permutations, product


@cache
def keypad_to_dict(keypad: str) -> dict[str, tuple[int, int]]:
    """Convert keypad string to dict (key = x,y coords, value = keypad key label)."""
    return {v: (x, y) for y, row in enumerate(keypad.split("\n")) for x, v in enumerate(row)}


@cache
def get_valid_moves(keypad: str, c1: str, c2: str) -> set[str]:
    """Find all valid paths to navigate from c1 to c2 on the keypad (cannot move through "#" spaces)."""
    keypad_dict = keypad_to_dict(keypad)
    x1, y1 = keypad_dict[c1]
    x2, y2 = keypad_dict[c2]
    dx, dy = x2 - x1, y2 - y1
    dxc, dyc = "><"[dx < 0], "v^"[dy < 0]
    moves = {"".join(m) for m in permutations(dxc * abs(dx) + dyc * abs(dy))}
    # drop any moves that go through the blank space ("#")
    ax, ay = keypad_dict["#"]
    valid_moves = set()
    for m in moves:
        x, y = x1, y1
        for c in m:
            match c:
                case "<":
                    x -= 1
                case ">":
                    x += 1
                case "^":
                    y -= 1
                case "v":
                    y += 1
            if x == ax and y == ay:
                break
        else:
            valid_moves.add(m)
    return valid_moves


def p21(codes: list[str], robots: int) -> int:
    """Sum the complexities of the codes for the given number of robots.

    Complexity is the product of a) the shortest sequence of button presses on the final keypad to enter the code
    and b) the numeric part of the code.

    Each robot has their own keypad, plus there is one final keypad for a human to control the last robot.
    Robots are initially aimed at the A button.
    Pressing a robot's A button causes it to push the button it's currently aimed at.

    The first keypad looks like
    ```
    7 8 9
    4 5 6
    1 2 3
      0 A
    ```

    All other keypads look like
    ```
      ^ A
    < v >
    ```
    """
    keypads = ["789\n456\n123\n#0A"] + (robots - 1) * ["#^A\n<v>"]
    pair_costs = {}
    for kpp in keypads[::-1]:
        valid_moves = {
            pair: get_valid_moves(kpp, *pair) for pair in product(kpp, kpp) if "#" not in pair and "\n" not in pair
        }
        pair_costs = {
            pair: min(sum(pair_costs.get(p, 1) for p in pairwise(["A", *m, "A"])) for m in moves)
            for pair, moves in valid_moves.items()
        }

    return sum(int(code[:3]) * sum(pair_costs[pair] for pair in pairwise(["A", *code])) for code in codes)


def p21a(input_stream: TextIOBase) -> int:
    """Sum the complexities of the codes for 3 robots (2 with directional keypads)."""
    door_codes = [x.strip() for x in input_stream]
    return p21(door_codes, 3)


def p21b(input_stream: TextIOBase) -> int:
    """Sum the complexities of the codes for 26 robots (25 with directional keypads)."""
    door_codes = [x.strip() for x in input_stream]
    if door_codes[0] == "029A":  # no test case provided for part b
        return -1
    return p21(door_codes, 26)
