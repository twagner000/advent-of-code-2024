from collections import defaultdict
from functools import reduce
from io import TextIOBase


def p23a(input_stream: TextIOBase) -> int:
    """TBD."""
    pairs = [x.strip().split("-") for x in input_stream]
    linked = defaultdict(list)
    for a, b in pairs:
        linked[a].append(b)
        linked[b].append(a)
    triples = set()
    for a, v in linked.items():
        for b in v:
            for c in linked[b]:
                if c in v:
                    triples.add(tuple(sorted([a, b, c])))
    t_triples = set()
    for a, c, b in triples:
        if a[0] == "t" or b[0] == "t" or c[0] == "t":
            t_triples.add((a, b, c))
    return len(t_triples)


def p23b(input_stream: TextIOBase) -> int:
    """TBD."""
    pairs = sorted([x.strip().split("-") for x in input_stream])
    linked = defaultdict(set)
    for a, b in pairs:
        linked[a].add(b)
        linked[b].add(a)
    linked = {k: {k} | v for k, v in linked.items()}
    groups = {tuple(sorted(pair)) for pair in pairs}
    while True:
        new_groups = set()
        for group in groups:
            for expansion in reduce(lambda a, b: a & b, (linked[x] for x in group)) - set(group):
                new_groups.add(tuple(sorted([*group, expansion])))
        if not new_groups:
            break
        groups = new_groups
    return ",".join(groups.pop())
