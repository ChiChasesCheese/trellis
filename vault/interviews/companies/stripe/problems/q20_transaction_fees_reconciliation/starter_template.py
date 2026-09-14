"""q20 Transaction Fees / Receivables / Reconciliation — YOUR implementation. Run: python drill.py test q20"""
from __future__ import annotations

import csv
import io
import sys
from collections import defaultdict
from decimal import Decimal

DISPUTE_FEE = 1500  # cents


def to_cents(s: str) -> int:
    """'1000' -> 1000 ; '10.00' -> 1000 (exact, Decimal)."""
    # TODO
    return 0


def parse_csv(lines: list[str]) -> list[dict]:
    """Header + rows -> list of dicts keyed by column name (values stripped)."""
    # TODO
    return []


def parse_rates(lines: list[str]) -> dict:
    """'provider,country,rate_bps,fixed_cents' lines -> {(provider, country): (bps, fixed)}."""
    # TODO
    return {}


def fee_cents(row: dict, rates: dict | None = None) -> int:
    """Parts 1-2: fee for one row (see problem.md table; half-up default, floor for table rates)."""
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    """'<id>,<fee>' per row."""
    # TODO
    return []


def part2(rate_lines: list[str], csv_lines: list[str]) -> list[str]:
    # TODO
    return []


def receivables(rows: list[dict], rates: dict | None = None) -> list[str]:
    """Part 3: header + 'merchant_id,card_type,payout_date,net' sorted by the three keys."""
    # TODO
    return ["merchant_id,card_type,payout_date,net"]


def part3(lines: list[str]) -> list[str]:
    # TODO
    return receivables(parse_csv(lines))


def reconcile(system: list[str], gateway: list[str], include_matches: bool = False) -> list[str]:
    """Part 4: MISSING_IN_GATEWAY / MISSING_IN_SYSTEM / AMOUNT_MISMATCH id sys gw, sorted by id."""
    # TODO
    return []


def part4(system: list[str], gateway: list[str]) -> list[str]:
    return reconcile(system, gateway)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out: list[str] = []
    # TODO: split sections (RATES/TRANSACTIONS, SYSTEM/GATEWAY) and dispatch
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
