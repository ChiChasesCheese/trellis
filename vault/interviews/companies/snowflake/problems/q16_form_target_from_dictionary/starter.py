"""q16 Number of Ways to Form a Target String Given a Dictionary -- YOUR implementation.
Run the tests against this file with IMPL=starter.
"""

from __future__ import annotations

import sys

MOD = 1_000_000_007


def num_ways_to_form_target(words: list[str], target: str) -> int:
    """Part1: LC1639. words all the same length (>= len(target)), lowercase.
    Count ways to form target by picking strictly-increasing columns, each column
    used at most once overall, mod 1e9+7. ValueError for malformed input (empty
    words/target, mismatched lengths, non-lowercase, target longer than words)."""
    # TODO
    return 0


def smallest_column_assignment(words: list[str], target: str) -> list[int]:
    """Part2: the lexicographically smallest strictly-increasing column sequence
    that can form target (ignoring which word supplies each character); [] if
    impossible."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'n' / n words / target -> [count mod 1e9+7]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> [one line: comma-separated column indices, empty if impossible]."""
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
