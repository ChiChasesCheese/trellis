"""Build: compile skeleton + cards into an Anki .apkg via genanki.

Stability guarantees that make re-import safe:
  * model ids and deck ids are hashes of stable names
  * note guid is a hash of the card id — editing a card updates it in
    place on re-import; renaming the id makes Anki treat it as new
  * notes are added in skeleton study order, so new cards are introduced
    in the order the skeleton prescribes
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import genanki
import markdown

from .cards import Card
from .links import go_deeper
from .readings import Reading
from .skeleton import Skeleton
from .traces import ID_TAG_PREFIX

_MD = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists"])

CSS = """
.card {
  font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 19px;
  line-height: 1.5;
  color: #1a1a1a;
  background: #fbfbfb;
  text-align: left;
  max-width: 620px;
  margin: 0 auto;
  padding: 20px;
}
.night_mode .card { color: #e8e8e8; background: #1e1e1e; }
code, pre {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.88em;
  background: rgba(140, 140, 140, 0.15);
  border-radius: 4px;
}
code { padding: 1px 5px; }
pre { padding: 10px 12px; overflow-x: auto; }
pre code { background: none; padding: 0; }
hr#answer { border: none; border-top: 2px solid #7aa2f7; margin: 16px 0; }
.crumb { font-size: 13px; color: #888; margin-bottom: 12px; }
table { border-collapse: collapse; }
td, th { border: 1px solid #999; padding: 4px 10px; }
.cloze { font-weight: 600; color: #4576f5; }
.ref { color: #7aa2f7; font-style: italic; }
.sources { margin-top: 18px; padding-top: 8px; border-top: 1px solid rgba(140,140,140,0.3);
           font-size: 14px; color: #888; }
.sources a { color: #7aa2f7; text-decoration: none; }
.sources a.web { color: #9aa; font-size: 12px; }
"""


def _stable_id(name: str) -> int:
    return int(hashlib.md5(name.encode("utf-8")).hexdigest()[:8], 16)


_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def _html(text: str) -> str:
    # Obsidian wikilinks have nowhere to point inside Anki; render the
    # display text as a styled reference instead.
    text = _WIKILINK_RE.sub(lambda m: f'<span class="ref">{m.group(2) or m.group(1)}</span>', text)
    _MD.reset()
    return _MD.convert(text)


def _qa_model() -> genanki.Model:
    return genanki.Model(
        _stable_id("trellis:model:qa"),
        "Trellis QA",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Crumb"}],
        templates=[{
            "name": "QA",
            "qfmt": '<div class="crumb">{{Crumb}}</div>{{Question}}',
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        }],
        css=CSS,
    )


def _cloze_model() -> genanki.Model:
    return genanki.Model(
        _stable_id("trellis:model:cloze"),
        "Trellis Cloze",
        model_type=genanki.Model.CLOZE,
        fields=[{"name": "Text"}, {"name": "Crumb"}],
        templates=[{
            "name": "Cloze",
            "qfmt": '<div class="crumb">{{Crumb}}</div>{{cloze:Text}}',
            "afmt": '<div class="crumb">{{Crumb}}</div>{{cloze:Text}}',
        }],
        css=CSS,
    )


def _sources_html(
    skeleton: Skeleton,
    readings: list[Reading],
    node_id: str,
    vault: str | None = None,
    clippings: dict | None = None,
    cases: list | None = None,
) -> str:
    """Clickable further-reading footer from the node's (and ancestors')
    readings — the card's road onward, tappable in Anki. Clipped readings
    open inside Obsidian; the web original stays available as ↗."""
    links = go_deeper(skeleton, readings, node_id, vault, clippings, cases)
    if not links:
        return ""
    rendered = []
    for link in links:
        marker = "▶ " if link.is_video else ""
        html = f'<a href="{link.href}">{marker}{link.title}</a>'
        if link.web_href:
            html += f' <a href="{link.web_href}" class="web" title="open the original online">↗</a>'
        rendered.append(html)
    return '<div class="sources">Go deeper: ' + " · ".join(rendered) + "</div>"


def build_package(
    skeleton: Skeleton,
    cards: list[Card],
    out_path: str | Path,
    readings: list[Reading] | None = None,
    vault: str | None = None,
    clippings: dict | None = None,
    cases: list | None = None,
    lang: str = "",
) -> dict:
    """Write the .apkg. Returns {'notes': int, 'decks': int, 'path': str}."""
    readings = readings or []
    qa_model, cloze_model = _qa_model(), _cloze_model()
    decks: dict[str, genanki.Deck] = {}

    def deck_for(node_id: str) -> genanki.Deck:
        name = skeleton.deck_name(skeleton.by_id[node_id])
        if name not in decks:
            decks[name] = genanki.Deck(_stable_id(f"trellis:deck:{name}"), name)
        return decks[name]

    study_order = {n.id: i for i, n in enumerate(skeleton.walk())}
    note_count = 0
    for card in sorted(cards, key=lambda c: (study_order[c.node], c.path.name)):
        node = skeleton.by_id[card.node]
        crumb = " › ".join(n.title for n in node.path())
        tags = [skeleton.domain + "::" + card.node.replace(".", "::")] + card.tags
        if card.source:
            tags.append(f"src::{card.source}")
        # The note GUID is a hash of the card id and cannot be reversed,
        # so the id also travels as a tag — that is how `trellis pull`
        # reads a review history back onto the card that earned it.
        tags.append(ID_TAG_PREFIX + card.id)
        footer = _sources_html(skeleton, readings, card.node, vault,
                               clippings, cases)
        question, answer = card.render(lang)
        if card.type == "qa":
            note = genanki.Note(
                model=qa_model,
                fields=[_html(question), _html(answer) + footer, crumb],
                guid=genanki.guid_for(f"trellis:{card.id}"),
                tags=tags,
            )
        else:
            note = genanki.Note(
                model=cloze_model,
                fields=[_html(question) + footer, crumb],
                guid=genanki.guid_for(f"trellis:{card.id}"),
                tags=tags,
            )
        deck_for(card.node).add_note(note)
        note_count += 1

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(decks.values())).write_to_file(out_path)
    return {"notes": note_count, "decks": len(decks), "path": str(out_path)}
