"""q16 Chargeback Parsing — YOUR implementation. Run: python drill.py test q16"""
from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """'network,txn_id,amount,currency,reason,date' -> '[NETWORK] txn_id: $x.xx CUR - reason (date)'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Skip corrupted rows; survivors in input order, then 'SKIPPED: n'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Part 2 + drop every row of a (network, txn_id) group that contains a 'withdrawn' row."""
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
