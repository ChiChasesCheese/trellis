"""q04 Card Range Obfuscation — reference solution.

Everything is integer arithmetic on FULL 16-digit numbers (BIN * 10^10 + offset).  Endpoints are
inclusive, so a gap between `covered_end` and `next.start` is closed with `end = next.start - 1`,
and "touching" means `end + 1 == next.start`.
"""
from __future__ import annotations

import sys

OFFSET_SPAN = 10**10  # 10-digit offsets: 0000000000 .. 9999999999

Interval = list  # [start, end, brand] — mutable so extension can edit in place


def parse(lines: list[str]) -> tuple[int, list[Interval]]:
    """Return (LO, intervals) where LO = BIN * 10^10 and intervals hold full numbers."""
    lines = [ln.strip() for ln in lines if ln.strip()]
    lo = int(lines[0]) * OFFSET_SPAN
    # lines[1] is N; we trust the lines that are actually present (tolerates N mismatch)
    intervals: list[Interval] = []
    for raw in lines[2:]:
        s, e, brand = (p.strip() for p in raw.split(","))
        intervals.append([full(lo, s), full(lo, e), brand])
    return lo, intervals


def full(lo: int, token: str) -> int:
    """10-digit offset -> full number; a token that is already >= 10^10 is a full number."""
    n = int(token)
    return n if n >= OFFSET_SPAN else lo + n


def sort_key(iv: Interval):
    return (iv[0], iv[1], iv[2])  # start, then end, then brand — deterministic


def render(intervals: list[Interval]) -> list[str]:
    intervals.sort(key=sort_key)  # sort on FINAL values
    return [f"{s:016d},{e:016d},{b}" for s, e, b in intervals]


def extend_outer(lo: int, hi: int, intervals: list[Interval]) -> None:
    """Part 1: smallest start -> LO; largest end -> HI (ties: first in sorted order)."""
    if not intervals:
        return
    intervals.sort(key=sort_key)
    intervals[0][0] = lo
    max(intervals, key=lambda iv: (iv[1], -iv[0]))[1] = hi  # largest end; tie -> smaller start


def fill_gaps(intervals: list[Interval]) -> None:
    """Part 2 + 3: close every interior gap by extending the interval that owns the highest end
    seen so far (the *covering* interval), never the contained one printed just before the gap."""
    intervals.sort(key=sort_key)
    owner = None  # interval holding the running maximum end
    for iv in intervals:
        if owner is not None and iv[0] > owner[1] + 1:  # strict: end+1 == start is touching, no gap
            owner[1] = iv[0] - 1  # inclusive endpoints
        if owner is None or iv[1] > owner[1]:  # strict '>' keeps the earlier (smaller-start) owner on ties
            owner = iv


def merge_same_brand(intervals: list[Interval]) -> list[Interval]:
    """Part 4: merge consecutive intervals with the identical brand that touch or overlap."""
    intervals.sort(key=sort_key)
    merged: list[Interval] = []
    for iv in intervals:
        cur = merged[-1] if merged else None
        if cur is not None and cur[2] == iv[2] and iv[0] <= cur[1] + 1:  # same brand, touching/overlap
            cur[1] = max(cur[1], iv[1])
        else:
            merged.append(list(iv))
    return merged


def obfuscate(lines: list[str], part: int = 4) -> list[str]:
    lo, intervals = parse(lines)
    hi = lo + OFFSET_SPAN - 1
    if not intervals:  # N = 0: nothing to assign a brand to
        return []
    extend_outer(lo, hi, intervals)
    if part >= 2:
        fill_gaps(intervals)
    if part >= 4:
        intervals = merge_same_brand(intervals)
    return render(intervals)


def part1(lines: list[str]) -> list[str]:
    return obfuscate(lines, 1)


def part2(lines: list[str]) -> list[str]:
    return obfuscate(lines, 2)


def part3(lines: list[str]) -> list[str]:
    return obfuscate(lines, 3)  # same algorithm as Part 2 when Part 2 tracks the covering interval


def part4(lines: list[str]) -> list[str]:
    return obfuscate(lines, 4)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 4  # no PART line -> the full, accumulated rule set
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = obfuscate(lines, part) if lines else []
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
