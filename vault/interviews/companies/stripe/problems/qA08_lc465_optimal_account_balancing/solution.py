"""qA08 LC 465 Optimal Account Balancing — reference solution.

Net every party, drop the zeros, then an exact search over the <= 12 non-zero nets: the first
unsettled party is settled completely against one later party of the opposite sign per branch.
Prunings: duplicate values at a level, stop after an exact cancel, branch-and-bound on the best count.
The bitmask DP (n - max #zero-sum subsets) is the cross-check the interviewer may ask for.
"""
from __future__ import annotations

import sys
from typing import NamedTuple

PLATFORM = -1  # virtual party that absorbs written-off balances (Part 3)


class Transfer(NamedTuple):
    frm: int
    to: int
    amount: int


class Settlement(NamedTuple):
    transfers: list[Transfer]
    written_off: list[tuple[int, int]]  # (party, net), ascending party


def net_balances(transactions: list[list[int]]) -> dict[int, int]:
    """Credit per party = given - received (positive: is owed money, negative: owes); zeros dropped,
    ascending party id. `[from, to, amount]` means `from` handed money to `to`, so `to` owes it back."""
    net: dict[int, int] = {}
    for frm, to, amount in transactions:
        net[frm] = net.get(frm, 0) + amount
        net[to] = net.get(to, 0) - amount
    return {p: v for p, v in sorted(net.items()) if v != 0}


def _search(nets: dict[int, int]) -> list[Transfer]:
    """Exact minimum transfer list over the non-zero nets (ascending party order, first-found)."""
    parties = list(nets)
    bal = [nets[p] for p in parties]
    n = len(bal)
    best: list[Transfer] = [Transfer(0, 0, 0)] * n  # n-1 transfers always suffice, so n is a safe cap
    path: list[Transfer] = []

    def dfs(i: int) -> None:
        nonlocal best
        while i < n and bal[i] == 0:
            i += 1
        if i == n:
            if len(path) < len(best):  # strict <: the first optimal list found is kept
                best = path[:]
            return
        if len(path) + 1 >= len(best):  # branch-and-bound: cannot beat the best any more
            return
        tried: set[int] = set()
        for j in range(i + 1, n):
            if bal[i] * bal[j] >= 0 or bal[j] in tried:  # same sign / duplicate value -> skip
                continue
            tried.add(bal[j])
            amount = abs(bal[i])
            # money flows from the negative credit (owes) to the positive credit (is owed)
            path.append(Transfer(parties[i], parties[j], amount) if bal[i] < 0 else Transfer(parties[j], parties[i], amount))
            saved_j, bal[j] = bal[j], bal[j] + bal[i]
            dfs(i + 1)
            bal[j] = saved_j
            path.pop()
            if saved_j + bal[i] == 0:  # exact cancel is never worse than any other j
                break

    dfs(0)
    return best


def min_transfers(transactions: list[list[int]]) -> int:
    """Part 1 (LC signature): fewest transfers that zero every net balance (DFS + pruning)."""
    return len(_search(net_balances(transactions)))


def min_transfers_bitmask(transactions: list[list[int]]) -> int:
    """Part 1 alt: n - (max number of disjoint zero-sum subsets), bitmask DP."""
    bal = list(net_balances(transactions).values())
    n = len(bal)
    total = [0] * (1 << n)
    dp = [0] * (1 << n)
    for mask in range(1, 1 << n):
        low = mask & -mask
        total[mask] = total[mask ^ low] + bal[low.bit_length() - 1]
        dp[mask] = max(dp[mask ^ (1 << i)] for i in range(n) if mask >> i & 1) + (total[mask] == 0)
    return n - dp[-1]


def settle(transactions: list[list[int]]) -> list[Transfer]:
    """Part 2: one optimal transfer list (first found; ascending-id search order)."""
    return _search(net_balances(transactions))


def settle_with_writeoff(transactions: list[list[int]], threshold: int) -> Settlement:
    """Part 3: write off parties with 0 < |net| < threshold; PLATFORM absorbs the residual."""
    nets = net_balances(transactions)
    written_off = [(p, v) for p, v in nets.items() if abs(v) < threshold]  # strict: == threshold is settled
    kept = {p: v for p, v in nets.items() if abs(v) >= threshold}
    residual = -sum(kept.values())
    if residual:
        kept = {PLATFORM: residual, **kept}  # PLATFORM = -1 sorts first, so it is settled first
    return Settlement(_search(kept), written_off)


def _name(p: int) -> str:
    return "PLATFORM" if p == PLATFORM else str(p)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    threshold, rest = 0, lines[1:]
    if rest and rest[0].upper().startswith("THRESHOLD"):
        threshold, rest = int(rest[0].split()[1]), rest[1:]
    transactions = [[int(x) for x in ln.split(",")] for ln in rest]
    if part == 1:
        out = [str(min_transfers(transactions))]
    elif part == 2:
        transfers = settle(transactions)
        out = [str(len(transfers))] + [f"from: {t.frm}, to: {t.to}, amount: {t.amount}" for t in transfers]
    else:
        transfers, written_off = settle_with_writeoff(transactions, threshold)
        out = [f"from: {_name(t.frm)}, to: {_name(t.to)}, amount: {t.amount}" for t in transfers]
        out.append("written_off: " + (",".join(f"{p}={v}" for p, v in written_off) or "none"))
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
