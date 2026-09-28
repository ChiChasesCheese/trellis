"""Roblox OA factory game: 24-hour simulator + anytime optimizer, built from the in-game instructions.

    python3 factory.py level.json [--time 60]       # prints the in-game settings to enter, and the simulated money

level.json — transcribe one entry per machine (see sandwich_tutorial.json):
{
  "hours": 24, "start_cash": 3000,
  "nodes": {
    "dough":    {"kind": "supplier", "row": 2, "rate": 24, "unit_cost": 0.5},          # "Order every hour", "Cost per item"
    "bread":    {"kind": "maker", "row": 2, "rate": 10,                                 # "Try to make"
                 "options": [{"name": "Crusty Bread", "inputs": {"dough": 1}},          # one entry per product it can make
                             {"name": "Crustless Bread", "inputs": {"dough": 2}}],
                 "mods": {"output2x": 0.1, "half": 0.1, "storage2x": 0.05}},            # modification: $ added per item
    "jam":      {"kind": "maker", "row": 3, "rate": 20, "options": [{"name": "Jam", "inputs": {...}, "period": 2}]},
    "sandwich": {"kind": "seller", "row": 2, "rate": 12, "options": [{"name": "Sandwich", "inputs": {...}, "price": 10}]}
  }
}
Optional per node: "max_rate" (maker/seller default 50, supplier 1000), "storage" (supplier 1000, maker 100),
"option" (index of the product currently selected). "row" = vertical position on screen, top = smallest.

Rules — [game] = in-game instructions, [Chi] = Chi confirmed 2026-09-28, [open] = best guess, a switch or a comment:
  [game] start with start_cash; score = money after the last hour; the best tested factory counts
  [game] a supplier's order arrives at once (usable this hour); every ordered item is paid, used or not
  [game] each hour a maker/seller tries to make `rate` items; if its inputs are not all in stock it makes nothing
  [game] made items go to the machine's storage at the end of the hour (2 h at the end of the second hour) and
         can be used from the next hour; sellers have no storage, what they make is sold at once
  [game] storage full -> the extra items are lost          [Chi] their materials and mod fees are still paid
  [game] a machine feeding several: the one closest to a seller is served first, ties -> topmost; a machine whose
         full request cannot be met is skipped (gets nothing)   [Chi] closest = fewest machines to a seller
  [Chi]  all makers pull at the start of the hour; a 2 h machine pulls once and is busy for 2 hours
  [game] mods (makers only) add a cost per item made: output2x doubles max_rate, half halves the inputs,
         fast makes a 2 h machine take 1 h, storage2x doubles storage
  [open] half of an odd input amount rounds up; a batch finishing after the last hour is never sold
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time

MODS = ("output2x", "half", "fast", "storage2x")
HARD_LIMIT = 280  # seconds: a result must be back within 5 minutes of receiving the level


def load(path):
    with open(path) as f:
        level = json.load(f)
    return prepare(level)


def prepare(level):
    level.setdefault("hours", 24)
    level.setdefault("start_cash", 0)
    nodes = level["nodes"]
    for i, (nid, n) in enumerate(nodes.items()):
        kind = n.setdefault("kind", "maker")
        assert kind in ("supplier", "maker", "seller"), f"{nid}: kind {kind}"
        n.setdefault("row", i)
        n.setdefault("rate", 0)
        n.setdefault("unit_cost", 0)
        n.setdefault("max_rate", 1000 if kind == "supplier" else 50)
        n.setdefault("storage", 1000 if kind == "supplier" else 0 if kind == "seller" else 100)
        n.setdefault("mods", {})
        n.setdefault("option", 0)
        if kind != "supplier":
            if "options" not in n:
                n["options"] = [{"name": nid, "inputs": n.get("inputs", {}), "price": n.get("price", 0),
                                 "period": n.get("period", 1)}]
            for o in n["options"]:
                o.setdefault("name", nid)
                o.setdefault("inputs", {})
                o.setdefault("price", 0)
                o.setdefault("period", 1)
                for src in o["inputs"]:
                    assert src in nodes, f"{nid} ({o['name']}) takes from unknown machine {src}"
        else:
            n["options"] = []
        for m in n["mods"]:
            assert m in MODS, f"{nid}: unknown mod {m} (use {MODS})"
    return level


def given_setting(level):
    return {nid: (n["rate"], n["option"], frozenset()) for nid, n in level["nodes"].items()}


def pull_order(level, setting):
    """Makers and sellers in the order they are served: fewest machines to a seller first, then topmost."""
    nodes = level["nodes"]
    down = {n: [] for n in nodes}
    for nid, n in nodes.items():
        if n["kind"] != "supplier":
            for src in n["options"][setting[nid][1]]["inputs"]:
                down[src].append(nid)
    dist = {}

    def d(n):
        if n not in dist:
            dist[n] = 0 if nodes[n]["kind"] == "seller" else 1 + min((d(c) for c in down[n]), default=99)
        return dist[n]

    return sorted((n for n in nodes if nodes[n]["kind"] != "supplier"), key=lambda n: (d(n), nodes[n]["row"]))


def simulate(level, setting, trace=None):
    """setting: {node: (rate, option index, frozenset(mods))}. Returns final money."""
    nodes, hours = level["nodes"], level["hours"]
    order = pull_order(level, setting)
    stock = {n: 0 for n in nodes}
    cap = {n: nodes[n]["storage"] * (2 if "storage2x" in setting[n][2] else 1) for n in nodes}
    busy_until = {n: 0 for n in nodes}
    pending = []  # (end hour, node, items)
    cash = level["start_cash"]
    sold, lost, batches = {}, {n: 0 for n in nodes}, {n: 0 for n in nodes}

    def put(n, items):
        room = cap[n] - stock[n]
        stock[n] += min(room, items)
        lost[n] += max(0, items - room)

    for h in range(hours):
        for n, node in nodes.items():  # orders arrive at once
            if node["kind"] == "supplier" and setting[n][0] > 0:
                cash -= setting[n][0] * node["unit_cost"]
                put(n, setting[n][0])
        for n in order:  # pulls at the start of the hour, in priority order
            rate, opt, mods = setting[n]
            if rate <= 0 or busy_until[n] > h:
                continue
            o = nodes[n]["options"][opt]
            need = {src: math.ceil(q * rate / 2) if "half" in mods else q * rate for src, q in o["inputs"].items()}
            if any(stock[src] < k for src, k in need.items()):
                continue
            for src, k in need.items():
                stock[src] -= k
            period = 1 if "fast" in mods else o["period"]
            busy_until[n] = h + period
            cash -= rate * sum(nodes[n]["mods"][m] for m in mods)
            pending.append((h + period - 1, n, rate))
            batches[n] += 1
        for item in [p for p in pending if p[0] == h]:  # end of the hour
            _, n, items = item
            o = nodes[n]["options"][setting[n][1]]
            if nodes[n]["kind"] == "seller":
                cash += items * o["price"]
                sold[o["name"]] = sold.get(o["name"], 0) + items
            else:
                put(n, items)
        pending = [p for p in pending if p[0] != h]
        if trace is not None:
            trace.append({"hour": h, "cash": cash, "stock": dict(stock)})
    if trace is not None:
        trace.append({"sold": sold, "lost": {k: v for k, v in lost.items() if v},
                      "left": {k: v for k, v in stock.items() if v}, "batches": batches})
    return cash


def valid(level, setting):
    for n, (rate, opt, mods) in setting.items():
        node = level["nodes"][n]
        top = node["max_rate"] * (2 if "output2x" in mods else 1)
        if not 0 <= rate <= top or not mods <= set(node["mods"]):
            return False
        if "fast" in mods and node["options"][opt]["period"] < 2:
            return False
    return True


def backward_fill(level, options, sellers_on):
    """Chi's step 1: sellers at max, every upstream machine gets exactly what its consumers use per hour (a 2 h machine
    makes two hours' worth per batch), then scale the sellers down until no machine is over its max."""
    nodes = level["nodes"]
    scale = {n: 1.0 if n in sellers_on else 0.0 for n in nodes if nodes[n]["kind"] == "seller"}
    per_hour = {}
    for _ in range(60):
        per_hour = {n: 0.0 for n in nodes}
        for s, k in scale.items():
            o = nodes[s]["options"][options[s]]
            per_hour[s] = nodes[s]["max_rate"] * k / o["period"]
        for n in reversed(topo(level, options)):
            if nodes[n]["kind"] != "supplier":
                for src, q in nodes[n]["options"][options[n]]["inputs"].items():
                    per_hour[src] += per_hour[n] * q
        worst = max(per_hour[n] * period(level, n, options) / nodes[n]["max_rate"] for n in nodes)
        if worst <= 1 + 1e-9:
            break
        for s in scale:
            scale[s] /= worst
    return {n: (min(nodes[n]["max_rate"], math.ceil(per_hour[n] * period(level, n, options) - 1e-9)),
                options[n], frozenset()) for n in nodes}


