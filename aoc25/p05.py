from io import TextIOBase

import polars as pl


def parse_input(input_stream: TextIOBase) -> tuple[list[tuple[int, ...]], list[int]]:
    """Separately parse ranges of fresh IDs and list of available IDs."""
    fresh, available = input_stream.read().strip().split("\n\n")
    fresh = [tuple(int(x) for x in line.split("-")) for line in fresh.splitlines()]
    available = [int(x.strip()) for x in available.splitlines() if x]
    return fresh, available


def p05a(input_stream: TextIOBase) -> int:
    """Count available IDs that are also fresh."""
    fresh, available = parse_input(input_stream)
    available_and_fresh = []
    for x in available:
        for start, end in fresh:
            if start <= x <= end:
                available_and_fresh.append(x)
                break
    return len(available_and_fresh)


def p05b(input_stream: TextIOBase) -> int:
    """Count total number of unique fresh IDs."""
    fresh, _ = parse_input(input_stream)
    fresh_df = pl.DataFrame(fresh, schema=["start", "end"])

    while True:
        fresh_df = (
            fresh_df.sort("start")
            .with_columns(pl.col("end").shift().alias("prev_end"))
            .with_columns(
                pl.when(pl.col("start") <= pl.col("prev_end"))
                .then(pl.col("prev_end") + 1)
                .otherwise("start")
                .alias("start"),
            )
        )

        fresh_df2 = fresh_df.filter(pl.col("start") <= pl.col("end"))
        if fresh_df2.height < fresh_df.height:
            # if we dropped a row, the prev_ends are now different and we need to keep going
            fresh_df = fresh_df2
        else:
            break  # no rows dropped, we can stop

    return fresh_df.select((pl.col("end") - pl.col("start") + 1).sum()).item()
