"""qA04 LC 1169 Invalid Transactions — YOUR implementation. Run: python drill.py test qA04"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Verdict(NamedTuple):
    index: int
    transaction: str
    reasons: list[str]


def invalid_transactions(transactions: list[str]) -> list[str]:
    """Part 1: amount > 1000 OR same name / different city within 60 min (inclusive). Input order."""
    # TODO
    return []


def invalid_reasons(transactions: list[str]) -> list[Verdict]:
    """Part 2: Verdict per invalid transaction: 'amount>1000' then 'city:<other>' by (time, index)."""
    # TODO
    return []


class TransactionStream:
    """Part 3: online version; add() returns transactions newly flagged by this arrival."""

    def __init__(self, window: int = 60, cap: int = 1000) -> None:
        self.window, self.cap = window, cap
        self.flagged: list[str] = []
        # TODO

    def add(self, transaction: str) -> list[str]:
        # TODO
        return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / transactions
    stdout.write("")


if __name__ == "__main__":
    main()
