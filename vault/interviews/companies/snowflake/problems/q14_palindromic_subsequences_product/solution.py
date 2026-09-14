"""q14 Maximum Product of the Length of Two Palindromic Subsequences -- reference solution.

Part 1 is LC 2002 verbatim: given a string `s` (2 <= len(s) <= 12, lowercase English
letters), pick two DISJOINT subsequences (their index sets don't overlap) that are
each palindromes, and maximize the product of their lengths.

n is tiny (<= 12) specifically so that a bitmask-over-subsets solution is intended:
for every subset (mask) of indices, check in O(n) whether the characters at those
indices (in order) form a palindrome, and record its length. Then for every
palindromic mask, enumerate every sub-mask of its complement (the classic "iterate
submasks of a mask" trick, O(3^n) total) and take the best product where the
sub-mask is also a palindrome. n=12 -> 3^12 ~= 5.3e5, trivially fast.

Part 2 (reconstructed): instead of just the number, return one optimal pair of
disjoint index lists (any pair achieving the max product is accepted -- the test
suite validates a *checker*, not one canonical answer).
"""
from __future__ import annotations

import sys


def _validate(s: str) -> None:
    if not isinstance(s, str):
        raise ValueError(f"s must be a str: {s!r}")
    if not 2 <= len(s) <= 12:
        raise ValueError(f"len(s) must be in [2, 12]: {len(s)}")
    if not all("a" <= c <= "z" for c in s):
        raise ValueError(f"s must be lowercase a-z only: {s!r}")


def _mask_chars(s: str, mask: int) -> str:
    return "".join(c for i, c in enumerate(s) if mask & (1 << i))


def _precompute(s: str) -> tuple[list[bool], list[int]]:
    n = len(s)
    is_pal = [False] * (1 << n)
    pal_len = [0] * (1 << n)
    is_pal[0] = True  # empty string is a (trivial) palindrome, length 0
    for mask in range(1, 1 << n):
        chars = _mask_chars(s, mask)
        if chars == chars[::-1]:
            is_pal[mask] = True
            pal_len[mask] = len(chars)
    return is_pal, pal_len


def _best_pair(s: str) -> tuple[int, int, int]:
    """Returns (best_product, mask1, mask2) for one optimal disjoint palindromic pair."""
    n = len(s)
    full = (1 << n) - 1
    is_pal, pal_len = _precompute(s)
    best = (0, 0, 0)
    for mask1 in range(1, 1 << n):
        if not is_pal[mask1]:
            continue
        comp = full & ~mask1
        sub = comp
        while True:
            if is_pal[sub]:
                product = pal_len[mask1] * pal_len[sub]
                if product > best[0]:
                    best = (product, mask1, sub)
            if sub == 0:
                break
            sub = (sub - 1) & comp
    return best


# --------------------------------------------------------------------------- Part 1
def max_product_two_palindromic_subsequences(s: str) -> int:
    """LC2002: max product of lengths of two disjoint palindromic subsequences."""
    _validate(s)
    return _best_pair(s)[0]


# --------------------------------------------------------------------------- Part 2
def max_product_with_subsequences(s: str) -> tuple[list[int], list[int]]:
    """One optimal disjoint pair, as ascending index lists into s. Any pair achieving
    the Part1 maximum is a valid answer."""
    _validate(s)
    _, mask1, mask2 = _best_pair(s)
    n = len(s)
    idx1 = [i for i in range(n) if mask1 & (1 << i)]
    idx2 = [i for i in range(n) if mask2 & (1 << i)]
    return idx1, idx2


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """one line: s -> [max product]."""
    s = lines[0].strip()
    return [str(max_product_two_palindromic_subsequences(s))]


def part2(lines: list[str]) -> list[str]:
    """one line: s -> [two lines: comma-separated indices for each subsequence]."""
    s = lines[0].strip()
    idx1, idx2 = max_product_with_subsequences(s)
    return [",".join(map(str, idx1)), ",".join(map(str, idx2))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
