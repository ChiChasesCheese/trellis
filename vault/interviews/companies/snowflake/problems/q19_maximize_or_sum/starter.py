"""q19 Maximize OR-Sum -- YOUR implementation. Run the tests against this file with IMPL=starter.

Up to k operations; each doubles one element. Maximise the bitwise OR of the whole array.
"""

from __future__ import annotations

import sys

MOD = 1_000_000_007


def max_or_sum(nums: list[int], k: int) -> int:
    """Part1: exact maximum OR. n up to 1e5, 0 <= nums[i] < 2^31, k up to 15.
    ValueError for an empty list, k < 0, or an element out of range."""
    # TODO
    return 0


def max_or_sum_mod(nums: list[int], k: int) -> int:
    """Part2: same, but k up to 1e9 -> return the maximum OR modulo 1e9+7."""
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    """'n k' / n integers -> [exact maximum OR]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> [maximum OR mod 1e9+7]."""
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
