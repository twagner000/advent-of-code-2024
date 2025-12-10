from io import TextIOBase

import numpy as np
import polars as pl
from tqdm import tqdm


def parse_input(input_stream: TextIOBase) -> np.ndarray:
    """Parse all corner xy-coordinates."""
    return np.array([x.split(",") for x in input_stream.read().strip().splitlines()], dtype=int)


def p09a(input_stream: TextIOBase) -> int:
    """Find the max area of a rectangle formed by 2 corner points."""
    corners = parse_input(input_stream)
    corners = pl.DataFrame({"x1": corners[:, 0], "y1": corners[:, 1]})
    rects = corners.join(corners.select(pl.col("x1").alias("x2"), pl.col("y1").alias("y2")), how="cross").with_columns(
        area=((pl.col("x2") - pl.col("x1")).abs() + 1) * ((pl.col("y2") - pl.col("y1")).abs() + 1),
    )
    return rects.select(pl.col("area").max()).item()


def cw(xy: tuple[int, int]) -> tuple[int, int]:
    """Rotate a unit vector 90 degrees clockwise."""
    return xy[1], -xy[0]


def ccw(xy: tuple[int, int]) -> tuple[int, int]:
    """Rotate a unit vector 90 degrees counterclockwise."""
    return -xy[1], xy[0]


def add(xy1: tuple[int, int], xy2: tuple[int, int]) -> tuple[int, int]:
    """Add tuples elementwise."""
    return xy1[0] + xy2[0], xy1[1] + xy2[1]


def sub(xy1: tuple[int, int], xy2: tuple[int, int]) -> tuple[int, int]:
    """Subtract tuples elementwise."""
    return xy1[0] - xy2[0], xy1[1] - xy2[1]


def get_uvec(xy1: tuple[int, int], xy2: tuple[int, int]) -> tuple[int, int]:
    """Find unit vector from xy1 to xy2."""
    return min(1, max(-1, xy2[0] - xy1[0])), min(1, max(-1, xy2[1] - xy1[1]))


def p09b(input_stream: TextIOBase) -> int:
    """Find the max area of a rectangle formed by 2 corner points with additional constraint.

    The rectangle must also remain within the path formed by connecting the corner points.
    """
    corners = parse_input(input_stream)
    corners = [tuple(xy.tolist()) for xy in corners]
    path = set()
    left = set()
    right = set()
    for c1, c2 in zip(corners, corners[1:] + corners[:1], strict=False):
        uvec = get_uvec(c1, c2)
        pos = sub(c1, uvec)
        while pos != c2:
            pos = add(pos, uvec)
            path.add(pos)
            left.add(add(pos, cw(uvec)))
            right.add(add(pos, ccw(uvec)))
    outer = (left if max(left) > max(right) else right) - path

    max_area = 0
    for i, (x1, y1) in enumerate(tqdm(corners)):
        for x2, y2 in corners[i + 1 :]:
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area <= max_area:
                continue  # this rect won't increase our max_area
            rect_corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            for c1, c2 in zip(rect_corners, rect_corners[1:] + rect_corners[:1], strict=False):
                uvec = get_uvec(c1, c2)
                pos = sub(c1, uvec)
                while pos != c2:
                    pos = add(pos, uvec)
                    if pos in outer:
                        break
                if pos in outer:
                    break
            else:
                max_area = area  # we've already checked that area > max_area
                print(f"{max_area=:,.0f}")
    return max_area


if __name__ == "__main__":
    from pathlib import Path

    puzzle_input_path = Path("data") / "aoc25" / "p09.txt"
    with puzzle_input_path.open() as f:
        print(p09b(f))
