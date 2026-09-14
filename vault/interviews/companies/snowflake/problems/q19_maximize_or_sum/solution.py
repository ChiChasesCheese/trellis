"""q19 Maximize OR-Sum -- reference solution.

You may apply up to k operations; each doubles one element (x -> 2x, i.e. x << 1). Maximise the
bitwise OR of the whole array.

Key fact: putting all k doublings on ONE element is optimal. Shifting one element by k moves its
highest bit to position msb+k, higher than anything a split could reach, and OR only cares about
which bits exist. So the answer is max over i of (nums[i] << k) | (OR of all others). "Double the
largest element" is NOT correct: [12, 9], k=1 -> 24|9 = 25 but 12|18 = 30.

Part1: prefix/suffix OR, O(n), exact Python int.
Part2 (reconstructed): k up to 1e9, so the exact answer has ~1e9 bits. Report it modulo 1e9+7.
When k is small (k <= 64) compute exactly and reduce. When k is large the shifted element's bits
sit entirely above every unshifted element (all < 2^31 <= 2^k), so candidate i is
nums[i] * 2^k + others_i with no overlap: the best candidate has the largest nums[i], ties broken
by the largest OR of the others -- compare those, then compute the result modulo with pow(2, k, M).
"""

from __future__ import annotations

import sys

MOD = 1_000_000_007
_EXACT_K = 64  # beyond this every shifted value clears 2^31, so no bit overlap is possible


def _validate(nums: list[int], k: int) -> None:
    if not nums:
        raise ValueError("nums must be non-empty")
    if k < 0:
        raise ValueError("k must be >= 0")
    for x in nums:
        if not 0 <= x < 2 ** 31:
            raise ValueError(f"element out of range: {x}")


def _others_or(nums: list[int]) -> list[int]:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] | x
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] | nums[i]
    return [prefix[i] | suffix[i + 1] for i in range(n)]


# --------------------------------------------------------------------------- Part 1
def max_or_sum(nums: list[int], k: int) -> int:
    """Exact maximum OR. O(n)."""
    _validate(nums, k)
    others = _others_or(nums)
    return max((x << k) | o for x, o in zip(nums, others))


# --------------------------------------------------------------------------- Part 2
def max_or_sum_mod(nums: list[int], k: int) -> int:
    """Maximum OR modulo 1e9+7, for k up to 1e9."""
    _validate(nums, k)
    if k <= _EXACT_K:
        return max_or_sum(nums, k) % MOD
    others = _others_or(nums)
    best_i = max(range(len(nums)), key=lambda i: (nums[i], others[i]))
    return (nums[best_i] * pow(2, k, MOD) + others[best_i]) % MOD


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[list[int], int]:
    n, k = map(int, lines[0].split())
    nums = list(map(int, lines[1].split())) if n else []
    if len(nums) != n:
        raise ValueError(f"expected {n} numbers, got {len(nums)}")
    return nums, k


def part1(lines: list[str]) -> list[str]:
    """'n k' / n integers -> [exact maximum OR]."""
    nums, k = _read(lines)
    return [str(max_or_sum(nums, k))]


def part2(lines: list[str]) -> list[str]:
    """same input -> [maximum OR mod 1e9+7]."""
    nums, k = _read(lines)
    return [str(max_or_sum_mod(nums, k))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
