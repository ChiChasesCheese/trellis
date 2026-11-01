"""Retire the old LeetCode Tops fragment cards (3-6 per problem) from the topic decks 01-17, keeping their history.

    uv run python research/leetcode-tops/archive_old.py [--dry-run]

Notes tagged `leetcode-tops::<topic branch>::...` move to `LeetCode Tops::99 旧卡归档（零碎小卡，已暂停）`, their cards are
suspended, and the tag prefix becomes `leetcode-tops-old::`, so `anki-push` of the new skeleton never pulls them back.
The Amazon and curated-list branches (amazon-a, amazon-b, amazon-recent-custom, select) are not touched.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

BRANCHES = ["arrays-hashing", "two-pointers", "sliding-window", "stack", "binary-search", "linked-list", "trees", "tries",
            "heap-priority-queue", "backtracking", "graphs", "dp-1d", "dp-2d", "greedy", "intervals", "math-geometry",
            "bit-manipulation"]
ARCHIVE = "LeetCode Tops::99 旧卡归档（零碎小卡，已暂停）"


def call(action: str, **params):
    for _ in range(30):
        try:
            r = json.load(urllib.request.urlopen("http://127.0.0.1:8765", json.dumps(
                {"action": action, "version": 6, "params": params}).encode(), timeout=120))
        except OSError:
            time.sleep(2)
            continue
        if r.get("error") and "lifecycle" in str(r["error"]):
            time.sleep(2)
            continue
        if r.get("error"):
            raise RuntimeError(f"{action}: {r['error']}")
        return r["result"]
    raise SystemExit("AnkiConnect busy")


def main(dry: bool) -> None:
    total = 0
    for b in BRANCHES:
        notes = call("findNotes", query=f"tag:leetcode-tops::{b}::*")
        if not notes:
            continue
        info = call("notesInfo", notes=notes)
        cards = [c for n in info for c in n["cards"]]
        total += len(notes)
        print(f"{b}: {len(notes)} notes, {len(cards)} cards")
        if dry:
            continue
        call("createDeck", deck=ARCHIVE)
        call("changeDeck", cards=cards, deck=ARCHIVE)
        call("suspend", cards=cards)
        for n in info:
            old = [t for t in n["tags"] if t.startswith("leetcode-tops::")]
            if old:
                call("removeTags", notes=[n["noteId"]], tags=" ".join(old))
                call("addTags", notes=[n["noteId"]], tags=" ".join("leetcode-tops-old::" + t.split("::", 1)[1] for t in old))
    print(total, "notes", "would be archived" if dry else "archived")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
