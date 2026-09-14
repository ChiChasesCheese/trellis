"""q21 Maximum Profit Query Selection -- reference solution.

n query types, durations[i] and revenues[i]. You have a time budget k. Running query type i
costs durations[i] time per run; you may run it floor(k / durations[i]) times back to back.
Pick the single best type to maximise profit = floor(k / durations[i]) * revenues[i].

Part1: exactly one type (the stated problem). O(n).
Part2 (reconstructed): you may split the SAME budget k between up to two DIFFERENT types --
run type i some number of times and type j some (possibly zero) number of times, as long as
their total time does not exceed k; maximise the combined revenue. This is an unbounded
knapsack over exactly two item "kinds" (any nonnegative combination of the two), so a mix can
beat either type alone (classic example: durations=[3,4], revenues=[4,5], k=7 -> single best is
2x duration-3 = 8, but 1x each = 4+5 = 9). Kept deliberately small (n, k bounded) so an
O(n^2 * k) unbounded-knapsack-per-pair DP is brute-force-checkable and fast.
"""

from __future__ import annotations

import sys


def _validate(durations: list[int], revenues: list[int], k: int) -> None:
    if not durations:
        raise ValueError("durations must be non-empty")
    if len(durations) != len(revenues):
        raise ValueError("durations and revenues must be the same length")
    if k < 0:
        raise ValueError("k must be >= 0")
    for d in durations:
        if d < 1:
            raise ValueError(f"duration must be >= 1: {d}")
    for r in revenues:
        if r < 0:
            raise ValueError(f"revenue must be >= 0: {r}")


# --------------------------------------------------------------------------- Part 1
def max_profit_single(durations: list[int], revenues: list[int], k: int) -> int:
    """Best profit picking exactly one query type. O(n)."""
    _validate(durations, revenues, k)
    return max((k // d) * r for d, r in zip(durations, revenues))


# --------------------------------------------------------------------------- Part 2
def _best_two_item_knapsack(d1: int, r1: int, d2: int, r2: int, k: int) -> int:
    """Max profit spending <= k budget on any nonnegative combo of two items (unbounded
    knapsack with exactly these two kinds). O(k)."""
    dp = [0] * (k + 1)
    for d, r in ((d1, r1), (d2, r2)):
        for c in range(d, k + 1):
            v = dp[c - d] + r
            if v > dp[c]:
                dp[c] = v
    return dp[k]


def max_profit_two_types(durations: list[int], revenues: list[int], k: int) -> int:
    """Best profit picking up to two DIFFERENT query types sharing the same budget k.
    Deliberately small: intended for n <= 30, k <= 2000. O(n^2 * k)."""
    _validate(durations, revenues, k)
    n = len(durations)
    best = max_profit_single(durations, revenues, k)
    for i in range(n):
        for j in range(i + 1, n):
            combo = _best_two_item_knapsack(durations[i], revenues[i], durations[j], revenues[j], k)
            if combo > best:
                best = combo
    return best


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[list[int], list[int], int]:
    n, k = map(int, lines[0].split())
    durations = list(map(int, lines[1].split())) if n else []
    revenues = list(map(int, lines[2].split())) if n else []
    if len(durations) != n or len(revenues) != n:
        raise ValueError(f"expected {n} durations and revenues")
    return durations, revenues, k


def part1(lines: list[str]) -> list[str]:
    """'n k' / n durations / n revenues -> [best single-type profit]."""
    durations, revenues, k = _read(lines)
    return [str(max_profit_single(durations, revenues, k))]


def part2(lines: list[str]) -> list[str]:
    """same input -> [best profit using at most two types]."""
    durations, revenues, k = _read(lines)
    return [str(max_profit_two_types(durations, revenues, k))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
