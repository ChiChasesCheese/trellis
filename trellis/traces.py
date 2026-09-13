"""Traces: the review history, pulled out of Anki and into the repo.

A Trace is the one thing in this project we do not write. Every card,
reading, drill and case is authored; a Trace is what happened when the
card was actually shown on a train platform, and only Anki knows it.

`trellis pull` is the only code that talks to Anki about it. It writes
`traces/<domain>.json` and stops. Everything downstream — Hold, the
Brief, the Feed, aimed scaffolding — reads that file and has never heard
of AnkiConnect. That is deliberate, and the reasons are in
docs/adr/0004-anki-is-a-source-not-the-source-of-truth.md: it makes the
loop work offline, on a phone-cloned repo, in CI, and in tests against a
fixture instead of a mock HTTP server.

The file is small (one object per card), stable in key order, and
committed, so `git log traces/` is a record of a subject being learned.

Mapping a note back to a card
-----------------------------
Anki notes carry `id::<card-id>` as a tag, written by `build`. A note
GUID is a hash of the card id and cannot be reversed; a tag can be read
straight back. Cards imported before the tag existed simply do not map,
and `pull` says how many — the repair is one `trellis anki-push`.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

TRACES_DIRNAME = "traces"
ID_TAG_PREFIX = "id::"

# Anki's card.type, which is what says whether a card is currently in
# trouble regardless of the interval it used to have.
TYPE_NEW, TYPE_LEARNING, TYPE_REVIEW, TYPE_RELEARNING = 0, 1, 2, 3


@dataclass
class Trace:
    """One card's review history, as Anki recorded it."""

    card_id: str
    reps: int = 0
    lapses: int = 0
    interval: int = 0          # days the scheduler currently trusts
    ease: float = 0.0          # factor/1000, e.g. 2.5
    type: int = TYPE_NEW
    due: int = 0
    last_review: int = 0       # epoch ms, 0 when unknown
    # FSRS, when the collection has it enabled. Absent on SM-2.
    difficulty: float | None = None
    stability: float | None = None

    @property
    def seen(self) -> bool:
        return self.reps > 0

    @property
    def lapsed_recently(self) -> bool:
        """In relearning right now: whatever this card's interval says,
        it is not held today."""
        return self.type == TYPE_RELEARNING


@dataclass
class TraceFile:
    domain: str
    pulled_at: str
    traces: dict[str, Trace]
    unmapped: int = 0          # Anki notes carrying no id:: tag

    @property
    def age_days(self) -> float | None:
        try:
            when = datetime.fromisoformat(self.pulled_at)
        except ValueError:
            return None
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - when).total_seconds() / 86400


def traces_path(root: str | Path, domain: str) -> Path:
    return Path(root) / TRACES_DIRNAME / f"{domain}.json"


def card_id_from_tags(tags: list[str]) -> str | None:
    for tag in tags:
        if tag.startswith(ID_TAG_PREFIX):
            return tag[len(ID_TAG_PREFIX):]
    return None


def save_traces(path: str | Path, file: TraceFile) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "domain": file.domain,
        "pulled_at": file.pulled_at,
        "unmapped": file.unmapped,
        # sorted so a pull that changed nothing produces no diff
        "traces": {k: _compact(asdict(file.traces[k]))
                   for k in sorted(file.traces)},
    }
    path.write_text(json.dumps(body, indent=1, sort_keys=False) + "\n",
                    encoding="utf-8")
    return path


def _compact(row: dict) -> dict:
    """Drop the fields Anki did not give us, so an SM-2 collection does
    not commit a screenful of nulls."""
    return {k: v for k, v in row.items()
            if k != "card_id" and v is not None and v != 0}


def load_traces(path: str | Path) -> TraceFile | None:
    """Read a trace file, or None if the loop has never been run for this
    domain. Absence is the normal state on a fresh clone, not an error."""
    path = Path(path)
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    traces = {
        card_id: Trace(card_id=card_id, **row)
        for card_id, row in raw.get("traces", {}).items()
    }
    return TraceFile(
        domain=raw.get("domain", path.stem),
        pulled_at=raw.get("pulled_at", ""),
        traces=traces,
        unmapped=raw.get("unmapped", 0),
    )


def now_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
