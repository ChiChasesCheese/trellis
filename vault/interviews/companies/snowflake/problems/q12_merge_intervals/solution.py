"""q12 Merge Intervals -- reference solution.

Part 1 is LC 56 "Merge Intervals" verbatim: given an array of intervals, merge all
overlapping intervals and return an array of the non-overlapping intervals that
cover all the intervals in the input, sorted by start. Touching intervals (end of
one == start of the next, e.g. [1,4],[4,5]) count as overlapping per the official
examples.

Part 2 (reconstructed): intervals arrive one at a time over a stream (`add`), and
at any point the caller can ask for the merged view so far (`snapshot`). This
models a live "busy time" tracker where a client keeps registering intervals and
occasionally needs the current merged picture -- e.g. up to 1e5 add/snapshot
calls total.
"""
from __future__ import annotations

import sys


def _validate_interval(iv) -> tuple[int, int]:
    if not isinstance(iv, (list, tuple)) or len(iv) != 2:
        raise ValueError(f"interval must be a 2-element [start, end]: {iv!r}")
    s, e = iv
    if not isinstance(s, int) or not isinstance(e, int) or isinstance(s, bool) or isinstance(e, bool):
        raise ValueError(f"interval bounds must be int: {iv!r}")
    if s > e:
        raise ValueError(f"start must be <= end: {iv!r}")
    return s, e


# --------------------------------------------------------------------------- Part 1
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """LC56: merge all overlapping (including touching) intervals, sorted by start."""
    pairs = [_validate_interval(iv) for iv in intervals]
    if not pairs:
        return []
    pairs.sort(key=lambda p: (p[0], p[1]))
    merged: list[list[int]] = [list(pairs[0])]
    for s, e in pairs[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


# --------------------------------------------------------------------------- Part 2
class IntervalStream:
    """Intervals arrive one at a time; `snapshot()` returns the merged view so far.

    O(1) amortized `add` (just buffers), O(m log m) `snapshot` where m is the
    number of intervals seen so far -- fine as long as `snapshot` is called
    sparsely relative to `add`, which is the realistic access pattern (many
    writes, occasional reads).
    """

    def __init__(self) -> None:
        self._intervals: list[list[int]] = []

    def add(self, interval: list[int]) -> None:
        s, e = _validate_interval(interval)
        self._intervals.append([s, e])

    def snapshot(self) -> list[list[int]]:
        return merge_intervals(self._intervals)


# --------------------------------------------------------------------------- line-driven wrappers
def _fmt(intervals: list[list[int]]) -> str:
    return " ".join(f"{s},{e}" for s, e in intervals)


def part1(lines: list[str]) -> list[str]:
    """'n' / n lines 'start end' -> [one line: merged intervals as 's,e' pairs]."""
    n = int(lines[0])
    intervals = [list(map(int, ln.split())) for ln in lines[1 : 1 + n]]
    return [_fmt(merge_intervals(intervals))]


def part2(lines: list[str]) -> list[str]:
    """'m' / m lines 'ADD s e' or 'SNAPSHOT' -> one output line per SNAPSHOT."""
    m = int(lines[0])
    stream = IntervalStream()
    out: list[str] = []
    for ln in lines[1 : 1 + m]:
        parts = ln.split()
        if parts[0] == "ADD":
            stream.add([int(parts[1]), int(parts[2])])
        elif parts[0] == "SNAPSHOT":
            out.append(_fmt(stream.snapshot()))
        else:
            raise ValueError(f"unknown op: {ln!r}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
