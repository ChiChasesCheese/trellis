"""q12 Merge Intervals -- YOUR implementation. Run the tests against this file with IMPL=starter.

Merge all overlapping (including touching) intervals; then support a live add/snapshot stream.
"""

from __future__ import annotations

import sys


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Part1: LC56. Merge overlapping/touching intervals, sorted by start.
    ValueError for a malformed interval (not length 2, non-int, or start > end)."""
    # TODO
    return []


class IntervalStream:
    """Part2: add(interval) buffers; snapshot() returns the merged view so far."""

    def __init__(self) -> None:
        # TODO
        pass

    def add(self, interval: list[int]) -> None:
        # TODO
        pass

    def snapshot(self) -> list[list[int]]:
        # TODO
        return []


def part1(lines: list[str]) -> list[str]:
    """'n' / n lines 'start end' -> [one line: merged intervals as 's,e' pairs]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """'m' / m lines 'ADD s e' or 'SNAPSHOT' -> one output line per SNAPSHOT."""
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
