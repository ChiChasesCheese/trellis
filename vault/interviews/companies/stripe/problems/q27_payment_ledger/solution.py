"""q27 PaymentLedger — reference solution.

Money is integer cents. Timestamps are validated against the exact format YYYY-MM-DDTHH:MM:SS and
then kept as strings: in that fixed-width format lexicographic order == chronological order, so
range checks are plain string comparisons. Events are bucketed by calendar day with a per-day
total, so a range query costs O(#days + events on the two edge days) instead of O(#events).
"""
from __future__ import annotations

import sys
from collections import defaultdict
from datetime import datetime
from typing import NamedTuple

TS_FMT = "%Y-%m-%dT%H:%M:%S"
PAYMENT, REFUND = 0, 1          # sort order at equal ts: payment rows before refund rows


class Event(NamedTuple):
    ts: str
    kind: int
    id: str
    amount: int                 # signed: refunds negative


class Payment:
    __slots__ = ("id", "amount", "ts", "refunded")

    def __init__(self, pid: str, amount: int, ts: str) -> None:
        self.id, self.amount, self.ts, self.refunded = pid, amount, ts, 0


def valid_ts(ts: str) -> bool:
    try:
        return datetime.strptime(ts, TS_FMT).strftime(TS_FMT) == ts   # exact, zero-padded form only
    except ValueError:
        return False


def check_ts(ts: str) -> str:
    if not valid_ts(ts):
        raise ValueError(f"bad timestamp {ts!r}")
    return ts


class PaymentLedger:
    def __init__(self) -> None:
        self.payments: dict[str, Payment] = {}
        self.refunds: dict[str, tuple[str, int]] = {}          # refund_id -> (payment_id, amount)
        self.by_day: dict[str, list[Event]] = defaultdict(list)
        self.day_total: dict[str, int] = defaultdict(int)
        self.total = 0

    def _record(self, ev: Event) -> None:
        self.by_day[ev.ts[:10]].append(ev)
        self.day_total[ev.ts[:10]] += ev.amount
        self.total += ev.amount

    def add_payment(self, payment_id: str, amount_cents: int, ts: str) -> bool:
        if payment_id in self.payments:                        # idempotent replay: same amount -> no-op
            return self.payments[payment_id].amount == amount_cents
        if amount_cents <= 0 or not valid_ts(ts):              # amount must be > 0
            return False
        self.payments[payment_id] = Payment(payment_id, amount_cents, ts)
        self._record(Event(ts, PAYMENT, payment_id, amount_cents))
        return True

    def add_refund(self, refund_id: str, payment_id: str, amount_cents: int, ts: str) -> bool:
        if refund_id in self.refunds:                          # replay: identical fields -> no-op
            return self.refunds[refund_id] == (payment_id, amount_cents)
        p = self.payments.get(payment_id)
        if p is None or amount_cents <= 0 or not valid_ts(ts):
            return False
        if ts < p.ts:                                          # refund before its payment (same second OK)
            return False
        if p.refunded + amount_cents > p.amount:               # cumulative cap: == is allowed
            return False
        p.refunded += amount_cents
        self.refunds[refund_id] = (payment_id, amount_cents)
        self._record(Event(ts, REFUND, refund_id, -amount_cents))
        return True

    def get_total_revenue(self, start_ts: str | None = None, end_ts: str | None = None) -> int:
        if start_ts is None and end_ts is None:
            return self.total
        lo = check_ts(start_ts) if start_ts is not None else None
        hi = check_ts(end_ts) if end_ts is not None else None
        lo_day, hi_day = lo and lo[:10], hi and hi[:10]
        total = 0
        for day, evs in self.by_day.items():
            if (lo_day and day < lo_day) or (hi_day and day > hi_day):
                continue
            if day != lo_day and day != hi_day:                # whole day inside the range
                total += self.day_total[day]
            else:                                              # edge day: inclusive bounds on both ends
                total += sum(e.amount for e in evs if (lo is None or e.ts >= lo) and (hi is None or e.ts <= hi))
        return total

    def get_payments_by_date(self, date: str) -> list[str]:
        check_ts(date + "T00:00:00")
        evs = sorted(e for e in self.by_day.get(date, []) if e.kind == PAYMENT)   # (ts, kind, id)
        return [e.id for e in evs]

    def get_balance_transactions(self) -> list[tuple[str, str, int, int]]:
        rows, net = [], 0
        for e in sorted(ev for evs in self.by_day.values() for ev in evs):       # ts, payment<refund, id
            net += e.amount
            rows.append(("payment" if e.kind == PAYMENT else "refund", e.id, e.amount, net))
        return rows


def run_commands(lines: list[str], max_part: int = 4) -> list[str]:
    led = PaymentLedger()
    out: list[str] = []
    for raw in lines:
        f = raw.split()
        if not f:
            continue
        verb, a = f[0].upper(), f[1:]
        try:
            if verb == "PAYMENT" and len(a) == 3:
                out.append("OK" if led.add_payment(a[0], int(a[1]), a[2]) else "REJECTED")
            elif verb == "REFUND" and len(a) == 4 and max_part >= 2:
                out.append("OK" if led.add_refund(a[0], a[1], int(a[2]), a[3]) else "REJECTED")
            elif verb == "REVENUE" and len(a) == 0:
                out.append(str(led.get_total_revenue()))
            elif verb == "REVENUE" and len(a) == 2 and max_part >= 3:
                out.append(str(led.get_total_revenue(a[0], a[1])))
            elif verb == "PAYMENTS" and len(a) == 1 and max_part >= 3:
                out.append(",".join(led.get_payments_by_date(a[0])) or "NONE")
            elif verb == "TRANSACTIONS" and len(a) == 0 and max_part >= 4:
                rows = led.get_balance_transactions()
                out.extend(f"{t},{i},{amt},{net}" for t, i, amt, net in rows) if rows else out.append("NONE")
            else:
                raise ValueError(verb)
        except ValueError:
            out.append("ERROR")
    return out


def part1(lines: list[str]) -> list[str]:
    return run_commands(lines, 1)


def part2(lines: list[str]) -> list[str]:
    return run_commands(lines, 2)


def part3(lines: list[str]) -> list[str]:
    return run_commands(lines, 3)


def part4(lines: list[str]) -> list[str]:
    return run_commands(lines, 4)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = part4(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
