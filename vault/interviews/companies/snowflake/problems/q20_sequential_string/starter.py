"""q20 Sequential String -- YOUR implementation. Run the tests against this file with IMPL=starter.

s is a string of digits, readable only left to right. For each query, find the minimum prefix
length of s whose digit MULTISET contains enough of every digit to form a permutation of the
query, or -1 if impossible.
"""

from __future__ import annotations

import sys


def sequential_prefix_lengths_binary(s: str, queries: list[str]) -> list[int]:
    """Part1: per query, binary search over per-digit prefix-count columns. ValueError if s or
    any query contains a non-digit character."""
    # TODO
    return []


def sequential_prefix_lengths_fast(s: str, queries: list[str]) -> list[int]:
    """Part2: same answers, O(n) precompute + O(total query length) using occurrence-position
    lists (direct indexing, no search)."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'s' / 'm' / m queries -> m answers."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> m answers."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
