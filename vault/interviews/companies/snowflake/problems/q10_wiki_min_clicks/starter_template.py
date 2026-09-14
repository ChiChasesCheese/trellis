"""q10 Wiki Minimum Clicks — YOUR implementation. Run: python drill.py test q10"""
from __future__ import annotations

import sys


def part1(edges: list[tuple[str, str]], start: str, target: str) -> int:
    """Minimum number of edges from start to target. -1 if unreachable."""
    # TODO
    return -1


def part2(edges: list[tuple[str, str]], start: str, target: str) -> list[str]:
    """(reconstructed) Same BFS, but returns the actual shortest path
    (start..target inclusive). [] if unreachable, [start] if start == target."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
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
