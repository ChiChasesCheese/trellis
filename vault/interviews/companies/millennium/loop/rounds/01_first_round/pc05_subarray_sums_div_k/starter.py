"""pc05 Subarray Sums Divisible by K -- YOUR implementation. Run the tests against this file
with IMPL=starter.

Every part is the same trick: turn "sum of a subarray" into a difference of two prefix sums,
then count / index those prefix sums with a dict.
"""

from __future__ import annotations

import sys


def count_subarrays_div_k(nums: list[int], k: int) -> int:
    """Part1 (LC 974): number of subarrays whose sum is divisible by k. k must be a positive
    int (a modulus); k < 1 or a non-int element of nums -> ValueError."""
    # TODO
    return 0


def count_subarrays_sum_k(nums: list[int], k: int) -> int:
    """Part2 (LC 560): number of subarrays whose sum equals exactly k. k is a target sum, may
    be any int (positive, negative or 0)."""
    # TODO
    return 0


def longest_subarray_sum_k(nums: list[int], k: int) -> tuple[int, int, int]:
    """Part3: (length, start, end) of the longest subarray summing to exactly k, 0-indexed
    inclusive; ties broken by the leftmost start. (0, -1, -1) if none exists."""
    # TODO
    return 0, -1, -1


def part1(lines: list[str]) -> list[str]:
    """lines come two at a time: a (possibly blank) nums line, then a k line."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """output line is 'length start end'."""
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
