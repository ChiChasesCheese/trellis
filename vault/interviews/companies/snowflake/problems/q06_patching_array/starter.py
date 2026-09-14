"""q06 Patching Array — YOUR implementation. Run: python drill.py test q06"""
from __future__ import annotations

import sys


def part1(nums: list[int], n: int) -> int:
    """Minimum number of patches so every integer in [1, n] is representable
    as a subset sum of the (patched) array."""
    # TODO
    return 0


def part2(nums: list[int], n: int) -> list[int]:
    """Same greedy as part1, but returns the actual patch values added, in
    the order they were added. len(part2(nums, n)) == part1(nums, n) always."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines:
        stdout.write("\n")
        return
    header = lines[0].split()
    part = int(header[1])
    n = int(lines[1]) if len(lines) > 1 else 0
    nums_line = lines[2] if len(lines) > 2 else ""
    nums = [int(x) for x in nums_line.split()]
    if part == 1:
        stdout.write(f"{part1(nums, n)}\n")
    else:
        stdout.write(" ".join(str(x) for x in part2(nums, n)) + "\n")


if __name__ == "__main__":
    main()
