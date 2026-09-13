"""q10 Wiki Minimum Clicks — reference solution.

Wikipedia pages are nodes in a DIRECTED graph: an edge A -> B means page A has a
hyperlink to page B (one-directional; B may or may not link back). Given the
edge list, a start page and a target page, find the minimum number of clicks
(edges traversed) from start to target. Return -1 if unreachable; 0 if
start == target.

part1 is plain BFS shortest-path distance. part2 (**reconstructed** follow-up,
no verbatim follow-up was recovered) is BFS with parent-pointer tracking that
also returns the actual path. Both process each node's own neighbor list in
ALPHABETICALLY SORTED order for determinism (part1's numeric output doesn't
actually depend on this, but it is kept for consistency with part2 and so a
future extension that needs a specific path is trivial to add).
"""
from __future__ import annotations

import sys
from collections import defaultdict, deque


def _build_adjacency(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    """directed adjacency map; each node's neighbor list sorted alphabetically."""
    adj: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    for node in adj:
        adj[node].sort()
    return adj


def part1(edges: list[tuple[str, str]], start: str, target: str) -> int:
    """Minimum number of edges from start to target. -1 if unreachable."""
    if start == target:
        return 0
    adj = _build_adjacency(edges)
    visited = {start}
    queue: deque[tuple[str, int]] = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        for nxt in adj.get(node, []):
            if nxt not in visited:
                if nxt == target:
                    return dist + 1
                visited.add(nxt)
                queue.append((nxt, dist + 1))
    return -1


def part2(edges: list[tuple[str, str]], start: str, target: str) -> list[str]:
    """**(reconstructed)** Same BFS, but tracks parent pointers and returns the
    actual shortest path (start..target inclusive). [] if unreachable, [start]
    if start == target. Deterministic: FIFO queue, each node's own neighbors
    visited in alphabetically sorted order, first-discovery parent wins."""
    if start == target:
        return [start]
    adj = _build_adjacency(edges)
    visited = {start}
    parent: dict[str, str] = {}
    queue: deque[str] = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in adj.get(node, []):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = node
            if nxt == target:
                queue.clear()
                break
            queue.append(nxt)

    if target not in visited:
        return []

    path = [target]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format:
    PART n
    E
    from,to        (repeated E times)
    start,target

    PART 1 prints the integer distance on one line.
    PART 2 prints the path as comma-separated page names on one line (blank
    line if unreachable).
    """
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip() != ""]
    idx = 0
    header = lines[idx].split()
    idx += 1
    part = int(header[1]) if header and header[0].upper() == "PART" else 1
    num_edges = int(lines[idx])
    idx += 1
    edges: list[tuple[str, str]] = []
    for _ in range(num_edges):
        a, b = (p.strip() for p in lines[idx].split(","))
        idx += 1
        edges.append((a, b))
    start, target = (p.strip() for p in lines[idx].split(","))
    idx += 1

    if part == 1:
        stdout.write(f"{part1(edges, start, target)}\n")
    else:
        stdout.write(",".join(part2(edges, start, target)) + "\n")


if __name__ == "__main__":
    main()
