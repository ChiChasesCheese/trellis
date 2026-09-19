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

from .skeleton import Skeleton, Study
from .traces import (TYPE_RELEARNING, Trace, TraceFile, card_id_from_tags,
                     now_stamp)

DEFAULT_URL = "http://127.0.0.1:8765"
# A note mirrored from a deck another tool owns; see trellis/adopt.py.
ADOPTED_TAG = "trellis::adopted"


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
        # to exactly the deck of the node its own tag names. An adopted
        # note was authored by another tool and stays in the deck that
        # tool put it in.
        query = f'tag:{tag} -tag:{tag}::* -tag:{ADOPTED_TAG} -deck:"{deck}"'
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


TYPE_NEW = 0
# Anki's own numbers for the options a Study sets (deck_config.proto, checked
# against Anki 26.8.1): gather new cards by lowest position, and show them in
# the order gathered.
GATHER_LOWEST_POSITION, SORT_AS_GATHERED = 1, 1
NEW_MIX = {"mixed": 0, "reviews-first": 1, "new-first": 2}
PRESET_PREFIX = "Trellis · "
BATCH = 100


def sequence_new(skeleton: Skeleton, ordered: list[str], call: Callable = invoke,
                 url: str = DEFAULT_URL) -> int:
    """Give every *new* card of this domain the position its card holds in
    `ordered` (card ids, first to last). Returns how many were moved.

    An import places a note it has never seen and leaves one it has where it
    was, so a collection drifts from the vault the first time anything is
    reordered, inserted, or declared core. This converges it. Only cards
    Anki still calls new are touched: once a card has been answered its
    `due` is a date the scheduler chose, and that is not ours to write.
    """
    place = {card_id: i for i, card_id in enumerate(ordered, start=1)}
    note_ids = call("findNotes", url, query=f"tag:{skeleton.domain}::*")
    if not note_ids:
        return 0
    wanted: dict[int, int] = {}
    for note in call("notesInfo", url, notes=note_ids):
        card_id = card_id_from_tags(note.get("tags") or [])
        if card_id in place and ADOPTED_TAG not in (note.get("tags") or []):
            for cid in note.get("cards") or []:
                wanted[cid] = place[card_id]
    moves = [(row["cardId"], wanted[row["cardId"]])
             for row in (call("cardsInfo", url, cards=list(wanted)) if wanted else [])
             if int(row.get("type") or 0) == TYPE_NEW and row.get("due") != wanted[row["cardId"]]]
    for start in range(0, len(moves), BATCH):
        results = call("multi", url, actions=[
            {"action": "setSpecificValueOfCard",
             "params": {"card": cid, "keys": ["due"], "newValues": [position]}}
            for cid, position in moves[start:start + BATCH]])
        failed = [r for r in results if r != [True]]
        if failed:
            raise AnkiConnectError(f"could not reposition {len(failed)} card(s): {failed[0]}")
    return len(moves)


def apply_study(skeleton: Skeleton, study: Study, call: Callable = invoke,
                url: str = DEFAULT_URL) -> str:
    """Put the domain's decks on a preset of their own that deals new cards
    by position, and carries the domain's Pace where it sets one. Returns a
    line saying what is now in force.

    The preset is cloned from whatever the domain's root deck was using, so
    everything Trellis has no opinion on — FSRS parameters, learning steps,
    timers — comes along unchanged; and the preset it was cloned from, which
    the rest of the collection usually shares, is never written to.
    """
    root = skeleton.title
    decks = [d for d in call("deckNames", url) if d == root or d.startswith(root + "::")]
    if not decks:
        return "no decks yet"
    name = PRESET_PREFIX + skeleton.title
    config = call("getDeckConfig", url, deck=root)
    if config["name"] != name:
        config = {**config, "id": call("cloneDeckConfigId", url, name=name, cloneFrom=config["id"]),
                  "name": name}
    wanted = {"newGatherPriority": GATHER_LOWEST_POSITION, "newSortOrder": SORT_AS_GATHERED}
    if study.mix is not None:
        wanted["newMix"] = NEW_MIX[study.mix]
    if any(config.get(k) != v for k, v in wanted.items()) \
            or (study.new_per_day is not None and config["new"]["perDay"] != study.new_per_day) \
            or (study.reviews_per_day is not None and config["rev"]["perDay"] != study.reviews_per_day):
        config.update(wanted)
        if study.new_per_day is not None:
            config["new"]["perDay"] = study.new_per_day
        if study.reviews_per_day is not None:
            config["rev"]["perDay"] = study.reviews_per_day
        call("saveDeckConfig", url, config=config)
    call("setDeckConfigId", url, decks=decks, configId=config["id"])

    if not study.sets_pace:
        return f"new cards dealt by position (preset '{name}')"
    limits = " + ".join(part for part in (
        f"{study.new_per_day} new" if study.new_per_day is not None else "",
        f"{study.reviews_per_day} review(s)" if study.reviews_per_day is not None else "") if part)
    said = ", ".join(part for part in (study.mix or "", f"{limits} a day" if limits else "") if part)
    return f"pace: {said} (preset '{name}')"


def push(
    skeleton: Skeleton,
    apkg: Path,
    call: Callable = invoke,
    url: str = DEFAULT_URL,
    ordered: list[str] | None = None,
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

    # The package numbered its cards, but only the ones this collection had
    # never seen took the number. Converge the rest, then make sure the decks
    # deal by that number at all (ADR 0010).
    if ordered is not None:
        steps.append(f"sequenced {sequence_new(skeleton, ordered, call=call, url=url)} new card(s)")
        steps.append(apply_study(skeleton, skeleton.study, call=call, url=url))

    call("sync", url)
    steps.append("pushed to AnkiWeb")

    return {"steps": steps, **moved}
