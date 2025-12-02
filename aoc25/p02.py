from io import TextIOBase


def parse_instructions(input_stream: TextIOBase) -> list[tuple[int, ...]]:
    """Parse product ID ranges."""
    return [tuple(int(y) for y in x.split("-")) for x in input_stream.read().strip().replace("\n", "").split(",")]


def p02a(input_stream: TextIOBase) -> int:
    """Find "invalid" product IDs in the given ranges.

    A product ID is invalid if it has an even number of digits
    and the first half equals the second half, e.g. 1010.
    """
    invalids = []
    for id_range in parse_instructions(input_stream):
        for i in range(id_range[0], id_range[1] + 1):
            i_str = str(i)
            i_len = len(i_str)
            if i_len % 2 == 0 and i_str[: i_len // 2] == i_str[i_len // 2 :]:
                invalids.append(i)
    return sum(invalids)


def p02b(input_stream: TextIOBase) -> int:
    """Find "invalid" product IDs in the given ranges.

    A product ID is invalid if it's entirely composed of repeated sequences,
    e.g. 1010, 123123123, 1111111.
    """
    invalids = []
    for id_range in parse_instructions(input_stream):
        for i in range(id_range[0], id_range[1] + 1):
            i_str = str(i)
            i_len = len(i_str)
            for seq_len in range(1, i_len // 2 + 1):
                if i_len % seq_len != 0:
                    continue  # i_len must be multiple of seq_len for sequence to repeat in full
                if all(i_str[:seq_len] == i_str[j : j + seq_len] for j in range(seq_len, i_len, seq_len)):
                    invalids.append(i)
                    break
    return sum(invalids)
