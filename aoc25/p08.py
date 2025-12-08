from collections import Counter
from io import TextIOBase
from math import prod

import polars as pl


def parse_input(input_stream: TextIOBase) -> pl.DataFrame:
    """Parse input into a dataframe of box numbers and coordinates."""
    return pl.DataFrame(
        {"xyz1": [[int(y) for y in x.split(",")] for x in input_stream.read().strip().splitlines()]},
    ).with_row_index("box1")


def calculate_distances(coords: pl.DataFrame) -> tuple[pl.DataFrame, list[int]]:
    """Calculate all pairwise distances between boxes; also return initial circuits."""
    distances = (
        coords.join(coords.rename({"box1": "box2", "xyz1": "xyz2"}), how="cross")
        .filter(pl.col("box1") > pl.col("box2"))
        .with_columns(distance=(pl.col("xyz1") - pl.col("xyz2")).list.eval(pl.element() ** 2).list.sum())
        .sort("distance")
    )
    circuits = list(range(len(coords)))
    return distances, circuits


def join_circuits(circuits: list[int], box1: int, box2: int) -> list[int]:
    """Join the circuits to which box1 and box2 belong.

    Return an updated `circuits` list, where index is box number and value is circuit number.
    """
    old_circuits = {circuits[box1], circuits[box2]}
    new_circuit = min(old_circuits)
    return [new_circuit if c in old_circuits else c for c in circuits]


def p08a(input_stream: TextIOBase, closest_n: int | None = None) -> int:
    """Find the product of the sizes of the three largest circuits after connecting `closest_n` boxes.

    Boxes are connected in order of increasing distance.
    """
    distances, circuits = calculate_distances(parse_input(input_stream))

    if closest_n is None:
        closest_n = 10 if len(circuits) == 20 else 1000

    for box1, box2 in distances.head(closest_n).select("box1", "box2").rows():
        circuits = join_circuits(circuits, box1, box2)

    return prod(sorted(Counter(circuits).values(), reverse=True)[:3])


def p08b(input_stream: TextIOBase) -> int:
    """Find the product of the x-coordinates of the first pair of boxes that connect all circuits.

    Boxes are connected in order of increasing distance.
    """
    distances, circuits = calculate_distances(parse_input(input_stream))
    for box1, xyz1, box2, xyz2, _ in distances.iter_rows():
        circuits = join_circuits(circuits, box1, box2)
        if min(circuits) == max(circuits):
            return xyz1[0] * xyz2[0]
