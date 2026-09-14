"""pc14 Meeting Rooms II -- YOUR implementation. Run the tests against this file with IMPL=starter.

See problem.md: intervals are HALF-OPEN [start, end) -- touching endpoints do NOT conflict (the
opposite convention from pc05's closed intervals).
"""

from __future__ import annotations

import sys


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """Part1 (LC 253): minimum rooms needed. Raise ValueError if start >= end for any interval (positive duration required)."""
    # TODO
    return 0


def assign_rooms(intervals: list[list[int]]) -> list[int]:
    """Part2: room id (0-based) per meeting, in ORIGINAL order. Lowest free room id wins; ties on
    start time broken by original index."""
    # TODO
    return []


def assign_rooms_with_capacity(
    meetings: list[tuple[int, int, int]], capacities: list[int]
) -> list[int | None]:
    """Part3: fixed rooms with capacities; meetings have sizes. Greedy: smallest adequate free
    room (ties by lowest room id). None if unschedulable. NOT guaranteed globally optimal."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'N n' / n 'start end' lines -> one line: the minimum number of rooms."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same input -> one 'room' line per meeting, in original order."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """'N n' / n 'start end size' lines / 'C m' / m capacities (one per line) -> one line per
    meeting (original order): the assigned room id, or '-' if unschedulable."""
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
