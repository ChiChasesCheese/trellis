"""q17 Remove Stones to Minimize the Total -- YOUR implementation.
Run the tests against this file with IMPL=starter.
"""

from __future__ import annotations

import sys


def min_total_after_k_removals(piles: list[int], k: int) -> int:
    """Part1: LC1962. Each of k operations halves (floor) the current largest
    pile. Return the total after k operations. ValueError for a non-positive
    pile or negative k."""
    # TODO
    return 0


class StoneStream:
    """Part2: add(pile) inserts a new pile; apply(k) runs k halving-operations
    against everything added so far and returns the current total."""

    def __init__(self) -> None:
        # TODO
        pass

    def add(self, pile: int) -> None:
        # TODO
        pass

    def apply(self, k: int) -> int:
        # TODO
        return 0


def part1(lines: list[str]) -> list[str]:
    """'n k' / n piles -> [total]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """'m' / m lines 'ADD pile' or 'APPLY k' -> one output line per APPLY."""
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
