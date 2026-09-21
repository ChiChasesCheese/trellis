"""pc06 Water Problems -- YOUR implementation. Run the tests against this file with IMPL=starter.

Three "how much water" problems, same 2-pointer / boundary idea escalated from 1D to 2D.
"""

from __future__ import annotations

import sys


def max_container_area(heights: list[int]) -> int:
    """Part1 (LC 11): max area two vertical lines + the x-axis can hold. O(n) time, O(1) space.
    heights must be list[int] of non-negative values -> ValueError otherwise."""
    # TODO
    return 0


def trap_prefix_suffix(heights: list[int]) -> int:
    """Part2 (LC 42), O(n) time / O(n) space: left_max / right_max arrays."""
    # TODO
    return 0


def trap_two_pointer(heights: list[int]) -> int:
    """Part2 follow-up, O(1) extra space: two pointers + running maxima, no arrays."""
    # TODO
    return 0


def trap_2d(grid: list[list[int]]) -> int:
    """Part3 (LC 407): total water a height map traps. grid must be a non-empty rectangular
    list[list[int]] of non-negative values -> ValueError otherwise. Grid smaller than 3x3 in
    either dimension traps 0."""
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    """each line: space-separated heights -> max container area."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """each line: space-separated heights -> trapped water (two-pointer version)."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """each block: a line with row count R, then R grid rows -> trapped water."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
