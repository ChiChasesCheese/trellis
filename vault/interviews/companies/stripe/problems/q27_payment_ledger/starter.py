"""q27 PaymentLedger — YOUR implementation. Run: python drill.py test q27"""
from __future__ import annotations

import sys


class PaymentLedger:
    def __init__(self) -> None:
        pass  # TODO

    def add_payment(self, payment_id: str, amount_cents: int, ts: str) -> bool:
        """amount > 0, ts 'YYYY-MM-DDTHH:MM:SS'. Same id+amount -> True no-op; same id other amount -> False."""
        return False  # TODO

    def add_refund(self, refund_id: str, payment_id: str, amount_cents: int, ts: str) -> bool:
        """Partial refunds while cumulative <= payment; ts >= payment ts; idempotent on refund_id."""
        return False  # TODO

    def get_total_revenue(self, start_ts: str | None = None, end_ts: str | None = None) -> int:
        """payments - refunds whose own ts is in [start_ts, end_ts] (inclusive, None = open). Bad ts -> ValueError."""
        return 0  # TODO

    def get_payments_by_date(self, date: str) -> list[str]:
        """Payment ids on 'YYYY-MM-DD', sorted by ts then id. Bad date -> ValueError."""
        return []  # TODO

    def get_balance_transactions(self) -> list[tuple[str, str, int, int]]:
        """(type, id, signed amount, running net) ordered by ts, payments before refunds, then id."""
        return []  # TODO


def run_commands(lines: list[str], max_part: int = 4) -> list[str]:
    """Drive one ledger over the command stream; commands above max_part -> ERROR."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """PAYMENT + REVENUE (no range)."""
    return run_commands(lines, 1)


def part2(lines: list[str]) -> list[str]:
    """+ REFUND."""
    return run_commands(lines, 2)


def part3(lines: list[str]) -> list[str]:
    """+ REVENUE start end, PAYMENTS date."""
    return run_commands(lines, 3)


def part4(lines: list[str]) -> list[str]:
    """+ TRANSACTIONS."""
    return run_commands(lines, 4)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = part4(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
