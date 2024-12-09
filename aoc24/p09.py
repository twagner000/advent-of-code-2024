from io import TextIOBase


def p09a(input_stream: TextIOBase) -> int:
    """Move file blocks one at a time from the right to the leftmost free space and return a checksum.

    Each digit in `input_stream` alternates between the size of a file or free space, in blocks.

    Files are assigned sequential integer IDs. The checksum sums the products of each block's position and file ID.
    """
    # expand the input into a list of blocks with IDs (use None for empty blocks)
    blocks = [i // 2 if i % 2 == 0 else None for i, x in enumerate(input_stream.read().strip()) for j in range(int(x))]

    src_i = len(blocks) - 1  # index starts from the right, search for file blocks to copy
    dest_i = 0  # index starts from left, search for empty blocks to copy file blocks into
    while src_i > dest_i:  # stop when we have no more empty blocks to the left of file blocks
        if blocks[src_i] is None:
            src_i -= 1  # keep searching for a non-empty block to copy
        elif blocks[dest_i] is not None:
            dest_i += 1  # keep searching for the next available empty block to copy into
        else:
            # swap the rightmost file block into the leftmost empty block
            blocks[dest_i], blocks[src_i] = blocks[src_i], blocks[dest_i]
            src_i -= 1
            dest_i += 1

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
