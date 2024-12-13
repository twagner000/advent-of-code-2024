import re
from io import TextIOBase

from ortools.linear_solver import pywraplp

re_machine = re.compile(r"Button A: X\+(\d+), Y\+(\d+)\s*Button B: X\+(\d+), Y\+(\d+)\s*Prize: X=(\d+), Y=(\d+)")


def parse_input(input_stream: TextIOBase) -> list[list[int]]:
    """Parse text using regex to get [ax, ay, bx, by, px, py] for each machine in the returned list."""
    return [[int(x) for x in m] for m in re_machine.findall(input_stream.read())]


def solve_exhaustively(ax: int, ay: int, bx: int, by: int, px: int, py: int) -> int | None:  # noqa: PLR0913
    """Try all combinations of a, b (<=100) to move the claw by ax,ay and bx,by to exactly reach px,py.

    Return the token cost of the cheapest solution (3 tokens per a, 1 token per b), or None if no solution found.
    """
    soln = []
    for a in range(101):
        for b in range(101):
            if a * ax + b * bx == px and a * ay + b * by == py:
                soln.append((3 * a + b, a, b))  # token cost goes first to make it easy to find the min cost solve
            # we can stop incrementing b and go to the next a if we've already exceeded the prize's location in x or y
            if a * ax + b * bx > px or a * ay + b * by > py:
                break
    if soln:
        return min(soln)[0]
    return None


def solve_as_mip(ax: int, ay: int, bx: int, by: int, px: int, py: int, pd: int) -> int | None:  # noqa: PLR0913
    """Solve the optimal token cost for a machine as a MIP (mixed-integer programming problem)."""
    solver = pywraplp.Solver.CreateSolver("SCIP")
    inf = solver.infinity()
    a = solver.IntVar(0.0, inf, "a")
    b = solver.IntVar(0.0, inf, "b")
    # pd is the delta we're adding to the base value, i.e. 1e13
    solver.Add(a * ax + b * bx == px + pd)
    solver.Add(a * ay + b * by == py + pd)
    solver.Minimize(3 * a + b)  # 3 tokens per a, 1 token per b
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    return None


def p13a(input_stream: TextIOBase) -> int:
    """Find the min tokens required to move a claw to each prize (where possible), and sum.

    Each claw machine has two buttons, A and B, that each move the claw a specific distance in positive x and y.
    Pressing A costs 3 tokens, pressing B costs 1 token.

    It is given that no button needs to be pressed >100 times.
    """
    return sum(solve_exhaustively(*machine) or 0 for machine in parse_input(input_stream))


def p13b(input_stream: TextIOBase) -> int:
    """Find the min tokens required to move a claw to each updated prize location (where possible), and sum.

    Prize locations have **1e13 added** to each of x and y, beyond the input.

    Each claw machine has two buttons, A and B, that each move the claw a specific distance in positive x and y.
    Pressing A costs 3 tokens, pressing B costs 1 token.

    It is no longer given that buttons are pressed <= 100 times.
    """
    return sum(solve_as_mip(*machine, 1e13) or 0 for machine in parse_input(input_stream))
