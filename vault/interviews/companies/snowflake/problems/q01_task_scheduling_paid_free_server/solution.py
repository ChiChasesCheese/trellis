"""q01 Task Scheduling: paid vs free server -- reference solution.

Model (see problem.md for the full derivation): tasks arrive one per time unit, in order
0..n-1. The paid server has a `free_at` counter (initially 0). Task i is FORCED onto the
paid server if `free_at <= i` (paid server idle when task i arrives): pay cost[i], and
`free_at` becomes `i + time[i]`. Otherwise (`free_at > i`, paid server still busy with a
backlog) we may choose:
  (a) run task i on the free server: cost += 0, free_at unchanged; or
  (b) queue task i on the paid server: cost += cost[i], free_at += time[i].
Goal: minimum total cost to process all n tasks. All math is exact integers.

part1: a direct memoized recursion over (task index, free_at). Correct and simple, but the
number of distinct (i, free_at) pairs can grow without bound for large/adversarial inputs, so
this is a reference/cross-check implementation, not the n=10^5-ready one.

part2: a DP over the *frontier* of reachable (free_at, min_cost) states, pruned each step to
its Pareto-optimal subset. See the "Pareto direction" note below -- this is the one place
where this file's algorithm differs from the naive first guess, and the difference matters
for correctness, not just speed.
"""
from __future__ import annotations

import sys


def part1(cost: list[int], time: list[int]) -> int:
    """Naive/clear reference: memoized recursion over (task index, paid-server free_at).

    Not intended for n=10^5 -- the state space is only *empirically* small for small n.
    Used to cross-check part2 in tests.
    """
    n = len(cost)
    memo: dict[tuple[int, int], int] = {}

    def rec(i: int, free_at: int) -> int:
        if i == n:
            return 0
        key = (i, free_at)
        cached = memo.get(key)
        if cached is not None:
            return cached
        if free_at <= i:
            # forced onto the paid server
            res = cost[i] + rec(i + 1, i + time[i])
        else:
            # choice: free server now, or queue on the paid server
            skip = rec(i + 1, free_at)
            queue = cost[i] + rec(i + 1, free_at + time[i])
            res = skip if skip < queue else queue
        memo[key] = res
        return res

    return rec(0, 0)


def part2(cost: list[int], time: list[int]) -> int:
    """n<=1e5-ready: DP over the Pareto frontier of reachable (free_at, cost) states.

    Frontier invariant: stored as {free_at: min_cost_to_reach_it}. At each step we split the
    frontier into "forced" states (free_at <= i, all collapse into ONE new state since the
    forced transition discards the exact incoming free_at) and "busy" states (free_at > i,
    each spawns two candidate successors: skip-for-free, or pay-and-queue).

    Pareto direction (the part the naive "smaller free_at is better" intuition gets backwards):
    a state with a LARGER free_at and equal-or-lower cost weakly dominates one with a SMALLER
    free_at and equal-or-higher cost -- being busy longer only ever gives you MORE options later
    (you can always choose to pay and end up at least as busy as the smaller-free_at state would
    have been forced to), whereas an idle (small free_at) paid server can be forced into an
    unavoidable payment a busy one could have dodged by choosing the free server. So after
    merging, keep the frontier sorted by free_at *descending* and drop any state whose cost is
    not strictly less than the best cost seen so far among all larger-or-equal free_at states.
    """
    n = len(cost)
    frontier: dict[int, int] = {0: 0}
    for i in range(n):
        forced_min = None
        busy: list[tuple[int, int]] = []
        for free_at, c in frontier.items():
            if free_at <= i:
                if forced_min is None or c < forced_min:
                    forced_min = c
            else:
                busy.append((free_at, c))

        new_frontier: dict[int, int] = {}
        ci, ti = cost[i], time[i]
        if forced_min is not None:
            fa, c = i + ti, forced_min + ci
            if fa not in new_frontier or c < new_frontier[fa]:
                new_frontier[fa] = c
        for free_at, c in busy:
            if free_at not in new_frontier or c < new_frontier[free_at]:
                new_frontier[free_at] = c
            fa2, c2 = free_at + ti, c + ci
            if fa2 not in new_frontier or c2 < new_frontier[fa2]:
                new_frontier[fa2] = c2

        # Pareto-prune: sort by free_at descending, keep strictly decreasing cost.
        items = sorted(new_frontier.items(), key=lambda kv: -kv[0])
        pruned: dict[int, int] = {}
        best = None
        for fa, c in items:
            if best is None or c < best:
                pruned[fa] = c
                best = c
        frontier = pruned

    return min(frontier.values()) if frontier else 0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format:
        PART <1|2>
        n
        cost[0] cost[1] ... cost[n-1]      (whitespace-separated; omitted/blank if n == 0)
        time[0] time[1] ... time[n-1]      (whitespace-separated; omitted/blank if n == 0)
    stdout: a single line, the minimum total cost.
    """
    lines = stdin.read().splitlines()
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    part_line = lines[idx].strip() if idx < len(lines) else "PART 2"
    idx += 1
    parts = part_line.split()
    part_num = int(parts[1]) if len(parts) > 1 else 2

    n = 0
    while idx < len(lines):
        stripped = lines[idx].strip()
        idx += 1
        if stripped:
            n = int(stripped)
            break

    cost: list[int] = []
    time_: list[int] = []
    if n > 0:
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        cost = [int(x) for x in lines[idx].split()] if idx < len(lines) else []
        idx += 1
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        time_ = [int(x) for x in lines[idx].split()] if idx < len(lines) else []
        idx += 1

    fn = part1 if part_num == 1 else part2
    stdout.write(f"{fn(cost, time_)}\n")


if __name__ == "__main__":
    main()
