"""Mechanical fixes on notes that live only in Anki (no vault source), field by field, keeping the HTML. Dry run by default.

    uv run python scripts/anki_field_fix.py unwrap 'tag:markets*'            # report
    uv run python scripts/anki_field_fix.py unwrap 'tag:markets*' --apply    # write through AnkiConnect, then sync

Rules:
- unwrap   hard line breaks inside running text are joined (no space between CJK, one space between Latin words), and
           ASCII , ? : ; ( ) next to a CJK character become full-width. <pre> and <code> blocks are left alone.

For cards that have a vault source use scripts/card_normalize.py instead: anki_refresh would overwrite an edit made here.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request

CJK = r"　-〿一-鿿＀-￯"
WIDE = {",": "，", "?": "？", ":": "：", ";": "；", "(": "（", ")": "）"}


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


def unwrap_text(text: str) -> str:
    text = re.sub(rf"(?<=[{CJK}])[ \t]*\n[ \t]*(?=\S)|(?<=\S)[ \t]*\n[ \t]*(?=[{CJK}])", "", text)   # CJK on either side: no space
    text = re.sub(r"(?<=[^\s>])[ \t]*\n[ \t]*(?=[^\s<])", " ", text)                                # Latin on both sides: a space
    text = re.sub(rf"(?<=[{CJK}])([,?:;)])|([(])(?=[{CJK}])", lambda m: WIDE[m.group(1) or m.group(2)], text)
    return re.sub(rf"([,?:;])(?=[{CJK}])(?<=[{CJK}A-Za-z0-9%][,?:;])", lambda m: WIDE[m.group(1)], text)


def unwrap(html: str) -> str:
    parts = re.split(r"(<pre.*?</pre>|<code.*?</code>|<[^>]+>|\{\{c\d+::|\}\})", html, flags=re.S)
    return "".join(p if i % 2 else unwrap_text(p) for i, p in enumerate(parts))


RULES = {"unwrap": unwrap}


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2 or args[0] not in RULES:
        print(__doc__)
        return 2
    rule, query = RULES[args[0]], args[1]
    notes = anki("notesInfo", notes=anki("findNotes", query=query))
    changed = 0
    for n in notes:
        new = {name: rule(f["value"]) for name, f in n["fields"].items()}
        diff = {k: v for k, v in new.items() if v != n["fields"][k]["value"]}
        if diff:
            changed += 1
            if changed <= 2:
                k = next(iter(diff))
                print(f"  e.g. note {n['noteId']} {k}:\n    - {n['fields'][k]['value'][:110]!r}\n    + {diff[k][:110]!r}")
            if "--apply" in sys.argv:
                anki("updateNoteFields", note={"id": n["noteId"], "fields": diff})
    print(f"{query}: {changed} of {len(notes)} notes {'updated' if '--apply' in sys.argv else 'would change'}")
    if "--apply" in sys.argv and changed:
        anki("sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
