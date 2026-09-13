"""q30 Stripe Capital — reference solution.

State: merchant_id -> {loan_id -> outstanding cents}; the inner dict keeps creation order so the
loan-less transaction variant can repay oldest-first.  Every amount is an integer number of cents.
Invalid actions (unknown merchant/loan, negative amount, pct outside 1..100, duplicate create,
unknown method) are silently ignored.
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Action(NamedTuple):
    method: str
    params: list[str]


def parse(line: str) -> Action | None:
    """'METHOD: p1, p2' -> Action('METHOD', ['p1', 'p2']); None when the line has no 'METHOD:' head."""
    head, sep, rest = line.partition(":")
    if not sep:
        return None
    return Action(head.strip(), [p.strip() for p in rest.split(",")])


def to_int(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None


class Capital:
    def __init__(self, duplicate_create: str = "ignore") -> None:
        self.loans: dict[str, dict[str, int]] = {}
        self.duplicate_create = duplicate_create

    def repay(self, merchant: str, loan: str, amount: int) -> None:
        book = self.loans[merchant]
        # a balance never goes negative: overpayment is capped, the remainder is ignored
        book[loan] = max(0, book[loan] - amount)

    def repay_oldest_first(self, merchant: str, amount: int) -> None:
        for loan, balance in self.loans[merchant].items():   # creation order
            use = min(balance, amount)
            self.loans[merchant][loan] = balance - use
            amount -= use
            if amount == 0:
                break

    def apply(self, act: Action) -> None:
        p = act.params
        if act.method == "CREATE_LOAN" and len(p) == 3:
            merchant, loan, amount = p[0], p[1], to_int(p[2])
            if amount is None or amount < 0 or not merchant or not loan:
                return
            book = self.loans.setdefault(merchant, {})
            if loan in book:  # duplicate create: Part 4 rule = ignore (variants: replace / add)
                if self.duplicate_create == "replace":
                    book[loan] = amount
                elif self.duplicate_create == "add":
                    book[loan] += amount
                return
            book[loan] = amount
            return

        if act.method == "TRANSACTION_PROCESSED" and len(p) == 3:   # loan-less variant (Part 3)
            merchant, amount, pct = p[0], to_int(p[1]), to_int(p[2])
            if merchant not in self.loans or amount is None or pct is None:
                return
            if amount < 0 or not 1 <= pct <= 100:
                return
            self.repay_oldest_first(merchant, amount * pct // 100)  # truncate
            return

        if len(p) < 3:
            return
        merchant, loan, amount = p[0], p[1], to_int(p[2])
        if merchant not in self.loans or loan not in self.loans[merchant]:
            return  # unknown merchant / loan -> no-op
        if amount is None or amount < 0:
            return
        if act.method == "PAY_LOAN" and len(p) == 3:
            self.repay(merchant, loan, amount)
        elif act.method == "INCREASE_LOAN" and len(p) == 3:
            self.loans[merchant][loan] += amount
        elif act.method == "TRANSACTION_PROCESSED" and len(p) == 4:
            pct = to_int(p[3])
            if pct is None or not 1 <= pct <= 100:
                return
            # withhold amount * pct / 100, truncated to whole cents (433.64 -> 433)
            self.repay(merchant, loan, amount * pct // 100)

    def report(self) -> list[str]:
        out = []
        for merchant in sorted(self.loans):   # plain string order
            total = sum(self.loans[merchant].values())
            if total > 0:                     # skip merchants with no outstanding balance
                out.append(f"{merchant},{total}")
        return out


def process(lines: list[str], duplicate_create: str = "ignore") -> list[str]:
    cap = Capital(duplicate_create)
    for raw in lines:
        act = parse(raw.strip()) if raw.strip() else None
        if act is not None:
            cap.apply(act)
    return cap.report()


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