def period(level, n, options):
    node = level["nodes"][n]
    return 1 if node["kind"] == "supplier" else node["options"][options[n]]["period"]


def topo(level, options):
    nodes, seen, out = level["nodes"], set(), []

    def visit(n):
        if n in seen:
            return
        seen.add(n)
        if nodes[n]["kind"] != "supplier":
            for src in nodes[n]["options"][options[n]]["inputs"]:
                visit(src)
        out.append(n)

    for n in nodes:
        visit(n)
    return out


def optimize(level, budget=60.0, seed=0, log=print):
    """Anytime: backward fill for every product choice x every subset of sellers switched off, then hill climbing
    on rate / product / mods from the best starts, then random restarts until the budget. Returns (money, setting)."""
    budget = min(budget, HARD_LIMIT)
    t0 = time.time()
    rng = random.Random(seed)
    nodes = level["nodes"]
    names = list(nodes)
    sellers = [n for n in nodes if nodes[n]["kind"] == "seller"]
    multi = [n for n in nodes if len(nodes[n]["options"]) > 1]

    starts = [given_setting(level)]
    for choice in itertools.product(*(range(len(nodes[n]["options"])) for n in multi)):
        options = {n: nodes[n]["option"] for n in nodes} | dict(zip(multi, choice))
        for k in range(len(sellers), 0, -1):
            for on in itertools.combinations(sellers, k):
                starts.append(backward_fill(level, options, set(on)))
            if time.time() - t0 > budget * 0.2:
                break
    scored = sorted(((simulate(level, s), i, s) for i, s in enumerate(starts) if valid(level, s)), reverse=True)
    best, _, best_setting = scored[0]
    log(f"{len(starts)} starts, best start {best:,.2f}  ({time.time() - t0:.1f}s)")

    steps = (1, 2, 3, 5, 10, 25)

    def climb(s, v):
        improved = True
        while improved and time.time() - t0 < budget:
            improved = False
            for n in rng.sample(names, len(names)):
                rate, opt, mods = s[n]
                cands = [(rate + d, opt, mods) for st in steps for d in (st, -st)] + [(0, opt, mods)]
                cands += [(rate, opt, mods ^ {m}) for m in nodes[n]["mods"]]
                cands += [(rate, o, mods) for o in range(len(nodes[n]["options"])) if o != opt]
                for c in cands:
                    trial = {**s, n: (c[0], c[1], frozenset(c[2]))}
                    if not valid(level, trial):
                        continue
                    tv = simulate(level, trial)
                    if tv > v + 1e-9:
                        s, v, improved = trial, tv, True
                        break
        return v, s

    for v, _, s in scored[:5]:
        v, s = climb(s, v)
        if v > best + 1e-9:
            best, best_setting = v, s
            log(f"climb: {best:,.2f}  ({time.time() - t0:.1f}s)")
    while time.time() - t0 < budget:
        s = dict(best_setting)
        for n in rng.sample(names, k=max(1, len(names) // 3)):
            rate, opt, mods = s[n]
            rate += rng.choice((-10, -5, -3, 3, 5, 10))
            if nodes[n]["mods"] and rng.random() < 0.3:
                mods = mods ^ {rng.choice(list(nodes[n]["mods"]))}
            s[n] = (rate, opt, frozenset(mods))
        if not valid(level, s):
            continue
        v, s = climb(s, simulate(level, s))
        if v > best + 1e-9:
            best, best_setting = v, s
            log(f"restart: {best:,.2f}  ({time.time() - t0:.1f}s)")
    return best, best_setting


MOD_LABEL = {"output2x": "2x Output Max", "half": "½ Materials", "fast": "1 Hour Production", "storage2x": "2x Storage"}


def report(level, setting):
    trace = []
    money = simulate(level, setting, trace)
    end = trace[-1]
    nodes = level["nodes"]
    lines = [f"money after {level['hours']} h: ${money:,.2f}  (start ${level['start_cash']:,})", "", "enter in the game:"]
    for n in sorted(nodes, key=lambda n: (nodes[n]["row"], n)):
        rate, opt, mods = setting[n]
        node = nodes[n]
        what = "Order every hour" if node["kind"] == "supplier" else "Try to make"
        product = f"  make {node['options'][opt]['name']}" if len(node["options"]) > 1 else ""
        mod = f"  mods: {', '.join(MOD_LABEL[m] for m in sorted(mods))}" if mods else ""
        runs = "" if node["kind"] == "supplier" else f"   (runs {end['batches'][n]} times)"
        lines.append(f"  {n:<16} {what} {rate:>4}{product}{mod}{runs}")
    lines.append(f"sold: {end['sold']}")
    if end["lost"]:
        lines.append(f"lost to full storage: {end['lost']}")
    lines.append(f"left in storage at the end (paid, unused): {end['left']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("level")
    ap.add_argument("--time", type=float, default=60, help=f"search seconds (capped at {HARD_LIMIT})")
    args = ap.parse_args()
    level = load(args.level)
    given = given_setting(level)
    print(f"as transcribed: ${simulate(level, given):,.2f}   <- compare with the game's Initial Test first\n")
    money, setting = optimize(level, args.time)
    print()
    print(report(level, setting))
    out = args.level.replace(".json", "_best.json")
    with open(out, "w") as f:
        json.dump({"money": money, "setting": {n: {"rate": r, "option": o, "mods": sorted(m)}
                                               for n, (r, o, m) in setting.items()}}, f, indent=1)
    print("saved", out)


if __name__ == "__main__":
    main()
