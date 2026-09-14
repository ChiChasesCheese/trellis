"""q06 Patching Array — reference solution.

This is LeetCode 484 "Patching Array", asked as-is at Snowflake:

    Given a sorted integer array `nums` and an integer `n`, add/patch elements
    to the array such that any number in the range [1, n] inclusive can be
    formed by the sum of some elements in the array. Return the minimum
    number of patches required.

Standard greedy: `miss` is the smallest positive integer NOT yet guaranteed
formable from the elements consumed so far. Walk `nums` in order; whenever the
next available element is <= miss, it extends the formable prefix to
[1, miss + nums[i] - 1], so consume it (miss += nums[i]). Otherwise no real
element can extend the range, so we patch with the value `miss` itself (the
smallest gap), which extends the range to [1, 2*miss - 1] -- hence `miss *= 2`
and a patch is counted. Stop once miss > n (the whole [1, n] range is covered).

part1 returns just the count (the original LC 484 signature). part2 is a
natural follow-up: instead of the count, return the actual patch VALUES in
the order they were added -- each time part1 would do `patches += 1`, part2
appends the pre-doubling `miss` value. The two are kept consistent by sharing
the exact same greedy loop.
"""
from __future__ import annotations

import sys


def part1(nums: list[int], n: int) -> int:
    """Minimum number of patches so every integer in [1, n] is representable
    as a subset sum of the (patched) array."""
    miss = 1
    i = 0
    patches = 0
    length = len(nums)
    while miss <= n:
        if i < length and nums[i] <= miss:
            miss += nums[i]
            i += 1
        else:
            miss *= 2
            patches += 1
    return patches


def part2(nums: list[int], n: int) -> list[int]:
    """Same greedy as part1, but returns the actual patch values added, in
    the order they were added. len(part2(nums, n)) == part1(nums, n) always."""
    miss = 1
    i = 0
    length = len(nums)
    result: list[int] = []
    while miss <= n:
        if i < length and nums[i] <= miss:
            miss += nums[i]
            i += 1
        else:
            result.append(miss)
            miss *= 2
    return result


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
