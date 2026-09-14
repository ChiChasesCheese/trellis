"""qA01 LC 2303 Calculate Amount Paid in Taxes — YOUR implementation. Run: python drill.py test qA01"""
from __future__ import annotations

import sys
from typing import NamedTuple


class BracketLine(NamedTuple):
    lower: int
    upper: int
    percent: int
    taxable: int
    tax: float


def calculate_tax(brackets: list[list[int]], income: int) -> float:
    """Part 1 (LC signature): brackets = [[upper, percent], ...] ascending; graduated total tax."""
    # TODO
    return 0.0


def tax_breakdown(brackets: list[list[int]], income: int) -> list[BracketLine]:
    """Part 2: one BracketLine per bracket with taxable > 0, in bracket order."""
    # TODO
    return []


def calculate_tax_cents(brackets_cents: list[list[int]], income_cents: int) -> int:
    """Part 3: uppers/income in integer cents; per-bracket half-up rounding; return total cents."""
    # TODO
    return 0


def calculate_tax_mode(brackets: list[list[int]], income: int, mode: str = "graduated") -> float:
    """Part 4: 'graduated' == Part 1; 'volume' taxes the whole income at its bracket's percent."""
    # TODO
    return 0.0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / income / [MODE m] / upper,percent lines
    stdout.write("")


if __name__ == "__main__":
    main()
