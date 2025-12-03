from io import TextIOBase

import numpy as np


def parse_battery_banks(input_stream: TextIOBase) -> np.ndarray:
    """Parse input as a numpy array of single-digit joltage rating, where a row is a bank of batteries."""
    return np.array([[int(x) for x in bank] for bank in input_stream.read().strip().split()])


def maximize_joltage(bank: np.ndarray, digits: int, value: int = 0) -> tuple[int, np.ndarray | None, int]:
    """Recursively maximize the total joltage value for a bank of batteries."""
    if digits == 1:
        return value * 10 + bank.max(), None, 0
    dig_idx = bank[: -digits + 1].argmax()
    dig = bank[dig_idx]
    return maximize_joltage(bank[dig_idx + 1 :], digits - 1, value * 10 + dig)


def p03a(input_stream: TextIOBase) -> int:
    """Sum the maximium joltage of all battery banks, where 2 sequential digits are used from each bank."""
    batteries = parse_battery_banks(input_stream)
    return sum(maximize_joltage(bank, 2)[0] for bank in batteries)


def p03b(input_stream: TextIOBase) -> int:
    """Sum the maximium joltage of all battery banks, where 12 sequential digits are used from each bank."""
    batteries = parse_battery_banks(input_stream)
    return sum(maximize_joltage(bank, 12)[0] for bank in batteries)
