"""q16 Chargeback Parsing — reference solution.

parse_row() returns a Dispute or None (corrupted).  Money is the integer minor-unit amount from the
file; formatting decides decimals per currency (zero-decimal: jpy/krw).  Part 3 groups valid rows by
(network, transaction_id) and drops every group that contains a 'withdrawn' row, regardless of order.
"""
from __future__ import annotations

import sys
from datetime import datetime
from typing import NamedTuple

NETWORKS = {"visa", "mastercard", "amex", "discover"}
SYMBOLS = {"usd": "$", "eur": "€", "gbp": "£", "jpy": "¥", "krw": "₩"}
ZERO_DECIMAL = {"jpy", "krw"}


class Dispute(NamedTuple):
    network: str
    txn_id: str
    amount: int  # minor units
    currency: str
    reason: str
    date: str    # normalized YYYY-MM-DD


def parse_row(line: str) -> Dispute | None:
    """None when the row is corrupted (field count, amount, date, network, empty fields)."""
    f = [p.strip() for p in line.split(",")]
    if len(f) != 6:
        return None
    network, txn_id, amount_s, currency, reason, date_s = f
    network, currency = network.lower(), currency.lower()
    if network not in NETWORKS or not txn_id or not currency or not reason:
        return None
    try:
        amount = int(amount_s)  # '25.00', 'abc', '' all fail
        date = datetime.strptime(date_s, "%Y-%m-%d").strftime("%Y-%m-%d")  # 2024-02-30 fails
    except ValueError:
        return None
    if amount < 0:
        return None
    return Dispute(network, txn_id, amount, currency, reason, date)


def fmt_money(amount: int, currency: str) -> str:
    sym = SYMBOLS.get(currency, "")
    if currency in ZERO_DECIMAL:
        return f"{sym}{amount}"
    return f"{sym}{amount // 100}.{amount % 100:02d}"


def render(d: Dispute) -> str:
    return f"[{d.network.upper()}] {d.txn_id}: {fmt_money(d.amount, d.currency)} {d.currency.upper()} - {d.reason} ({d.date})"


def parse_all(lines: list[str]) -> tuple[list[Dispute], int]:
    """-> (valid disputes in input order, corrupted count)."""
    valid, skipped = [], 0
    for raw in lines:
        if not raw.strip():
            continue
        d = parse_row(raw)
        if d is None:
            skipped += 1
        else:
            valid.append(d)
    return valid, skipped


def part1(lines: list[str]) -> list[str]:
    valid, _ = parse_all(lines)
    return [render(d) for d in valid]


def part2(lines: list[str]) -> list[str]:
    valid, skipped = parse_all(lines)
    return [render(d) for d in valid] + [f"SKIPPED: {skipped}"]


def part3(lines: list[str]) -> list[str]:
    valid, skipped = parse_all(lines)
    # any 'withdrawn' row cancels its whole (network, txn_id) group, whichever order the rows arrived
    withdrawn = {(d.network, d.txn_id) for d in valid if d.reason == "withdrawn"}
    return [render(d) for d in valid if (d.network, d.txn_id) not in withdrawn] + [f"SKIPPED: {skipped}"]


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
