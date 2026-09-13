"""q30 Stripe Capital — YOUR implementation. Run: python drill.py test q30"""
from __future__ import annotations

import sys


def process(lines: list[str], duplicate_create: str = "ignore") -> list[str]:
    """Evaluate every 'METHOD: p1,p2,...' line in order; return ['merchant,total', ...] for merchants with
    total > 0, sorted by merchant id. duplicate_create in {'ignore', 'replace', 'add'}."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """CREATE_LOAN + PAY_LOAN (overpayment capped at 0)."""
    return process(lines)


def part2(lines: list[str]) -> list[str]:
    """+ TRANSACTION_PROCESSED: floor(amount * pct / 100) repaid toward the loan."""
    return process(lines)


def part3(lines: list[str]) -> list[str]:
    """+ INCREASE_LOAN, several loans per merchant (summed), loan-less transaction -> oldest-first."""
    return process(lines)


def part4(lines: list[str]) -> list[str]:
    """+ invalid actions are no-ops (unknown ids, negative amounts, pct outside 1..100, duplicate create)."""
    return process(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = part4(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
