"""cd11 PaymentIntent lifecycle — reference solution.

The interview asks for a class (`PaymentIntentEngine`), not a `partN(lines)` pipeline: the
lifecycle methods (`init_merchant`, `create_intent`, `confirm`, `settle`, `fail`, `cancel`,
`expire`, `update_amount`, `change_method`) are cumulative across the four interview stages on
*one* object, exactly the way an onsite interviewer reveals them. `run_commands`/`part1..4`/
`main()` are a thin command-stream harness around the same class (see problem.md's "Input"
section for the exact protocol and REPORT.md's "CONVENTIONS 对照") so this suite's other
`impl.partN(lines)` / `main(stdin, stdout)` expectations still hold.

Money is always integer cents. `ts` values are opaque integers (never calendar dates) that only
matter from Part 4 onward, where `settle_window` gates how long after `confirm` a `processing`
intent may still be `settle`d/`fail`ed/cancelled, and `expire` reaps ones that ran out the clock.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

REQUIRES_PAYMENT_METHOD = "requires_payment_method"
PROCESSING = "processing"
SUCCEEDED = "succeeded"
CANCELED = "canceled"

METHODS = ("card", "bank_debit")


@dataclass
class PaymentIntent:
    """One PaymentIntent. `confirm_attempts` and `confirmed_at` persist across a fail/retry
    cycle -- that persistence is what lets `confirm` auto-cancel after too many attempts, and
    what lets Part 4's window checks measure from the *most recent* confirm."""

    id: str
    merchant_id: str
    amount_cents: int
    method: str
    settle_window: int | None = None
    status: str = REQUIRES_PAYMENT_METHOD
    confirm_attempts: int = 0
    confirmed_at: int | None = None


