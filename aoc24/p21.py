from functools import cache
from io import TextIOBase
from itertools import permutations, product


@cache
def keypad_to_dict(keypad: str) -> dict[str, tuple[int, int]]:
    """TBD."""
    return {v: (x, y) for y, row in enumerate(keypad.split("\n")) for x, v in enumerate(row)}


@cache
def get_valid_moves(keypad: str, c1: str, c2: str) -> set[str]:
    """TBD."""
    keypad2 = keypad_to_dict(keypad)
    x1, y1 = keypad2[c1]
    x2, y2 = keypad2[c2]
    dx, dy = x2 - x1, y2 - y1
    dxc, dyc = "<" if dx < 0 else ">", "^" if dy < 0 else "v"
    moves = {"".join(m) for m in permutations(dxc * abs(dx) + dyc * abs(dy))}
    # drop any moves that go throught the blank space ("#")
    ax, ay = keypad2["#"]
    moves2 = set()
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
            moves2.add(m)
    return moves2


@cache
def get_pair_cost(keypad: str, c1: str, c2: str) -> int:
    """TBD."""
    return min(len(x) for x in get_valid_moves(keypad, c1, c2))


def p21(codes: list[str], robots: int) -> int:
    """TBD."""
    keypads = ["789\n456\n123\n#0A"] + robots * ["#^A\n<v>"]
    pair_costs = {}
    for kpp in keypads[::-1]:
        valid_moves = {
            pair: get_valid_moves(kpp, *pair) for pair in product(kpp, kpp) if "#" not in pair and "\n" not in pair
        }
        pair_costs = {
            pair: min(sum(pair_costs.get(p, 1) for p in zip(["A", *m], [*m, "A"], strict=False)) for m in moves)
            for pair, moves in valid_moves.items()
        }

    return sum(
        int(code[:3]) * sum(pair_costs[pair] for pair in zip(["A", *code], code, strict=False)) for code in codes
    )


def p21a(input_stream: TextIOBase) -> int:
    """TBD."""
    door_codes = [x.strip() for x in input_stream]
    return p21(door_codes, 2)


def p21b(input_stream: TextIOBase) -> int:
    """TBD."""
    door_codes = [x.strip() for x in input_stream]
    if door_codes[0] == "029A":  # no test case provided for part b
        return -1
    return p21(door_codes, 25)
