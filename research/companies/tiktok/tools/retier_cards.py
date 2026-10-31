"""Move each problem's cards to the folder and node of its current tier (index.json), in both decks.

    uv run python research/companies/tiktok/tools/retier_cards.py

A problem leaf is `<band>.<slug>` (band p1..p5 for tier A, b for tier B) and its cards live in `cards/<band>/`; after select_tiers.py changes a tier, this
moves the files and rewrites the `node:` line. Card ids do not contain the tier, so Anki keeps the review history and
anki-push only moves the cards to the other sub-deck.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
index = json.loads((ROOT / "research/companies/tiktok/index.json").read_text(encoding="utf-8"))
moved = 0
for vault in ("tiktok", "tiktok-drill"):
    cards = ROOT / "vault/interviews/core/leetcode" / vault / "cards"
    for slug, p in index.items():
        new = p.get("band") or p["tier"].lower()
        for old in ("a", "b", "c", "p1", "p2", "p3", "p4", "p5"):
            if old == new:
                continue
            for f in sorted((cards / old).glob(f"tlc-{slug}-*.md")):
                text = f.read_text(encoding="utf-8")
                if not re.search(rf"^node: {old}\.{re.escape(slug)}$", text, re.M):
                    continue  # another problem whose slug starts with this one
                (cards / new).mkdir(exist_ok=True)
                (cards / new / f.name).write_text(
                    re.sub(rf"^node: {old}\.", f"node: {new}.", text, count=1, flags=re.M), encoding="utf-8")
                f.unlink()
                moved += 1
print(moved, "card files moved")
