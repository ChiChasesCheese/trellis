"""q02 Merchant Fraud Score — YOUR implementation. Run: python drill.py test q02"""
from __future__ import annotations

import sys


def parse(lines: list[str]) -> tuple[list[tuple[str, int]], list[tuple[str, int, str, int]], list[tuple[int, int, int, int]]]:
    """Split the MERCHANTS / TRANSACTIONS / RULES sections into typed tuples."""
    # TODO
    return [], [], []


def score(merchants, transactions, rules, upto: int = 3, repeat_mode: str = "cumulative") -> list[str]:
    """merchants: [(id, base)], transactions: [(merchant, amount, customer, hour)],
    rules: [(min_amount, mult, add, penalty)] aligned with transactions.
    Apply passes 1..upto. Return ['id, score', ...] sorted by id."""
    # TODO
    return []


def score_variant_grouped(merchants, transactions) -> list[str]:
    """programhelp NG variant: (m,c) group >= 3 -> add group amount; (m,c,h) group >= 3 -> add again."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """Amount rule only."""
    return score(*parse(lines), upto=1)


def part2(lines: list[str]) -> list[str]:
    """Amount + repeat-customer rules."""
    return score(*parse(lines), upto=2)


def part3(lines: list[str]) -> list[str]:
    """All three passes."""
    return score(*parse(lines), upto=3)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
