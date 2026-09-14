"""q14 Maximum Product of the Length of Two Palindromic Subsequences -- YOUR implementation.
Run the tests against this file with IMPL=starter.
"""

from __future__ import annotations

import sys


def max_product_two_palindromic_subsequences(s: str) -> int:
    """Part1: LC2002. 2 <= len(s) <= 12, lowercase a-z. Max product of the lengths
    of two DISJOINT palindromic subsequences. ValueError if s is out of bounds or
    has non-lowercase characters."""
    # TODO
    return 0


def max_product_with_subsequences(s: str) -> tuple[list[int], list[int]]:
    """Part2: one optimal disjoint pair of index lists (ascending) achieving the
    Part1 maximum. Any valid optimal pair is accepted."""
    # TODO
    return [], []


def part1(lines: list[str]) -> list[str]:
    """one line: s -> [max product]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """one line: s -> [two lines: comma-separated indices for each subsequence]."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
