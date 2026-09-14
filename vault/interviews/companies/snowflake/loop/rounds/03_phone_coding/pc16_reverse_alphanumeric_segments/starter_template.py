"""pc16 Reverse Alphanumeric Segments -- YOUR implementation. Run the tests against this file
with IMPL=starter.

Reverse each maximal run of alphanumeric characters in place; every other character (spaces,
punctuation, apostrophes, ...) stays where it is. "We're" -> "eW'er" (the apostrophe is a
boundary between the runs "We" and "re").
"""

from __future__ import annotations

import sys


def reverse_alnum_segments(s: str) -> str:
    """Part1: any correct approach."""
    # TODO
    return s


def reverse_alnum_segments_inplace(chars: list) -> None:
    """Part2: mutate `chars` (a list of single-character strings) in place, O(1) extra space
    beyond the input list, Unicode-aware."""
    # TODO
    return None


def part1(lines: list[str]) -> list[str]:
    """one string per line -> its transformed form, one per line."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw or not raw[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(raw[0].split()[1])
    out = {1: part1, 2: part2}[n](raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
