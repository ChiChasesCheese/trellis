"""Search for the best command placement under the budget.

A command matters only on a floor that some cat destroys, and it acts from the moment that floor falls. So the search
walks turn by turn and branches only when a floor is destroyed: no command, a turn to one of the other directions, or
Stomp. Placing the command at that moment is the same as having placed it before the test.

Branching is exact; to keep it tractable each turn keeps the `width` best states (beam search). States that differ
only in money left are merged, keeping the richer one. The result is exact when no state was ever cut, and is
otherwise checked for convergence by re-running with a wider beam.
"""
from __future__ import annotations

import itertools
import sys
import time

from sim import BOARD, COST, DIRS, Game, Rules

OPTIONS = [None, "N", "S", "E", "W", "stomp"]  # Power Up left out until its effect is known (ASSUMPTIONS A7)
BONUS = [lambda p: p + 2000, lambda p: p * 3, lambda p: p * 5]


def potential(game, key):
    """Beam ranking: current powers, with each cat that can still reach its bed in the turns left (Manhattan
    distance) given the best remaining bed bonus by the rearrangement rule: bigger power, bigger multiplier."""
    turn, cats, _, arrivals = key
    left = game.rules.turns - turn
    total, hopeful = 0.0, []
    for color, r, c, d, power, stuck, stomp, status in cats:
        if status == "out":
            continue
        if status == "" and abs(r - game.beds[color][0]) + abs(c - game.beds[color][1]) <= left:
            hopeful.append(power)
        else:
            total += power
    slots = BONUS[arrivals:arrivals + len(hopeful)]
    hopeful.sort()
    # smallest power takes the earliest remaining slot (+2000 is flat), largest takes the last (x5)
    offset = len(hopeful) - len(slots)
    for i, p in enumerate(hopeful):
        total += slots[i - offset](p) if i >= offset else p
    return total


def search(width=5000, rules: Rules = Rules(), board=BOARD, options=OPTIONS):
    game = Game(board, rules)
    game.beds = {v[1]: pos for pos, v in game.kinds.items() if v[0] == "bed"}
    # frontier: state-without-money -> (money, plan)
    frontier = {game.initial[:4]: (game.initial[4], {})}
    cut = False
    for _ in range(rules.turns):
        nxt = {}
        for key, (money, plan) in frontier.items():
            state = key + (money,)
            events = []
            game.step(state, lambda color, fid, m: events.append((color, fid)) or None)
            dirs_now = {k[0]: k[3] for k in state[1]}
            per_event = []
            for color, fid in events:
                opts = [o for o in options if o is None or (o != dirs_now[color] and COST[o] <= money)]
                per_event.append(opts)
            for combo in itertools.product(*per_event) if events else [()]:
                if sum(COST[o] for o in combo if o) > money:
                    continue
                it = iter(combo)
                child = game.step(state, lambda color, fid, m: next(it))
                if child is None:
                    continue
                ckey, cmoney = child[:4], child[4]
                if ckey not in nxt or nxt[ckey][0] < cmoney:
                    cplan = dict(plan)
                    for (color, fid), o in zip(events, combo):
                        if o:
                            cplan[fid] = o
                    nxt[ckey] = (cmoney, cplan)
        if len(nxt) > width:
            cut = True
            ranked = sorted(nxt.items(), key=lambda kv: (potential(game, kv[0]), kv[1][0]), reverse=True)
            nxt = dict(ranked[:width])
        frontier = nxt
    best_key, (money, plan) = max(frontier.items(), key=lambda kv: (Game.score(kv[0] + (0,)), kv[1][0]))
    return Game.score(best_key + (0,)), plan, rules.budget - money, not cut


if __name__ == "__main__":
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    t = time.time()
    score, plan, spent, exact = search(width)
    print(f"width={width} best={score:.0f} spent=${spent} exact={exact} seconds={time.time() - t:.1f}")
    for fid, cmd in sorted(plan.items()):
        print(f"  row {fid[0] + 1} col {fid[1]} floor {'top' if fid[2] == 0 else 'bottom'}: {cmd}")
