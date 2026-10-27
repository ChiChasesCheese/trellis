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
from .sequence import CORE_FIRST, CORE_TAG, core_leaves, sequence
from .skeleton import Skeleton
from .traces import ID_TAG_PREFIX

_MD = markdown.Markdown(
    extensions=["fenced_code", "tables", "sane_lists", "codehilite"],
    extension_configs={"codehilite": {"css_class": "hl", "guess_lang": False}},
)

_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")
_TITLE = re.compile(r"^<p><strong>(.+?)</strong>[｜|]\s*(.+?)</p>", re.S)
# A short bold lead such as **思路。** opens a section: render it as a label chip.
_LABEL = re.compile(r"<p><strong>([^<]{1,12}?)[。:：]</strong>\s*")


_CODE_OR_TAG = re.compile(r"(<pre>.*?</pre>|<code>.*?</code>|<[^>]+>)", re.S)


def _break_semicolons(html: str) -> str:
    """A full-width semicolon separates clauses that read better one per line; code is left alone."""
    parts = _CODE_OR_TAG.split(html)
    return "".join(p if i % 2 else p.replace("；", "；<br>") for i, p in enumerate(parts))


def _blank_before_lists(text: str) -> str:
    """Markdown needs a blank line before a list; cards often put one right under a bold lead line."""
    out: list[str] = []
    fenced = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if (not fenced and _LIST_ITEM.match(line) and out and out[-1].strip()
                and not _LIST_ITEM.match(out[-1]) and not out[-1].startswith((" ", "\t"))):
            out.append("")
        out.append(line)
    return "\n".join(out)

CSS = """
:root {
  --ink: #1a1a1a; --dim: #6b7280; --paper: #fbfbfb;
  --accent: #3b6fd4; --rule: rgba(140, 140, 140, 0.28);
  --chip: rgba(59, 111, 212, 0.10);
  --codebg: #f6f8fa; --codeline: #e3e6ea;
}
.night_mode {
  --ink: #e6e6e6; --dim: #9aa2ad; --paper: #1e1e1e;
  --accent: #7aa2f7; --rule: rgba(160, 160, 160, 0.24);
  --chip: rgba(122, 162, 247, 0.16);
  --codebg: #161b22; --codeline: #30363d;
}
.card {
  font-family: -apple-system, "Segoe UI", Roboto, "PingFang SC",
               "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 18px;
  line-height: 1.6;
  color: var(--ink);
  background: var(--paper);
  text-align: left;
  max-width: 620px;
  margin: 0 auto;
  padding: 20px 18px 28px;
  overflow-wrap: break-word;
}
.card p { margin: 0 0 0.85em; }

/* ---- front: breadcrumb, title line, problem statement ---- */
.crumb {
  font-size: 12px;
  letter-spacing: 0.04em;
  color: var(--dim);
  margin-bottom: 14px;
}
p.title {
  font-size: 1.06em;
  font-weight: 650;
  line-height: 1.45;
  margin-bottom: 0.7em;
}
p.title .meta {
  display: block;
  font-size: 0.74em;
  font-weight: 500;
  color: var(--dim);
  letter-spacing: 0.02em;
  margin-top: 3px;
}

/* ---- back: one labelled block per section ---- */
.label {
  display: inline-block;
  font-size: 0.72em;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--accent);
  background: var(--chip);
  border-radius: 4px;
  padding: 2px 7px;
  margin-right: 8px;
  vertical-align: 0.1em;
}
hr#answer { border: none; border-top: 2px solid var(--accent); margin: 18px 0 16px; }

/* ---- code ---- */
code, pre, .hl { font-family: "SF Mono", Menlo, Consolas, monospace; }
code {
  font-size: 0.86em;
  background: var(--chip);
  border-radius: 4px;
  padding: 1px 5px;
}
.hl {
  background: var(--codebg);
  border: 1px solid var(--codeline);
  border-radius: 8px;
  margin: 0 0 1em;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.hl pre, pre {
  margin: 0;
  padding: 12px 14px;
  font-size: 14.5px;
  line-height: 1.5;
  tab-size: 4;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
pre code, .hl code {
  background: none;
  padding: 0;
  font-size: inherit;
  white-space: pre;
}
.hl .c, .hl .c1, .hl .cm, .hl .ch { color: #6a9955; font-style: italic; }
.hl .k, .hl .kn, .hl .kc, .hl .kd, .hl .ow, .hl .kr { color: #a626a4; }
.hl .nf, .hl .fm { color: #4078f2; }
.hl .nc, .hl .nn { color: #c18401; }
.hl .nb, .hl .bp { color: #0184bc; }
.hl .s, .hl .s1, .hl .s2, .hl .sa, .hl .se, .hl .sd { color: #50a14f; }
.hl .mi, .hl .mf, .hl .il { color: #b76b01; }
.hl .o, .hl .p { color: inherit; }
.night_mode .hl .c, .night_mode .hl .c1, .night_mode .hl .cm { color: #7c9f6a; }
.night_mode .hl .k, .night_mode .hl .kn, .night_mode .hl .kc,
.night_mode .hl .kd, .night_mode .hl .ow, .night_mode .hl .kr { color: #c792ea; }
.night_mode .hl .nf, .night_mode .hl .fm { color: #82aaff; }
.night_mode .hl .nc, .night_mode .hl .nn { color: #ffcb6b; }
.night_mode .hl .nb, .night_mode .hl .bp { color: #89ddff; }
.night_mode .hl .s, .night_mode .hl .s1, .night_mode .hl .s2,
.night_mode .hl .sa, .night_mode .hl .se, .night_mode .hl .sd { color: #c3e88d; }
.night_mode .hl .mi, .night_mode .hl .mf, .night_mode .hl .il { color: #f78c6c; }

/* ---- the rest ---- */
table { border-collapse: collapse; margin: 0 0 1em; font-size: 0.92em; }
td, th { border: 1px solid var(--rule); padding: 5px 10px; }
.cloze { font-weight: 650; color: var(--accent); }
.ref { color: var(--accent); font-style: italic; }
.sources {
  margin-top: 22px; padding-top: 10px; border-top: 1px solid var(--rule);
  font-size: 13px; color: var(--dim);
}
.sources a { color: var(--accent); text-decoration: none; }
.sources a.web { color: var(--dim); font-size: 12px; }

@media (max-width: 500px) {
  .card { font-size: 17px; padding: 16px 14px 24px; }
  .hl pre, pre { font-size: 13px; padding: 10px 12px; }
}
"""


