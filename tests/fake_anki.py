"""A collection that imports real packages, remembers reviews, and deals a day.

Not a script of canned answers. It opens the .apkg `build` really produced and
keeps what it finds the way Anki's importer does — a note it already has
keeps its scheduling *and its position*, only its tags are rewritten — and it
answers the AnkiConnect actions Trellis uses in the shapes the real one was
observed to return (2026-09-19, Anki 26.8.1).

`today()` is the part a person would see: which cards a deck shows, in what
order, under the options the deck has been given. It follows the v3
scheduler's rules for the options Trellis sets and no others.
"""

from __future__ import annotations

import copy
import json
import sqlite3
import tempfile
import zipfile
from pathlib import Path

DEFAULT_PRESET = {
    "id": 1, "name": "Default", "newMix": 0, "newGatherPriority": 0, "newSortOrder": 0,
    "new": {"perDay": 50, "order": 0}, "rev": {"perDay": 50},
}


class FakeAnki:
    def __init__(self):
        self.notes: dict[str, dict] = {}     # guid -> {noteId, tags}
        self.cards: dict[int, dict] = {}     # cardId -> row
        self.presets: dict[int, dict] = {1: copy.deepcopy(DEFAULT_PRESET)}
        self.deck_preset: dict[str, int] = {}
        self.calls: list[str] = []

    # -- what AnkiConnect answers ------------------------------------------------
    def __call__(self, action, url=None, **params):
        self.calls.append(action)
        handler = getattr(self, f"_{action}", None)
        if handler is None:
            raise AssertionError(f"Trellis must not call {action}")
        return handler(**params)

    def _sync(self):
        return None

    def _importPackage(self, path):
        with zipfile.ZipFile(path) as z, tempfile.TemporaryDirectory() as tmp:
            z.extract("collection.anki2", tmp)
            db = sqlite3.connect(Path(tmp) / "collection.anki2")
            decks = {int(k): v["name"] for k, v in
                     json.loads(db.execute("select decks from col").fetchone()[0]).items()}
            rows = db.execute("select n.guid, n.tags, c.did, c.due from notes n "
                              "join cards c on c.nid = n.id").fetchall()
            db.close()
        for guid, tags, did, due in rows:
            known = guid in self.notes
            note = self.notes.setdefault(guid, {"noteId": len(self.notes) + 1, "tags": []})
            note["tags"] = tags.split()
            if not known:
                cid = note["noteId"] * 10
                self.cards[cid] = {"cardId": cid, "note": note["noteId"], "deckName": decks[did],
                                   "reps": 0, "lapses": 0, "interval": 0, "factor": 2500,
                                   "type": 0, "queue": 0, "due": due, "mod": 0}
        return True

    def _findNotes(self, query):
        prefix = query.removeprefix("tag:").removesuffix("*")
        return [n["noteId"] for n in self.notes.values()
                if any(t.startswith(prefix) for t in n["tags"])]

    def _notesInfo(self, notes):
        wanted = set(notes)
        return [{"noteId": n["noteId"], "tags": n["tags"], "cards": [n["noteId"] * 10]}
                for n in self.notes.values() if n["noteId"] in wanted]

    def _cardsInfo(self, cards):
        return [dict(self.cards[c]) for c in cards]

    def _findCards(self, query):
        if "-deck:" in query:
            return []                        # align: every card is already in its deck
        if query.startswith('deck:"'):
            return [c["cardId"] for c in self._under(query[6:-1])]
        raise AssertionError(f"unexpected search {query!r}")

    def _deckNames(self):
        names = set()
        for c in self.cards.values():
            parts = c["deckName"].split("::")
            names |= {"::".join(parts[:i]) for i in range(1, len(parts) + 1)}
        return sorted(names)

    def _getDeckConfig(self, deck):
        return copy.deepcopy(self.presets[self.deck_preset.get(deck, 1)])

    def _cloneDeckConfigId(self, name, cloneFrom=1):
        new_id = max(self.presets) + 1
        self.presets[new_id] = {**copy.deepcopy(self.presets[cloneFrom]), "id": new_id, "name": name}
        return new_id

    def _saveDeckConfig(self, config):
        self.presets[config["id"]] = copy.deepcopy(config)
        return True

    def _setDeckConfigId(self, decks, configId):
        for deck in decks:
            self.deck_preset[deck] = configId
        return True

    def _setSpecificValueOfCard(self, card, keys, newValues, warning_check=False):
        if card not in self.cards:
            return [[False, f"Card was not found: {card}"]]
        self.cards[card].update(zip(keys, newValues))
        return [True]

    def _multi(self, actions):
        return [self(a["action"], **a.get("params", {})) for a in actions]

    # -- what a person with a phone does -------------------------------------------
    def card_of(self, card_id: str) -> dict:
        note = next(n for n in self.notes.values() if f"id::{card_id}" in n["tags"])
        return self.cards[note["noteId"] * 10]

    def review(self, card_id: str, *, reps: int, lapses: int = 0, interval: int, type: int = 2):
        self.card_of(card_id).update(reps=reps, lapses=lapses, interval=interval,
                                     type=type, queue=2, due=20000 + interval)

    def tagged(self, tag: str) -> list[str]:
        return sorted(self._id(n) for n in self.notes.values() if tag in n["tags"])

    def today(self, deck: str) -> list[str]:
        """The card ids `deck` would show today, in order. Every reviewed
        card counts as due, which is the hard case for a Pace."""
        cfg = self.presets[self.deck_preset.get(deck, 1)]
        new = [c for c in self._under(deck) if c["type"] == 0]
        if cfg["newGatherPriority"] == 1:                      # lowest position
            new.sort(key=lambda c: c["due"])
        else:                                                  # deck by deck
            new.sort(key=lambda c: (c["deckName"], c["due"]))
        new = new[: cfg["new"]["perDay"]]
        due = [c for c in self._under(deck) if c["type"] != 0][: cfg["rev"]["perDay"]]
        if cfg["newMix"] == 2:
            shown = new + due
        elif cfg["newMix"] == 1:
            shown = due + new
        else:
            shown = [c for pair in zip(new, due) for c in pair] + new[len(due):] + due[len(new):]
        by_note = {n["noteId"]: self._id(n) for n in self.notes.values()}
        return [by_note[c["note"]] for c in shown]

    def _under(self, deck):
        return [c for c in self.cards.values()
                if c["deckName"] == deck or c["deckName"].startswith(deck + "::")]

    @staticmethod
    def _id(note) -> str:
        return next(t for t in note["tags"] if t.startswith("id::")).removeprefix("id::")
