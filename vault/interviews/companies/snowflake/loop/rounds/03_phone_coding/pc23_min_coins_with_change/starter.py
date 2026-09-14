"""pc23 Min Coins with Change -- YOUR implementation. Run the tests against this file with
IMPL=starter.

You may pay any P >= n (coins from a fixed set, unlimited supply) and receive exact change
C = P - n from the same set. Minimise the total number of coins that change hands.
"""

from __future__ import annotations

import sys

CANONICAL_DENOMINATIONS: tuple[int, ...] = (1, 5, 10, 50, 100, 200)


def min_coins(x: int, denominations: tuple[int, ...] = CANONICAL_DENOMINATIONS) -> int:
    """Minimum coins to make exactly x >= 0 from `denominations`. ValueError if impossible or
    x < 0. Must be a DP over amounts, not greedy (Part 2 uses non-canonical sets)."""
    # TODO
    return 0


def min_total_coins_fixed(n: int) -> int:
    """Part1: canonical denominations, n up to 1e4. Search P in [n, n + max(denoms)]."""
    # TODO
    return 0


def min_total_coins_custom(n: int, denominations: list[int]) -> int:
    """Part2: arbitrary denominations (reconstructed). Search P in [n, n + 2*max(denoms)]."""
    # TODO
    return 0


def min_total_coins_breakdown(
    n: int, denominations: tuple[int, ...] | list[int] = CANONICAL_DENOMINATIONS
) -> tuple[list[int], list[int]]:
    """Part3 (reconstructed): return ONE optimal (paid_coins, change_coins) breakdown."""
    # TODO
    return [], []


def is_valid_optimal_breakdown(
    n: int, paid: list[int], change: list[int], denominations: tuple[int, ...] | list[int] = CANONICAL_DENOMINATIONS
) -> bool:
    """Checker: valid denominations, correct net amount, and optimal total coin count."""
    # TODO
    return False


def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def part1(lines: list[str]) -> list[str]:
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
