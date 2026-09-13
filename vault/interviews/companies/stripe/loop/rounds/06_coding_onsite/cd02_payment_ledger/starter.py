"""cd02 PaymentLedger — YOUR implementation.

Public API (must match solution.py):
    class PaymentLedger:
        add_payment(payment_id, amount_cents, ts_iso, customer) -> bool
        add_refund(refund_id, payment_id, amount_cents, ts_iso) -> bool
        get_total_revenue() -> int
        get_payments_by_date(start_iso, end_iso) -> list[dict]
        export_json() -> str
        load_json(blob) -> PaymentLedger   # classmethod
    run_commands(lines) -> list[str]
    part1(lines) / part2(lines) / part3(lines) -> list[str]   # thin wrappers over run_commands
    main(stdin=sys.stdin, stdout=sys.stdout) -> None

See problem.md for the exact timestamp profile (`YYYY-MM-DDTHH:MM:SS`, naive), the
idempotent-duplicate vs. KeyError vs. ValueError contract, and the command-stream protocol.
"""

from __future__ import annotations

import sys


class PaymentLedger:
    def __init__(self) -> None:
        # TODO
        pass

    def add_payment(self, payment_id: str, amount_cents: int, ts_iso: str, customer: str) -> bool:
        """Record a payment. Return False (no-op) if payment_id already exists."""
        # TODO
        raise NotImplementedError

    def add_refund(self, refund_id: str, payment_id: str, amount_cents: int, ts_iso: str) -> bool:
        """Apply a partial/full refund. Return False if refund_id already applied.
        Raise KeyError for an unknown payment_id, ValueError if the refund would exceed the
        remaining balance."""
        # TODO
        raise NotImplementedError

    def get_total_revenue(self) -> int:
        """sum(amount_cents) - sum(all successful refunds), never negative."""
        # TODO
        raise NotImplementedError

    def get_payments_by_date(self, start_iso: str, end_iso: str) -> list[dict]:
        """Payments with ts in [start_iso, end_iso] inclusive, sorted by (ts, payment_id)."""
        # TODO
        raise NotImplementedError

    def export_json(self) -> str:
        # TODO
        raise NotImplementedError

    @classmethod
    def load_json(cls, blob: str) -> "PaymentLedger":
        # TODO
        raise NotImplementedError


def run_commands(lines: list[str]) -> list[str]:
    """Execute a command stream (PAY / REFUND / REVENUE / RANGE) against a fresh PaymentLedger."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    return run_commands(lines)


def part2(lines: list[str]) -> list[str]:
    return run_commands(lines)


def part3(lines: list[str]) -> list[str]:
    return run_commands(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = run_commands(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
