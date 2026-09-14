"""pc02 Closest Facility Grid -- reference solution.

Multi-source BFS from every bathroom ('B') at once. `_bfs_with_source` processes the frontier
one whole BFS layer at a time (not as a single mixed FIFO queue) specifically so that ties -- two
different bathrooms reaching the same cell at the same distance -- can be resolved deterministically
by comparing the *source* bathroom's (row, col), smallest wins. A plain single-queue multi-source
BFS would make the tie winner depend on push order, which is not the contract Part 2/3 need.
"""

from __future__ import annotations

import sys

Cell = tuple[int, int]

_DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _bfs_with_source(
    grid: list[str], blocked_char: str | None = None
) -> tuple[list[list[int]], list[list[Cell | None]]]:
    m = len(grid)
    n = len(grid[0]) if m else 0
    dist = [[-1] * n for _ in range(m)]
    source: list[list[Cell | None]] = [[None] * n for _ in range(m)]

    bathrooms = sorted(
        (r, c) for r in range(m) for c in range(n) if grid[r][c] == "B"
    )
    frontier: list[Cell] = []
    for r, c in bathrooms:
        dist[r][c] = 0
        source[r][c] = (r, c)
        frontier.append((r, c))

    d = 0
    while frontier:
        claims: dict[Cell, Cell] = {}
        for r, c in frontier:
            for dr, dc in _DIRS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < m and 0 <= nc < n):
                    continue
                if dist[nr][nc] != -1:
                    continue
                if blocked_char is not None and grid[nr][nc] == blocked_char:
                    continue
                cand = source[r][c]
                assert cand is not None
                prev = claims.get((nr, nc))
                if prev is None or cand < prev:
                    claims[(nr, nc)] = cand
        if not claims:
            break
        d += 1
        next_frontier: list[Cell] = []
        for (nr, nc), src in claims.items():
            dist[nr][nc] = d
            source[nr][nc] = src
            next_frontier.append((nr, nc))
        frontier = next_frontier
    return dist, source


def _desks(grid: list[str]) -> list[Cell]:
    return [
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[0]) if grid else 0)
        if grid[r][c] == "D"
    ]


# --------------------------------------------------------------------------- Part 1
def nearest_bathroom_distances(grid: list[str]) -> list[int]:
    """Shortest 4-directional distance from every desk to the nearest bathroom, in row-major
    desk order. No bathroom anywhere in the grid -> -1 for every desk."""
    dist, _ = _bfs_with_source(grid)
    return [dist[r][c] for r, c in _desks(grid)]


# --------------------------------------------------------------------------- Part 2
def nearest_bathroom_with_location(grid: list[str]) -> list[tuple[int, Cell]]:
    """Same distances as Part 1, plus which bathroom achieves it. Ties (multiple bathrooms at
    the same shortest distance) break by smallest row, then smallest column. Unreachable/no
    bathroom -> (-1, (-1, -1))."""
    dist, source = _bfs_with_source(grid)
    out: list[tuple[int, Cell]] = []
    for r, c in _desks(grid):
        d = dist[r][c]
        if d == -1:
            out.append((-1, (-1, -1)))
        else:
            src = source[r][c]
            assert src is not None
            out.append((d, src))
    return out


# --------------------------------------------------------------------------- Part 3
def nearest_bathroom_with_obstacles(grid: list[str]) -> list[tuple[int, Cell]]:
    """Same contract as Part 2, but '#' cells are impassable walls that block the BFS. A desk
    walled off from every bathroom gets (-1, (-1, -1)), same as "no bathroom reachable"."""
    dist, source = _bfs_with_source(grid, blocked_char="#")
    out: list[tuple[int, Cell]] = []
    for r, c in _desks(grid):
        d = dist[r][c]
        if d == -1:
            out.append((-1, (-1, -1)))
        else:
            src = source[r][c]
            assert src is not None
            out.append((d, src))
    return out


# --------------------------------------------------------------------------- line-driven wrappers
def _read_grid(lines: list[str]) -> list[str]:
    r, c = (int(x) for x in lines[0].split())
    return list(lines[1 : 1 + r])


def part1(lines: list[str]) -> list[str]:
    """'<rows> <cols>' then <rows> grid lines -> one distance per desk (row-major)."""
    grid = _read_grid(lines)
    return [str(d) for d in nearest_bathroom_distances(grid)]


def part2(lines: list[str]) -> list[str]:
    """Same input; one '<dist>,<row>,<col>' per desk (row-major)."""
    grid = _read_grid(lines)
    out = []
    for d, (br, bc) in nearest_bathroom_with_location(grid):
        out.append(f"{d},{br},{bc}")
    return out


def part3(lines: list[str]) -> list[str]:
    """Same input shape as part2; grid may contain '#' walls."""
    grid = _read_grid(lines)
    out = []
    for d, (br, bc) in nearest_bathroom_with_obstacles(grid):
        out.append(f"{d},{br},{bc}")
    return out


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
