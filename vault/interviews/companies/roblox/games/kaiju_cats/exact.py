"""Provably optimal command placement, by solo enumeration + bound-and-verify.

1. Solo: for each cat alone on the board, enumerate every reachable outcome exhaustively (branching only when it
   destroys a floor: no command / a turn / Stomp) and keep, per (arrival turn, money spent), the highest power.
2. Bound: for a triple of solo outcomes, the other cats can only take floors away or kill a cat, so the combined
   score computed from the three solo powers and their arrival order is an upper bound on what that triple can
   really score.
3. Verify: walk triples from the highest bound down and run each merged plan in the full simulator. The first one
   whose real score equals the best remaining bound is optimal: no other triple can beat it.
"""
from __future__ import annotations

import heapq
import itertools
import sys
import time

from sim import BOARD, COST, Game, Rules, simulate

OPTIONS = [None, "N", "S", "E", "W", "stomp"]  # Power Up left out until its effect is known (ASSUMPTIONS A7)


def solo(color, rules: Rules = Rules(), board=BOARD, options=OPTIONS, keep=1):
    """-> [(arrival_turn or None, spent, power_before_bed_bonus, plan)]: per (arrival, spent) the `keep` best
    distinct plans; with keep=1 only the Pareto front over (spent, power) per arrival turn."""
    g = Game(board, rules, colors=(color,))
    frontier = {g.initial[:4] + (None,): (g.initial[4], ())}  # key: state-without-money + arrival turn
    for _ in range(rules.turns):
        nxt = {}
        for key, (money, plan) in frontier.items():
            state, arrival = key[:4] + (money,), key[4]
            events = []
            g.step(state, lambda c, fid, m: events.append(fid) or None)
            d = state[1][0][3]
            per = [[o for o in options if o is None or (o != d and COST[o] <= money)] for _ in events]
            for combo in itertools.product(*per) if events else [()]:
                it = iter(combo)
                child = g.step(state, lambda c, fid, m: next(it))
                if child is None:
                    continue
                arr = arrival
                if arr is None and child[1][0][7] == "bed":
                    arr = child[0]
                ckey = child[:4] + (arr,)
                if ckey not in nxt or nxt[ckey][0] < child[4]:
                    nxt[ckey] = (child[4], plan + tuple((f, o) for f, o in zip(events, combo) if o))
        frontier = nxt
    buckets = {}
    for key, (money, plan) in frontier.items():
        power, arrival = key[1][0][4], key[4]
        pre = power - 2000 if arrival is not None else power  # alone, a cat is always first into its bed
        buckets.setdefault((arrival, rules.budget - money), []).append((pre, plan))
    if keep > 1:
        return [(a, s, pre, plan) for (a, s), items in buckets.items()
                for pre, plan in sorted(items, key=lambda x: -x[0])[:keep]]
    best = {k: max(items, key=lambda x: x[0]) for k, items in buckets.items()}
    # Pareto: for a fixed arrival turn, drop outcomes that cost more for no more power.
    front = []
    for arrival in {a for a, _ in best}:
        top = -1
        for spent in sorted(s for a, s in best if a == arrival):
            pre, plan = best[(arrival, spent)]
            if pre > top:
                front.append((arrival, spent, pre, plan))
                top = pre
    return front


def combined(outcomes):
    """Bed bonuses by arrival order (same turn: lower power first). outcomes: [(arrival, pre_power)]."""
    total, order = 0.0, []
    for arrival, pre in outcomes:
        if arrival is None:
            total += pre
        else:
            order.append((arrival, pre))
    for i, (_, pre) in enumerate(sorted(order)):
        total += pre + 2000 if i == 0 else pre * (3 if i == 1 else 5)
    return total


def solve(rules: Rules = Rules(), board=BOARD, log=print, keep=1):
    t = time.time()
    fronts = {c: solo(c, rules, board, keep=keep) for c in "RGB"}
    log(f"solo fronts: " + ", ".join(f"{c}={len(f)}" for c, f in fronts.items()) + f" ({time.time() - t:.0f}s)")
    # All affordable triples with their bounds; a max-heap walks them best-first.
    heap = []
    for r in fronts["R"]:
        for g in fronts["G"]:
            if r[1] + g[1] > rules.budget:
                continue
            for b in fronts["B"]:
                if r[1] + g[1] + b[1] <= rules.budget:
                    bound = combined([(r[0], r[2]), (g[0], g[2]), (b[0], b[2])])
                    heap.append((-bound, r[1] + g[1] + b[1], id(r), id(g), id(b), r, g, b))
    heapq.heapify(heap)
    log(f"affordable triples: {len(heap)}")
    best_real, best = -1.0, None
    checked = 0
    while heap:
        neg_bound, spent, *_ignore, r, g, b = heapq.heappop(heap)
        if -neg_bound <= best_real:
            break  # no remaining triple can beat what is already verified
        plan = {}
        clash = False
        for f, o in r[3] + g[3] + b[3]:
            if plan.get(f, o) != o:
                clash = True
            plan[f] = o
        if clash:
            continue
        real, _ = simulate(plan, rules, board)
        checked += 1
        if real > best_real:
            best_real, best = real, (plan, spent, -neg_bound)
    top_bound = -heap[0][0] if heap else best_real
    log(f"verified {checked} triples ({time.time() - t:.0f}s total); "
        f"proven optimal among these candidates: {not heap or top_bound <= best_real}")
    return best_real, best


if __name__ == "__main__":
    keep = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    score, (plan, spent, bound) = solve(keep=keep)
    print(f"best verified score={score:.0f} spent=${spent} (bound of that triple {bound:.0f}), keep={keep}")
    for (r, c, fl), cmd in sorted(plan.items()):
        print(f"  row {r + 1} col {c} {'top' if fl == 0 else 'bottom'} floor: {cmd}")
