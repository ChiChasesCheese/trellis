"""q21 Currency Conversion — YOUR implementation. Run: python drill.py test q21"""
from __future__ import annotations

import sys

Rates = dict[tuple[str, str], float]


def parse_rates(s: str) -> Rates:
    """'USD:AUD:1.4,CAD:USD:0.8' -> {('USD','AUD'): 1.4, ...}. Last duplicate wins; rate <= 0 -> ValueError."""
    # TODO
    return {}


def fmt_rate(x: float) -> str:
    """At most 6 decimals, trailing zeros/dot stripped: 1.4, 0.714286, 88, 1."""
    # TODO
    return ""


def convert(rates: Rates, src: str, dst: str) -> float | None:
    """Part 1: direct quote only; src == dst -> 1.0; unknown -> None."""
    # TODO
    return None


def convert_with_inverse(rates: Rates, src: str, dst: str) -> float | None:
    """Part 2: direct quote, else 1 / quote(dst, src), else None."""
    # TODO
    return None


def find_path(rates: Rates, src: str, dst: str) -> list[str] | None:
    """Part 3a (BFS): fewest-hop path as a list of currencies, or None."""
    # TODO
    return None


def best_conversion(rates: Rates, src: str, dst: str) -> tuple[float, list[str]] | None:
    """Part 3b (DFS): (max product over simple paths, path) or None."""
    # TODO
    return None


def convert_payouts(rates: Rates, payouts: list[str]) -> list[str]:
    """Part 4: 'amount,from,to' -> '<amount> <from> -> <to> = <x.xx>' (half-up) or '= N/A'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    rates = parse_rates(lines[1]) if len(lines) > 1 else {}
    queries = lines[2:]
    out: list[str] = []
    # TODO: dispatch on part, append one output line per query
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
