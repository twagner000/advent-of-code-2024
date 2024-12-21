from functools import cache
from io import TextIOBase
from itertools import permutations, product

from tqdm import tqdm


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


def enter_code(keypad: str, codes: set[str], start: str = "A") -> set[str]:
    """TBD."""
    all_commands = set()
    for code in codes:
        commands = []
        pos = start
        for c in code:
            commands.append(get_valid_moves(keypad, pos, c))
            commands.append({"A"})
            pos = c
        all_commands |= {"".join(p) for p in product(*commands)}
    min_len = min(len(p) for p in all_commands)
    return {p for p in all_commands if len(p) == min_len}


def p21a(input_stream: TextIOBase) -> int:
    """TBD."""
    door_codes = [{x.strip()} for x in input_stream]
    commands = [enter_code("789\n456\n123\n#0A", code) for code in door_codes]
    for _ in range(2):
        commands = [enter_code("#^A\n<v>", code) for code in commands]
    shortest = [min(len(final) for final in finals) for finals in commands]
    return sum(int(next(iter(code))[:3]) * short for code, short in zip(door_codes, shortest, strict=False))


def p21b(input_stream: TextIOBase) -> int:
    """TBD."""
    door_codes = [{x.strip()} for x in input_stream]
    shortest = []
    for code in door_codes:
        if code == {"029A"}:
            return -1
        commands = enter_code("789\n456\n123\n#0A", code)
        print(code)
        for i in tqdm(range(25)):
            commands = enter_code("#^A\n<v>", commands)
            print(i, len(commands))
        shortest.append(len(next(iter(commands))))
    return sum(int(next(iter(code))[:3]) * short for code, short in zip(door_codes, shortest, strict=False))
