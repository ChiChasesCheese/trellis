"""Best-response improvement: fix two cats' commands, enumerate every choice of the third cat exhaustively inside the
full three-cat simulation (so floor sharing, fights and bed order are exact), keep the best, rotate until no cat can
improve. The result is a local optimum that no single cat can beat by changing only its own commands.
"""
from __future__ import annotations

import itertools
import sys
import time

from sim import BOARD, COST, Game, Rules, simulate

OPTIONS = [None, "N", "S", "E", "W", "stomp"]


def owners(plan, rules=Rules(), board=BOARD):
    """Which cat destroys each floor under `plan` -> {floor_id: color}."""
    g, state, who = Game(board, rules), None, {}
    state = g.initial
    for _ in range(rules.turns):
        state = g.step(state, lambda color, fid, m: who.setdefault(fid, color) and plan.get(fid))
    return who


def best_response(color, plan, rules=Rules(), board=BOARD):
    who = owners(plan, rules, board)
    fixed = {f: o for f, o in plan.items() if who.get(f) != color}
    g = Game(board, rules)
    start = g.initial[:4] + (g.initial[4] - sum(COST[o] for o in fixed.values()),)
    frontier = {start[:4]: (start[4], ())}
    for _ in range(rules.turns):
        nxt = {}
        for key, (money, mine) in frontier.items():
            state = key + (money,)
            events = []
            g.step(state, lambda c, fid, m: events.append((c, fid)) or None)
            dirs = {k[0]: k[3] for k in state[1]}
            per = []
            for c, fid in events:
                if fid in fixed:  # a command already on this floor fires for whoever destroys it
                    per.append([("paid", fixed[fid])])
                elif c == color:
                    per.append([o for o in OPTIONS if o is None or (o != dirs[c] and COST[o] <= money)])
                else:
                    per.append([None])
            for combo in itertools.product(*per):
                it = iter(combo)
                child = g.step(state, lambda c, fid, m: next(it))  # fixed commands were paid up front
                if child is None:
                    continue
                cmoney, ckey = child[4], child[:4]
                if ckey not in nxt or nxt[ckey][0] < cmoney:
                    nxt[ckey] = (cmoney, mine + tuple((f, o) for (c, f), o in zip(events, combo)
                                                      if o and f not in fixed))
        frontier = nxt
    best_key, (money, mine) = max(frontier.items(), key=lambda kv: (Game.score(kv[0] + (0,)), kv[1][0]))
    new_plan = dict(fixed)
    new_plan.update(dict(mine))
    return Game.score(best_key + (0,)), new_plan


def improve(plan, rules=Rules(), board=BOARD, log=print):
    score = simulate(plan, rules, board)[0]
    log(f"start {score:.0f}")
    stale = 0
    while stale < 3:
        for color in "RGB":
            t = time.time()
            s, p = best_response(color, plan, rules, board)
            if s > score:
                score, plan, stale = s, p, 0
                log(f"  {color} improves -> {score:.0f} ({time.time() - t:.0f}s)")
            else:
                stale += 1
                log(f"  {color} no gain ({time.time() - t:.0f}s)")
            if stale >= 3:
                break
    assert simulate(plan, rules, board)[0] == score
    return score, plan


if __name__ == "__main__":
    from exact import solve
    keep = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    _, (plan, _, _) = solve(keep=keep, log=lambda *a: None)
    score, plan = improve(plan)
    spent = sum(COST[o] for o in plan.values())
    print(f"local optimum {score:.0f}, spent ${spent}")
    for (r, c, fl), cmd in sorted(plan.items()):
        print(f"  row {r + 1} col {c} {'top' if fl == 0 else 'bottom'} floor: {cmd}")
