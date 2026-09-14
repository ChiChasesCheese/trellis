"""qA07 LC 56 Merge Intervals + LC 1288 Remove Covered Intervals — reference solution.

One sort + one sweep each. `merge` and `merge_inclusive` share `_merge(gap)` where `gap` is how far
apart two intervals may be and still merge (0 = touching real endpoints, 1 = adjacent integers).
Part 3 follows q04's BIN-range rules with inclusive integer endpoints and brand labels.
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Labeled(NamedTuple):
    start: int
    end: int
    label: str


def _merge(intervals: list[list[int]], gap: int) -> list[list[int]]:
    out: list[list[int]] = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1] + gap:  # gap=0: [1,4]+[4,5] merge ; gap=1: [1,2]+[3,4] merge
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def merge(intervals: list[list[int]]) -> list[list[int]]:
    """Part 1 (LC 56)."""
    return _merge(intervals, 0)


def merge_inclusive(intervals: list[list[int]]) -> list[list[int]]:
    """Part 4: integer ranges, adjacent integers merge."""
    return _merge(intervals, 1)


def uncovered(intervals: list[list[int]]) -> list[list[int]]:
    """Part 2: sort by (start asc, end DESC); survive iff end > max_end seen so far."""
    out: list[list[int]] = []
    max_end = float("-inf")
    for s, e in sorted(intervals, key=lambda iv: (iv[0], -iv[1])):
        if e > max_end:  # strict: an equal end means a longer-or-equal interval already covers it
            out.append([s, e])
            max_end = e
    return out


def remove_covered_intervals(intervals: list[list[int]]) -> int:
    """Part 2 (LC 1288)."""
    return len(uncovered(intervals))


def fill_gaps(labeled: list[Labeled], lo: int, hi: int) -> list[Labeled]:
    """Part 3: q04 rules. Works on mutable [start, end, label] rows, then re-wraps."""
    if not labeled:
        return []
    rows = [[s, e, lb] for s, e, lb in sorted(labeled)]
    # (1) outer ends: smallest start -> lo ; largest end -> hi (tie -> smaller start = covering one)
    rows[0][0] = lo
    top = max(range(len(rows)), key=lambda i: (rows[i][1], -rows[i][0]))
    rows[top][1] = hi
    # (2) interior gaps: extend the holder of the max end seen so far, not the previous row
    holder = 0
    for i in range(1, len(rows)):
        covered_end = rows[holder][1]
        if rows[i][0] > covered_end + 1:  # a gap of at least one integer
            rows[holder][1] = rows[i][0] - 1
        if rows[i][1] > rows[holder][1]:  # strictly larger end takes over; ties keep the earlier (covering) row
            holder = i
    # (3) merge consecutive same-label rows that touch/overlap (inclusive: next.start <= cur.end + 1)
    rows.sort()
    merged: list[list] = []
    for r in rows:
        if merged and merged[-1][2] == r[2] and r[0] <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], r[1])
        else:
            merged.append(r)
    return sorted(Labeled(s, e, lb) for s, e, lb in merged)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    if part == 3:
        lo, hi = (int(x) for x in lines[1].split())
        labeled = [Labeled(int(s), int(e), lb) for s, e, lb in (ln.split() for ln in lines[2:])]
        out = [f"{r.start} {r.end} {r.label}" for r in fill_gaps(labeled, lo, hi)]
    else:
        ivs = [[int(x) for x in ln.split()] for ln in lines[1:]]
        if part == 1:
            out = [f"{s} {e}" for s, e in merge(ivs)]
        elif part == 2:
            rest = uncovered(ivs)
            out = [str(len(rest))] + [f"{s} {e}" for s, e in rest]
        else:
            out = [f"{s} {e}" for s, e in merge_inclusive(ivs)]
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