def _stable_id(name: str) -> int:
    return int(hashlib.md5(name.encode("utf-8")).hexdigest()[:8], 16)


_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def _html(text: str) -> str:
    # Obsidian wikilinks have nowhere to point inside Anki; render the
    # display text as a styled reference instead.
    text = _WIKILINK_RE.sub(lambda m: f'<span class="ref">{m.group(2) or m.group(1)}</span>', text)
    _MD.reset()
    html = _MD.convert(_blank_before_lists(text))
    html = _TITLE.sub(lambda m: f'<p class="title">{m.group(1)}<span class="meta">{m.group(2)}</span></p>', html, count=1)
    html = _LABEL.sub(lambda m: f'<p><span class="label">{m.group(1)}</span>', html)
    return _break_semicolons(html)


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
    order: str = CORE_FIRST,
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

    note_count = 0
    core = core_leaves(skeleton)
    # The Sequence leaves out adopted cards — building one would put a second
    # copy of a note another tool owns into the collection. A card's place in
    # it is its new-card position: what a first import studies in. A
    # collection that already has the card keeps its old position through an
    # import, which is why `anki-push` sets it again afterwards (ADR 0010).
    for position, card in enumerate(sequence(skeleton, cards, order), start=1):
        node = skeleton.by_id[card.node]
        crumb = " › ".join(n.title for n in node.path())
        tags = [skeleton.domain + "::" + card.node.replace(".", "::")] + card.tags
        if card.node in core:
            tags.append(CORE_TAG)
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
                due=position,
            )
        else:
            note = genanki.Note(
                model=cloze_model,
                fields=[_html(question) + footer, crumb],
                guid=genanki.guid_for(f"trellis:{card.id}"),
                tags=tags,
                due=position,
            )
        deck_for(card.node).add_note(note)
        note_count += 1

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(decks.values())).write_to_file(out_path)
    return {"notes": note_count, "decks": len(decks), "path": str(out_path)}
