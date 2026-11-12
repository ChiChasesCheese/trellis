"""Chi's questions on his cards, answered.

Every note type ends with the fields Note and NoteAnswer (trellis/build.py). On the phone Chi writes what he does not
understand into Note, or only stars the card (Mark, tag `marked`). This script lists those cards and writes the
explanations, which docs/card-notes.md says how to write, back into NoteAnswer.

    uv run python scripts/card_notes.py pending [-o FILE]   # the cards waiting for an explanation, as JSON
    uv run python scripts/card_notes.py apply FILE          # [{"nid": ..., "answer": "<markdown>"}] -> NoteAnswer
    uv run python scripts/card_notes.py status

A card waits when its Note was written or changed since its last explanation, or when it is starred and has none.
sources/local/notes/answered.json keeps, per note id, the Note text each explanation answered.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from anki_refresh import call  # noqa: E402
from trellis.build import NOTE_FIELDS, _html  # noqa: E402

NOTE, ANSWER = NOTE_FIELDS
HOME = ROOT / "sources/local/notes"
STATE = HOME / "answered.json"
QUERY = f'"{NOTE}:_*" OR tag:marked'


def plain(field: str) -> str:
    """A field's HTML as readable text: line breaks kept, tags and scripts dropped."""
    s = re.sub(r"<(script|style)\b.*?</\1>", "", field, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>|</(p|div|li|tr|h\d|pre|summary)>", "\n", s, flags=re.I)
    s = html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ")
    return re.sub(r"\n\s*\n+", "\n\n", s).strip()


def key(note: str) -> str:
    """What an explanation answered: the Note's text, or the star alone."""
    return hashlib.sha1(note.encode()).hexdigest()[:12] if note else "marked"


def state() -> dict[str, str]:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def notes() -> list[dict]:
    ids = call("findNotes", query=QUERY)
    out = []
    for i in range(0, len(ids), 400):
        out += call("notesInfo", notes=ids[i:i + 400])
    return [n for n in out if ANSWER in n["fields"]]


def waiting(n: dict, done: dict[str, str]) -> bool:
    note = plain(n["fields"][NOTE]["value"])
    if note:
        return done.get(str(n["noteId"])) != key(note)
    return "marked" in n["tags"] and not n["fields"][ANSWER]["value"].strip()


def pending() -> list[dict]:
    done = state()
    out = []
    for n in notes():
        if not waiting(n, done):
            continue
        f = n["fields"]
        cards = call("cardsInfo", cards=n["cards"][:1])
        out.append({
            "nid": n["noteId"],
            "deck": cards[0]["deckName"] if cards else "",
            "model": n["modelName"],
            "id": next((t[4:] for t in n["tags"] if t.startswith("id::")), ""),
            "marked": "marked" in n["tags"],
            "note": plain(f[NOTE]["value"]),
            "card": {k: plain(v["value"])[:4000] for k, v in sorted(f.items(), key=lambda kv: kv[1]["order"])
                     if k not in NOTE_FIELDS and plain(v["value"])},
            "previous": plain(f[ANSWER]["value"]),
        })
    return out


def apply(path: Path) -> int:
    answers = json.loads(path.read_text(encoding="utf-8"))
    done = state()
    info = {n["noteId"]: n for n in call("notesInfo", notes=[a["nid"] for a in answers])}
    for a in answers:
        n = info.get(a["nid"])
        if not n or ANSWER not in n["fields"] or not a.get("answer", "").strip():
            print(f"skipped {a['nid']}")
            continue
        call("updateNoteFields", note={"id": a["nid"], "fields": {ANSWER: _html(a["answer"].strip())}})
        done[str(a["nid"])] = key(plain(n["fields"][NOTE]["value"]))
    HOME.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(done, indent=1), encoding="utf-8")
    call("sync")
    print(f"{len(answers)} explanations written")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] not in ("pending", "apply", "status"):
        print(__doc__)
        return 2
    if args[0] == "apply":
        return apply(Path(args[1]))
    call("sync")
    if args[0] == "status":
        all_notes, done = notes(), state()
        wait = sum(waiting(n, done) for n in all_notes)
        print(f"{len(all_notes)} cards with a note or a star, {wait} waiting for an explanation")
        return 0
    items = pending()
    text = json.dumps(items, ensure_ascii=False, indent=1)
    if "-o" in args:
        out = Path(args[args.index("-o") + 1])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"{len(items)} cards waiting -> {out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
