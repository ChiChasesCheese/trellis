"""A budget for new cards on the focus decks, a normal pace on the rest, nothing under the idle decks. Dry run by default.

    uv run python scripts/daily_cap.py            # show what would change
    uv run python scripts/daily_cap.py --apply    # write the presets through AnkiConnect, then sync

The settings live in sources/local/plan/config.json:

    "caps": {"total": 100, "mix": "reviews-first",
             "decks": {"系统设计": 30, "2 算法模式识别": 10, ...},   # the focus decks: their numbers must sum to `total`
             "open": {"Sr 工作方法": 20, ...},                   # other decks: every card stays available at a normal pace
             "open_mix": "new-first",                            # how the open decks order new cards and reviews
             "zero": ["算法知识树（灵神题单）"],                  # top-level decks whose new cards come only through a daily deck
             "zero_under": ["📦 其他"]}                          # every preset used below these decks gets 0

A top-level deck that is not named anywhere is left exactly as it is (a planner may own it, e.g. 碎片速刷).
A deck's limit is its preset's `new.perDay`. Focus decks show reviews before new cards, so their budget is a ceiling:
on a short day the reviews are done first and fewer new cards are seen. Anki has no collection-wide limit, and opening
a sub-deck directly applies that sub-deck's own count, so this is a budget, not a lock.

Other scripts set presets too (study_plan, quick_plan, company_deck, anki-align). Run this last — study_plan's
`daily` calls it at its end — so these numbers win every morning. The previous values are saved once per day in
sources/local/plan/preset_backup-<date>.json.
"""
from __future__ import annotations

import datetime
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "sources/local/plan/config.json"
MIX = {"mixed": 0, "reviews-first": 1, "new-first": 2}


def anki(action: str, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", json.dumps({"action": action, "version": 6, "params": params}).encode())
    for _ in range(60):
        out = json.load(urllib.request.urlopen(req, timeout=300))
        if out["error"] and "lifecycle" in str(out["error"]):
            time.sleep(2)
            continue
        if out["error"]:
            raise RuntimeError(out["error"])
        return out["result"]
    raise RuntimeError("Anki stayed busy for two minutes")


def apply_caps(apply: bool) -> int:
    caps = json.loads(CONFIG.read_text(encoding="utf-8")).get("caps")
    if not caps:
        print("no `caps` in", CONFIG)
        return 0
    focus_mix = MIX[caps.get("mix", "reviews-first")]
    open_mix = MIX[caps.get("open_mix", "new-first")]
    budget: dict[str, int] = caps["decks"]
    if sum(budget.values()) != caps["total"]:
        print(f"warning: the focus decks sum to {sum(budget.values())}, not {caps['total']}", file=sys.stderr)
    names = anki("deckNames")
    tops = {d.split("::")[0] for d in names}
    plan: dict[int, tuple[dict, int, str, int]] = {}     # preset id -> (config, new per day, a deck that uses it, mix)
    wanted = [(d, n, focus_mix) for d, n in budget.items()] + [(d, n, open_mix) for d, n in caps.get("open", {}).items()] \
        + [(d, 0, focus_mix) for d in caps.get("zero", [])]
    for deck, n, mix in wanted:
        if deck not in tops:
            print(f"warning: no deck named {deck!r}", file=sys.stderr)
            continue
        conf = anki("getDeckConfig", deck=deck)
        if conf["id"] in plan and plan[conf["id"]][1] != n:
            print(f"warning: {deck!r} shares a preset with {plan[conf['id']][2]!r}; keeping {plan[conf['id']][1]}", file=sys.stderr)
            continue
        plan[conf["id"]] = (conf, n, deck, mix)
    for parent in caps.get("zero_under", []):
        for deck in [parent, *[d for d in names if d.startswith(parent + "::")]]:
            conf = anki("getDeckConfig", deck=deck)
            plan.setdefault(conf["id"], (conf, 0, deck, focus_mix))
    backup = ROOT / f"sources/local/plan/preset_backup-{datetime.date.today()}.json"
    if apply and not backup.exists():
        backup.write_text(json.dumps({str(i): {"name": c["name"], "new": c["new"]["perDay"], "newMix": c.get("newMix")}
                                      for i, (c, _, _, _) in plan.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
    changed = 0
    for conf, n, deck, mix in sorted(plan.values(), key=lambda t: (-t[1], t[2])):
        before = (conf["new"]["perDay"], conf.get("newMix"))
        if before != (n, mix):
            changed += 1
            if n or before[0]:
                print(f"  {deck[:34]:34} new/day {before[0]:>5} -> {n:<4}")
            if apply:
                conf["new"]["perDay"], conf["newMix"] = n, mix
                anki("saveDeckConfig", config=conf)
    focus = sum(budget.values())
    print(f"focus budget {focus} new cards a day over {len(budget)} decks; {len(caps.get('open', {}))} open decks at their own pace; "
          f"{changed} preset(s) {'changed' if apply else 'would change'}")
    if apply and changed:
        anki("sync")
    return changed


def main() -> int:
    apply_caps("--apply" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
