"""Snapshot: where every published node stands on one date (ADR 0014).

The only thing that leaves the machine of what Anki knows. It holds per-node aggregates and per-day review counts,
never a card id with a time, never a timestamp finer than a day. The Traces it is computed from stay local.

Reach counts a card as studied when its own Anki card has been reviewed, or when the test question built on it has:
a test question's back is the card itself (CONTEXT.md, "Reach").
"""

from __future__ import annotations

import hashlib
import json
from datetime import date as _date
from pathlib import Path
from typing import Callable

from .anki import DEFAULT_URL, _weakest, trace_from_row
from .atlas import PublishedDomain
from .hold import assess
from .traces import Trace, card_id_from_tags

SCHEMA = "trellis.snapshot/1"
SNAPSHOTS_DIRNAME = "snapshots"

# The test sets (scripts/card_tests.py SETS): a question per source card, tagged `<tag>::id::<tag>-<sha1[:10]>` with
# the sha1 of the source card's id. scripts/daily_quiz.py's `recog` set is not here: its question id hashes the
# question text and not a source card id, so no rule maps it back to a card (it is listed as unmapped).
TEST_SETS: dict[str, dict] = {
    "lld": {"tag": "tlld"},
    "ai": {"tag": "tai"},
}

BATCH = 500


def question_id(tag: str, source_id: str) -> str:
    return f"{tag}-" + hashlib.sha1(source_id.encode()).hexdigest()[:10]


def level(studied: int | None, cards: int) -> int | None:
    """The shade: -1 no cards, 0 none studied, 1 under 25%, 2 under 50%, 3 under 75%, 4 under 100%, 5 all."""
    if cards == 0:
        return -1
    if studied is None:
        return None
    if studied <= 0:
        return 0
    if studied >= cards:
        return 5
    for step, shade in ((75, 4), (50, 3), (25, 2)):
        if studied * 100 >= step * cards:
            return shade
    return 1


def _traces(call: Callable, url: str, query: str, key_of: Callable[[list[str]], str | None]) -> dict[str, Trace]:
    """Trace per key for the notes a query finds; a note's cards fold into one, as `anki.pull` does."""
    note_ids = call("findNotes", url, query=query)
    owners: dict[int, str] = {}
    for i in range(0, len(note_ids), BATCH):
        for note in call("notesInfo", url, notes=note_ids[i:i + BATCH]):
            key = key_of(note.get("tags") or [])
            if key is None:
                continue
            for cid in note.get("cards") or []:
                owners[cid] = key
    traces: dict[str, Trace] = {}
    ids = list(owners)
    for i in range(0, len(ids), BATCH):
        for row in call("cardsInfo", url, cards=ids[i:i + BATCH]):
            owner = owners.get(row.get("cardId"))
            if owner is None:
                continue
            trace = trace_from_row(owner, row)
            traces[owner] = trace if owner not in traces else _weakest(traces[owner], trace)
    return traces


def read_anki(call: Callable, url: str = DEFAULT_URL) -> tuple[dict[str, Trace], dict[str, dict[str, Trace]], dict[str, int]]:
    """(own traces by card id, test-question traces by set name then question id, reviews per day)."""
    own = _traces(call, url, "tag:id::*", card_id_from_tags)
    tests = {}
    for name, cfg in TEST_SETS.items():
        prefix = f"{cfg['tag']}::id::"
        tests[name] = _traces(call, url, f"tag:{prefix}*",
                              lambda tags, p=prefix: next((t[len(p):] for t in tags if t.startswith(p)), None))
    raw = call("getNumCardsReviewedByDay", url)
    pairs = raw.items() if isinstance(raw, dict) else raw
    daily = {str(d): int(n) for d, n in pairs}
    return own, tests, daily


