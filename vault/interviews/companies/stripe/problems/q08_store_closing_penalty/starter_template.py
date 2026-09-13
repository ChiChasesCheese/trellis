"""q08 Store Closing-Time Penalty — YOUR implementation. Run: python drill.py test q08"""
from __future__ import annotations

import sys


def parse_log(log: str) -> list[str]:
    """'Y Y N Y' or 'YYNY' -> ['Y','Y','N','Y']."""
    # TODO
    return []


def compute_penalty(log: str, closing_time: int) -> int:
    """N while open (hours 1..closing_time) + Y while closed (closing_time+1..n)."""
    # TODO
    return 0


def find_best_closing_time(log: str) -> int:
    """Closing time with the minimum penalty; smallest on tie. O(n)."""
    # TODO
    return 0


def get_best_closing_times(aggregate_log: str) -> list[int]:
    """Extract valid BEGIN ... END logs (restart on nested BEGIN, ignore stray END / garbage /
    invalid tokens) and return the best closing time of each, in order."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """Each line 'log|closing_time' -> str(penalty)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Each line a log -> str(best closing time)."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """All lines form one aggregate log -> one str per valid log."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    lines = [ln.strip() for ln in raw if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
