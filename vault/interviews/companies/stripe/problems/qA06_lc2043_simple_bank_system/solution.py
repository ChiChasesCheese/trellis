"""qA06 LC 2043 Simple Bank System — reference solution.

All mutation goes through two primitives: `_debit(acct, money, allow_loan)` and `_credit(acct,
money)`. Validation happens before any mutation, so a rejected call never leaves a partial effect.
Part 3's platform lending lives in `_debit`, automatic repayment in `_credit`; with reserve=0 the
class is exactly LC 2043.
"""
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
        self._bal = list(balance)           # index 0 = account 1
        self._debt = [0] * len(balance)
        self._outstanding = 0                # sum(self._debt), kept incrementally
        self.reserve = reserve
        self.max_outstanding = 0
        self.log: list[TxnRecord] = []
        self.reversed_ids: set[int] = set()

    # ------------------------------------------------------------ helpers
    def _valid(self, account: int) -> bool:
        return 1 <= account <= len(self._bal)  # accounts are 1-indexed

    def _can_debit(self, account: int, money: int, allow_loan: bool) -> bool:
        shortfall = money - self._bal[account - 1]
        if shortfall <= 0:
            return True  # exactly the balance is fine (== allowed)
        return allow_loan and shortfall <= self.reserve  # platform lends only what it has

    def _debit(self, account: int, money: int) -> None:
        """Caller has checked _can_debit. Lends the shortfall from the reserve when needed."""
        i = account - 1
        shortfall = money - self._bal[i]
        if shortfall > 0:
            self.reserve -= shortfall
            self._debt[i] += shortfall
            self._outstanding += shortfall
            self._bal[i] = 0
            self.max_outstanding = max(self.max_outstanding, self._outstanding)
        else:
            self._bal[i] -= money

    def _credit(self, account: int, money: int) -> None:
        """Incoming money repays outstanding debt first (q13 automatic repayment)."""
        i = account - 1
        repay = min(self._debt[i], money)
        self._debt[i] -= repay
        self._outstanding -= repay
        self.reserve += repay
        self._bal[i] += money - repay

    def _record(self, kind: str, src: int | None, dst: int | None, amount: int, ok: bool, ref: int | None = None) -> bool:
        self.log.append(TxnRecord(len(self.log) + 1, kind, src, dst, amount, ok, ref))
        return ok

    # ------------------------------------------------------------ Part 1 (+3)
    def balances(self) -> list[int]:
        return list(self._bal)

    def debts(self) -> list[int]:
        return list(self._debt)

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        ok = self._valid(account1) and self._valid(account2) and money >= 0 and self._can_debit(account1, money, True)
        if ok:  # validate BOTH accounts before touching either
            self._debit(account1, money)
            self._credit(account2, money)
        return self._record("transfer", account1, account2, money, ok)

    def deposit(self, account: int, money: int) -> bool:
        ok = self._valid(account) and money >= 0
        if ok:
            self._credit(account, money)
        return self._record("deposit", account, None, money, ok)

    def withdraw(self, account: int, money: int) -> bool:
        ok = self._valid(account) and money >= 0 and self._can_debit(account, money, True)
        if ok:
            self._debit(account, money)
        return self._record("withdraw", account, None, money, ok)

    # ------------------------------------------------------------ Part 2
    def reverse(self, txn_id: int) -> bool:
        rec = self.log[txn_id - 1] if 1 <= txn_id <= len(self.log) else None
        ok = rec is not None and rec.ok and rec.kind != "reverse" and txn_id not in self.reversed_ids
        if ok:
            if rec.kind == "deposit":        # undo = debit the account, never with a loan
                ok = self._can_debit(rec.src, rec.amount, False)
                if ok:
                    self._debit(rec.src, rec.amount)
            elif rec.kind == "withdraw":     # undo = credit it back
                self._credit(rec.src, rec.amount)
            else:                            # transfer: move the money back from dst to src
                ok = self._can_debit(rec.dst, rec.amount, False)
                if ok:
                    self._debit(rec.dst, rec.amount)
                    self._credit(rec.src, rec.amount)
        if ok:
            self.reversed_ids.add(txn_id)
        return self._record("reverse", None, None, rec.amount if rec else 0, ok, txn_id)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    balances = [int(x) for x in lines[1].split()]
    cmds = lines[2:]
    reserve = 0
    if cmds and cmds[0].upper().startswith("RESERVE"):
        reserve = int(cmds[0].split()[1])
        cmds = cmds[1:]
    bank = Bank(balances, reserve)
    out = []
    for c in cmds:
        op, *args = c.split()
        args = [int(a) for a in args]
        ok = getattr(bank, op)(*args)
        out.append("true" if ok else "false")
    out.append("balances " + " ".join(map(str, bank.balances())))
    if part == 3:
        out.append(f"reserve {bank.reserve}")
        out.append("debts " + " ".join(map(str, bank.debts())))
        out.append(f"max_outstanding {bank.max_outstanding}")
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
