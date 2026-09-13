"""cd02 PaymentLedger — reference solution.

The interview asks for a class, not a `partN(lines)` pipeline, so the class *is* the product:
`add_payment` / `add_refund` / `get_total_revenue` / `get_payments_by_date` / `export_json` /
`load_json` are cumulative on one object exactly as an interviewer would reveal them part by
part. `run_commands` / `part1..3` / `main()` are a thin command-stream harness around the same
class (see REPORT.md "CONVENTIONS 对照") so the suite still has the `impl.partN(lines)` and
`main(stdin, stdout)` surfaces this repo's tests expect.

Money is always integer cents. Timestamps use one fixed profile, naive `YYYY-MM-DDTHH:MM:SS`
(see problem.md "Variants" for why): every field is zero-padded and fixed-width, so on
*validated* strings plain string order == chronological order. The ledger therefore stores and
compares the raw strings and only parses to validate; invalid timestamps raise `ValueError` at
every entry point that accepts one (`add_payment`, `add_refund`, `get_payments_by_date`).
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime

_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
_TS_FMT = "%Y-%m-%dT%H:%M:%S"


def _validate_ts(ts: str) -> str:
    """Return `ts` unchanged if it has the fixed shape AND is a real calendar time; else ValueError."""
    if not isinstance(ts, str) or not _TS_RE.match(ts):
        raise ValueError(f"invalid timestamp: {ts!r}")
    try:
        datetime.strptime(ts, _TS_FMT)  # rejects 2026-02-30, 25:00:00, ...
    except ValueError as e:
        raise ValueError(f"invalid timestamp: {ts!r}") from e
    return ts


@dataclass
class Payment:
    """One recorded payment plus the running total already refunded against it."""

    payment_id: str
    amount_cents: int
    ts: str
    customer: str
    refunded_cents: int = 0

    @property
    def net_cents(self) -> int:
        """What this payment still contributes to revenue (never negative by construction)."""
        return self.amount_cents - self.refunded_cents


class PaymentLedger:
    """Single-merchant ledger.

    State: `payments` keyed by payment_id, plus the set of refund ids already applied — kept so a
    retried refund is a no-op, and persisted so a reloaded ledger still rejects the same replay.
    """

    def __init__(self) -> None:
        self._payments: dict[str, Payment] = {}
        self._refund_ids: set[str] = set()

    # ---------------------------------------------------------------- Part 1
    def add_payment(self, payment_id: str, amount_cents: int, ts_iso: str, customer: str) -> bool:
        """Record a payment; a repeated payment_id is an idempotent retry -> False, original untouched."""
        _validate_ts(ts_iso)  # validate before touching state: a bad ts on a duplicate still raises
        if payment_id in self._payments:
            return False
        self._payments[payment_id] = Payment(payment_id, amount_cents, ts_iso, customer)
        return True

    def get_total_revenue(self) -> int:
        """Sum of every payment's amount minus what was refunded against it."""
        return sum(p.net_cents for p in self._payments.values())

    # ---------------------------------------------------------------- Part 2
    def add_refund(self, refund_id: str, payment_id: str, amount_cents: int, ts_iso: str) -> bool:
        """Apply a (partial) refund. Checks run in a fixed order: bad timestamp -> ValueError;
        repeated refund_id -> False (idempotent); unknown payment_id -> KeyError; cumulative refunds
        over the original amount -> ValueError (refunding exactly the remainder is allowed)."""
        _validate_ts(ts_iso)
        if refund_id in self._refund_ids:
            return False
        payment = self._payments.get(payment_id)
        if payment is None:
            raise KeyError(payment_id)
        if amount_cents > payment.net_cents:
            raise ValueError(f"refund exceeds remaining balance: {payment_id}")
        payment.refunded_cents += amount_cents
        self._refund_ids.add(refund_id)
        return True

    # ---------------------------------------------------------------- Part 3
    def get_payments_by_date(self, start_iso: str, end_iso: str) -> list[dict]:
        """Payments with ts in [start_iso, end_iso] (both inclusive), sorted by (ts, payment_id).
        Both bounds are validated first; a bad bound raises before any payment is looked at."""
        lo, hi = _validate_ts(start_iso), _validate_ts(end_iso)
        # both sides are validated fixed-width strings, so plain string order == time order
        rows = [p for p in self._payments.values() if lo <= p.ts <= hi]
        rows.sort(key=lambda p: (p.ts, p.payment_id))
        return [asdict(p) for p in rows]

    def export_json(self) -> str:
        """Serialize payments AND the applied refund ids — without the ids a reload would accept replays."""
        state = {
            "payments": [asdict(p) for p in self._payments.values()],
            "refund_ids": sorted(self._refund_ids),
        }
        return json.dumps(state, sort_keys=True)

    @classmethod
    def load_json(cls, blob: str) -> "PaymentLedger":
        """Inverse of export_json: a fresh ledger with identical revenue, queries and dedup behaviour."""
        data = json.loads(blob)
        ledger = cls()
        for row in data["payments"]:
            ledger._payments[row["payment_id"]] = Payment(**row)
        ledger._refund_ids = set(data["refund_ids"])
        return ledger


