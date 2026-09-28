"""Roblox OA factory game: 24-hour production-line simulator + anytime optimizer.

    python3 factory.py level.json [--time 60] [--batch all|partial] [--same-hour]

level.json (transcribe from the screenshot; see sandwich_tutorial.json):
{
  "hours": 24, "start_cash": 0,
  "nodes": {
    "<id>": {"rate": 20,            # the number the node shows: units per batch (sources: per hour)
             "period": 1,           # hours per batch ("1 of 2hrs" -> 2)
             "inputs": {"<id>": 1}, # units of each input per unit of output; absent/empty = raw source
             "unit_cost": 0.5,      # $ per unit produced ("x$0.50" under a source)
             "price": 0,            # $ per unit sold; > 0 marks a terminal (its output is sold at once)
             "max_rate": 50,        # the highest setting the UI allows
             "buffs": ["half_input", "double_output", "fast"]}   # buffs this node offers
  },
  "buff_cost": {"half_input": {"per_unit": 0.2}, "double_output": {"per_unit": 0.3}, "fast": {"flat": 25}}
}

Rules, tagged by source:
  [Chi]    raw sources charge unit_cost for every unit supplied, used or not
  [Chi]    buffs: half_input halves the inputs per output; double_output doubles what a batch yields and is charged
           on every unit it yields; fast turns a 2-hour batch into 1 hour
  [Chi]    a node's first batch waits for its inputs, so a chain starts staggered (hour x, x+1, x+2 ...)
  [open]   Rules.batch: "all" = a batch runs only when inputs for the full setting are in stock (default; fits Chi's
           tip 4, "set a bit more but fewer batches"), "partial" = it makes as many as the stock allows
  [open]   Rules.same_hour: False = what a node makes in hour h is usable from hour h+1 (default)
  [open]   a product feeding several consumers is handed out in the order the consumers are listed in the json
  [open]   stock never expires or overflows; what is left at hour 24 is worth nothing
Score = start_cash + sales - raw costs - buff costs at the end of the last hour.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass

BUFFS = ("half_input", "double_output", "fast")


@dataclass(frozen=True)
class Rules:
    batch: str = "all"
    same_hour: bool = False


def load(path):
    with open(path) as f:
        level = json.load(f)
    for nid, n in level["nodes"].items():
        n.setdefault("inputs", {})
        n.setdefault("period", 1)
        n.setdefault("unit_cost", 0)
        n.setdefault("price", 0)
        n.setdefault("max_rate", 50)
        n.setdefault("buffs", [])
        for i in n["inputs"]:
            assert i in level["nodes"], f"{nid} needs unknown input {i}"
    level.setdefault("hours", 24)
    level.setdefault("start_cash", 0)
    level.setdefault("buff_cost", {})
    level["order"] = topo(level["nodes"])
    return level


def topo(nodes):
    done, order = set(), []

    def visit(n):
        if n in done:
            return
        for i in nodes[n]["inputs"]:
            visit(i)
        done.add(n)
        order.append(n)

    for n in nodes:
        visit(n)
    return order


def buff_cost(level, buff, units):
    c = level["buff_cost"].get(buff, {})
    return c.get("per_unit", 0) * units + c.get("flat", 0)


def simulate(level, setting, rules=Rules(), trace=None):
    """setting: {node: (rate, frozenset(buffs))}. Returns final cash. trace (list) gets one dict per hour."""
    nodes, order = level["nodes"], level["order"]
    stock = {n: 0.0 for n in nodes}
    pending = []  # (hour available, node, units)
    busy_until = {n: 0 for n in nodes}
    cash = level["start_cash"]
    sold = {n: 0 for n in nodes if nodes[n]["price"] > 0}
    buffs_on = {n: setting[n][1] for n in nodes}
    for b in BUFFS:  # flat buff fees are paid once
        for n in nodes:
            if b in buffs_on[n]:
                cash -= buff_cost(level, b, 0)
    for h in range(level["hours"]):
        for when, n, u in [p for p in pending if p[0] == h]:
            stock[n] += u
        pending = [p for p in pending if p[0] != h]
        for n in order:
            node, (rate, buffs) = nodes[n], setting[n]
            if rate <= 0 or busy_until[n] > h:
                continue
            period = 1 if "fast" in buffs else node["period"]
            per = 0.5 if "half_input" in buffs else 1.0
            make = rate
            for i, q in node["inputs"].items():
                need = q * per
                can = int(stock[i] // need + 1e-9) if need else rate
                make = min(make, can)
            if node["inputs"] and make < rate and rules.batch == "all":
                continue
            if make <= 0:
                continue
            for i, q in node["inputs"].items():
                stock[i] -= q * per * make
            out = make * (2 if "double_output" in buffs else 1)
            cash -= node["unit_cost"] * make
            if "double_output" in buffs:
                cash -= level["buff_cost"].get("double_output", {}).get("per_unit", 0) * out
            if "half_input" in buffs:
                cash -= level["buff_cost"].get("half_input", {}).get("per_unit", 0) * out
            if "fast" in buffs:
                cash -= level["buff_cost"].get("fast", {}).get("per_unit", 0) * out
            busy_until[n] = h + period
            ready = h + period - (1 if rules.same_hour and period == 1 else 0)
            if node["price"] > 0:
                if h + period <= level["hours"]:  # a batch finishing after the last hour never sells
                    cash += node["price"] * out
                    sold[n] += out
            elif rules.same_hour and period == 1:
                stock[n] += out
            else:
                pending.append((ready, n, out))
        if trace is not None:
            trace.append({"hour": h, "cash": round(cash, 2), "stock": {k: v for k, v in stock.items() if v}})
    if trace is not None:
        trace.append({"sold": sold, "left": {k: v for k, v in stock.items() if v}})
    return cash


def backward_fill(level, cap_sinks=True):
    """Chi's step 1: set each terminal to its max, give every upstream node exactly what downstream consumes per hour,
    and shrink terminals until nothing exceeds its max setting. Returns a setting with no buffs."""
    nodes = level["nodes"]
    sinks = [n for n in nodes if nodes[n]["price"] > 0]
    scale = {s: 1.0 for s in sinks}
    for _ in range(50):
        per_hour = {n: 0.0 for n in nodes}
        for s in sinks:
            per_hour[s] = nodes[s]["max_rate"] * scale[s] / nodes[s]["period"]
        for n in reversed(level["order"]):
            for i, q in nodes[n]["inputs"].items():
                per_hour[i] += per_hour[n] * q
        over = {n: per_hour[n] * nodes[n]["period"] / nodes[n]["max_rate"] for n in nodes}
        worst = max(over.values())
        if worst <= 1 + 1e-9:
            break
        for s in sinks:
            scale[s] /= worst
    return {n: (round(per_hour[n] * nodes[n]["period"]), frozenset()) for n in nodes}


def optimize(level, rules=Rules(), budget=60.0, seed=0, log=print):
    """Anytime hill climbing with restarts on (rate, buffs) per node. Returns (cash, setting)."""
    rng = random.Random(seed)
    nodes = level["nodes"]
    names = list(nodes)
    t0 = time.time()
    best_setting = backward_fill(level)
    best = simulate(level, best_setting, rules)
    log(f"backward fill: {best:,.2f}")

    def climb(setting, score):
        steps = (1, 2, 5, 10, 25)
        improved = True
        while improved and time.time() - t0 < budget:
            improved = False
            for n in names:
                rate, buffs = setting[n]
                cands = [(max(0, min(nodes[n]["max_rate"], rate + d)), buffs) for s in steps for d in (s, -s)]
                cands += [(rate, buffs ^ {b}) for b in nodes[n]["buffs"]]
                for c in cands:
                    if c == setting[n]:
                        continue
                    trial = {**setting, n: (c[0], frozenset(c[1]))}
                    v = simulate(level, trial, rules)
                    if v > score + 1e-9:
                        setting, score, improved = trial, v, True
                        break
        return score, setting

    best, best_setting = climb(best_setting, best)
    log(f"climb: {best:,.2f}  ({time.time() - t0:.1f}s)")
    while time.time() - t0 < budget:
        s = dict(best_setting)
        for n in rng.sample(names, k=max(1, len(names) // 3)):
            rate, buffs = s[n]
            rate = max(0, min(nodes[n]["max_rate"], rate + rng.choice((-10, -5, -2, 2, 5, 10))))
            if nodes[n]["buffs"] and rng.random() < 0.3:
                buffs = buffs ^ {rng.choice(nodes[n]["buffs"])}
            s[n] = (rate, frozenset(buffs))
        v, s = climb(s, simulate(level, s, rules))
        if v > best + 1e-9:
            best, best_setting = v, s
            log(f"restart: {best:,.2f}  ({time.time() - t0:.1f}s)")
    return best, best_setting


def report(level, setting, rules=Rules()):
    trace = []
    cash = simulate(level, setting, rules, trace)
    lines = [f"final cash {cash:,.2f}"]
    for n in level["order"]:
        rate, buffs = setting[n]
        node = level["nodes"][n]
        tag = "SELL" if node["price"] > 0 else "raw " if not node["inputs"] else "make"
        lines.append(f"  {tag} {n:<16} set {rate:>3}  every {node['period']}h"
                     f"{'  +' + ','.join(sorted(buffs)) if buffs else ''}")
    lines.append(f"  sold {trace[-1]['sold']}")
    lines.append(f"  left over at the end (paid for, never used) {trace[-1]['left']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("level")
    ap.add_argument("--time", type=float, default=60)
    ap.add_argument("--batch", default="all")
    ap.add_argument("--same-hour", action="store_true")
    args = ap.parse_args()
    level = load(args.level)
    rules = Rules(batch=args.batch, same_hour=args.same_hour)
    given = {n: (level["nodes"][n]["rate"], frozenset()) for n in level["nodes"]}
    print(f"as transcribed: {simulate(level, given, rules):,.2f}")
    cash, setting = optimize(level, rules, args.time)
    print(report(level, setting, rules))
    out = args.level.replace(".json", "_best.json")
    json.dump({n: {"rate": r, "buffs": sorted(b)} for n, (r, b) in setting.items()} | {"_cash": cash},
              open(out, "w"), indent=1)
    print("saved", out)


if __name__ == "__main__":
    main()
