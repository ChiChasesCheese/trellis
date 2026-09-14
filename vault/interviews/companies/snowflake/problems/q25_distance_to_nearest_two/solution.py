"""q25 Distance to Nearest Two -- reference solution.

An array of 0/1/2. For every 1 (in left-to-right order) output its distance to the nearest 2,
or -1 if the array has no 2 at all. If the array has no 1s, there is nothing to output.

Part1: classic two-pass scan (left-to-right then right-to-left), same technique as LC 542 "01
Matrix" and pc02's multi-source BFS, specialised to a 1D line so a plain two-pass sweep suffices
-- O(n), O(1) extra space beyond the output.

Part2 (reconstructed): the 2D grid analogue. Cells are 0/1/2, no obstacles (every cell is
freely traversable regardless of its own value); for every cell that is 1, its distance to the
nearest 2 is the Manhattan distance via multi-source BFS seeded from every 2 simultaneously
(exactly LC 542's technique; see also pc02's multi-source-BFS-to-nearest-facility). Output is
row-major, skipping non-1 cells, -1 if the grid has no 2 at all.
"""

from __future__ import annotations

import sys
from collections import deque

INF = float("inf")


def _validate_1d(arr: list[int]) -> None:
    for x in arr:
        if x not in (0, 1, 2):
            raise ValueError(f"array must contain only 0, 1, 2: {x}")


def _validate_2d(grid: list[list[int]]) -> None:
    if not grid or not grid[0]:
        return
    width = len(grid[0])
    for row in grid:
        if len(row) != width:
            raise ValueError("grid rows must all have the same length")
        for x in row:
            if x not in (0, 1, 2):
                raise ValueError(f"grid must contain only 0, 1, 2: {x}")


# --------------------------------------------------------------------------- Part 1
def nearest_two_distances(arr: list[int]) -> list[int]:
    """For each 1 (left to right), its distance to the nearest 2, or -1 if there is no 2 at
    all. Empty result if there are no 1s. O(n)."""
    _validate_1d(arr)
    n = len(arr)
    dist = [INF] * n
    last_two = None
    for i in range(n):
        if arr[i] == 2:
            last_two = i
        elif last_two is not None:
            dist[i] = min(dist[i], i - last_two)
    last_two = None
    for i in range(n - 1, -1, -1):
        if arr[i] == 2:
            last_two = i
        elif last_two is not None:
            dist[i] = min(dist[i], last_two - i)
    return [(-1 if dist[i] == INF else dist[i]) for i in range(n) if arr[i] == 1]


# --------------------------------------------------------------------------- Part 2
def nearest_two_distances_grid(grid: list[list[int]]) -> list[int]:
    """2D analogue: for each cell == 1 (row-major order), Manhattan distance to the nearest 2
    via multi-source BFS. -1 if the grid has no 2 at all. Obstacle-free: every cell is
    traversable. O(rows * cols)."""
    _validate_2d(grid)
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    dist = [[INF] * cols for _ in range(rows)]
    q: deque[tuple[int, int]] = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == INF:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))

    out: list[int] = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                out.append(-1 if dist[r][c] == INF else dist[r][c])
    return out


# --------------------------------------------------------------------------- line-driven wrappers
def _read_1d(lines: list[str]) -> list[int]:
    n = int(lines[0]) if lines else 0
    return list(map(int, lines[1].split())) if n else []


def _read_2d(lines: list[str]) -> list[list[int]]:
    rows, cols = map(int, lines[0].split())
    return [list(map(int, lines[1 + r].split())) for r in range(rows)] if rows and cols else []


def part1(lines: list[str]) -> list[str]:
    """'n' / n values (0/1/2) -> distances for each 1, left to right (blank if no 1s)."""
    arr = _read_1d(lines)
    return [str(x) for x in nearest_two_distances(arr)]


def part2(lines: list[str]) -> list[str]:
    """'rows cols' / rows lines of cols values (0/1/2) -> distances for each 1, row-major."""
    grid = _read_2d(lines)
    return [str(x) for x in nearest_two_distances_grid(grid)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
