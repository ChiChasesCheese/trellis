"""pc18 Number Transformation Path -- YOUR implementation. Run the tests against this file with
IMPL=starter.

From a positive integer n you may move to n+2 (add), n-2 (sub, only while the result stays >=1),
or n//2 (split, only when n is even -- an odd n can never be split). transform(a, b) returns any
sequence of positive integers from a to b inclusive using these moves (not necessarily
shortest), or None if b is unreachable from a.
"""

from __future__ import annotations

import sys


def transform(a: int, b: int) -> list[int] | None:
    """Part1: any valid path (not necessarily shortest). ValueError if a or b < 1."""
    # TODO
    return None


def shortest_transform(a: int, b: int) -> list[int] | None:
    """Part2: a SHORTEST valid path (BFS). ValueError if a or b < 1."""
    # TODO
    return None


def part1(lines: list[str]) -> list[str]:
    """each line: 'a b' -> the path (space-separated) or 'IMPOSSIBLE'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
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
