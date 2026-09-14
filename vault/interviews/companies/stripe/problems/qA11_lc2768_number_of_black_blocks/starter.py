"""qA11 LC 2768 Number of Black Blocks — YOUR implementation. Run: python drill.py test qA11"""
from __future__ import annotations

import sys


def count_black_blocks(m: int, n: int, coordinates: list[list[int]]) -> list[int]:
    """Part 1 (LC signature): five counts, result[i] = number of 2x2 blocks with exactly i black cells."""
    # TODO
    return [0, 0, 0, 0, 0]


def count_black_blocks_k(m: int, n: int, coordinates: list[list[int]], k: int) -> list[int]:
    """Part 2: k*k+1 counts for k x k blocks (k == 2 is Part 1)."""
    # TODO
    return [0] * (k * k + 1)


class BlockCounter:
    """Part 3: streaming paints with an always-ready histogram of 2x2 block counts."""

    def __init__(self, m: int, n: int) -> None:
        self.m, self.n = m, n
        # TODO

    def paint(self, x: int, y: int, black: bool) -> None:
        """Set the cell colour (idempotent); O(1)."""
        # TODO

    def counts(self) -> list[int]:
        """Five counts as in Part 1; O(1)."""
        # TODO
        return [0, 0, 0, 0, 0]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / m n / [K k] / x,y lines  or  B x,y | W x,y | Q events
    stdout.write("")


if __name__ == "__main__":
    main()
