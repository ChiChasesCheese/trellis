"""cd11 PaymentIntent lifecycle — YOUR implementation.

Public API (must match solution.py):
    class PaymentIntentEngine:
        __init__(max_confirm_attempts: int = 3)
        init_merchant(merchant_id, balance_cents) -> bool
        create_intent(intent_id, merchant_id, amount_cents, method, settle_window=None) -> bool
        confirm(intent_id, ts=None) -> str          # "succeeded"|"processing"|"canceled"|"ignored"
        settle(intent_id, ts=None) -> bool
        fail(intent_id, ts=None) -> bool
        cancel(intent_id, ts=None) -> bool
        expire(intent_id, ts) -> bool
        update_amount(intent_id, amount_cents) -> bool
        change_method(intent_id, method) -> bool
        get_status(intent_id) -> str | None
        get_balance(merchant_id) -> int | None
        balances() -> list[tuple[str, int]]
    run_commands(lines, part=4) -> list[str]
    part1(lines) / part2(lines) / part3(lines) / part4(lines) -> list[str]
    main(stdin=sys.stdin, stdout=sys.stdout) -> None

See problem.md for the exact state machine (card=sync, bank_debit=async), the
confirm-attempt auto-cancel rule, the fail-returns-to-requires_payment_method rule, and the
Part 4 settle_window / expire timing rules, plus the command-stream protocol.
"""

from __future__ import annotations

import sys

REQUIRES_PAYMENT_METHOD = "requires_payment_method"
PROCESSING = "processing"
SUCCEEDED = "succeeded"
CANCELED = "canceled"

METHODS = ("card", "bank_debit")


class PaymentIntentEngine:
    def __init__(self, max_confirm_attempts: int = 3) -> None:
        # TODO
        pass

    # ---------------------------------------------------------------- Part 1
    def init_merchant(self, merchant_id: str, balance_cents: int) -> bool:
        """Create a merchant. Repeated id -> False, balance untouched."""
        # TODO
        raise NotImplementedError

    def create_intent(
        self,
        intent_id: str,
        merchant_id: str,
        amount_cents: int,
        method: str,
        settle_window: int | None = None,
    ) -> bool:
        """Create a PaymentIntent in requires_payment_method. See problem.md for all ignore rules."""
        # TODO
        raise NotImplementedError

    def confirm(self, intent_id: str, ts: int | None = None) -> str:
        """card -> succeeded now (credits balance); bank_debit -> processing.
        Returns "succeeded"/"processing"/"canceled"/"ignored"."""
        # TODO
        raise NotImplementedError

    def settle(self, intent_id: str, ts: int | None = None) -> bool:
        """processing -> succeeded, crediting the balance now."""
        # TODO
        raise NotImplementedError

    def balances(self) -> list[tuple[str, int]]:
        # TODO
        raise NotImplementedError

    def get_balance(self, merchant_id: str) -> int | None:
        # TODO
        raise NotImplementedError

    def get_status(self, intent_id: str) -> str | None:
        # TODO
        raise NotImplementedError

    # ---------------------------------------------------------------- Part 2
    def update_amount(self, intent_id: str, amount_cents: int) -> bool:
        """Only while requires_payment_method."""
        # TODO
        raise NotImplementedError

    def change_method(self, intent_id: str, method: str) -> bool:
        """Only while requires_payment_method."""
        # TODO
        raise NotImplementedError

    # ---------------------------------------------------------------- Part 3
    def fail(self, intent_id: str, ts: int | None = None) -> bool:
        """processing -> requires_payment_method (retry). Does not reset confirm_attempts."""
        # TODO
        raise NotImplementedError

    def cancel(self, intent_id: str, ts: int | None = None) -> bool:
        """requires_payment_method -> canceled always; processing -> canceled only for
        bank_debit; terminal states are a no-op."""
        # TODO
        raise NotImplementedError

    # ---------------------------------------------------------------- Part 4
    def expire(self, intent_id: str, ts: int) -> bool:
        """processing, settle_window set and elapsed -> canceled. Else no-op."""
        # TODO
        raise NotImplementedError


def run_commands(lines: list[str], part: int = 4) -> list[str]:
    """Execute a command stream (see problem.md Input/Output) against a fresh
    PaymentIntentEngine, gated to the commands unlocked by `part`."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    return run_commands(lines, part=1)


def part2(lines: list[str]) -> list[str]:
    return run_commands(lines, part=2)


def part3(lines: list[str]) -> list[str]:
    return run_commands(lines, part=3)


def part4(lines: list[str]) -> list[str]:
    return run_commands(lines, part=4)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw_lines = stdin.read().splitlines()
    part = 4
    body_start = 0
    for i, line in enumerate(raw_lines):
        if line.strip():
            if line.strip().upper().startswith("PART"):
                tokens = line.strip().split()
                if len(tokens) == 2 and tokens[1].isdigit():
                    part = int(tokens[1])
                body_start = i + 1
            break
    lines = [ln.strip() for ln in raw_lines[body_start:] if ln.strip()]
    out = {1: part1, 2: part2, 3: part3, 4: part4}.get(part, part4)(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
