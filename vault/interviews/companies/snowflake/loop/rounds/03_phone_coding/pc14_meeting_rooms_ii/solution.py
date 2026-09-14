"""pc14 Meeting Rooms II -- reference solution.

Intervals are HALF-OPEN `[start, end)`, the LC 253 convention: a meeting ending at `t` and another
starting at exactly `t` do NOT conflict (contrast with pc05, where the interval is closed and
touching endpoints DO conflict -- always re-check which convention a given problem uses).

Part1 is LC 253 exactly: the minimum number of rooms needed to hold every meeting. Classic
two-pointer sweep over sorted start times and sorted end times.

Part2 (reconstructed) additionally assigns a concrete room id to every meeting: process meetings
by start time (ties broken by original index, so equal-start input order decides who is "first"),
keep a min-heap of occupied rooms ordered by their current meeting's end time so a room can be
freed the moment its meeting ends, and keep a min-heap of just-freed room ids so the LOWEST free
room id is always reused before a brand new room id is minted.

Part3 (reconstructed) is a genuinely different, harder problem: a FIXED list of rooms, each with a
capacity, and meetings that each need a room whose capacity is at least the meeting's size. The
policy implemented here -- process meetings by start time (ties by index), and for each meeting
pick the room with the SMALLEST capacity that is both free and big enough (ties by lowest room id)
-- is a reasonable greedy, but it is a GREEDY, not an exact bin-packing-with-time-windows solver:
it can leave a meeting unscheduled (`None`) in situations where a different room assignment for an
earlier, still-pending meeting would have made room for it. This is expected and by design; the
tests in this kit check that the implementation matches the DOCUMENTED rule exactly (via an
independent re-implementation and a linear-scan cross-check), not that it finds a globally optimal
assignment -- finding that is `NP-hard` in general (equivalent to interval graph colouring with
typed bins).
"""

from __future__ import annotations

import sys
from heapq import heappop, heappush


def _validate_intervals(intervals: list[list[int]]) -> None:
    for iv in intervals:
        if len(iv) != 2:
            raise ValueError(f"interval must be [start, end], got {iv!r}")
        s, e = iv
        if s >= e:
            raise ValueError(f"a meeting must have positive duration (start < end), got {iv!r}")


# --------------------------------------------------------------------------- Part 1
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    _validate_intervals(intervals)
    if not intervals:
        return 0
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = max_rooms = 0
    i = j = 0
    n = len(intervals)
    while i < n and j < n:
        if starts[i] < ends[j]:
            rooms += 1
            max_rooms = max(max_rooms, rooms)
            i += 1
        else:
            rooms -= 1
            j += 1
    return max_rooms


# --------------------------------------------------------------------------- Part 2
def assign_rooms(intervals: list[list[int]]) -> list[int]:
    """Room id (0-based) for each meeting, in the ORIGINAL input order. Lowest free room id wins;
    ties among simultaneously-starting meetings are broken by original index."""
    _validate_intervals(intervals)
    order = sorted(range(len(intervals)), key=lambda i: (intervals[i][0], i))
    busy: list[tuple[int, int]] = []  # (end_time, room_id), min-heap by end_time
    free_ids: list[int] = []  # min-heap of currently-unused room ids
    next_id = 0
    result = [0] * len(intervals)
    for i in order:
        start, end = intervals[i]
        while busy and busy[0][0] <= start:
            _, freed = heappop(busy)
            heappush(free_ids, freed)
        if free_ids:
            room = heappop(free_ids)
        else:
            room = next_id
            next_id += 1
        result[i] = room
        heappush(busy, (end, room))
    return result


# --------------------------------------------------------------------------- Part 3
def assign_rooms_with_capacity(
    meetings: list[tuple[int, int, int]], capacities: list[int]
) -> list[int | None]:
    """Fixed rooms `capacities[r]`. Room id (0-based) for each meeting in ORIGINAL order, or None
    if the greedy below could not place it. Greedy: process meetings by start time (ties by
    original index); among rooms both free at that start time and big enough, pick the SMALLEST
    capacity (ties by lowest room id) -- reserves large rooms for meetings that actually need them.
    NOT guaranteed globally optimal -- see module docstring."""
    if any(c < 0 for c in capacities):
        raise ValueError("capacities must be >= 0")
    for start, end, size in meetings:
        if start >= end:
            raise ValueError(f"a meeting must have positive duration (start < end), got {(start, end, size)!r}")
        if size <= 0:
            raise ValueError(f"meeting size must be > 0, got {size}")
    order = sorted(range(len(meetings)), key=lambda i: (meetings[i][0], i))
    free_at = [0] * len(capacities)  # each room is free from time 0
    result: list[int | None] = [None] * len(meetings)
    for i in order:
        start, end, size = meetings[i]
        candidates = [r for r, cap in enumerate(capacities) if cap >= size and free_at[r] <= start]
        if not candidates:
            continue
        best = min(candidates, key=lambda r: (capacities[r], r))
        result[i] = best
        free_at[best] = end
    return result


# --------------------------------------------------------------------------- line-driven wrappers
def _read_intervals(lines: list[str], idx: int) -> tuple[list[list[int]], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    intervals = [list(map(int, lines[idx + t].split())) for t in range(n)]
    return intervals, idx + n


def part1(lines: list[str]) -> list[str]:
    """'N n' / n 'start end' lines -> one line: the minimum number of rooms."""
    intervals, _ = _read_intervals(lines, 0)
    return [str(min_meeting_rooms(intervals))]


def part2(lines: list[str]) -> list[str]:
    """Same input -> one 'room' line per meeting, in original order."""
    intervals, _ = _read_intervals(lines, 0)
    return [str(r) for r in assign_rooms(intervals)]


def part3(lines: list[str]) -> list[str]:
    """'N n' / n 'start end size' lines / 'C m' / m capacities (one per line) -> one line per
    meeting (original order): the assigned room id, or '-' if unschedulable."""
    tag, n = lines[0].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[0]!r}")
    n = int(n)
    meetings = [tuple(map(int, lines[1 + t].split())) for t in range(n)]
    idx = 1 + n
    tag, m = lines[idx].split()
    if tag != "C":
        raise ValueError(f"expected 'C <m>', got {lines[idx]!r}")
    m = int(m)
    capacities = [int(lines[idx + 1 + t]) for t in range(m)]
    assignment = assign_rooms_with_capacity(meetings, capacities)
    return [str(r) if r is not None else "-" for r in assignment]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