class PaymentIntentEngine:
    """Single-process, multi-merchant PaymentIntent ledger.

    State: `_merchants` (balance in cents, keyed by merchant id) and `_intents` (PaymentIntent,
    keyed by intent id). `max_confirm_attempts` is the anti-abuse cap from
    `loop/study/20-cards/stripe_api.md` (a real PaymentIntent auto-cancels once confirmed too
    many times); it is a constructor parameter, not a magic constant, so a test can shrink it to
    exercise the auto-cancel path without a long command stream.
    """

    def __init__(self, max_confirm_attempts: int = 3) -> None:
        self.max_confirm_attempts = max_confirm_attempts
        self._merchants: dict[str, int] = {}
        self._intents: dict[str, PaymentIntent] = {}

    # ---------------------------------------------------------------- Part 1
    def init_merchant(self, merchant_id: str, balance_cents: int) -> bool:
        """Create a merchant. A repeated id is ignored -- the existing balance is never reset."""
        if merchant_id in self._merchants:
            return False
        self._merchants[merchant_id] = balance_cents
        return True

    def create_intent(
        self,
        intent_id: str,
        merchant_id: str,
        amount_cents: int,
        method: str,
        settle_window: int | None = None,
    ) -> bool:
        """Create a PaymentIntent in `requires_payment_method`. `settle_window` only matters from
        Part 4 -- but a negative one is rejected outright at every part (malformed, not "unlimited")."""
        if intent_id in self._intents:
            return False
        if merchant_id not in self._merchants:
            return False
        if not isinstance(amount_cents, int) or amount_cents < 0:
            return False
        if method not in METHODS:
            return False
        if settle_window is not None and settle_window < 0:
            return False  # malformed window -> reject the whole command, unlike q10's REFUND limit
        self._intents[intent_id] = PaymentIntent(
            id=intent_id,
            merchant_id=merchant_id,
            amount_cents=amount_cents,
            method=method,
            settle_window=settle_window,
        )
        return True

    def confirm(self, intent_id: str, ts: int | None = None) -> str:
        """Confirm a PaymentIntent. Returns one of "succeeded"/"processing"/"canceled"/"ignored".

        `card` is synchronous (succeeds immediately, credits the merchant now); `bank_debit` is
        asynchronous (moves to `processing`; a later `settle` credits it). Every attempt that
        reaches an intent still in `requires_payment_method` bumps `confirm_attempts` *before*
        deciding whether it is the one-too-many attempt that auto-cancels instead of processing.
        """
        pi = self._intents.get(intent_id)
        if pi is None or pi.status != REQUIRES_PAYMENT_METHOD:
            return "ignored"
        pi.confirm_attempts += 1
        if pi.confirm_attempts > self.max_confirm_attempts:
            pi.status = CANCELED
            return "canceled"
        pi.confirmed_at = ts
        if pi.method == "card":
            pi.status = SUCCEEDED
            self._merchants[pi.merchant_id] += pi.amount_cents
            return "succeeded"
        pi.status = PROCESSING
        return "processing"

    def settle(self, intent_id: str, ts: int | None = None) -> bool:
        """`processing` -> `succeeded`, crediting the (possibly since-updated) amount now."""
        pi = self._intents.get(intent_id)
        if pi is None or pi.status != PROCESSING:
            return False
        if not self._within_window(pi, ts):
            return False
        pi.status = SUCCEEDED
        self._merchants[pi.merchant_id] += pi.amount_cents
        return True

    def balances(self) -> list[tuple[str, int]]:
        """`[(merchant_id, balance_cents), ...]` for every merchant ever init'ed, sorted by id."""
        return sorted(self._merchants.items())

    def get_balance(self, merchant_id: str) -> int | None:
        return self._merchants.get(merchant_id)

    def get_status(self, intent_id: str) -> str | None:
        pi = self._intents.get(intent_id)
        return pi.status if pi is not None else None

    # ---------------------------------------------------------------- Part 2
    def update_amount(self, intent_id: str, amount_cents: int) -> bool:
        """Change the amount, only while still `requires_payment_method`."""
        pi = self._intents.get(intent_id)
        if pi is None or pi.status != REQUIRES_PAYMENT_METHOD:
            return False
        if not isinstance(amount_cents, int) or amount_cents < 0:
            return False
        pi.amount_cents = amount_cents
        return True

    def change_method(self, intent_id: str, method: str) -> bool:
        """Swap card <-> bank_debit, only while still `requires_payment_method`. Because
        `confirm` branches on `method`, this can reshape whether the *next* confirm is
        synchronous or asynchronous."""
        pi = self._intents.get(intent_id)
        if pi is None or pi.status != REQUIRES_PAYMENT_METHOD:
            return False
        if method not in METHODS:
            return False
        pi.method = method
        return True

    # ---------------------------------------------------------------- Part 3
    def fail(self, intent_id: str, ts: int | None = None) -> bool:
        """`processing` -> back to `requires_payment_method` for a retry -- the real Stripe
        behavior (see stripe_api.md), and NOT the same target state as q10's FAIL. Does not
        reset `confirm_attempts`."""
        pi = self._intents.get(intent_id)
        if pi is None or pi.status != PROCESSING:
            return False
        if not self._within_window(pi, ts):
            return False
        pi.status = REQUIRES_PAYMENT_METHOD
        return True

    def cancel(self, intent_id: str, ts: int | None = None) -> bool:
        """Manual cancellation. Always allowed from `requires_payment_method`; from `processing`
        only for an async (`bank_debit`) method, and (Part 4) only within the settle window;
        never from a terminal state (`succeeded`/`canceled`)."""
        pi = self._intents.get(intent_id)
        if pi is None:
            return False
        if pi.status == REQUIRES_PAYMENT_METHOD:
            pi.status = CANCELED
            return True
        if pi.status == PROCESSING:
            if pi.method != "bank_debit":
                return False
            if not self._within_window(pi, ts):
                return False
            pi.status = CANCELED
            return True
        return False  # succeeded / canceled: terminal

    # ---------------------------------------------------------------- Part 4
    def _within_window(self, pi: PaymentIntent, ts: int | None) -> bool:
        """True if `settle`/`fail`/a processing-`cancel` may still act on `pi` at time `ts`.
        `settle_window=None` -> unlimited. Parts 1-3 never set a window and pass ts=None from
        their command handlers, so this is always True there regardless of `ts`."""
        if pi.settle_window is None:
            return True
        if ts is None or pi.confirmed_at is None:
            return True
        return (ts - pi.confirmed_at) <= pi.settle_window

    def expire(self, intent_id: str, ts: int) -> bool:
        """Reap a `processing` intent whose settle window has strictly elapsed -> `canceled`.
        A no-op if the window hasn't passed yet, or if `settle_window` is None (unlimited grace
        never expires on its own -- it must be resolved by hand)."""
        pi = self._intents.get(intent_id)
        if pi is None or pi.status != PROCESSING:
            return False
        if pi.settle_window is None or pi.confirmed_at is None:
            return False
        if (ts - pi.confirmed_at) > pi.settle_window:
            pi.status = CANCELED
            return True
        return False


