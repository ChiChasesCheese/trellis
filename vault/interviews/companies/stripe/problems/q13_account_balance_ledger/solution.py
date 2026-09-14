"""q13 Account Balance Ledger — reference solution.

All money is integer cents (parsed from the decimal string without floats).  One Ledger class with a
`mode` (1 = allow negatives, 2 = reject overdrafts, 3 = platform lending) processes lines in order.
Overdraft test is STRICT: balance - amount < 0 rejects; landing exactly on 0 is fine.
"""
from __future__ import annotations

import sys
from decimal import ROUND_HALF_UP, Decimal

PLATFORM = "platform"


def to_cents(text: str) -> int:
    """'12.34' -> 1234, '7' -> 700, '0.5' -> 50. Decimal, half-up if >2 decimals ever appear."""
    return int(Decimal(text.strip()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)


def fmt(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"


class Ledger:
    def __init__(self, mode: int) -> None:
        self.mode = mode
        self.bal: dict[str, int] = {}
        self.loan: dict[str, int] = {}     # user -> outstanding loan from the platform (Part 3)
        self.rejected: list[str] = []
        self.max_reserve = 0               # peak of sum(loan.values())

    # -- primitives ---------------------------------------------------------------
    def credit(self, user: str, amount: int) -> None:
        if self.mode == 3 and user != PLATFORM and self.loan.get(user, 0) > 0:
            # automatic repayment: incoming money first pays down the loan, capped at the loan
            repay = min(self.loan[user], amount)
            self.loan[user] -= repay
            self.bal[PLATFORM] = self.bal.get(PLATFORM, 0) + repay
            amount -= repay
        self.bal[user] = self.bal.get(user, 0) + amount

    def can_debit(self, user: str, amount: int) -> tuple[bool, int]:
        """-> (allowed, shortfall to borrow). Part 1 always allows; Part 2/3 reject strict overdrafts."""
        balance = self.bal.get(user, 0)
        shortfall = amount - balance
        if self.mode == 1 or shortfall <= 0:  # shortfall == 0 lands exactly on 0.00: accepted
            return True, 0
        if self.mode == 3 and user != PLATFORM and self.bal.get(PLATFORM, 0) >= shortfall:
            return True, shortfall            # platform can cover it (>=: lending all of it is allowed)
        return False, 0

    def debit(self, user: str, amount: int, shortfall: int) -> None:
        if shortfall:
            self.bal[PLATFORM] -= shortfall
            self.loan[user] = self.loan.get(user, 0) + shortfall
            self.bal[user] = self.bal.get(user, 0) + shortfall
            self.max_reserve = max(self.max_reserve, sum(self.loan.values()))  # peak measured right after lending
        self.bal[user] = self.bal.get(user, 0) - amount

    # -- one line ------------------------------------------------------------------
    def apply(self, line: str) -> None:
        f = [p.strip() for p in line.split(",")]
        txn, user, kind = f[0], f[1], f[2].lower()
        if kind == "credit":
            self.credit(user, to_cents(f[3]))
        elif kind == "debit":
            amount = to_cents(f[3])
            ok, short = self.can_debit(user, amount)
            if ok:
                self.debit(user, amount, short)
            else:
                self.rejected.append(txn)
        elif kind == "transfer" and self.mode == 3:
            to, amount = f[3], to_cents(f[4])
            ok, short = self.can_debit(user, amount)
            if ok:
                self.debit(user, amount, short)  # borrow (peak reserve) BEFORE the receiver repays
                self.credit(to, amount)
            else:
                self.rejected.append(txn)        # nothing changes on either side
        else:
            raise ValueError(f"bad line {line!r}")

    # -- output ----------------------------------------------------------------------
    def render(self) -> list[str]:
        # sort key: plain string order of user_id
        out = [f"{u} {fmt(c)}" for u, c in sorted(self.bal.items()) if c != 0]
        if self.mode >= 2:
            out.append("REJECTED: " + (",".join(self.rejected) if self.rejected else "NONE"))
        if self.mode == 3:
            out.append(f"MAX_RESERVE: {fmt(self.max_reserve)}")
        return out


def run(lines: list[str], mode: int) -> list[str]:
    ledger = Ledger(mode)
    for raw in lines:
        if raw.strip():
            ledger.apply(raw)
    return ledger.render()


def part1(lines: list[str]) -> list[str]:
    return run(lines, 1)


def part2(lines: list[str]) -> list[str]:
    return run(lines, 2)


def part3(lines: list[str]) -> list[str]:
    return run(lines, 3)


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
