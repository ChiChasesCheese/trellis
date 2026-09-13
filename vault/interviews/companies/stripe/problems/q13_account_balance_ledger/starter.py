"""q13 Account Balance Ledger — YOUR implementation. Run: python drill.py test q13"""
from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """'txn,user,credit|debit,amount' -> ['user x.xx', ...] non-zero balances sorted by user (may be negative)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Reject debits that would go below 0. Balances, then 'REJECTED: id1,id2' or 'REJECTED: NONE'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """+ 'txn,from,transfer,to,amount' and the lending 'platform' account. Balances, REJECTED, MAX_RESERVE."""
    # TODO
    return []


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
