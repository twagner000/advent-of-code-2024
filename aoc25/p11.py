from io import TextIOBase


def parse_input(input_stream: TextIOBase) -> str:
    return input_stream.read()


def p11a(input_stream: TextIOBase) -> int:
    print(parse_input(input_stream))


def p11b(input_stream: TextIOBase) -> int:
    print(parse_input(input_stream))