# ------------------------------------------------------------ command-stream harness (io/perf)
# One handler per verb. Handlers own arity/int-parsing (a malformed line -> [] i.e. no output
# line at all); the engine's own bool/str returns become the OK/IGNORED or status text. Errors
# never raise here -- an unusable line is simply silent, per problem.md's Input section.
def _int_or_none(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


def _h_init(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 2:
        return []
    m, bal = args
    bal = _int_or_none(bal)
    if bal is None:
        return []
    engine.init_merchant(m, bal)
    return []  # INIT never produces an output line


def _h_create(engine: PaymentIntentEngine, ts, args: list[str], part: int) -> list[str]:
    if len(args) != 4 and not (part >= 4 and len(args) == 5):
        return []
    pid, m, amount, method = args[:4]
    amount = _int_or_none(amount)
    if amount is None:
        return []
    window = None
    if len(args) == 5:
        window = _int_or_none(args[4])
        if window is None:
            return []
    ok = engine.create_intent(pid, m, amount, method, settle_window=window)
    return [f"CREATE {pid} {'OK' if ok else 'IGNORED'}"]


def _h_confirm(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 1:
        return []
    (pid,) = args
    return [f"CONFIRM {pid} {engine.confirm(pid, ts=ts)}"]


def _h_settle(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 1:
        return []
    (pid,) = args
    return [f"SETTLE {pid} {'OK' if engine.settle(pid, ts=ts) else 'IGNORED'}"]


def _h_fail(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 1:
        return []
    (pid,) = args
    return [f"FAIL {pid} {'OK' if engine.fail(pid, ts=ts) else 'IGNORED'}"]


def _h_cancel(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 1:
        return []
    (pid,) = args
    return [f"CANCEL {pid} {'OK' if engine.cancel(pid, ts=ts) else 'IGNORED'}"]


def _h_expire(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 1 or ts is None:
        return []
    (pid,) = args
    return [f"EXPIRE {pid} {'OK' if engine.expire(pid, ts) else 'IGNORED'}"]


def _h_update(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 2:
        return []
    pid, amount = args
    amount = _int_or_none(amount)
    if amount is None:
        return []
    return [f"UPDATE {pid} {'OK' if engine.update_amount(pid, amount) else 'IGNORED'}"]


def _h_change_method(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 2:
        return []
    pid, method = args
    return [f"CHANGE_METHOD {pid} {'OK' if engine.change_method(pid, method) else 'IGNORED'}"]


def _h_balance(engine: PaymentIntentEngine, ts, args: list[str]) -> list[str]:
    if len(args) != 1:
        return []
    (m,) = args
    bal = engine.get_balance(m)
    return [f"BALANCE {m} {bal if bal is not None else 'UNKNOWN'}"]


def _handlers_for_part(part: int) -> dict:
    handlers: dict = {
        "INIT": _h_init,
        "CREATE": lambda engine, ts, args: _h_create(engine, ts, args, part),
        "CONFIRM": _h_confirm,
        "SETTLE": _h_settle,
        "BALANCE": _h_balance,
    }
    if part >= 2:
        handlers["UPDATE"] = _h_update
        handlers["CHANGE_METHOD"] = _h_change_method
    if part >= 3:
        handlers["FAIL"] = _h_fail
        handlers["CANCEL"] = _h_cancel
    if part >= 4:
        handlers["EXPIRE"] = _h_expire
    return handlers


def run_commands(lines: list[str], part: int = 4) -> list[str]:
    """Execute a command stream against a fresh PaymentIntentEngine for the given part."""
    handlers = _handlers_for_part(part)
    engine = PaymentIntentEngine()
    out: list[str] = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        fields = raw.split()
        if part >= 4:
            if len(fields) < 2:
                continue
            ts = _int_or_none(fields[0])
            if ts is None:
                continue
            cmd, args = fields[1], fields[2:]
        else:
            ts, cmd, args = None, fields[0], fields[1:]
        handler = handlers.get(cmd)
        if handler is None:
            continue  # not unlocked by this part, or unknown word -> silently skip
        out.extend(handler(engine, ts, args))
    return out


def part1(lines: list[str]) -> list[str]:
    return run_commands(lines, part=1)


def part2(lines: list[str]) -> list[str]:
    return run_commands(lines, part=2)


def part3(lines: list[str]) -> list[str]:
    return run_commands(lines, part=3)


def part4(lines: list[str]) -> list[str]:
    return run_commands(lines, part=4)


_PARTS = {1: part1, 2: part2, 3: part3, 4: part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw_lines = stdin.read().splitlines()
    part = 4  # Parts 1-4 accumulate; the full rule set is the default when no header is given
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
    out = _PARTS.get(part, part4)(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
