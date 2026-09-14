"""q13 Minimum Interval to Include Each Query -- YOUR implementation.
Run the tests against this file with IMPL=starter.
"""

from __future__ import annotations

import sys


def min_interval_sizes(intervals: list[list[int]], queries: list[int]) -> list[int]:
    """Part1: LC1851. For each query, size of the smallest interval containing it, or -1.
    ValueError for a malformed interval (not length 2, non-int, or left > right) or
    a non-int query."""
    # TODO
    return []


def min_interval_bounds(intervals: list[list[int]], queries: list[int]) -> list[tuple[int, int]]:
    """Part2: for each query, the (start, end) of the chosen interval (smallest size,
    ties broken by smallest start), or (-1, -1) if none covers it."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'n q' / n lines 'left right' / one line of q queries -> [sizes space-separated]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> [one line: 's,e' pairs, '-1,-1' when uncovered]."""
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
