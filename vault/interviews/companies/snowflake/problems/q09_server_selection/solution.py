"""q09 Server Selection with switching cost — reference solution.

**(reconstructed)** — see problem.md. There are `m` servers and `n` time slots
processed in order 0..n-1. `cost[j][i]` is the cost of having server j active
during slot i. `switch_cost` is a fixed extra cost incurred whenever the active
server changes between consecutive slots (slot 0 is always free of switch
penalty). Exactly one server is active per slot; minimize total cost.

part1 is the "natural but slow" O(m^2 * n) DP: for each slot and each server,
scan every other server's total cost at the previous slot to find the best
transition. part2 is the O(m*n) version: track only the best and second-best
total cost among all servers at the previous slot (plus which server achieved
the best) so each cell's transition is O(1) instead of O(m).

Tie-break (documented in problem.md): when a "stay" (no switch) transition ties
with the best "switch" transition, PREFER STAYING. If there is still a tie with
no clear notion of "previous" to prefer (e.g. picking among multiple servers
tied at slot 0, or the final minimum-cost server at slot n-1), prefer the
LOWEST server index.
"""
from __future__ import annotations

import sys


def part1(m: int, n: int, cost: list[list[int]], switch_cost: int) -> int:
    """O(m^2 * n): for each slot/server, scan all other servers at the previous
    slot. Deliberately not optimized -- this is the baseline part2 must beat."""
    if n == 0:
        return 0
    dp = [cost[j][0] for j in range(m)]
    for i in range(1, n):
        ndp = [0] * m
        for j in range(m):
            best = min(dp[k] + (0 if k == j else switch_cost) for k in range(m))
            ndp[j] = cost[j][i] + best
        dp = ndp
    return min(dp)


def part2(m: int, n: int, cost: list[list[int]], switch_cost: int) -> tuple[int, list[int]]:
    """O(m*n): track best/second-best previous-slot total cost (and the server
    achieving the best) so each cell is O(1). Returns (min_total_cost, assignment)
    where assignment[i] is the server active at slot i achieving the minimum,
    using the tie-break documented above."""
    if n == 0:
        return 0, []

    dp = [cost[j][0] for j in range(m)]
    # parents[i - 1][j] = predecessor server chosen for server j at slot i
    parents: list[list[int]] = []

    for i in range(1, n):
        best1_val = best2_val = float("inf")
        best1_server = best2_server = -1
        for k in range(m):
            v = dp[k]
            if v < best1_val:
                best2_val, best2_server = best1_val, best1_server
                best1_val, best1_server = v, k
            elif v < best2_val:
                best2_val, best2_server = v, k

        ndp = [0] * m
        preds = [0] * m
        for j in range(m):
            if best1_server != j:
                switch_val, switch_pred = best1_val + switch_cost, best1_server
            else:
                switch_val, switch_pred = best2_val + switch_cost, best2_server
            stay_val = dp[j]
            if stay_val <= switch_val:  # tie-break: prefer NOT switching
                ndp[j] = cost[j][i] + stay_val
                preds[j] = j
            else:
                ndp[j] = cost[j][i] + switch_val
                preds[j] = switch_pred
        dp = ndp
        parents.append(preds)

    total = min(dp)
    # tie-break: lowest server index among ties for the final minimum
    last = min(range(m), key=lambda k: dp[k])
    assignment = [last]
    for preds in reversed(parents):
        last = preds[last]
        assignment.append(last)
    assignment.reverse()
    return total, assignment


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format:
    PART 1|2
    m n switch_cost
    cost[0][0] cost[0][1] ... cost[0][n-1]
    ...
    cost[m-1][0] ... cost[m-1][n-1]

    PART 1 prints the total cost on one line.
    PART 2 prints the total cost on one line, then the assignment (space
    separated server indices, one per slot) on a second line (blank if n == 0).
    """
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip() != ""]
    idx = 0
    header = lines[idx].split()
    idx += 1
    part = int(header[1]) if header and header[0].upper() == "PART" else 2
    m, n, switch_cost = (int(x) for x in lines[idx].split())
    idx += 1
    cost: list[list[int]] = []
    for _ in range(m):
        row = [int(x) for x in lines[idx].split()] if n > 0 else []
        idx += 1 if n > 0 else 0
        cost.append(row)

    if part == 1:
        stdout.write(f"{part1(m, n, cost, switch_cost)}\n")
    else:
        total, assignment = part2(m, n, cost, switch_cost)
        stdout.write(f"{total}\n")
        stdout.write(" ".join(str(s) for s in assignment) + "\n")


if __name__ == "__main__":
    main()
