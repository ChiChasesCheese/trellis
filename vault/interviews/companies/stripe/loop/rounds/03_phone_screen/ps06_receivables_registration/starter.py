"""ps06 Receivables registration — YOUR implementation."""

from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """lines[0]: header 'customer_id,merchant_id,payout_date,card_type,amount'. lines[1:]:
    well-formed data rows (no validation needed). Group by (merchant_id, card_type, payout_date),
    sum amount in integer cents, return 'merchant_id,card_type,payout_date,total' sorted by
    merchant_id, payout_date, card_type."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same shape as part1, but rows may be malformed. Skip + count bad rows (wrong field count,
    bad amount, bad date), allow negative amounts, roll a weekend payout_date forward to the
    following Monday before aggregating, and append a trailing 'SKIPPED n' line."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    parts = {"PART 1": part1, "PART 2": part2}
    if header not in parts:
        raise ValueError(f"unknown header: {header!r}")
    out = parts[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
