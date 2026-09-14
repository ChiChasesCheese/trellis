"""pc09 Parallel Courses III -- reference solution.

Part1 is LC 2050 exactly: `n` courses (1-based ids), `relations[i] = [prevCourse, nextCourse]`
(1-based) meaning prevCourse must finish before nextCourse starts, `time[i]` (0-based) is how long
course `i+1` takes. Arbitrarily many courses may run in parallel as long as their prerequisites are
done. Return the minimum months to finish every course.

Standard Kahn topological sweep (iterative -- a recursive DFS would blow the stack on the
5*10^4-long chain LC's own stress tests use): `finish[v] = time[v] + max(finish[u] for u in
preds(v))` (0 if `v` has no predecessors), relaxed as each predecessor is popped off the queue so
`v`'s value is only read once every predecessor has contributed. The answer is `max(finish)`.
`relations` that do not form a DAG (a cycle) raise `ValueError` -- LC guarantees a DAG, but nothing
stops a caller from handing us a bad graph.

Part2 (reconstructed) returns one CRITICAL PATH: a chain of courses c1 -> c2 -> ... -> ck, each an
immediate prerequisite of the next, whose total time equals `minimum_time(...)`. By optimal
substructure of the `finish` DP, every such chain is built entirely from "tight" edges (u, v) with
`finish[v] == finish[u] + time[v]`), starts at a true source (no predecessors) and ends at a node
whose `finish` equals the global maximum. Among every such chain we want the LEXICOGRAPHICALLY
SMALLEST sequence of course ids. Because tight edges always go from a strictly smaller `finish`
value to a strictly larger one, processing nodes in decreasing `finish` order lets us compute, for
every node v, the lexicographically smallest "suffix" chain starting at v in one backward-DP pass:
    best_suffix(v) = [v]                                        if finish[v] == global_max
    best_suffix(v) = [v] + min(best_suffix(w) for tight w)       otherwise
(Python list comparison is exactly lexicographic, prefix-shorter-is-smaller included.) The final
answer is the smallest `best_suffix(source)` over every true source that can reach the maximum.
This is O(n + m) node/edge work plus the cost of the `min()` list comparisons, which can touch
O(n) elements each in a pathological single chain -- fine at the `n <= 2000` scale Part2 is
exercised at; see problem.md for why Part1's 5*10^4-node perf test is not repeated for Part2.
"""

from __future__ import annotations

import sys
from collections import deque


def _validate(n: int, relations: list[list[int]], time: list[int]) -> None:
    if n < 1:
        raise ValueError("n must be >= 1")
    if len(time) != n:
        raise ValueError(f"time must have exactly n={n} entries, got {len(time)}")
    if any(t < 1 for t in time):
        raise ValueError("every course time must be >= 1")
    for rel in relations:
        if len(rel) != 2:
            raise ValueError(f"relation must be [prevCourse, nextCourse], got {rel!r}")
        u, v = rel
        if not (1 <= u <= n) or not (1 <= v <= n):
            raise ValueError(f"relation {rel!r} references a course outside 1..{n}")
        if u == v:
            raise ValueError(f"a course cannot be its own prerequisite: {rel!r}")


def _build(n: int, relations: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    g: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in relations:
        g[u - 1].append(v - 1)
        indeg[v - 1] += 1
    return g, indeg


def _finish_times(n: int, g: list[list[int]], indeg0: list[int], time: list[int]) -> list[int]:
    """Kahn sweep computing finish[v] = time[v] + max(finish[pred], default 0). Iterative."""
    indeg = indeg0[:]
    finish = [0] * n
    dq: deque[int] = deque()
    for i in range(n):
        if indeg[i] == 0:
            finish[i] = time[i]
            dq.append(i)
    processed = 0
    while dq:
        u = dq.popleft()
        processed += 1
        for v in g[u]:
            cand = finish[u] + time[v]
            if cand > finish[v]:
                finish[v] = cand
            indeg[v] -= 1
            if indeg[v] == 0:
                dq.append(v)
    if processed != n:
        raise ValueError("relations contain a cycle -- not a valid DAG of prerequisites")
    return finish


# --------------------------------------------------------------------------- Part 1
def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    _validate(n, relations, time)
    g, indeg0 = _build(n, relations)
    finish = _finish_times(n, g, indeg0, time)
    return max(finish)


# --------------------------------------------------------------------------- Part 2
def critical_path(n: int, relations: list[list[int]], time: list[int]) -> tuple[int, list[int]]:
    """(minimum_time, one lexicographically smallest critical path, 1-based course ids)."""
    _validate(n, relations, time)
    g, indeg0 = _build(n, relations)
    finish = _finish_times(n, g, indeg0, time)
    global_max = max(finish)

    order = sorted(range(n), key=lambda i: -finish[i])  # decreasing finish: successors first
    best_suffix: list[list[int] | None] = [None] * n
    for v in order:
        if finish[v] == global_max:
            best_suffix[v] = [v + 1]
            continue
        candidates = [
            best_suffix[w]
            for w in g[v]
            if best_suffix[w] is not None and finish[w] == finish[v] + time[w]
        ]
        best_suffix[v] = [v + 1] + min(candidates) if candidates else None

    sources = [i for i in range(n) if indeg0[i] == 0]
    chains = [best_suffix[i] for i in sources if best_suffix[i] is not None]
    return global_max, min(chains)


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str], idx: int) -> tuple[int, list[list[int]], list[int], int]:
    n, m = map(int, lines[idx].split())
    idx += 1
    relations = [list(map(int, lines[idx + t].split())) for t in range(m)]
    idx += m
    time = list(map(int, lines[idx].split()))
    return n, relations, time, idx + 1


def part1(lines: list[str]) -> list[str]:
    """'n m' / m relation lines 'u v' / one line of n times -> one line: minimum_time."""
    n, relations, time, _ = _read(lines, 0)
    return [str(minimum_time(n, relations, time))]


def part2(lines: list[str]) -> list[str]:
    """Same input -> line 1 minimum_time, line 2 the critical path course ids space-separated."""
    n, relations, time, _ = _read(lines, 0)
    best, path = critical_path(n, relations, time)
    return [str(best), " ".join(map(str, path))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
