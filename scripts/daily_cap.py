"""One budget for new cards across every Anki deck, and reviews before new cards. Dry run by default.

    uv run python scripts/daily_cap.py            # show the budget and what would change
    uv run python scripts/daily_cap.py --apply    # write the presets through AnkiConnect, then sync

The budget lives in sources/local/plan/config.json:

    "caps": {"total": 100, "mix": "reviews-first",
             "decks": {"1 今日计划": 30, "2 今日算法": 10, ...},      # new cards a day per top-level deck
             "zero_under": ["📦 其他"]}                              # every preset used below these decks gets 0

Any top-level deck that is not listed gets 0, so the listed numbers are the whole day (they must sum to `total`).
A deck's limit is its preset's `new.perDay`; the preset is also set to show reviews before new cards, so the cap is
a ceiling: on a short day the reviews are done first and fewer new cards are seen. Anki has no collection-wide limit,
and opening a sub-deck directly applies that sub-deck's own count, so this is a budget, not a lock.

Other scripts set presets too (study_plan, quick_plan, company_deck, anki-align). Run this last — study_plan's
`daily` calls it at its end — so the budget wins every morning. The previous values are saved once per day in
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
    wanted_mix = MIX[caps.get("mix", "reviews-first")]
    budget: dict[str, int] = caps["decks"]
    if sum(budget.values()) != caps["total"]:
        print(f"warning: the listed decks sum to {sum(budget.values())}, not {caps['total']}", file=sys.stderr)
    names = anki("deckNames")
    tops = sorted({d.split("::")[0] for d in names})
    plan: dict[int, tuple[dict, int, str]] = {}          # preset id -> (config, new per day, a deck that uses it)
    for top in tops:
        conf = anki("getDeckConfig", deck=top)
        n = budget.get(top, 0)
        prev = plan.get(conf["id"])
        plan[conf["id"]] = (conf, max(n, prev[1]) if prev else n, prev[2] if prev and prev[1] >= n else top)
    for parent in caps.get("zero_under", []):
        for deck in names:
            if deck.startswith(parent + "::"):
                conf = anki("getDeckConfig", deck=deck)
                plan.setdefault(conf["id"], (conf, 0, deck))
    backup = ROOT / f"sources/local/plan/preset_backup-{datetime.date.today()}.json"
    if apply and not backup.exists():
        backup.write_text(json.dumps({str(i): {"name": c["name"], "new": c["new"]["perDay"], "newMix": c.get("newMix")}
                                      for i, (c, _, _) in plan.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
    changed = 0
    for conf, n, deck in sorted(plan.values(), key=lambda t: (-t[1], t[2])):
        before = (conf["new"]["perDay"], conf.get("newMix"))
        if before != (n, wanted_mix):
            changed += 1
            if n or before[0]:
                print(f"  {deck[:34]:34} new/day {before[0]:>5} -> {n:<4}" + ("" if before[1] == wanted_mix else "  reviews first"))
            if apply:
                conf["new"]["perDay"], conf["newMix"] = n, wanted_mix
                anki("saveDeckConfig", config=conf)
    print(f"budget {sum(v for _, v, _ in plan.values())} new cards a day over {sum(1 for _, v, _ in plan.values() if v)} decks; "
          f"{changed} preset(s) {'changed' if apply else 'would change'}")
    if apply and changed:
        anki("sync")
    return changed


def main() -> int:
    apply_caps("--apply" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
