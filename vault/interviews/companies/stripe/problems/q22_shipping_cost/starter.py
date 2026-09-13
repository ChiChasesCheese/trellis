"""q22 Shipping Cost — YOUR implementation. Run: python drill.py test q22

Parts 1-3: carrier routes  "US:UK:FedEx:5,UK:US:UPS:4,..."  (directed legs)
Parts 4-5: country x product price matrix with quantity tiers (cents).
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Route(NamedTuple):
    src: str
    dst: str
    carrier: str
    cost: int


def parse_routes(s: str) -> list[Route]:
    """'US:UK:FedEx:5,UK:US:UPS:4' -> [Route('US','UK','FedEx',5), ...]"""
    # TODO
    return []


def shipping_cost(routes: list[Route], src: str, dst: str, method: str) -> int:
    """Part 1: cost of the direct leg src->dst by `method`, or -1."""
    # TODO
    return -1


def shipping_cost_one_transfer(routes: list[Route], src: str, dst: str) -> tuple[int, list[str]]:
    """Part 2: (cost, [src, carrier, X, carrier, dst]); direct leg preferred; (-1, []) if none."""
    # TODO
    return -1, []


def cheapest_shipping(routes: list[Route], src: str, dst: str) -> tuple[int, list[str]]:
    """Part 3: cheapest path over any number of legs (Dijkstra). (-1, []) if unreachable."""
    # TODO
    return -1, []


def calculate_shipping_cost(order: dict, matrix: dict, mode: str = "volume") -> int:
    """Parts 4-5: total shipping in cents for `order` priced by `matrix`.
    mode='volume' (whole quantity at its band's unit cost) or 'graduated' (each band separately).
    Raise ValueError for unknown country/product or negative quantity."""
    # TODO
    return 0


def format_path(cost: int, path: list[str]) -> str:
    """(7, ['US','FedEx','UK','DHL','FR']) -> '7 US-FedEx->UK-DHL->FR' ; (-1, []) -> '-1'."""
    # TODO
    return "-1"


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out: list[str] = []
    # TODO: dispatch on part (see problem.md for the stdin encoding)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
