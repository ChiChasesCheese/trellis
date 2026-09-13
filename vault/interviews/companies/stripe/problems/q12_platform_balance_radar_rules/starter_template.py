"""q12 Platform Balance + Radar Rules — YOUR implementation. Run: python drill.py test q12"""
from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """'API: amount=..&merchant=..' updates, 'BAL: merchant=..' prints the integer balance."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Part 1 + 'RULE: field==value' / 'field != value' block rules applied to later API lines."""
    # TODO
    return []


def should_accept_transaction(transaction: dict[str, str], rules: list[str]) -> bool:
    """Radar-style rules 'ACCEPT if (...)' / 'BLOCK if (...)'; first match wins; no match -> True."""
    # TODO
    return True


def part3(lines: list[str]) -> list[str]:
    """Part 1 lines + 'RULE: <radar rule>' + 'TXN: k=v&..' -> prints ACCEPT / BLOCK per TXN."""
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
