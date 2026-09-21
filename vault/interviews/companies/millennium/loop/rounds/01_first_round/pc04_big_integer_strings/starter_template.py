"""pc04 Big-Integer String Arithmetic -- YOUR implementation. Run tests against this file
with IMPL=starter.

Add / subtract / multiply arbitrary-precision numbers given as digit strings, without ever
converting through int() -- do the carry/borrow bookkeeping by hand, like on paper.
"""

from __future__ import annotations

import sys

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
_VALUE = {c: i for i, c in enumerate(_DIGITS)}


def add_unsigned(a: str, b: str) -> str:
    """Part1: add two non-negative decimal digit strings. '' is invalid (ValueError).
    Leading zeros in the operands are tolerated; the result has none (except "0" itself)."""
    # TODO
    return ""


def add_signed(a: str, b: str) -> str:
    """Part2: decimal add with an optional leading '-' (or '+') sign. "0" is never signed."""
    # TODO
    return ""


def subtract_signed(a: str, b: str) -> str:
    """Part2: a - b, same sign rules as add_signed."""
    # TODO
    return ""


def multiply_signed(a: str, b: str, base: int = 10) -> str:
    """Part3: signed multiplication in an arbitrary base (2..36, digits '0'-'9' then 'a'-'z',
    case-insensitive input). O(len(a) * len(b)). ValueError for base outside [2, 36] or an
    operand with a digit not valid in that base."""
    # TODO
    return ""


def part1(lines: list[str]) -> list[str]:
    """each line: '<a> <b>' -> add_unsigned(a, b)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """each line: 'ADD <a> <b>' or 'SUB <a> <b>'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """each line: '<a> <b> <base>' -> multiply_signed(a, b, base)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
