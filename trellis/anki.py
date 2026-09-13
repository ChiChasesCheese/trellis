"""Align a live Anki collection's deck tree to the current skeleton.

Anki identifies decks by name and its .apkg importer never moves existing
cards, so any skeleton restructuring (renamed branch, split leaf, new
ordinal) strands previously imported cards in stale decks. This module
talks to the AnkiConnect add-on (desktop Anki, add-on code 2055492159)
and converges the collection:

  1. every card carries a stable hierarchical tag (domain::node::path,
     rewritten on each import), so cards are moved to the deck the
     current skeleton derives for their node;
  2. decks under the domain root that end up with zero cards are deleted.

Run AFTER importing the freshly built .apkg (the import updates tags),
then sync to AnkiWeb so mobile picks it up.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Callable

from .skeleton import Skeleton
from .traces import (TYPE_RELEARNING, Trace, TraceFile, card_id_from_tags,
                     now_stamp)

DEFAULT_URL = "http://127.0.0.1:8765"


class AnkiConnectError(RuntimeError):
    pass


def invoke(action: str, url: str = DEFAULT_URL, **params) -> object:
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except OSError as exc:
        raise AnkiConnectError(
            f"cannot reach AnkiConnect at {url} — is desktop Anki running "
            "with the AnkiConnect add-on (code 2055492159)?"
        ) from exc
    if data.get("error"):
        raise AnkiConnectError(data["error"])
    return data["result"]


def align(skeleton: Skeleton, call: Callable = invoke, url: str = DEFAULT_URL) -> dict:
    """Move mis-decked cards and drop empty stale decks. Returns
    {'moved': int, 'deleted': [names]}."""
    moved = 0
    for node in skeleton.walk():
        deck = skeleton.deck_name(node)
        tag = skeleton.domain + "::" + node.id.replace(".", "::")
        # tag:X also matches child tags, so exclude them — a card belongs
        # to exactly the deck of the node its own tag names
        query = f'tag:{tag} -tag:{tag}::* -deck:"{deck}"'
        card_ids = call("findCards", url, query=query)
        if card_ids:
            call("createDeck", url, deck=deck)
            call("changeDeck", url, cards=card_ids, deck=deck)
            moved += len(card_ids)

    root = skeleton.title
    stale = []
    for name in call("deckNames", url):
        if name == root or name.startswith(root + "::"):
            # deck:X matches subdecks too, so empty means the whole
            # subtree is empty and safe to delete
            if not call("findCards", url, query=f'deck:"{name}"'):
                stale.append(name)
    if stale:
        call("deleteDecks", url, decks=stale, cardsToo=True)
    return {"moved": moved, "deleted": stale}


def pull(
    skeleton: Skeleton,
    call: Callable = invoke,
    url: str = DEFAULT_URL,
) -> TraceFile:
    """Read this domain's review history back out of Anki.

    This is the only function in Trellis that asks Anki a question. It
    writes nothing and decides nothing: it returns Traces, and
    `trellis/hold.py` does the thinking, from a file, offline. See
    docs/adr/0004.

    A note can own several cards (every cloze deletion is one), and the
    note is only as well held as its weakest card — so reps and lapses
    sum across a note's cards while the interval takes the minimum.
    """
    note_ids = call("findNotes", url, query=f"tag:{skeleton.domain}::*")
    if not note_ids:
        return TraceFile(domain=skeleton.domain, pulled_at=now_stamp(), traces={})

    notes = call("notesInfo", url, notes=note_ids)
    card_ids: list[int] = []
    card_owner: dict[int, str] = {}
    unmapped = 0
    for note in notes:
        card_id = card_id_from_tags(note.get("tags") or [])
        if card_id is None:
            # Imported before `build` started writing the id:: tag. One
            # `trellis anki-push` repairs every one of them.
            unmapped += 1
            continue
        for cid in note.get("cards") or []:
            card_ids.append(cid)
            card_owner[cid] = card_id

    traces: dict[str, Trace] = {}
    for row in call("cardsInfo", url, cards=card_ids) if card_ids else []:
        owner = card_owner.get(row.get("cardId"))
        if owner is None:
            continue
        existing = traces.get(owner)
        trace = Trace(
            card_id=owner,
            reps=int(row.get("reps") or 0),
            lapses=int(row.get("lapses") or 0),
            interval=int(row.get("interval") or 0),
            ease=(row.get("factor") or 0) / 1000,
            type=int(row.get("type") or 0),
            due=int(row.get("due") or 0),
            last_review=int(row.get("mod") or 0),
        )
        traces[owner] = trace if existing is None else _weakest(existing, trace)

    return TraceFile(domain=skeleton.domain, pulled_at=now_stamp(),
                     traces=traces, unmapped=unmapped)


def _weakest(a: Trace, b: Trace) -> Trace:
    """Fold a note's second card into the first: the note is held only as
    well as the card that holds worst."""
    return Trace(
        card_id=a.card_id,
        reps=a.reps + b.reps,
        lapses=a.lapses + b.lapses,
        interval=min(a.interval, b.interval),
        ease=min(a.ease, b.ease) or max(a.ease, b.ease),
        # relearning on any card means the note is not held today
        type=max(a.type, b.type) if TYPE_RELEARNING in (a.type, b.type)
        else min(a.type, b.type),
        due=min(a.due, b.due),
        last_review=max(a.last_review, b.last_review),
    )


def push(
    skeleton: Skeleton,
    apkg: Path,
    call: Callable = invoke,
    url: str = DEFAULT_URL,
) -> dict:
    """Publish a freshly built deck into the running Anki and out to AnkiWeb.

    The order matters and is the whole point of having this as one
    command. Syncing *first* pulls whatever the phone reviewed since the
    last push, so the import lands on top of current scheduling instead
    of a stale collection. Only then is the package imported, aligned to
    the skeleton's decks, and pushed back out — so the phone ends up with
    the new cards and its own review history intact.
    """
    steps: list[str] = []

    call("sync", url)
    steps.append("pulled from AnkiWeb")

    call("importPackage", url, path=str(Path(apkg).resolve()))
    steps.append(f"imported {Path(apkg).name}")

    moved = align(skeleton, call=call, url=url)
    steps.append(f"moved {moved['moved']} card(s), removed "
                 f"{len(moved['deleted'])} stale deck(s)")

    call("sync", url)
    steps.append("pushed to AnkiWeb")

    return {"steps": steps, **moved}
