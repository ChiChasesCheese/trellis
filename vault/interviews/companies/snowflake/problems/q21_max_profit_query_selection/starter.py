"""q21 Maximum Profit Query Selection -- YOUR implementation. Run tests against this file with
IMPL=starter.

n query types with durations[i]/revenues[i]. Budget k. Running type i floor(k/durations[i])
times earns floor(k/durations[i]) * revenues[i]. Part1: pick exactly one type. Part2
(reconstructed): pick up to two different types sharing the budget.
"""

from __future__ import annotations

import sys


def max_profit_single(durations: list[int], revenues: list[int], k: int) -> int:
    """Part1: best profit picking exactly one query type."""
    # TODO
    return 0


def max_profit_two_types(durations: list[int], revenues: list[int], k: int) -> int:
    """Part2: best profit picking up to two different query types sharing budget k."""
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    """'n k' / n durations / n revenues -> [best single-type profit]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> [best profit using at most two types]."""
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
