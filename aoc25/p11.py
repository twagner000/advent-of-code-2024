from functools import cache
from io import TextIOBase


def parse_input(input_stream: TextIOBase) -> dict[str, list[str]]:
    """Parse input to a dict where value is the list of devices to which the key device outputs."""
    outputs = dict(x.split(": ") for x in input_stream.read().strip().splitlines())
    return {k: v.split() for k, v in outputs.items()}


def p11a(input_stream: TextIOBase) -> int:
    """Find the number of paths from `you` to `out`."""
    outputs = parse_input(input_stream)

    @cache
    def count_paths(from_node: str, to_node: str) -> int:
        if from_node == to_node:
            return 1
        return sum(count_paths(new_from, to_node) for new_from in outputs[from_node])

    return count_paths("you", "out")


def p11b(input_stream: TextIOBase) -> int:
    """Find the number of paths from `svr` to `out` that pass through `dac` and `fft`."""
    outputs = parse_input(input_stream)

    @cache
    def count_paths(from_node: str, to_node: str, thru_dac: bool = False, thru_fft: bool = False) -> int:
        if from_node == to_node:
            return 1 * (thru_dac and thru_fft)
        return sum(
            count_paths(new_from, to_node, thru_dac or from_node == "dac", thru_fft or from_node == "fft")
            for new_from in outputs[from_node]
        )

    return count_paths("svr", "out")
