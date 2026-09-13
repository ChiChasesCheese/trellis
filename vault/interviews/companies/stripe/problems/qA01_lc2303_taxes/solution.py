"""qA01 LC 2303 Calculate Amount Paid in Taxes — reference solution.

Part 1 is the LeetCode loop. Everything is computed in integers (`taxable * percent`) and divided
once per bracket, so the float result is as exact as the answer allows. Part 3 never touches floats:
per-bracket half-up rounding is `(taxable * percent + 50) // 100` cents.
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class BracketLine(NamedTuple):
    lower: int
    upper: int
    percent: int
    taxable: int
    tax: float


def _slices(brackets: list[list[int]], income: int):
    """Yield (lower, upper, percent, taxable) for every bracket whose taxable slice is > 0."""
    lower = 0
    for upper, percent in brackets:
        # income exactly == upper belongs to THIS bracket (min(income, upper) - lower == width)
        taxable = min(income, upper) - lower
        if taxable <= 0:
            break  # uppers are strictly increasing, so every later bracket is empty too
        yield lower, upper, percent, taxable
        lower = upper


def calculate_tax(brackets: list[list[int]], income: int) -> float:
    """Part 1 (LC 2303): graduated tax, float."""
    hundredths = sum(taxable * percent for _, _, percent, taxable in _slices(brackets, income))
    return hundredths / 100


def tax_breakdown(brackets: list[list[int]], income: int) -> list[BracketLine]:
    """Part 2: per-bracket invoice lines (only brackets that received income)."""
    return [
        BracketLine(lower, upper, percent, taxable, taxable * percent / 100)
        for lower, upper, percent, taxable in _slices(brackets, income)
    ]


def calculate_tax_cents(brackets_cents: list[list[int]], income_cents: int) -> int:
    """Part 3: integer cents; each bracket line rounded HALF-UP to the cent, then summed."""
    total = 0
    for _, _, percent, taxable in _slices(brackets_cents, income_cents):
        total += (taxable * percent + 50) // 100  # half-up: x.5 cents rounds away from zero
    return total


def calculate_tax_mode(brackets: list[list[int]], income: int, mode: str = "graduated") -> float:
    """Part 4: graduated (Part 1) or volume (whole income at the containing bracket's percent)."""
    if mode == "graduated":
        return calculate_tax(brackets, income)
    if mode != "volume":
        raise ValueError(f"unknown mode {mode!r}")
    if income <= 0:
        return 0.0
    for upper, percent in brackets:
        if income <= upper:  # first bracket whose upper >= income contains it (boundary inclusive)
            return income * percent / 100
    raise ValueError("income exceeds the last bracket")


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    income = int(lines[1])
    mode = "graduated"
    rest = lines[2:]
    if rest and rest[0].upper().startswith("MODE"):
        mode = rest[0].split()[1].lower()
        rest = rest[1:]
    brackets = [[int(p.strip()) for p in ln.split(",")] for ln in rest]
    if part == 1:
        out = [f"{calculate_tax(brackets, income):.2f}"]
    elif part == 2:
        out = [f"{b.lower}-{b.upper} @{b.percent}%: {b.taxable} -> {b.tax:.2f}" for b in tax_breakdown(brackets, income)]
    elif part == 3:
        cents = calculate_tax_cents(brackets, income)
        out = [f"${cents // 100}.{cents % 100:02d}"]
    else:
        out = [f"{calculate_tax_mode(brackets, income, mode):.2f}"]
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
