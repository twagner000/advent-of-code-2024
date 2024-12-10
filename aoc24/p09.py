from io import TextIOBase


def p09a(input_stream: TextIOBase) -> int:
    """Move file blocks one at a time from the right to the leftmost free space and return a checksum.

    Each digit in `input_stream` alternates between the size of a file or free space, in blocks.

    Files are assigned sequential integer IDs. The checksum sums the products of each block's position and file ID.
    """
    # expand the input into a list of blocks with IDs (use None for empty blocks)
    blocks = [i // 2 if i % 2 == 0 else None for i, x in enumerate(input_stream.read().strip()) for j in range(int(x))]

    src_i = len(blocks) - 1  # "source" index from right (search for file blocks to copy)
    dest_i = 0  # "destination" index from left (search for empty blocks to copy file blocks into)
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


def p09b(input_stream: TextIOBase) -> int:
    """TBD."""
    disk_map = input_stream.read().strip()
    blocks = [(i // 2 if i % 2 == 0 else None, int(x)) for i, x in enumerate(disk_map)]
    for file in blocks[-1::-2]:
        src_i = blocks.index(file)  # index of file we're trying to move
        dest_i = 0  # index of file/space we're trying to move the file into
        while (dest := blocks[dest_i]) != file:  # stop once we've hit our file
            if dest[0] is None and dest[1] >= file[1]:
                blocks[src_i] = (None, file[1])  # replace the original file location with empty space
                blocks[dest_i] = file
                if (remainder := dest[1] - file[1]) > 0:
                    # if our file was smaller than the empty space, we need to keep the remainder
                    if blocks[dest_i + 1][0] is None:
                        blocks[dest_i + 1] = (None, blocks[dest_i + 1][1] + remainder)  # merge into following space
                    else:
                        blocks.insert(dest_i + 1, (None, remainder))  # add new block with remainder
                break
            dest_i += 1

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
