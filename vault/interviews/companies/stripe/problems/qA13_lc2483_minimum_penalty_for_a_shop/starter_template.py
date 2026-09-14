"""qA13 LC 2483 Minimum Penalty for a Shop — YOUR implementation. Run: python drill.py test qA13"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Window(NamedTuple):
    open: int      # first open hour
    close: int     # first closed hour (half-open window [open, close))
    penalty: int


def penalty(customers: str, closing_hour: int) -> int:
    """'N' before closing_hour + 'Y' at or after it."""
    # TODO
    return 0


def best_closing_time(customers: str) -> int:
    """Part 1 (LC signature): earliest closing hour with the minimum penalty; O(n)."""
    # TODO
    return 0


def best_open_close(customers: str) -> Window:
    """Part 2: best half-open window [open, close); ties -> smallest open, then smallest close."""
    # TODO
    return Window(0, 0, 0)


def min_penalty_k_windows(customers: str, k: int) -> int:
    """Part 3: minimum penalty with at most k disjoint open windows; O(n*k)."""
    # TODO
    return 0


def best_closing_time_weighted(customers: str, weights: list[int]) -> int:
    """Part 4: earliest closing hour minimising the weighted penalty."""
    # TODO
    return 0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / customers / [K k] / [weights]
    stdout.write("")


if __name__ == "__main__":
    main()