# ------------------------------------------------------------ command-stream harness (io/perf)
# One handler per verb; each takes the ledger and the verb's arguments and returns output lines.
# Errors are mapped to text here so the class itself never knows about the CLI protocol.
def _cmd_pay(ledger: PaymentLedger, args: list[str]) -> list[str]:
    payment_id, amount, ts, customer = args
    try:
        ok = ledger.add_payment(payment_id, int(amount), ts, customer)
    except ValueError as e:
        return [f"PAY {payment_id} ERROR {e}"]
    return [f"PAY {payment_id} {'OK' if ok else 'DUP'}"]


def _cmd_refund(ledger: PaymentLedger, args: list[str]) -> list[str]:
    refund_id, payment_id, amount, ts = args
    try:
        ok = ledger.add_refund(refund_id, payment_id, int(amount), ts)
    except KeyError:
        return [f"REFUND {refund_id} ERROR unknown_payment {payment_id}"]
    except ValueError as e:
        return [f"REFUND {refund_id} ERROR {e}"]
    return [f"REFUND {refund_id} {'OK' if ok else 'DUP'}"]


def _cmd_revenue(ledger: PaymentLedger, args: list[str]) -> list[str]:
    return [f"REVENUE {ledger.get_total_revenue()}"]


def _cmd_range(ledger: PaymentLedger, args: list[str]) -> list[str]:
    start, end = args
    try:
        rows = ledger.get_payments_by_date(start, end)
    except ValueError as e:
        return [f"RANGE ERROR {e}"]
    return [f"RANGE {len(rows)}"] + [_format_row(r) for r in rows]


def _format_row(r: dict) -> str:
    return f"{r['payment_id']} {r['amount_cents']} {r['ts']} {r['customer']} {r['refunded_cents']}"


COMMANDS = {"PAY": _cmd_pay, "REFUND": _cmd_refund, "REVENUE": _cmd_revenue, "RANGE": _cmd_range}


def run_commands(lines: list[str]) -> list[str]:
    """Execute a command stream against a fresh PaymentLedger; return the output lines."""
    ledger = PaymentLedger()
    out: list[str] = []
    for raw in lines:
        fields = raw.split()
        if not fields or fields[0] not in COMMANDS:
            continue  # blank line or unknown verb: neither is defined by the problem; skip
        out.extend(COMMANDS[fields[0]](ledger, fields[1:]))
    return out


# The class is cumulative (one interviewer-revealed method set on one object), so all three parts
# run the identical full command engine -- they differ in which commands/tests exercise them, not
# in capability. See REPORT.md's CONVENTIONS note.
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
