"""pc15 Parentheses Matching -- YOUR implementation. Run the tests against this file with IMPL=starter.

See problem.md: Part1 uses three bracket types ()[]{}; Part2/Part3 follow their own original LC
problems (921, 32) and only accept '(' and ')'.
"""

from __future__ import annotations

import sys


def is_valid(s: str) -> bool:
    """Part1 (LC 20): stack match across ()[]{}. Raise ValueError for any other character."""
    # TODO
    return False


def min_add_to_make_valid(s: str) -> tuple[int, str]:
    """Part2 (LC 921): (min insertions, one resulting valid string). '(' and ')' only."""
    # TODO
    return 0, ""


def longest_valid_substring(s: str) -> tuple[int, int]:
    """Part3 (LC 32): (length, start index) of one longest valid substring, leftmost on a tie.
    '(' and ')' only. (0, 0) if there is none."""
    # TODO
    return 0, 0


def part1(lines: list[str]) -> list[str]:
    """One line: the string -> 'true' or 'false'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """One line: the string -> line1 min insertions, line2 one resulting valid string."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """One line: the string -> 'length start_index'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
