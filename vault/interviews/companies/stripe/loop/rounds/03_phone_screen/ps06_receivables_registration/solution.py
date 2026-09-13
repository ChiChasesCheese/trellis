"""ps06 Receivables registration — reference solution.

Pipeline for both parts: data lines -> parse each row into a `Row` -> aggregate cents by
(merchant_id, card_type, payout_date) -> render sorted lines. Part 1 trusts the rows; Part 2 swaps
in a checked parser (skip + count malformed rows) and normalizes the payout_date (weekend -> next
Monday) *before* the row reaches the aggregation key. Money is integer cents everywhere in
between; the only string<->cents conversions are at the parse and format boundaries.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from typing import Iterable, NamedTuple

# ------------------------------------------------------------------ rules (constants, one place)
FIELD_COUNT = 5  # customer_id,merchant_id,payout_date,card_type,amount
AMOUNT_RE = re.compile(r"^-?\d+\.\d{2}$")  # exactly two decimal digits, optional leading minus
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # shape only; calendar validity checked separately
SATURDAY, SUNDAY = 5, 6  # date.weekday(): Mon=0 .. Sun=6
ROLL_FORWARD_DAYS = {SATURDAY: 2, SUNDAY: 1}  # weekend payout -> following Monday


class Row(NamedTuple):
    merchant_id: str
    card_type: str
    payout_date: str  # YYYY-MM-DD
    cents: int


GroupKey = tuple[str, str, str]  # (merchant_id, card_type, payout_date)


# ------------------------------------------------------------------ parsing
def _data_lines(lines: list[str]) -> list[str]:
    """Drop the CSV header (lines[0]) and blank lines; strip the rest."""
    return [ln.strip() for ln in lines[1:] if ln.strip()]


def _fields(raw: str) -> list[str]:
    return [p.strip() for p in raw.split(",")]


def _amount_to_cents(amount: str) -> int:
    """'150.00' -> 15000 ; '-15.50' -> -1550. Caller guarantees AMOUNT_RE already matched."""
    sign = -1 if amount.startswith("-") else 1
    whole, frac = amount.lstrip("-").split(".")
    return sign * (int(whole) * 100 + int(frac))


def _is_valid_date(text: str) -> bool:
    """YYYY-MM-DD shape *and* a real calendar date (2026-02-30 is not)."""
    if not DATE_RE.fullmatch(text):
        return False
    try:
        date.fromisoformat(text)
    except ValueError:
        return False
    return True


def _parse_row_trusted(raw: str) -> Row:
    """Part 1: rows are promised well-formed, so no validation."""
    _customer, merchant, payout_date, card_type, amount = _fields(raw)
    return Row(merchant, card_type, payout_date, _amount_to_cents(amount))


def _parse_row_checked(raw: str) -> Row | None:
    """Part 2: None for a malformed row (field count, amount format, date shape/validity)."""
    fields = _fields(raw)
    if len(fields) != FIELD_COUNT:
        return None
    _customer, merchant, payout_date, card_type, amount = fields
    if not AMOUNT_RE.fullmatch(amount) or not _is_valid_date(payout_date):
        return None
    return Row(merchant, card_type, payout_date, _amount_to_cents(amount))


def _roll_weekend(row: Row) -> Row:
    """Saturday -> +2 days, Sunday -> +1 day, weekday unchanged."""
    d = date.fromisoformat(row.payout_date)
    d += timedelta(days=ROLL_FORWARD_DAYS.get(d.weekday(), 0))
    return row._replace(payout_date=d.isoformat())


# ------------------------------------------------------------------ core + formatting
def _aggregate(rows: Iterable[Row]) -> dict[GroupKey, int]:
    """Sum cents per (merchant_id, card_type, payout_date); duplicate keys merge, never overwrite."""
    totals: dict[GroupKey, int] = defaultdict(int)
    for row in rows:
        totals[(row.merchant_id, row.card_type, row.payout_date)] += row.cents
    return totals


def _fmt_cents(cents: int) -> str:
    """Two-decimal string, no currency sign, '-' prefix when negative (-5 -> '-0.05')."""
    sign = "-" if cents < 0 else ""
    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"


def _render(totals: dict[GroupKey, int]) -> list[str]:
    """'merchant_id,card_type,payout_date,total' sorted by merchant_id, payout_date, card_type."""
    ordered = sorted(totals.items(), key=lambda kv: (kv[0][0], kv[0][2], kv[0][1]))
    return [
        f"{merchant},{card_type},{payout_date},{_fmt_cents(cents)}"
        for (merchant, card_type, payout_date), cents in ordered
    ]


# ------------------------------------------------------------------ parts
def part1(lines: list[str]) -> list[str]:
    """Happy path: well-formed rows, group + sum, render."""
    rows = [_parse_row_trusted(raw) for raw in _data_lines(lines)]
    return _render(_aggregate(rows))


def part2(lines: list[str]) -> list[str]:
    """Skip + count malformed rows, roll weekend dates before keying, append 'SKIPPED n'."""
    rows: list[Row] = []
    skipped = 0
    for raw in _data_lines(lines):
        row = _parse_row_checked(raw)
        if row is None:
            skipped += 1
        else:
            rows.append(_roll_weekend(row))  # normalize BEFORE the date becomes part of the key
    return _render(_aggregate(rows)) + [f"SKIPPED {skipped}"]


# ------------------------------------------------------------------ I/O
PARTS = {"PART 1": part1, "PART 2": part2}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    if header not in PARTS:
        raise ValueError(f"unknown header: {header!r}")
    out = PARTS[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
