"""Search for the best command plan on board.py under sim.py's rules — an anytime search under a hard time budget.

    python3 solve.py [--rebound stay|step] [--powerup-first] [--time 300]

1. solo: each cat alone on the board, every command choice on every floor it destroys, states merged per turn
   (same cat state + same floors left -> keep the cheapest). ~50 s. Gives each cat's strongest routes as seeds.
2. polish, from many starts (no commands, Chi's plan, each cat's top solo routes): in the full three-cat simulation,
   re-search one cat's commands exhaustively with the other two fixed (~1 s), round-robin until no cat can improve.
   The result is a local optimum: no single cat changing its own commands scores more.
Every new best is replayed through sim.simulate, saved to plan_<rules>.json at once and printed as CHECKPOINT, so a
result exists long before the budget runs out. Known best, not proven optimal.
"""
from __future__ import annotations

import argparse
import json
import time
from itertools import product

from board import BOARD, CHI_PLAN_MAP2, COST, MAP2
from sim import COLORS, Game, Rules, simulate

OPTIONS = (None, "N", "S", "E", "W", "stomp", "powerup")


def branches(game, state, fixed=None, free=None):
    """Yield (choices made this turn, next state). fixed: plan for floors already decided; free: colors that choose."""
    asked = []
    game.step(state, lambda col, fid, m: asked.append((col, fid)))
    open_ = [(col, fid) for col, fid in asked if not (fixed and fid in fixed) and (free is None or col in free)]
    for combo in product(OPTIONS, repeat=len(open_)):
        pick = {fid: cmd for (_, fid), cmd in zip(open_, combo)}
        nxt = game.step(state, lambda col, fid, m: pick[fid] if fid in pick
                        else ("paid", fixed[fid]) if fixed and fid in fixed else None)
        if nxt is not None:
            yield {f: c for f, c in pick.items() if c}, nxt


def solo(color, rules):
    """Every way one cat alone can end: (raw power, bed arrival turn or None, floor mask, cost, plan, trajectory).
    Bed arrivals are recorded with the power before the bed bonus; cats still out after the last turn also score."""
    game = Game(rules=rules, colors=(color,))
    layer = {game.initial[1:3]: (game.initial, {}, ())}
    arrivals, sizes = [], []
    for _ in range(rules.turns):
        nxt = {}
        for state, plan, traj in layer.values():
            for pick, s in branches(game, state):
                k = s[1][0]
                p = {**plan, **pick}
                t = traj + ((k[1], k[2]),)
                if k[7]:
                    arrivals.append((k[4] - 2000, s[0], mask(game, s[2]), rules.budget - s[4], p, t))
                    continue
                key = s[1:3]
                if key not in nxt or nxt[key][0][4] < s[4]:
                    nxt[key] = (s, p, t)
        layer = nxt
        sizes.append(len(layer))
    for s, p, t in layer.values():
        arrivals.append((s[1][0][4], None, mask(game, s[2]), rules.budget - s[4], p, t))
    return arrivals, sizes


def mask(game, floors):
    from board import FLOORS
    m = 0
    for b, left in enumerate(floors):
        total = len(FLOORS[game.buildings[b][1]])
        for i in range(total - left):
            m |= 1 << (2 * b + i)
    return m


def best_response(plan, color, rules):
    """Re-search one cat's commands in the full game, others' commands fixed. Returns (score, plan)."""
    game = Game(rules=rules)
    others = {f: c for f, c in plan.items() if f not in owned(plan, color, rules)}
    start = game.initial[:4] + (rules.budget - sum(COST[c] for c in others.values()),)  # others' commands prepaid
    layer = {start[1:4]: (start, dict(others))}
    for _ in range(rules.turns):
        nxt = {}
        for state, p in layer.values():
            for pick, s in branches(game, state, fixed=p, free=(color,)):
                key = s[1:4]
                if key not in nxt or nxt[key][0][4] < s[4]:
                    nxt[key] = (s, {**p, **pick})
        layer = nxt
    s, p = max(layer.values(), key=lambda v: (Game.score(v[0]), v[0][4]))
    return Game.score(s), p


def owned(plan, color, rules):
    """Floors in plan that `color` destroys when the plan runs."""
    game, state, mine = Game(rules=rules), None, set()
    state = game.initial
    for _ in range(rules.turns):
        state = game.step(state, lambda col, fid, m: (mine.add(fid) if col == color else None) or (("paid", plan[fid]) if fid in plan else None))
    return mine & set(plan)


def live_only(plan, rules):
    """Drop commands on floors that are never destroyed: in the game every attached command is paid for."""
    game, fired, state = Game(rules=rules), set(), None
    state = game.initial
    for _ in range(rules.turns):
        state = game.step(state, lambda col, fid, m: fired.add(fid) or (("paid", plan[fid]) if fid in plan else None))
    return {f: c for f, c in plan.items() if f in fired}


def polish(plan, rules, deadline):
    """Round-robin best responses until no cat improves (or time runs out). Returns (score, plan)."""
    plan = live_only(plan, rules)
    score = simulate(plan, rules)[0]
    improved = True
    while improved and time.time() < deadline:
        improved = False
        for color in COLORS:
            s, p = best_response(live_only(plan, rules), color, rules)
            if s > score:
                score, plan, improved = s, live_only(p, rules), True
    return score, plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebound", default="stay")
    ap.add_argument("--powerup-first", action="store_true")
    ap.add_argument("--time", type=float, default=300, help="hard budget in seconds")
    ap.add_argument("--seeds", type=int, default=40, help="top solo routes per cat used as starts")
    args = ap.parse_args()
    rules = Rules(rebound=args.rebound, powerup_first=args.powerup_first)
    t0 = time.time()
    deadline = t0 + args.time
    out = f"plan_{args.rebound}{'_pf' if args.powerup_first else ''}.json"
    best = [-1, None]

    def offer(score, plan, where):
        plan = live_only(plan, rules)
        if score > best[0]:
            assert simulate(plan, rules)[0] == score
            best[:] = [score, plan]
            json.dump({"rules": {"rebound": args.rebound, "powerup_first": args.powerup_first}, "score": score,
                       "cost": sum(COST[c] for c in plan.values()),
                       "plan": [[*f, c] for f, c in sorted(plan.items())]}, open(out, "w"), indent=1)
            print(f"CHECKPOINT {score:g} from {where}, ${sum(COST[c] for c in plan.values())}, "
                  f"{time.time() - t0:.0f}s -> {out}", flush=True)

    starts = [({}, "no commands"), (dict(CHI_PLAN_MAP2), "Chi's plan")] if BOARD is MAP2 else [({}, "no commands")]
    for plan, name in starts:
        offer(*polish(plan, rules, deadline), name)

    seeds = []
    for color in COLORS:
        ends, _ = solo(color, rules)
        ends.sort(key=lambda e: -(5 * e[0] if e[1] is not None else e[0]))
        seeds += [(e[4], f"{color} solo #{i + 1}") for i, e in enumerate(ends[:args.seeds])]
        del ends
        print(f"{color} solo done, {time.time() - t0:.0f}s", flush=True)
    for plan, name in seeds:
        if time.time() > deadline:
            print("time budget reached", flush=True)
            break
        offer(*polish(dict(plan), rules, deadline), name)
    print(f"best {best[0]:g}, {time.time() - t0:.0f}s, saved {out}")


if __name__ == "__main__":
    main()