def card_traces(cards, own: dict[str, Trace], tests: dict[str, dict[str, Trace]]) -> dict[str, Trace]:
    """One Trace per published card: its own when it has been reviewed, else its test question's."""
    out: dict[str, Trace] = {}
    for card in cards:
        mine = own.get(card.id)
        if mine is not None and mine.reps > 0:
            out[card.id] = mine
            continue
        for name, cfg in TEST_SETS.items():
            t = tests.get(name, {}).get(question_id(cfg["tag"], card.id))
            if t is not None and t.reps > 0:
                out[card.id] = Trace(card_id=card.id, reps=t.reps, lapses=t.lapses, interval=t.interval,
                                     ease=t.ease, type=t.type, due=t.due)
                break
        else:
            if mine is not None:
                out[card.id] = mine
    return out


def domain_standing(pub: PublishedDomain, traces: dict[str, Trace]) -> dict:
    """One domain's block of a Snapshot."""
    sk = pub.skeleton
    a = assess(sk, pub.cards, traces)
    leaf = {s.node.id: s for s in a.leaves}
    cards: dict[str, int] = {}
    studied: dict[str, int] = {}
    for card in pub.cards:
        reached = card.id in traces and traces[card.id].reps > 0
        for n in sk.by_id[card.node].path():
            cards[n.id] = cards.get(n.id, 0) + 1
            if reached:
                studied[n.id] = studied.get(n.id, 0) + 1
    nodes: dict[str, dict] = {}
    for node in sk.walk():
        if node.id not in pub.nodes:
            continue
        entry: dict = {}
        if cards.get(node.id):
            entry["cards"] = cards[node.id]
        if studied.get(node.id):
            entry["studied"] = studied[node.id]
        s = leaf.get(node.id)
        hold = s.hold if s is not None else a.node_hold.get(node.id)
        if hold is not None:
            entry["hold"] = round(hold, 3)
        if s is not None:
            flags = [f for f, on in (("weak", s.weak), ("uncovered", s.uncovered),
                                     ("sealed", s.sealed), ("settling", s.settling)) if on]
            if flags:
                entry["flags"] = flags
        if entry:
            nodes[node.id] = entry
    block: dict = {"cards": len(pub.cards)}
    done = sum(1 for c in pub.cards if c.id in traces and traces[c.id].reps > 0)
    if done:
        block["studied"] = done
    if a.hold is not None:
        block["hold"] = round(a.hold, 3)
    block["nodes"] = nodes
    return block


def build_snapshot(published: dict[str, PublishedDomain], call: Callable, date: str | None = None,
                   url: str = DEFAULT_URL) -> dict:
    own, tests, daily = read_anki(call, url)
    domains = {}
    for domain, pub in published.items():
        domains[domain] = domain_standing(pub, card_traces(pub.cards, own, tests))
    return {"schema": SCHEMA, "date": date or _date.today().isoformat(),
            "domains": domains, "daily": dict(sorted(daily.items()))}


def dumps(snapshot: dict) -> str:
    """JSON with one line per node, so a day's diff in git reads node by node."""
    def j(x) -> str:
        return json.dumps(x, ensure_ascii=False, separators=(",", ":"))
    lines = ["{", f'"schema":{j(snapshot["schema"])},', f'"date":{j(snapshot["date"])},', '"domains":{']
    blocks = []
    for domain, block in snapshot["domains"].items():
        head = {k: v for k, v in block.items() if k != "nodes"}
        rows = ",\n".join(f"{j(nid)}:{j(entry)}" for nid, entry in block["nodes"].items())
        blocks.append(f'{j(domain)}:{j(head)[:-1]},"nodes":{{\n{rows}\n}}}}')
    lines.append(",\n".join(blocks))
    lines.append("},")
    lines.append(f'"daily":{j(snapshot["daily"])}')
    lines.append("}")
    return "\n".join(lines) + "\n"


def write_snapshot(root: str | Path, snapshot: dict) -> Path:
    path = Path(root) / SNAPSHOTS_DIRNAME / f"{snapshot['date']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(snapshot), encoding="utf-8")
    return path


def load_snapshots(root: str | Path) -> list[dict]:
    """Every snapshot file, oldest first."""
    folder = Path(root) / SNAPSHOTS_DIRNAME
    out = []
    for path in sorted(folder.glob("*.json")) if folder.exists() else []:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if data.get("schema") == SCHEMA:
            out.append(data)
    return sorted(out, key=lambda s: s["date"])
