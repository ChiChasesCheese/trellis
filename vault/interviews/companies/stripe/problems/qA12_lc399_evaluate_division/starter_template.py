"""qA12 LC 399 Evaluate Division — YOUR implementation. Run: python drill.py test qA12"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Conflict(NamedTuple):
    index: int      # position in equations
    a: str
    b: str
    given: float    # values[index]
    implied: float  # ratio implied by the earlier (accepted) equations


def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    """Part 1 (LC signature): BFS with inverse edges; -1.0 when underivable."""
    # TODO
    return [-1.0] * len(queries)


def calc_equation_union_find(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    """Part 2: weighted union-find with path compression; same answers as Part 1."""
    # TODO
    return [-1.0] * len(queries)


def best_rate_path(equations: list[list[str]], values: list[float], src: str, dst: str) -> tuple[float, list[str]] | None:
    """Part 3: max product over simple paths (inverse edges included); ties fewer hops, then lexicographic."""
    # TODO
    return None


def find_conflicts(equations: list[list[str]], values: list[float], rel_tol: float = 1e-9) -> list[Conflict]:
    """Part 4: equations that contradict the accepted ones before them (relative tolerance); not applied."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / A/B=v lines / ? / queries (C/D | SRC DST | nothing)
    stdout.write("")


if __name__ == "__main__":
    main()
