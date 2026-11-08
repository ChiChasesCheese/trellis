"""Update cards already in Anki from the vault, without importing anything.

    uv run python scripts/anki_refresh.py [--dry-run] <domain> [<domain> ...]
    uv run python scripts/anki_refresh.py --style                # push the card CSS to the note types
    uv run python scripts/anki_refresh.py --add <id-prefix> <domain>   # also add built notes missing from Anki whose id starts so
    uv run python scripts/anki_refresh.py --add @ids.txt <domain>      # ... or exactly the ids listed in a file

`anki-push` imports the whole package, which brings back any card Chi has deleted in Anki and can move cards he has moved.
This only rewrites the fields of notes that already exist and differ: it moves nothing and leaves scheduling alone.
It creates nothing unless `--add` names an id prefix; then only new notes with that prefix are imported, from a package
trimmed to them, so they keep the package's deal order and a deleted card outside the prefix stays deleted.
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
    due_of = dict(db.execute("select nid, min(due) from cards group by nid"))  # the deal position the package sets
    out = {}
    for nid, mid, flds, tags in db.execute("select id, mid, flds, tags from notes"):
        ident = next((t[4:] for t in tags.split() if t.startswith("id::")), None)
        if ident:
            out[ident] = {"fields": flds.split(SEP), "tags": tags.split(), "deck": decks[deck_of[nid]], "model": models[mid],
                          "due": due_of[nid], "nid": nid}
    db.close()
    return out


def domain_root(built: dict[str, dict]) -> str:
    return next(iter(built.values()))["deck"].split("::")[0]


def add_subset(folder: Path, nids: list[int]) -> None:
    """Import a copy of the package holding only these notes. Anki numbers a note it has never seen by the package's
    position, so the new cards are dealt in the package's order; addNote would number them by the preset's insertion
    order, which is random. Notes outside the subset are not in the file, so nothing deleted comes back."""
    db_path = folder / "subset.anki2"
    shutil.copy(folder / "collection.anki2", db_path)
    db = sqlite3.connect(db_path)
    keep = ",".join(str(n) for n in nids)
    db.execute(f"delete from cards where nid not in ({keep})")
    db.execute(f"delete from notes where id not in ({keep})")
    db.commit()
    db.execute("vacuum")
    db.close()
    apkg = folder / "subset.apkg"
    with zipfile.ZipFile(apkg, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(db_path, "collection.anki2")
        z.writestr("media", "{}")
    call("importPackage", path=str(apkg))


def refresh(domain: str, dry: bool, add: str | None = None) -> None:
    from trellis.skeleton import load_skeleton
    via = load_skeleton(ROOT / "skeleton" / f"{domain}.yaml").anki_via
    if via:
        raise RuntimeError(f"reaches Anki through {via}; refresh that domain instead")
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
    wanted = set(Path(add[1:]).read_text().split()) if add and add.startswith("@") else None  # @file: exactly these ids
    additions = sorted((i for i in built if add and (i in wanted if wanted is not None else i.startswith(add)) and i not in present),
                       key=lambda i: built[i]["due"])
    print(f"{domain}: {len(built)} built, {len(info)} in Anki, {len(changes)} to update, {len(additions)} to add", flush=True)
    if not dry:
        for i in range(0, len(changes), BATCH):
            call("multi", actions=[{"action": "updateNoteFields", "params": {"note": c}} for c in changes[i:i + BATCH]])
        if additions:
            add_subset(folder, [built[i]["nid"] for i in additions])
            root = call("getDeckConfig", deck=domain_root(built))
            for deck in sorted({built[i]["deck"] for i in additions}):
                if call("getDeckConfig", deck=deck)["id"] != root["id"]:  # a deck the import created starts on Default
                    call("setDeckConfigId", decks=[deck], configId=root["id"])
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
