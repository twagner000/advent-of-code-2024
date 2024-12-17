import re
from io import TextIOBase

re_program = re.compile(r"Register A:\s*(\d+)\s*Register B:\s*(\d+)\s*Register C:\s*(\d+)\s*Program:\s*([\d+,]+)")


def run_computer(reg: list[int], program: list[int]) -> list[int]:  # noqa: C901
    """Run a program throught the 3-bit computer with functionality as described in the puzzle."""
    ptr = [0]
    output = []

    def combo(x: int) -> int:
        if x < 4:
            return x
        if x < 7:
            return reg[x - 4]
        raise NotImplementedError

    def adv(x: int) -> None:
        reg[0] //= 2 ** combo(x)

    def bxl(x: int) -> None:
        reg[1] ^= x

    def bst(x: int) -> None:
        reg[1] = combo(x) % 8

    def jnz(x: int) -> None:
        if reg[0]:
            ptr[0] = x - 2

    def bxc(x: int) -> None:  # noqa: ARG001
        reg[1] ^= reg[2]

    def out(x: int) -> None:
        output.append(combo(x) % 8)

    def bdv(x: int) -> None:
        reg[1] = reg[0] // 2 ** combo(x)

    def cdv(x: int) -> None:
        reg[2] = reg[0] // 2 ** combo(x)

    inst = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

    try:
        for _ in range(1000):
            inst[program[ptr[0]]](program[ptr[0] + 1])
            ptr[0] += 2
    except IndexError:
        pass

    return output


def p17a(input_stream: TextIOBase) -> str:
    """Find the 3-bit computer output given a program and initial register values."""
    program = re_program.findall(input_stream.read())[0]
    reg = [int(x) for x in program[:3]]
    program = [int(x) for x in program[3].split(",")]
    return ",".join(str(x) for x in run_computer(reg, program))


def p17b(input_stream: TextIOBase) -> int:
    """Find initial value of register A such that the 3-bit computer output equals the input program.

    Analysis of the specific puzzle input:
    2, 4: B = A % 8
    1, 5: B ^= 5
    7, 5: C = A // 2**B
    1, 6: B ^= 6
    4, 3: B = B ^ C
    5, 5: OUT = B % 8
    0, 3: A //= 2**3
    3, 0: JUMP to start if A > 0

    OUT = ((((A % 8) ^ 5) ^ 6) ^ (A // 2**((A % 8) ^ 5))) % 8
    A //= 2**3
    """
    prog = re_program.findall(input_stream.read())[0]
    prog = [int(x) for x in prog[3].split(",")]
    if prog == [0, 1, 5, 4, 3, 0]:
        return -1  # no test case for part b

    a = 0
    for i in range(1, len(prog) + 1):
        a *= 8
        for da in range(1000000):
            if run_computer([a + da, 0, 0], prog) == prog[-i:]:
                a += da
                break
        else:
            raise Exception("Couldn't find target output, try increasing range.")
        print(a)
    return a
