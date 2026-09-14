"""q10 Payment Intent Commands — YOUR implementation. Run: python drill.py test q10"""
from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """INIT / CREATE / ATTEMPT / SUCCEED. Return ['merchant balance', ...] sorted by merchant."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Part 1 + UPDATE (only in REQUIRES_ACTION, negative ignored)."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Part 2 + FAIL (PROCESSING -> REQUIRES_ACTION) + REFUND (COMPLETED, once)."""
    # TODO
    return []


def part4(lines: list[str], immediate_credit: bool = True) -> list[str]:
    """Timestamped lines, INIT with optional refund_limit; CREATE credits immediately."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
