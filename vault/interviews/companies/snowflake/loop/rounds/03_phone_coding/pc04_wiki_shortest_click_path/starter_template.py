"""pc04 Wiki Shortest Click Path -- YOUR implementation. Run pytest against this file with
IMPL=starter.

See problem.md for the full contract: BFS distance (Part1), reconstruct the lexicographically
smallest shortest path (Part2 -- requires a backward BFS from `end` over the reversed graph, not
just a greedy forward walk), and a lazy crawl via a `fetch` callback that may raise, skipping and
counting failures (Part3).
"""

from __future__ import annotations

import sys
from typing import Callable


def shortest_path_length(graph: dict[str, list[str]], start: str, end: str) -> int:
    """BFS distance from start to end over directed edges `graph[u] -> [v, ...]`. -1 if
    unreachable; 0 if start == end."""
    # TODO
    return -1


def shortest_path(graph: dict[str, list[str]], start: str, end: str) -> list[str]:
    """The lexicographically smallest sequence of page names among ALL shortest start->end
    paths. Empty list if unreachable."""
    # TODO
    return []


def crawl_shortest_path(
    fetch: Callable[[str], list[str]], start: str, end: str
) -> tuple[list[str], int]:
    """BFS shortest path where outgoing links are discovered lazily via `fetch(page)` (may
    raise). A failed fetch is treated as a dead end, incrementing the returned failure count,
    but the crawl continues elsewhere. Returns (path, failure_count)."""
    # TODO
    return [], 0


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
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same input shape as part1 -> one line, comma-joined path (empty line if unreachable)."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """e / e "u v" edge lines (the full graph, used to build a `fetch`) / f / f page names whose
    fetch fails / "start end". Output: comma-joined path (or "-" if unreachable) then failure
    count, as two lines."""
    # TODO
    return []


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
