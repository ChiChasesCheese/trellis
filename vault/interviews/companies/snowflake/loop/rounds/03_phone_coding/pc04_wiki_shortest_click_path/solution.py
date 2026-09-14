"""pc04 Wiki Shortest Click Path -- reference solution.

Part1 is plain BFS distance. Part2 needs the *lexicographically smallest* path among all shortest
paths -- greedily picking "the smallest-named neighbor" during a forward BFS does NOT guarantee
that (a locally smallest choice can dead-end into a longer detour before reaching `end`). The
standard correct technique: BFS backwards from `end` over the REVERSED graph to get, for every
node, its shortest distance TO `end`; then walk forward from `start`, at each step choosing the
lexicographically smallest neighbor whose distance-to-end is exactly one less than the current
node's -- that neighbor is guaranteed to still be on a shortest path.

Part3 crawls lazily via a `fetch` callback (links are not known ahead of time) that may raise;
failed fetches are treated as dead ends (no outgoing links) and counted, but do not stop the
crawl. Because the reverse graph isn't available up front in a lazy crawl, Part3 cannot offer
Part2's global lexicographic-minimum guarantee -- it gives *a* shortest path, deterministically
(BFS visits each node's freshly-fetched neighbors in sorted order, first discovery wins).
"""

from __future__ import annotations

import sys
from collections import deque
from typing import Callable


# --------------------------------------------------------------------------- Part 1
def shortest_path_length(graph: dict[str, list[str]], start: str, end: str) -> int:
    """BFS distance from start to end over directed edges `graph[u] -> [v, ...]`. -1 if
    unreachable; 0 if start == end."""
    if start == end:
        return 0
    visited = {start}
    q: deque[tuple[str, int]] = deque([(start, 0)])
    while q:
        node, d = q.popleft()
        for nxt in graph.get(node, []):
            if nxt == end:
                return d + 1
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, d + 1))
    return -1


# --------------------------------------------------------------------------- Part 2
def _reverse_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    rev: dict[str, list[str]] = {}
    for u, neighbors in graph.items():
        for v in neighbors:
            rev.setdefault(v, []).append(u)
    return rev


def shortest_path(graph: dict[str, list[str]], start: str, end: str) -> list[str]:
    """The lexicographically smallest sequence of page names among ALL shortest start->end
    paths. Empty list if unreachable."""
    if start == end:
        return [start]

    rev = _reverse_graph(graph)
    dist_to_end: dict[str, int] = {end: 0}
    q: deque[str] = deque([end])
    while q:
        node = q.popleft()
        for prev in rev.get(node, []):
            if prev not in dist_to_end:
                dist_to_end[prev] = dist_to_end[node] + 1
                q.append(prev)

    if start not in dist_to_end:
        return []

    path = [start]
    current = start
    while current != end:
        remaining = dist_to_end[current] - 1
        candidates = [n for n in graph.get(current, []) if dist_to_end.get(n) == remaining]
        nxt = min(candidates)
        path.append(nxt)
        current = nxt
    return path


# --------------------------------------------------------------------------- Part 3
def crawl_shortest_path(
    fetch: Callable[[str], list[str]], start: str, end: str
) -> tuple[list[str], int]:
    """BFS shortest path where outgoing links are discovered lazily via `fetch(page)` (may
    raise). A failed fetch is treated as a dead end (no outgoing links), incrementing the
    returned failure count, but the crawl continues elsewhere. Returns (path, failure_count);
    path is [] if `end` is unreachable given the pages that were successfully fetched."""
    if start == end:
        return [start], 0

    visited = {start}
    parent: dict[str, str] = {}
    failures = 0
    q: deque[str] = deque([start])
    found = False

    while q and not found:
        node = q.popleft()
        try:
            neighbors = fetch(node)
        except Exception:
            failures += 1
            continue
        for nxt in sorted(neighbors):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = node
            if nxt == end:
                found = True
                break
            q.append(nxt)

    if end not in visited:
        return [], failures

    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path, failures


# --------------------------------------------------------------------------- line-driven wrappers
def _read_graph(lines: list[str], idx: int) -> tuple[dict[str, list[str]], int]:
    e = int(lines[idx])
    idx += 1
    graph: dict[str, list[str]] = {}
    for _ in range(e):
        u, v = lines[idx].split()
        graph.setdefault(u, []).append(v)
        idx += 1
    return graph, idx


def part1(lines: list[str]) -> list[str]:
    """e / e "u v" edge lines / "start end"."""
    graph, idx = _read_graph(lines, 0)
    start, end = lines[idx].split()
    return [str(shortest_path_length(graph, start, end))]


def part2(lines: list[str]) -> list[str]:
    """Same input shape as part1 -> one line, comma-joined path (empty line if unreachable)."""
    graph, idx = _read_graph(lines, 0)
    start, end = lines[idx].split()
    path = shortest_path(graph, start, end)
    return [",".join(path)]


def part3(lines: list[str]) -> list[str]:
    """e / e "u v" edge lines (the full graph, used to build a `fetch`) / f / f page names whose
    fetch fails / "start end". Output: comma-joined path (or "-" if unreachable) then failure
    count, as two lines."""
    graph, idx = _read_graph(lines, 0)
    f = int(lines[idx])
    idx += 1
    failing = set(lines[idx : idx + f])
    idx += f
    start, end = lines[idx].split()

    def fetch(page: str) -> list[str]:
        if page in failing:
            raise RuntimeError(f"fetch failed for {page!r}")
        return graph.get(page, [])

    path, failures = crawl_shortest_path(fetch, start, end)
    return [",".join(path) if path else "-", str(failures)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
