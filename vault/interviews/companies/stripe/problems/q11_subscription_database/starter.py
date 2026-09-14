"""q11 Subscription Database — YOUR implementation. Run: python drill.py test q11"""
from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """start / end / check (no durations). Return ['active'|'inactive', ...] one per check, input order."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """start may carry a duration d: active while t <= start + d. A new start REPLACES the old one."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Like part2 but a start on a still-active finite subscription EXTENDS it: expiry += d."""
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
