import re
from io import TextIOBase

from ortools.linear_solver import pywraplp

re_machine = re.compile(r"Button A: X\+(\d+), Y\+(\d+)\s*Button B: X\+(\d+), Y\+(\d+)\s*Prize: X=(\d+), Y=(\d+)")


def exhaustive_combos(ax: int, ay: int, bx: int, by: int, px: int, py: int) -> tuple[int, int, int] | None:  # noqa: PLR0913
    """Try all combinations of a, b (<=100) to move the claw by ax,ay and bx,by to exactly reach px,py.

    Return the solution that costs the fewest tokens (3 tokens per a, 1 token per b) as a tuple of (tokens, a, b).
    If no solution is found, return None.
    """
    soln = []
    for a in range(101):
        for b in range(101):
            if a * ax + b * bx == px and a * ay + b * by == py:
                soln.append((3 * a + b, a, b))
            if a * ax + b * bx > px or a * ay + b * by > py:
                break
    if soln:
        return min(soln)
    return None


def p13a(input_stream: TextIOBase) -> int:
    """Find the min tokens required to move a claw to each prize (where possible), and sum.

    Each claw machine has two buttons, A and B, that each move the claw a specific distance in positive x and y.
    Pressing A costs 3 tokens, pressing B costs 1 token.

    It is given that no button needs to be pressed >100 times.
    """
    cost = 0
    for machine in re_machine.findall(input_stream.read()):
        if soln := exhaustive_combos(*[int(x) for x in machine]):
            cost += soln[0]
    return cost


def p13b(input_stream: TextIOBase) -> int:
    """Find the min tokens required to move a claw to each updated prize location (where possible), and sum.

    Prize locations have **1e13 added** to each of x and y, beyond the input.

    Each claw machine has two buttons, A and B, that each move the claw a specific distance in positive x and y.
    Pressing A costs 3 tokens, pressing B costs 1 token.

    It is no longer given that buttons are pressed <= 100 times.
    """
    total_tokens = 0
    for machine in [[int(x) for x in m] for m in re_machine.findall(input_stream.read())]:
        ax, ay, bx, by, px, py = machine
        solver = pywraplp.Solver.CreateSolver("SCIP")
        inf = solver.infinity()
        a = solver.IntVar(0.0, inf, "a")
        b = solver.IntVar(0.0, inf, "b")
        solver.Add(a * ax + b * bx == px + 1e13)
        solver.Add(a * ay + b * by == py + 1e13)
        solver.Minimize(3 * a + b)
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            tokens = int(solver.Objective().Value())
            print(f"optimal cost {tokens} for {machine}, a={a.solution_value():.0f}, b={b.solution_value():.0f}")
            total_tokens += tokens
        else:
            print(f"no optimal solution found for {machine}")
    return total_tokens
