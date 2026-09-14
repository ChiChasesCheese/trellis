"""pc06 Happy Number -- YOUR implementation. Run the tests against this file with IMPL=starter.

f(n) = sum of the squares of n's digits. n is happy if iterating f reaches 1.
"""

from __future__ import annotations

import sys


def is_happy_set(n: int) -> bool:
    """Part1: any correct approach (a set of seen values is fine). ValueError for n < 1."""
    # TODO
    return False


def is_happy_floyd(n: int) -> bool:
    """Part2: O(1) extra space -- no set, no dict, no list that grows. ValueError for n < 1."""
    # TODO
    return False


def cycle_info(n: int, base: int = 10, power: int = 2) -> tuple[int, int]:
    """Part3: f(n) = sum of digit**power in `base`. Return (cycle length, smallest value in the
    cycle) that the sequence from n falls into. ValueError for n < 1, base < 2, power < 1."""
    # TODO
    return 0, 0


def part1(lines: list[str]) -> list[str]:
    """one positive integer per line -> 'true' / 'false' per line."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """'n base power' per line -> 'length smallest' per line."""
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
