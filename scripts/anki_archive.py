"""Archive a set of Anki cards without deleting them: suspend, tag, move to 📦 其他::归档::<name>. Reversible.

    uv run python scripts/anki_archive.py 'deck:LeetCode::Patterns' 'LeetCode 旧英文填空'           # report
    uv run python scripts/anki_archive.py 'deck:LeetCode::Patterns' 'LeetCode 旧英文填空' --apply
    uv run python scripts/anki_archive.py --restore 'LeetCode 旧英文填空' --apply                  # undo: back to the old decks, unsuspended

The decks each card came from are recorded in sources/local/audit/archive/<name>.json, so a restore puts every card
back where it was. Cards already suspended before archiving stay suspended after a restore. Chi's rule: nothing is
deleted by a script; he deletes decks himself.
"""
from __future__ import annotations

import collections
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "sources/local/audit/archive"
TAG = "archived"


def anki(action: str, **params):
    """One AnkiConnect call; waits while Anki is syncing ("Collection lifecycle operation is active")."""
    import time
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


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    STORE.mkdir(parents=True, exist_ok=True)
    if "--restore" in sys.argv:
        record = json.loads((STORE / f"{args[0]}.json").read_text(encoding="utf-8"))
        by_deck: dict[str, list[int]] = collections.defaultdict(list)
        for cid, deck in record["decks"].items():
            by_deck[deck].append(int(cid))
        print(f"restore {len(record['decks'])} cards to {len(by_deck)} deck(s)")
        if apply:
            for deck, cids in by_deck.items():
                anki("changeDeck", cards=cids, deck=deck)
            anki("unsuspend", cards=[int(c) for c in record["decks"] if int(c) not in set(record["was_suspended"])])
            anki("removeTags", notes=record["notes"], tags=TAG)
            anki("sync")
        return 0
    if len(args) != 2:
        print(__doc__)
        return 2
    query, name = args
    cards = anki("findCards", query=query)
    info = anki("cardsInfo", cards=cards)
    decks = {str(c["cardId"]): c["deckName"] for c in info}
    notes = sorted({c["note"] for c in info})
    was_suspended = [c["cardId"] for c in info if c["queue"] == -1]
    target = f"📦 其他::归档::{name}"
    print(f"{len(cards)} cards / {len(notes)} notes from {len(set(decks.values()))} deck(s) -> {target}"
          f" ({len(was_suspended)} already suspended)")
    if apply and cards:
        (STORE / f"{name}.json").write_text(json.dumps({"query": query, "decks": decks, "notes": notes, "was_suspended": was_suspended},
                                                       ensure_ascii=False), encoding="utf-8")
        anki("createDeck", deck=target)
        anki("changeDeck", cards=cards, deck=target)
        anki("suspend", cards=cards)
        anki("addTags", notes=notes, tags=TAG)
        anki("sync")
        print("archived; restore with --restore", repr(name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
