"""pc05 Subarray sums divisible by K -- reference solution.

All three parts are the same trick: a running prefix sum plus a dict that counts (or
remembers the first index of) each prefix-sum "signature" seen so far.

Part1 (LC 974): two indices (l, r] form a subarray whose sum is divisible by K iff
P[r] % K == P[l] % K (same residue). Count pairs of equal residues with a counter dict --
one pass, O(n) time, O(K) extra space. Python's `%` already returns a value in [0, K) for a
positive K, so negative numbers in `nums` need no special-casing (the interview follow-up is
about languages where `%` can return negative, e.g. C/Java, not about this code).

Part2 (LC 560): same prefix-sum trick, no modulus -- (l, r] sums to exactly K iff
P[r] - P[l] == K, i.e. P[l] == P[r] - K. Count occurrences of each raw prefix sum.

Part3 (reconstructed, LC 325 "Maximal Size Subarray Sum Equals k"): want the *longest*
(l, r] with P[r] - P[l] == K. For a fixed r we want the smallest l with P[l] == P[r] - K,
so the dict must remember only the *first* index each prefix sum occurred at (a later,
larger l would only shorten the subarray). Scanning r left to right and only replacing the
best answer on a strictly longer match also gives the leftmost subarray on ties: two subarrays
of equal length differ in r by exactly as much as they differ in l, so the one with the
smaller r (found first) has the smaller l too.
"""

from __future__ import annotations

import sys


def _check_nums(nums: list[int]) -> None:
    if not isinstance(nums, list) or any(not isinstance(x, int) or isinstance(x, bool) for x in nums):
        raise ValueError(f"nums must be a list[int], got {nums!r}")


def _check_k(k: int, *, positive_only: bool) -> None:
    if not isinstance(k, int) or isinstance(k, bool):
        raise ValueError(f"k must be an int, got {k!r}")
    if positive_only and k < 1:
        raise ValueError(f"k must be >= 1 (it is a modulus), got {k}")


# --------------------------------------------------------------------------- Part 1
def count_subarrays_div_k(nums: list[int], k: int) -> int:
    """Number of (contiguous, non-empty) subarrays whose sum is divisible by k. O(n) time,
    O(min(n, k)) space. k must be a positive int (it is used as a modulus)."""
    _check_nums(nums)
    _check_k(k, positive_only=True)
    seen = {0: 1}  # prefix-sum residue -> count of prefixes with that residue (P[0] = 0)
    prefix = 0
    count = 0
    for x in nums:
        prefix = (prefix + x) % k
        count += seen.get(prefix, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count


# --------------------------------------------------------------------------- Part 2
def count_subarrays_sum_k(nums: list[int], k: int) -> int:
    """Number of (contiguous, non-empty) subarrays whose sum equals exactly k. O(n) time,
    O(n) space. k may be any int (positive, negative or zero)."""
    _check_nums(nums)
    _check_k(k, positive_only=False)
    seen = {0: 1}  # prefix sum -> how many prefixes had this exact sum
    prefix = 0
    count = 0
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count


# --------------------------------------------------------------------------- Part 3
def longest_subarray_sum_k(nums: list[int], k: int) -> tuple[int, int, int]:
    """(length, start, end) of the longest (contiguous, non-empty) subarray whose sum equals
    exactly k, 0-indexed and inclusive on both ends. Ties broken by the leftmost start.
    (0, -1, -1) when no such subarray exists. O(n) time, O(n) space."""
    _check_nums(nums)
    _check_k(k, positive_only=False)
    first_seen = {0: -1}  # prefix sum -> smallest index it was first reached at (P[-1] = 0)
    prefix = 0
    best_len, best_start, best_end = 0, -1, -1
    for r, x in enumerate(nums):
        prefix += x
        l = first_seen.get(prefix - k)
        if l is not None:
            length = r - l
            if length > best_len:  # strict: keeps the earliest (leftmost) match on ties
                best_len, best_start, best_end = length, l + 1, r
        if prefix not in first_seen:
            first_seen[prefix] = r
    return best_len, best_start, best_end


# --------------------------------------------------------------------------- line-driven wrappers
def _parse_pairs(lines: list[str]) -> list[tuple[list[int], int]]:
    """Consume `lines` two at a time: a (possibly blank) nums line, then a k line."""
    queries = []
    for i in range(0, len(lines), 2):
        nums_line = lines[i]
        k_line = lines[i + 1]
        nums = [int(t) for t in nums_line.split()] if nums_line.strip() else []
        queries.append((nums, int(k_line)))
    return queries


def part1(lines: list[str]) -> list[str]:
    return [str(count_subarrays_div_k(nums, k)) for nums, k in _parse_pairs(lines)]


def part2(lines: list[str]) -> list[str]:
    return [str(count_subarrays_sum_k(nums, k)) for nums, k in _parse_pairs(lines)]


def part3(lines: list[str]) -> list[str]:
    out = []
    for nums, k in _parse_pairs(lines):
        length, start, end = longest_subarray_sum_k(nums, k)
        out.append(f"{length} {start} {end}")
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
