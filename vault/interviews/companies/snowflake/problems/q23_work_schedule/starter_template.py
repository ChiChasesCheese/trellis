"""q23 Work Schedule -- YOUR implementation. Run tests against this file with IMPL=starter.

pattern is exactly 7 characters, each a literal digit '0'-'8' or '?'. Replace each '?' with an
hour count in [0, dayHours] so the week sums to workHours.
"""

from __future__ import annotations

import sys

MOD = 1_000_000_007


def all_schedules(pattern: str, work_hours: int, day_hours: int) -> list[str]:
    """Part1: every valid 7-char schedule, sorted lexicographically."""
    # TODO
    return []


def count_schedules_mod(pattern: str, work_hours: int, day_hours: int) -> int:
    """Part2 (reconstructed): count only, mod 1e9+7. pattern length up to 1e3, workHours up to
    1e4."""
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    """'pattern' / 'workHours dayHours' -> all valid schedules, sorted lexicographically."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> [count mod 1e9+7]."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
