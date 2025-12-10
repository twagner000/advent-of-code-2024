import itertools
import re
from functools import reduce
from io import TextIOBase

from ortools.linear_solver import pywraplp

re_machine = re.compile(r"^\[([.#]+)\] ([()\d,\s]+) \{([\d,]+)\}", re.MULTILINE)
re_buttons = re.compile(r"\(([\d,]+)\)")


def parse_input(input_stream: TextIOBase) -> list[dict]:
    """Parse each machine row into its lights, buttons, and joltage."""
    return [
        {
            "lights": int(lights.replace("#", "1").replace(".", "0")[::-1], 2),
            "buttons": [[int(y) for y in x.split(",")] for x in re_buttons.findall(buttons)],
            "joltage": [int(x) for x in joltage.split(",")],
        }
        for lights, buttons, joltage in re_machine.findall(input_stream.read())
    ]


def p10a(input_stream: TextIOBase) -> int:
    """Sum the minimum button presses for each machine to light its target indicators.

    Inspired by https://math.stackexchange.com/questions/2150103/xor-number-combinations

    Pressing a button is equivalent to an XOR op on the indicator lights.

    Since we are using XOR, coefficients >1 for linear combinations are redundant.
    """
    machines = parse_input(input_stream)
    total_buttons = 0
    for m in machines:
        fewest = int(1e6)
        buttons = [sum(2**y for y in x) for x in m["buttons"]]
        for combo in itertools.product(*((0, v) for v in buttons)):
            n_buttons = sum(min(1, x) for x in combo)
            if n_buttons >= fewest:
                continue
            if reduce(lambda a, b: a ^ b, combo) == m["lights"]:
                fewest = n_buttons
        total_buttons += fewest
    return total_buttons


def p10b(input_stream: TextIOBase) -> int:
    """Sum the minimum button presses for each machine to reach the specified joltage levels.

    Each button press increments the corresponding joltage level(s) by one.

    Solved using a quick MIP per machine.
    """
    machines = parse_input(input_stream)
    total_buttons = 0
    for m in machines:
        solver = pywraplp.Solver.CreateSolver("SCIP")
        inf = solver.infinity()
        # one integer decision variable per button
        # representing the number of presses
        buttons = [solver.IntVar(0.0, inf, f"b{i}") for i in range(len(m["buttons"]))]
        for i, target in enumerate(m["joltage"]):
            # one constraint per joltage counter
            # only include button variables that trigger that counter
            # variable coefficients are 1 because joltage counter is incremented by 1 per button press
            solver.Add(sum(v for v, b in zip(buttons, m["buttons"], strict=False) if i in b) == target)
        solver.Minimize(sum(buttons))
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            total_buttons += int(solver.Objective().Value())
        else:
            print(m)
            raise Exception("can't find optimal solution")
    return total_buttons
