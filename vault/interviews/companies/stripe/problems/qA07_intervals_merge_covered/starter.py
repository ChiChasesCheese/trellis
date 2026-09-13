"""qA07 LC 56 Merge Intervals + LC 1288 Remove Covered Intervals — YOUR implementation. Run: python drill.py test qA07"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Labeled(NamedTuple):
    start: int
    end: int
    label: str


def merge(intervals: list[list[int]]) -> list[list[int]]:
    """Part 1 (LC 56): merge overlapping/touching closed intervals; sorted by start."""
    # TODO
    return []


def uncovered(intervals: list[list[int]]) -> list[list[int]]:
    """Part 2: intervals not covered by another, sorted by start (duplicates -> one copy)."""
    # TODO
    return []


def remove_covered_intervals(intervals: list[list[int]]) -> int:
    """Part 2 (LC 1288): number of intervals that survive."""
    # TODO
    return 0


def fill_gaps(labeled: list[Labeled], lo: int, hi: int) -> list[Labeled]:
    """Part 3 (q04 rules): extend ends to [lo, hi], fill gaps by the holder of the max end, merge
    consecutive same-label touching intervals. Sorted by (start, end, label)."""
    # TODO
    return []


def merge_inclusive(intervals: list[list[int]]) -> list[list[int]]:
    """Part 4: LC 56 on integer ranges — adjacent integers ([1,2],[3,4]) merge too."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / intervals
    stdout.write("")


if __name__ == "__main__":
    main()
