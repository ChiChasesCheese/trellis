"""Exhaustive search for the best command placement under a budget.

A command only changes what happens after the floor carrying it is destroyed, so every plan can be built by adding
commands in the order they fire: the next command goes on a floor destroyed after the previous command fired, in the
timeline those earlier commands produce. Each effective plan is generated exactly once; a command on a floor no cat
destroys would do nothing and is never generated.
"""
from __future__ import annotations

import sys
import time

from sim import DIRS, Rules, simulate


def search(rules: Rules = Rules(), max_commands: int | None = None):
    k_max = rules.budget // rules.cost_per_command if max_commands is None else max_commands
    best = {"score": -1.0, "plan": {}}
    count = 0

    def rec(plan, after_event_index, depth):
        nonlocal count
        score, _, events = simulate(plan, rules)
        count += 1
        if score > best["score"]:
            best["score"], best["plan"] = score, dict(plan)
        if depth == k_max:
            return
        for idx in range(after_event_index + 1, len(events)):
            turn, color, r, c, floor = events[idx]
            key = (r, c, floor)
            if key in plan:
                continue
            for d in DIRS:
                plan[key] = d
                rec(plan, idx, depth + 1)
                del plan[key]

    start = time.time()
    rec({}, -1, 0)
    return best["score"], best["plan"], count, time.time() - start


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else None
    score, plan, n, secs = search(max_commands=k)
    print(f"best={score:.0f} plan={plan} plans_simulated={n} seconds={secs:.1f}")
