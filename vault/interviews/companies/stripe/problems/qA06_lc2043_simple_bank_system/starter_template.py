"""qA06 LC 2043 Simple Bank System — YOUR implementation. Run: python drill.py test qA06"""
from __future__ import annotations

import sys
from typing import NamedTuple


class TxnRecord(NamedTuple):
    id: int
    kind: str            # deposit | withdraw | transfer | reverse
    src: int | None
    dst: int | None
    amount: int
    ok: bool
    ref: int | None = None   # reversed txn id for kind == "reverse"


class Bank:
    def __init__(self, balance: list[int], reserve: int = 0) -> None:
        self.log: list[TxnRecord] = []
        self.reversed_ids: set[int] = set()
        self.reserve = reserve
        self.max_outstanding = 0
        # TODO

    def balances(self) -> list[int]:
        return []  # TODO

    def debts(self) -> list[int]:
        return []  # TODO

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        return False  # TODO

    def deposit(self, account: int, money: int) -> bool:
        return False  # TODO

    def withdraw(self, account: int, money: int) -> bool:
        return False  # TODO

    def reverse(self, txn_id: int) -> bool:
        return False  # TODO


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / balances / [RESERVE r] / commands
    stdout.write("")


if __name__ == "__main__":
    main()
