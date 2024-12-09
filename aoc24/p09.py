from io import TextIOBase


def p09a(input_stream: TextIOBase) -> int:
    """TBD."""
    disk_map = input_stream.read().strip()
    files = [int(x) for x in disk_map[::2]]
    free_space = [int(x) for x in disk_map[1::2]] + [1]
    blocks = []
    for i, (file, free) in enumerate(zip(files, free_space, strict=False)):
        blocks += file * [i] + free * [None]
    for i in range(-1, -len(blocks) + 1, -1):
        first_dot = blocks.index(None)
        if len(set(blocks[first_dot:])) == 1:
            break
        if (cur_digit := blocks[i]) is None:
            continue
        blocks[first_dot] = cur_digit
        blocks[i] = None
    return sum(i * v for i, v in enumerate(blocks) if v is not None)


def p09b(input_stream: TextIOBase) -> int:  # noqa: C901
    """TBD."""
    disk_map = input_stream.read().strip()
    blocks = [(i // 2 if i % 2 == 0 else None, int(x)) for i, x in enumerate(disk_map)]
    for src_id in range(blocks[-1][0], 0, -1):
        for src_idx, src in enumerate(blocks):  # noqa: B007
            if src[0] == src_id:
                src_size = src[1]
                break
        for dest_idx, (dest_id, dest_size) in enumerate(blocks[:src_idx]):
            if dest_id is not None:
                continue
            if dest_size == src_size:
                # swap
                blocks[src_idx], blocks[dest_idx] = blocks[dest_idx], blocks[src_idx]
                break
            if dest_size > src_size:
                # dest becomes src + a new empty block (remainder)
                blocks[dest_idx] = (src_id, src_size)
                blocks[src_idx] = (None, src_size)
                blocks.insert(dest_idx + 1, (None, dest_size - src_size))
                break
        # consolidate empty blocks
        i = 1
        while i < len(blocks):
            if blocks[i - 1][0] == blocks[i][0] and blocks[i][0] is None:
                blocks[i - 1] = (None, blocks[i - 1][1] + blocks[i][1])
                blocks.pop(i)
            i += 1
    i = 0
    total = 0
    for x, n in blocks:
        if x is None:
            i += n
            continue
        for _ in range(n):
            total += x * i
            i += 1
    return total
