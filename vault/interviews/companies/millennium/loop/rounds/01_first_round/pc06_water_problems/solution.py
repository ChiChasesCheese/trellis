"""pc06 Water Problems -- reference solution.

Three "how much water" problems that escalate the same two-pointer / boundary idea from 1D to
2D:

Part1 (LC 11, Container With Most Water): two vertical lines + the x-axis hold
`min(height[l], height[r]) * (r - l)` water. Two pointers starting at both ends; always move
the SHORTER wall inward, because moving the taller one can only keep or shrink the area (the
width shrinks by 1 and the height is capped by the still-shorter wall either way), so it can
never find a better answer -- moving the shorter wall is the only move that can improve.

Part2 (LC 42, Trapping Rain Water): water trapped above bar i is
`max(0, min(max_left[i], max_right[i]) - height[i])`. First an O(n) two-pass / two-array
version (easy to derive under time pressure), then the O(1)-extra-space two-pointer version
interviewers ask as the follow-up: walk `l` and `r` inward tracking running maxima
`left_max`/`right_max`; whichever side has the smaller running max determines the water at
that pointer, because the other side is guaranteed to have a wall at least that tall somewhere
between the pointers.

Part3 (reconstructed, LC 407, Trapping Rain Water II): the 2D generalisation. Water trapped
above a cell is bounded by the lowest "rim" reachable from the grid border without going
downhill in terms of the water level -- computed by growing the water level outward from the
border with a min-heap (always expand from the currently-lowest boundary cell first, so every
cell is finalised at the highest level water could reach it without spilling over the border).
"""

from __future__ import annotations

import heapq
import sys


def _check_heights(heights) -> None:
    if not isinstance(heights, list) or any(
        not isinstance(x, int) or isinstance(x, bool) or x < 0 for x in heights
    ):
        raise ValueError(f"heights must be a list[int] of non-negative values, got {heights!r}")


def _check_grid(grid) -> None:
    if not isinstance(grid, list) or not grid or any(not isinstance(row, list) or not row for row in grid):
        raise ValueError("grid must be a non-empty list of non-empty rows")
    width = len(grid[0])
    for row in grid:
        if len(row) != width:
            raise ValueError("grid rows must all have the same length")
        if any(not isinstance(x, int) or isinstance(x, bool) or x < 0 for x in row):
            raise ValueError("grid heights must be non-negative ints")


# --------------------------------------------------------------------------- Part 1
def max_container_area(heights: list[int]) -> int:
    """LC 11: max water two vertical lines (indices i < j, x-axis as the floor) can hold.
    O(n) time, O(1) extra space."""
    _check_heights(heights)
    if len(heights) < 2:
        return 0
    l, r = 0, len(heights) - 1
    best = 0
    while l < r:
        h = min(heights[l], heights[r])
        best = max(best, h * (r - l))
        if heights[l] <= heights[r]:
            l += 1
        else:
            r -= 1
    return best


# --------------------------------------------------------------------------- Part 2
def trap_prefix_suffix(heights: list[int]) -> int:
    """LC 42, O(n) time / O(n) space: precompute running max from the left and from the right,
    then sum max(0, min(left_max[i], right_max[i]) - heights[i])."""
    _check_heights(heights)
    n = len(heights)
    if n < 3:
        return 0
    left_max = [0] * n
    running = 0
    for i in range(n):
        running = max(running, heights[i])
        left_max[i] = running
    right_max = [0] * n
    running = 0
    for i in range(n - 1, -1, -1):
        running = max(running, heights[i])
        right_max[i] = running
    return sum(min(left_max[i], right_max[i]) - heights[i] for i in range(n))


def trap_two_pointer(heights: list[int]) -> int:
    """LC 42 follow-up, O(1) extra space: two pointers walking inward, tracking running maxima
    on each side. No `left_max` / `right_max` arrays."""
    _check_heights(heights)
    n = len(heights)
    if n < 3:
        return 0
    l, r = 0, n - 1
    left_max = right_max = 0
    water = 0
    while l < r:
        if heights[l] <= heights[r]:
            left_max = max(left_max, heights[l])
            water += left_max - heights[l]
            l += 1
        else:
            right_max = max(right_max, heights[r])
            water += right_max - heights[r]
            r -= 1
    return water


# --------------------------------------------------------------------------- Part 3
def trap_2d(grid: list[list[int]]) -> int:
    """LC 407 (reconstructed): total water an m x n height map can trap. Border cells trap
    nothing (water would spill off the grid). Grow the water level inward from the border with
    a min-heap: the currently-lowest boundary cell determines how high water can rise at its
    unvisited neighbours before it would spill; push each neighbour in at max(its own height,
    the current water level). O(m*n log(m*n)) time."""
    _check_grid(grid)
    m, n = len(grid), len(grid[0])
    if m < 3 or n < 3:
        return 0
    visited = [[False] * n for _ in range(m)]
    heap: list[tuple[int, int, int]] = []
    for i in range(m):
        for j in range(n):
            if i in (0, m - 1) or j in (0, n - 1):
                visited[i][j] = True
                heapq.heappush(heap, (grid[i][j], i, j))
    water = 0
    while heap:
        level, i, j = heapq.heappop(heap)
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj]:
                visited[ni][nj] = True
                water += max(0, level - grid[ni][nj])
                heapq.heappush(heap, (max(level, grid[ni][nj]), ni, nj))
    return water


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """each line: space-separated heights -> max container area."""
    out = []
    for line in lines:
        heights = [int(t) for t in line.split()] if line.strip() else []
        out.append(str(max_container_area(heights)))
    return out


def part2(lines: list[str]) -> list[str]:
    """each line: space-separated heights -> trapped water (two-pointer, O(1) space)."""
    out = []
    for line in lines:
        heights = [int(t) for t in line.split()] if line.strip() else []
        out.append(str(trap_two_pointer(heights)))
    return out


def part3(lines: list[str]) -> list[str]:
    """each block: a line with the row count R, then R rows of space-separated heights ->
    one output line with the trapped water."""
    out = []
    i = 0
    while i < len(lines):
        r = int(lines[i])
        grid = [[int(t) for t in lines[i + 1 + k].split()] for k in range(r)]
        i += 1 + r
        out.append(str(trap_2d(grid)))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
