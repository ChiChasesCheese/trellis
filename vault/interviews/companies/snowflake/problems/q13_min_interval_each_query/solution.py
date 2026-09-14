"""q13 Minimum Interval to Include Each Query -- reference solution.

Part 1 is LC 1851 "Minimum Interval to Include Each Query" verbatim: intervals[i]
= [left, right] (size = right - left + 1); for each query, find the size of the
smallest interval that contains it (left <= query <= right), or -1 if none does.

Part 2 (reconstructed): instead of just the size, return which interval was
chosen -- its (start, end) -- so a caller can look up what actually covers each
query, not just how big the answer is. Tie-break when two intervals of the same
minimal size both contain the query: prefer the smaller start.

Standard offline sweep: sort intervals by start, sort queries but remember their
original index, and sweep queries in increasing order while maintaining a
min-heap (ordered by (size, start)) of every interval whose start has come into
range; lazily discard heap entries whose end has already passed the current
query. O((n + q) log n).
"""
from __future__ import annotations

import heapq
import sys


def _validate_intervals(intervals: list[list[int]]) -> list[tuple[int, int]]:
    out = []
    for iv in intervals:
        if not isinstance(iv, (list, tuple)) or len(iv) != 2:
            raise ValueError(f"interval must be [left, right]: {iv!r}")
        l, r = iv
        if not isinstance(l, int) or not isinstance(r, int) or isinstance(l, bool) or isinstance(r, bool):
            raise ValueError(f"interval bounds must be int: {iv!r}")
        if l > r:
            raise ValueError(f"left must be <= right: {iv!r}")
        out.append((l, r))
    return out


def _validate_queries(queries: list[int]) -> list[int]:
    for q in queries:
        if not isinstance(q, int) or isinstance(q, bool):
            raise ValueError(f"query must be int: {q!r}")
    return list(queries)


def _sweep(intervals: list[list[int]], queries: list[int]):
    """Yields, per original query index, the winning (size, start, end) heap
    entry or None if no interval covers that query."""
    ivs = sorted(_validate_intervals(intervals))
    qs = _validate_queries(queries)
    order = sorted(range(len(qs)), key=lambda i: qs[i])
    heap: list[tuple[int, int, int]] = []  # (size, start, end)
    result: list[tuple[int, int, int] | None] = [None] * len(qs)
    i = 0
    for qi in order:
        q = qs[qi]
        while i < len(ivs) and ivs[i][0] <= q:
            l, r = ivs[i]
            heapq.heappush(heap, (r - l + 1, l, r))
            i += 1
        while heap and heap[0][2] < q:
            heapq.heappop(heap)
        if heap:
            result[qi] = heap[0]
    return result


# --------------------------------------------------------------------------- Part 1
def min_interval_sizes(intervals: list[list[int]], queries: list[int]) -> list[int]:
    """For each query, the size of the smallest covering interval, or -1."""
    return [entry[0] if entry else -1 for entry in _sweep(intervals, queries)]


# --------------------------------------------------------------------------- Part 2
def min_interval_bounds(intervals: list[list[int]], queries: list[int]) -> list[tuple[int, int]]:
    """For each query, the (start, end) of the chosen interval (smallest size,
    ties broken by smallest start), or (-1, -1) if none covers it."""
    return [(entry[1], entry[2]) if entry else (-1, -1) for entry in _sweep(intervals, queries)]


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[list[list[int]], list[int]]:
    n, q = map(int, lines[0].split())
    intervals = [list(map(int, lines[1 + i].split())) for i in range(n)]
    queries = list(map(int, lines[1 + n].split())) if q and len(lines) > 1 + n else []
    if len(queries) != q:
        raise ValueError(f"expected {q} queries, got {len(queries)}")
    return intervals, queries


def part1(lines: list[str]) -> list[str]:
    """'n q' / n lines 'left right' / one line of q queries -> [sizes space-separated]."""
    intervals, queries = _read(lines)
    return [" ".join(map(str, min_interval_sizes(intervals, queries)))]


def part2(lines: list[str]) -> list[str]:
    """same input -> [one line: 's,e' pairs, '-1,-1' when uncovered]."""
    intervals, queries = _read(lines)
    bounds = min_interval_bounds(intervals, queries)
    return [" ".join(f"{s},{e}" for s, e in bounds)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
