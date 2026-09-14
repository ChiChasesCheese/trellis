"""qA13 LC 2483 Minimum Penalty for a Shop — reference solution.

Part 1/4: one running pass — penalty(0) = weighted count of 'Y'; moving the close past hour j
subtracts w_j for a 'Y' and adds w_j for an 'N'; strict '<' keeps the earliest minimum.
Part 2: maximum-subarray via prefix sums (score +1 for 'Y', -1 for 'N'), earliest-min prefix.
Part 3: the classic "max sum of <= k disjoint subarrays" DP, O(n*k) time, O(n) memory.
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Window(NamedTuple):
    open: int      # first open hour
    close: int     # first closed hour (half-open window [open, close))
    penalty: int


def penalty(customers: str, closing_hour: int) -> int:
    """'N' before closing_hour + 'Y' at or after it."""
    return customers[:closing_hour].count("N") + customers[closing_hour:].count("Y")


def best_closing_time_weighted(customers: str, weights: list[int]) -> int:
    """Part 4: earliest closing hour minimising the weighted penalty."""
    cur = sum(w for c, w in zip(customers, weights) if c == "Y")  # closing at 0: every 'Y' is missed
    best, best_hour = cur, 0
    for j, (c, w) in enumerate(zip(customers, weights), start=1):
        cur += -w if c == "Y" else w  # hour j-1 is now open: a 'Y' is served, an 'N' is idle
        if cur < best:  # strict <: the earliest hour keeps the tie
            best, best_hour = cur, j
    return best_hour


def best_closing_time(customers: str) -> int:
    """Part 1 (LC signature): earliest closing hour with the minimum penalty; O(n)."""
    return best_closing_time_weighted(customers, [1] * len(customers))


def _scores(customers: str) -> list[int]:
    return [1 if c == "Y" else -1 for c in customers]


def best_open_close(customers: str) -> Window:
    """Part 2: best half-open window [open, close); ties -> smallest open, then smallest close."""
    total_y = customers.count("Y")
    prefix = 0
    min_prefix, min_at = 0, 0  # earliest index attaining the minimum prefix (strict < below)
    best = (0, 0, 0)  # (score, open, close): empty window at [0, 0)
    for close, s in enumerate(_scores(customers), start=1):
        prefix += s
        score = prefix - min_prefix  # best window ending at `close` opens at the earliest min prefix
        if score > best[0] or (score == best[0] and (min_at, close) < (best[1], best[2])):
            best = (score, min_at, close)
        if prefix < min_prefix:
            min_prefix, min_at = prefix, close
    score, open_, close = best
    return Window(open_, close, total_y - score)


def min_penalty_k_windows(customers: str, k: int) -> int:
    """Part 3: minimum penalty with at most k disjoint open windows; O(n*k)."""
    s = _scores(customers)
    n = len(s)
    neg_inf = float("-inf")
    f_prev = [0] * (n + 1)  # f_prev[i]: best total with <= j-1 windows inside hours [0, i)
    for _ in range(k):
        f = [0] * (n + 1)
        g = neg_inf  # best total with the j-th window ending exactly at hour i-1
        for i in range(1, n + 1):
            g = max(g, f_prev[i - 1]) + s[i - 1]  # extend the open window, or open a new one at i-1
            f[i] = max(f[i - 1], g)
        f_prev = f
    return customers.count("Y") - f_prev[n]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    customers = lines[1].replace(" ", "") if len(lines) > 1 else ""
    if part == 1:
        out = str(best_closing_time(customers))
    elif part == 2:
        w = best_open_close(customers)
        out = f"{w.open} {w.close} {w.penalty}"
    elif part == 3:
        k = int(lines[2].split()[1])
        out = str(min_penalty_k_windows(customers, k))
    else:
        weights = [int(x) for x in lines[2].split()]
        out = str(best_closing_time_weighted(customers, weights))
    stdout.write(out + "\n")


if __name__ == "__main__":
    main()
