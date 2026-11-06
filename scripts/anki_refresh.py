"""Update cards already in Anki from the vault, without importing anything.

    uv run python scripts/anki_refresh.py [--dry-run] <domain> [<domain> ...]
    uv run python scripts/anki_refresh.py --style                # push the card CSS to the note types
    uv run python scripts/anki_refresh.py --add <id-prefix> <domain>   # also add built notes missing from Anki whose id starts so

`anki-push` imports the whole package, which brings back any card Chi has deleted in Anki and can move cards he has moved.
This only rewrites the fields of notes that already exist and differ: it moves nothing and leaves scheduling alone.
It creates nothing unless `--add` names an id prefix; then only new notes with that prefix are added, so a deleted card
outside it stays deleted.
"""
from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
BATCH = 50
SEP = "\x1f"


def call(action: str, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    for _ in range(60):
        with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8765", body), timeout=300) as r:
            out = json.load(r)
        if out["error"] and "lifecycle" in out["error"]:
            time.sleep(4)
            continue
        if out["error"]:
            raise RuntimeError(f"{action}: {out['error']}")
        return out["result"]
    raise RuntimeError("Anki stayed busy")


def built_notes(domain: str, folder: Path) -> dict[str, dict]:
    """card id -> fields, tags, deck and note type, from a package built the normal way and never imported."""
    apkg = folder / f"{domain}.apkg"
    r = subprocess.run(["uv", "run", "trellis", "--domain", domain, "build", "-o", str(apkg)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode or not apkg.exists():
        raise RuntimeError(r.stderr.strip()[-300:] or "build failed")
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", folder)
    db = sqlite3.connect(folder / "collection.anki2")
    models_json, decks_json = db.execute("select models, decks from col").fetchone()
    models = {int(k): v["name"] for k, v in json.loads(models_json).items()}
    decks = {int(k): v["name"] for k, v in json.loads(decks_json).items()}
    deck_of = dict(db.execute("select nid, did from cards"))
    out = {}
    for nid, mid, flds, tags in db.execute("select id, mid, flds, tags from notes"):
        ident = next((t[4:] for t in tags.split() if t.startswith("id::")), None)
        if ident:
            out[ident] = {"fields": flds.split(SEP), "tags": tags.split(), "deck": decks[deck_of[nid]], "model": models[mid]}
    db.close()
    return out


def refresh(domain: str, dry: bool, add: str | None = None) -> None:
    folder = Path(tempfile.mkdtemp(prefix="anki-refresh-"))
    try:
        built = built_notes(domain, folder)
    finally:
        pass
    ids = call("findNotes", query=f"tag:{domain}::*")
    info = []
    for i in range(0, len(ids), 400):
        info += call("notesInfo", notes=ids[i:i + 400])
    changes = []
    present = set()
    for note in info:
        ident = next((t[4:] for t in note["tags"] if t.startswith("id::")), None)
        present.add(ident)
        new = built.get(ident, {}).get("fields")
        if not new:
            continue
        names = sorted(note["fields"], key=lambda k: note["fields"][k]["order"])
        if len(names) != len(new):
            continue
        fields = {k: v for k, v in zip(names, new) if note["fields"][k]["value"] != v}
        if fields:
            changes.append({"id": note["noteId"], "fields": fields})
    additions = sorted(i for i in built if add and i.startswith(add) and i not in present)
    print(f"{domain}: {len(built)} built, {len(info)} in Anki, {len(changes)} to update, {len(additions)} to add", flush=True)
    if not dry:
        for i in range(0, len(changes), BATCH):
            call("multi", actions=[{"action": "updateNoteFields", "params": {"note": c}} for c in changes[i:i + BATCH]])
        for ident in additions:  # in id order, which is the order the cards are dealt
            b = built[ident]
            call("createDeck", deck=b["deck"])
            names = call("modelFieldNames", modelName=b["model"])
            call("addNote", note={"deckName": b["deck"], "modelName": b["model"], "tags": b["tags"],
                                  "fields": dict(zip(names, b["fields"])), "options": {"allowDuplicate": True}})
    shutil.rmtree(folder, ignore_errors=True)


def style() -> None:
    from trellis.build import CSS
    for name in ("Trellis QA", "Trellis Cloze"):
        call("updateModelStyling", model={"name": name, "css": CSS})
        print(name, "styled")


def main() -> int:
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    add = None
    if "--add" in args:
        i = args.index("--add")
        add = args[i + 1]
        del args[i:i + 2]
    if args == ["--style"]:
        style()
        return 0
    failed = []
    for domain in args:
        try:
            refresh(domain, dry, add)
        except Exception as e:  # noqa: BLE001 - one domain failing must not stop the rest
            failed.append(domain)
            print(f"{domain}: {e}", flush=True)
    if not dry:
        call("sync")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
