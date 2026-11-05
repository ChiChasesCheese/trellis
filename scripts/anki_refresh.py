"""Update cards already in Anki from the vault, without importing anything.

    uv run python scripts/anki_refresh.py [--dry-run] <domain> [<domain> ...]
    uv run python scripts/anki_refresh.py --style                # push the card CSS to the note types

`anki-push` imports the whole package, which brings back any card Chi has deleted in Anki and can move cards he has moved.
This only rewrites the fields of notes that already exist and differ: it creates nothing, moves nothing and leaves scheduling alone.
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


def built_notes(domain: str, folder: Path) -> dict[str, list[str]]:
    """card id -> fields, from a package built the normal way and never imported."""
    apkg = folder / f"{domain}.apkg"
    r = subprocess.run(["uv", "run", "trellis", "--domain", domain, "build", "-o", str(apkg)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode or not apkg.exists():
        raise RuntimeError(r.stderr.strip()[-300:] or "build failed")
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", folder)
    db = sqlite3.connect(folder / "collection.anki2")
    out = {}
    for flds, tags in db.execute("select flds, tags from notes"):
        ident = next((t[4:] for t in tags.split() if t.startswith("id::")), None)
        if ident:
            out[ident] = flds.split(SEP)
    db.close()
    return out


def refresh(domain: str, dry: bool) -> None:
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
    for note in info:
        ident = next((t[4:] for t in note["tags"] if t.startswith("id::")), None)
        new = built.get(ident)
        if not new:
            continue
        names = sorted(note["fields"], key=lambda k: note["fields"][k]["order"])
        if len(names) != len(new):
            continue
        fields = {k: v for k, v in zip(names, new) if note["fields"][k]["value"] != v}
        if fields:
            changes.append({"id": note["noteId"], "fields": fields})
    print(f"{domain}: {len(built)} built, {len(info)} in Anki, {len(changes)} to update", flush=True)
    if not dry:
        for i in range(0, len(changes), BATCH):
            call("multi", actions=[{"action": "updateNoteFields", "params": {"note": c}} for c in changes[i:i + BATCH]])
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
    if args == ["--style"]:
        style()
        return 0
    failed = []
    for domain in args:
        try:
            refresh(domain, dry)
        except Exception as e:  # noqa: BLE001 - one domain failing must not stop the rest
            failed.append(domain)
            print(f"{domain}: {e}", flush=True)
    if not dry:
        call("sync")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
