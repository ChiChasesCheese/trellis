"""Push recent/cards/*.json into Anki as whole-problem recall cards, in file order.

    uv run --with markdown --with pygments python scripts/amazon_push_cards.py [--dry-run] [--set recent|patterns]

`--set recent` (default): research/companies/amazon/cards/coding.json → `LeetCode Tops::22 Amazon 近一月原题（2026-10）`.
`--set patterns`: research/companies/amazon/cards/patterns_*.json → `LeetCode Tops::23 Amazon 模式强化（patterns）`.
Note type `Trellis QA` (the same front/back styling as the
`leetcode-tops::amazon-a` cards: title line + meta chip on the front, label chips and highlighted code on the back).
A note is keyed by its `id::<id>` tag, so re-running updates fields instead of duplicating. New cards are positioned
after every other new LeetCode Tops card, in the order the JSON lists them; answered cards are never moved. The deck
uses the parent deck's options preset (never the shared Default one). The footer links only the study note in Obsidian
(vault `Trellis_`, addressed by note name) — no provenance on a card (proposals/WRITING_RULES.md §11).
"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import quote

import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

CARDS = Path(__file__).resolve().parents[1] / "research/companies/amazon/cards"
PARENT = "LeetCode Tops"
SETS = {
    "recent": (["coding.json"], f"{PARENT}::22 Amazon 近一月原题（2026-10）", "Amazon 近一月原题",
               "leetcode-tops::amazon-recent-1m"),
    "patterns": (["patterns_*.json"], f"{PARENT}::23 Amazon 模式强化（patterns）", "Amazon 模式强化",
                 "leetcode-tops::amazon-patterns"),
}
DECK = CRUMB = TAG_BRANCH = ""
VAULT = "Trellis_"
MODEL = "Trellis QA"
FENCE = re.compile(r"```python\n(.*?)```", re.S)
LABEL = re.compile(r"^(\S{1,6})｜", re.M)


def anki(action: str, **params):
    req = urllib.request.Request("http://localhost:8765",
                                 json.dumps({"action": action, "version": 6, "params": params}).encode())
    out = json.loads(urllib.request.urlopen(req).read())
    if out.get("error"):
        raise RuntimeError(f"{action}: {out['error']}")
    return out["result"]


def render(md_text: str) -> str:
    """Markdown → HTML; ```python blocks become the same `div.hl` pygments markup the amazon-a cards use."""
    codes: list[str] = []

    def stash(m: re.Match) -> str:
        codes.append(highlight(m.group(1), PythonLexer(), HtmlFormatter(cssclass="hl", wrapcode=True)))
        return f"\n\nCODEBLOCK{len(codes) - 1}\n\n"

    text = FENCE.sub(stash, md_text)
    text = LABEL.sub(lambda m: f'<span class="label">{m.group(1)}</span>', text)
    out = markdown.markdown(text, extensions=["tables", "sane_lists"])
    for i, block in enumerate(codes):
        out = out.replace(f"<p>CODEBLOCK{i}</p>", block)
    return out


def front(card: dict) -> str:
    title = f'<p class="title">{html.escape(card["title"])}<span class="meta">{html.escape(card["meta"])}</span></p>'
    return title + render(card["question_md"])


def back(card: dict) -> str:
    links = []
    if card.get("note"):
        name = Path(card["note"]).stem
        links.append(f'<a href="obsidian://open?vault={quote(VAULT)}&file={quote(name)}">{html.escape(name)}</a>')
    footer = '<div class="sources">Go deeper: ' + " · ".join(links) + "</div>" if links else ""
    return render(card["answer_md"]) + footer


def tags(card: dict) -> list[str]:
    return ["amazon", f"id::{card['id']}", f"{TAG_BRANCH}::{card['slug']}"]


def main(argv: list[str]) -> int:
    global DECK, CRUMB, TAG_BRANCH
    dry = "--dry-run" in argv
    name = argv[argv.index("--set") + 1] if "--set" in argv else "recent"
    patterns, DECK, CRUMB, TAG_BRANCH = SETS[name]
    cards = []
    for pattern in patterns:
        for f in sorted(CARDS.glob(pattern)):
            cards += json.loads(f.read_text(encoding="utf-8"))
    ids = [c["id"] for c in cards]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate card ids")
    if dry:
        for c in cards:
            print(c["id"], len(front(c)), len(back(c)))
        return 0
    if DECK not in anki("deckNames"):
        anki("createDeck", deck=DECK)
    parent_conf = anki("getDeckConfig", deck=PARENT)["id"]
    anki("setDeckConfigId", decks=[DECK], configId=parent_conf)

    added = updated = 0
    note_of: dict[str, int] = {}
    for c in cards:
        fields = {"Question": front(c), "Answer": back(c), "Crumb": f"{CRUMB} › {c['title']}"}
        found = anki("findNotes", query=f'"tag:id::{c["id"]}"')
        if found:
            anki("updateNoteFields", note={"id": found[0], "fields": fields})
            anki("addTags", notes=found, tags=" ".join(tags(c)))
            note_of[c["id"]] = found[0]
            updated += 1
        else:
            nid = anki("addNote", note={"deckName": DECK, "modelName": MODEL, "fields": fields, "tags": tags(c),
                                        "options": {"allowDuplicate": True}})
            note_of[c["id"]] = nid
            added += 1

    # position: after the last new LeetCode Tops card that is not ours, in JSON order
    ours = {cid for nid in note_of.values() for cid in anki("notesInfo", notes=[nid])[0]["cards"]}
    others = anki("cardsInfo", cards=[x for x in anki("findCards", query=f'deck:"{PARENT}" is:new') if x not in ours])
    base = max((x["due"] for x in others), default=0)
    moved = 0
    for i, c in enumerate(cards, start=1):
        for cid in anki("notesInfo", notes=[note_of[c["id"]]])[0]["cards"]:
            info = anki("cardsInfo", cards=[cid])[0]
            if info["type"] == 0 and info["due"] != base + i:
                anki("setSpecificValueOfCard", card=cid, keys=["due"], newValues=[base + i])
                moved += 1
    print(f"{len(cards)} card(s): {added} added, {updated} updated, {moved} positioned after {base}; deck {DECK}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
