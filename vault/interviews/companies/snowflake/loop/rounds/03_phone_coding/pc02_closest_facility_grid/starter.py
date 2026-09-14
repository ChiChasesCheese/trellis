"""pc02 Closest Facility Grid -- YOUR implementation. Run pytest against this file with
IMPL=starter.

See problem.md for the full contract: multi-source BFS from every bathroom ('B') to every desk
('D'), 4-directional moves, distances only (Part1); also report which bathroom won with a
smallest-row-then-col tie-break (Part2); '#' walls block movement (Part3).
"""

from __future__ import annotations

import sys

Cell = tuple[int, int]


def nearest_bathroom_distances(grid: list[str]) -> list[int]:
    """Shortest 4-directional distance from every desk to the nearest bathroom, in row-major
    desk order. No bathroom anywhere in the grid -> -1 for every desk."""
    # TODO
    return []


def nearest_bathroom_with_location(grid: list[str]) -> list[tuple[int, Cell]]:
    """Same distances as Part 1, plus which bathroom achieves it. Ties break by smallest row,
    then smallest column. Unreachable/no bathroom -> (-1, (-1, -1))."""
    # TODO
    return []


def nearest_bathroom_with_obstacles(grid: list[str]) -> list[tuple[int, Cell]]:
    """Same contract as Part 2, but '#' cells are impassable walls."""
    # TODO
    return []


def _read_grid(lines: list[str]) -> list[str]:
    r, c = (int(x) for x in lines[0].split())
    return list(lines[1 : 1 + r])


def part1(lines: list[str]) -> list[str]:
    """'<rows> <cols>' then <rows> grid lines -> one distance per desk (row-major)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same input; one '<dist>,<row>,<col>' per desk (row-major)."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Same input shape as part2; grid may contain '#' walls."""
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
