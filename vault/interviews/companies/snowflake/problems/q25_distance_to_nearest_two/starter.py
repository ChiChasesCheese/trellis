"""q25 Distance to Nearest Two -- YOUR implementation. Run tests against this file with
IMPL=starter.

Array of 0/1/2: for each 1 (left to right), output its distance to the nearest 2, or -1 if
there is no 2 at all.
"""

from __future__ import annotations

import sys


def nearest_two_distances(arr: list[int]) -> list[int]:
    """Part1: two-pass O(n) scan."""
    # TODO
    return []


def nearest_two_distances_grid(grid: list[list[int]]) -> list[int]:
    """Part2 (reconstructed): 2D grid, Manhattan distance via multi-source BFS."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'n' / n values (0/1/2) -> distances for each 1, left to right."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """'rows cols' / rows lines of cols values -> distances for each 1, row-major."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
