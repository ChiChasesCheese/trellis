"""qA02 LC 787 Cheapest Flights Within K Stops — YOUR implementation. Run: python drill.py test qA02"""
from __future__ import annotations

import sys


def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    """Part 1: Bellman-Ford, k+1 rounds over a COPY of last round's distances. -1 if unreachable."""
    # TODO
    return -1


def find_cheapest_price_bfs(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    """Part 2: frontier expansion by hops with global best-cost pruning. Must equal Part 1."""
    # TODO
    return -1


def cheapest_path(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> list[int] | None:
    """Part 3: cities of a cheapest itinerary; ties -> fewer flights, then lexicographic. None if none."""
    # TODO
    return None


def cheapest_with_carrier(routes: list[str], src: str, dst: str, k: int, carrier: str = "*") -> int:
    """Part 4: routes 'FROM:TO:CARRIER:price'; only `carrier`'s routes unless '*'. -1 if unreachable."""
    # TODO
    return -1


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / header / edges
    stdout.write("")


if __name__ == "__main__":
    main()
