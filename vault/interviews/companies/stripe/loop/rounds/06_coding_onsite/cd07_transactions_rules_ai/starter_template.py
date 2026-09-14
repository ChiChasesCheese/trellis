"""cd07 Transactions + rules (AI Programming Exercise) — YOUR implementation.

Run: python3 loop/mock.py test cd07
"""

from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """lines: RULES section (ALLOW|BLOCK if field == value) then TRANSACTIONS section
    (id,amount,currency,country,card_brand,merchant), no leading 'PART 1' line.
    Return ['id ALLOW (rule k)' | 'id BLOCK (rule k)' | 'id ALLOW', ...] in input order."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Adds !=, >, <, >=, <= and `field in [v1, v2, ...]` to the single condition per rule."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Adds AND/OR/NOT and parentheses (not > and > or). Invalid rules emit
    'ERROR line k: <reason>' (k = 1-indexed line within RULES) and are skipped."""
    # TODO
    return []


PARTS = {1: part1, 2: part2, 3: part3}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw_lines = stdin.read().splitlines()
    lines = [ln for ln in raw_lines if ln.strip()]
    out: list[str] = []
    if lines and lines[0].strip().upper().startswith("PART"):
        part = int(lines[0].split()[1])
        out = PARTS[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
