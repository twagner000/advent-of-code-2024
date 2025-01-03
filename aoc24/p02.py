from io import TextIOBase

import pandas as pd


def check_report(report: str | list) -> bool:
    """Return True if the report is safe.

    A report is safe if both of the following are true:

    1. All levels are increasing or decreasing.
    2. All differences between adjacent levels are between 1 and 3.
    """
    if isinstance(report, str):
        report = report.split()
    diffs = pd.Series(report, dtype=int).diff().dropna()
    return ((diffs > 0).all() or (diffs < 0).all()) and (diffs.abs() >= 1).all() and (diffs.abs() <= 3).all()


def check_report_with_problem_dampener(report: str) -> bool:
    """Return True if the report is safe, or if it can be made safe by dropping a single level from the report."""
    levels = report.split()
    for drop_index in range(-1, len(levels)):
        if drop_index < 0 and check_report(levels) or check_report(levels[:drop_index] + levels[drop_index + 1 :]):
            return True
    return False


def p02a(input_stream: TextIOBase) -> int:
    """Return number of safe reports (rows)."""
    puzzle_input = pd.read_csv(input_stream, names=["levels"])
    return puzzle_input["levels"].apply(check_report).sum()


def p02b(input_stream: TextIOBase) -> int:
    """Return number of safe reports (rows), with the Problem Dampener enabled."""
    puzzle_input = pd.read_csv(input_stream, names=["levels"])
    return puzzle_input["levels"].apply(check_report_with_problem_dampener).sum()
