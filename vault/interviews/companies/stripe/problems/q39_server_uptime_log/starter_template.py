"""q39 Server Uptime Log — YOUR implementation. Run: python drill.py test q39

'1' = crashed (down), '0' = up. Part 1 penalty -> Part 2 best remove_at (smallest on tie)
-> Part 3 BEGIN/END aggregate logs -> Part 4 at most k off-network intervals (DP).
"""
from __future__ import annotations

import sys


def parse_log(log: str) -> list[str]:
    """Whitespace-separated tokens; a token like '0010' counts as several hours."""
    return [ch for tok in log.split() for ch in tok]


def compute_penalty(log: str, remove_at: int) -> int:
    # TODO
    return 0


def find_best_removal_time(log: str) -> int:
    # TODO (O(n), smallest remove_at on a tie)
    return 0


def get_best_removal_times(aggregate_log: str) -> list[int]:
    # TODO
    return []


def min_penalty_k(log: str, k: int) -> int:
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    return [str(compute_penalty(log, int(t))) for log, _, t in (ln.rpartition("|") for ln in lines)]


def part2(lines: list[str]) -> list[str]:
    return [str(find_best_removal_time(ln)) for ln in lines]


def part3(lines: list[str]) -> list[str]:
    return [str(t) for t in get_best_removal_times(" ".join(lines))]


def part4(lines: list[str]) -> list[str]:
    return [str(min_penalty_k(log, int(k))) for log, _, k in (ln.rpartition("|") for ln in lines)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
