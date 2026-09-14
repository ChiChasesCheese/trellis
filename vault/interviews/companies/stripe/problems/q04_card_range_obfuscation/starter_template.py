"""q04 Card Range Obfuscation — YOUR implementation. Run: python drill.py test q04"""
from __future__ import annotations

import sys

OFFSET_SPAN = 10**10  # 10-digit offsets: 0000000000 .. 9999999999


def part1(lines: list[str]) -> list[str]:
    """lines = [BIN, N, 'start,end,brand' * N] (no PART line). Extend the outer ends only.
    Return ['start,end,brand', ...] with full zero-padded 16-digit numbers, sorted by (start, end, brand)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Part 1 + fill interior gaps by extending the lower (covering) interval upward."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Part 2 + nested intervals: only the covering interval is extended."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """Part 3 + merge touching/overlapping intervals of the same brand."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 4
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
