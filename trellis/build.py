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


_CODE_OR_TAG = re.compile(r"(<pre>.*?</pre>|<code>.*?</code>|<svg.*?</svg>|<[^>]+>)", re.S)
# A fenced ```svg block is a diagram: it goes into the card as inline SVG, so it can use the theme's colours.
_SVG_FENCE = re.compile(r"^```svg[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
# **例题：** opens a worked problem at the end of an answer; it is folded so the card stays short.
_EXAMPLE = re.compile(r'<p><span class="label">例题</span>(.*?)</p>(.*)\Z', re.S)


def _break_semicolons(html: str) -> str:
    """A full-width semicolon separates clauses that read better one per line; code is left alone."""
    parts = _CODE_OR_TAG.split(html)
    return "".join(p if i % 2 else p.replace("；", "；<br>") for i, p in enumerate(parts))


_EXAMPLE_LEAD = '<p><span class="label">例题</span>'


_LI = re.compile(r"<li>(.*?)</li>", re.S)
_LC_NUM = re.compile(r"LC\s*(\d+)")


def _example_key(title: str) -> str:
    m = _LC_NUM.search(title)
    return f"LC {m.group(1)}" if m else re.sub(r"<[^>]+>", "", title).split("（")[0].strip()


def _fold_examples(html: str) -> str:
    """Each **例题：** paragraph opens a folded block that runs to the next 例题 or the end of the card.

    When a list item on the same card names the problem (its LC number, or the title of a problem without one), the
    block opens right there: the item itself becomes the summary. Blocks no item names stay folded at the end.
    """
    head, *examples = html.split(_EXAMPLE_LEAD)
    blocks = []
    for ex in examples:
        title, _, body = ex.partition("</p>")
        blocks.append([_example_key(title), title, body, False])

    def mentions(item: str) -> list:
        text = re.sub(r"<[^>]+>", "", item)
        nums = {f"LC {n}" for n in _LC_NUM.findall(text)}
        return [b for b in blocks if not b[3] and (b[0] in nums or (not b[0].startswith("LC ") and b[0] and b[0] in text))]

    def inline(m: re.Match) -> str:
        item = m.group(1)
        if "<details" in item or "<ul" in item or "<ol" in item:
            return m.group(0)
        found = mentions(item)
        for b in found:
            b[3] = True
        if len(found) == 1:
            return f'<li><details class="inline-example"><summary>{item}</summary>{found[0][2]}</details></li>'
        if found:
            extra = "".join(f'<details class="inline-example"><summary>{b[1]}</summary>{b[2]}</details>' for b in found)
            return f"<li>{item}{extra}</li>"
        return m.group(0)

    head = _LI.sub(inline, head)
    rest = [f'<details class="example"><summary><span class="label">例题</span>{t}</summary>{body}</details>'
            for _, t, body, used in blocks if not used]
    return head + "".join(rest)


_RELATED_LABELS = ("同模式的题", "同模式", "同类", "对应 LeetCode", "相关题")
_RELATED_P = re.compile(r'<p>(?:<span class="label">(%s)</span>|<strong>(%s)</strong>[：:])\s*(.*?)</p>'
                        % ("|".join(_RELATED_LABELS), "|".join(_RELATED_LABELS)), re.S)
_LI_LEAD_LC = re.compile(r"<li>((?:<strong>)?LC\s*(\d+)(?![\d]).*?)</li>", re.S)


def load_related(folder: Path) -> dict[int, tuple[str, str]]:
    """LC number -> (title, html with a one-line statement and the main solution) from whole-answer cards."""
    md = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists", "codehilite"],
                           extension_configs={"codehilite": {"css_class": "hl", "guess_lang": False}})
    out: dict[int, tuple[str, str]] = {}
    for f in sorted(folder.glob("**/*-0-whole.md")):
        text = f.read_text(encoding="utf-8")
        q, _, a = text.partition("## A")
        head = re.search(r"^\*\*(LC (\d+) [^*\n]+)\*\*｜", q, re.M)
        code = re.search(r"```python\n.*?```", a, re.S)
        if not head or not code or int(head.group(2)) in out:
            continue
        body = q[head.end():].split("\n\n")
        stmt = next((b.strip() for b in body[1:] if b.strip()), "")
        stmt = re.split(r"(?<=。)", stmt)[0][:220]
        md.reset()
        out[int(head.group(2))] = (head.group(1), md.convert(stmt + "\n\n" + code.group(0)))
    return out


def _expand_related(html: str, related: dict[int, tuple[str, str]], own: set[int]) -> str:
    def fold(summary: str, n: int) -> str:
        return f'<details class="inline-example"><summary>{summary}</summary>{related[n][1]}</details>'

    def para(m: re.Match) -> str:
        label, content = m.group(1) or m.group(2), m.group(3)
        items = [i.strip() for i in re.split(r"[、，,；;]\s*", content.rstrip("。. ")) if i.strip()]
        hits = [int(x) for i in items for x in _LC_NUM.findall(re.sub(r"<[^>]+>", "", i))]
        if not any(n in related and n not in own for n in hits):
            return m.group(0)
        lis = []
        for item in items:
            nums = [int(x) for x in _LC_NUM.findall(re.sub(r"<[^>]+>", "", item))]
            n = next((x for x in nums if x in related and x not in own), None)
            lis.append(f"<li>{fold(item, n)}</li>" if n is not None else f"<li>{item}</li>")
        return f'<p><span class="label">{label}</span></p><ul class="related">{"".join(lis)}</ul>'

    def item(m: re.Match) -> str:
        n = int(m.group(2))
        if "<details" in m.group(1) or n not in related or n in own:
            return m.group(0)
        return f"<li>{fold(m.group(1), n)}</li>"

    return _LI_LEAD_LC.sub(item, _RELATED_P.sub(para, html))


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

.fig { margin: 12px 0; text-align: center; }
.fig svg { max-width: 100%; height: auto; color: var(--ink); }
details.example { margin-top: 18px; padding-top: 10px; border-top: 1px solid var(--rule); }
details.example + details.example { margin-top: 8px; }
details.inline-example > summary { cursor: pointer; list-style: none; }
details.inline-example > summary::-webkit-details-marker { display: none; }
details.inline-example > summary::after { content: " ▸"; color: var(--accent); }
details.inline-example[open] > summary::after { content: " ▾"; }
details.inline-example[open] { margin-bottom: 10px; }
details.example > summary { cursor: pointer; list-style: none; color: var(--accent); }
details.example > summary::-webkit-details-marker { display: none; }
details.example > summary::after { content: " ▸"; color: var(--dim); }
details.example[open] > summary::after { content: " ▾"; }

@media (max-width: 500px) {
  .card { font-size: 17px; padding: 16px 14px 24px; }
  .hl pre, pre { font-size: 13px; padding: 10px 12px; }
}
"""


def _stable_id(name: str) -> int:
    return int(hashlib.md5(name.encode("utf-8")).hexdigest()[:8], 16)


_CODE_SPANS = re.compile(r"(^```.*?^```[ \t]*$|``.+?``|`[^`\n]+`)", re.S | re.M)
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def _html(text: str, related: dict | None = None, own: set[int] | None = None) -> str:
    # Obsidian wikilinks have nowhere to point inside Anki; render the
    # display text as a styled reference instead.
    # (only outside code: `[[0]] * 3` in a code span is Python, not a link)
    parts = _CODE_SPANS.split(text)
    text = "".join(p if i % 2 else _WIKILINK_RE.sub(lambda m: f'<span class="ref">{m.group(2) or m.group(1)}</span>', p)
                   for i, p in enumerate(parts))
    svgs: list[str] = []

    def _stash(m: re.Match) -> str:
        svgs.append(m.group(1).strip())
        return f"\n\nTRELLISSVG{len(svgs) - 1}\n\n"
    text = _SVG_FENCE.sub(_stash, text)
    _MD.reset()
    html = _MD.convert(_blank_before_lists(text))
    for i, svg in enumerate(svgs):
        html = html.replace(f"<p>TRELLISSVG{i}</p>", f'<div class="fig">{svg}</div>')
    html = _TITLE.sub(lambda m: f'<p class="title">{m.group(1)}<span class="meta">{m.group(2)}</span></p>', html, count=1)
    html = _LABEL.sub(lambda m: f'<p><span class="label">{m.group(1)}</span>', html)
    html = _fold_examples(html)
    if related:
        html = _expand_related(html, related, own or set())
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
    related = (load_related(Path(__file__).resolve().parents[1] / "vault" / skeleton.examples_from)
               if skeleton.examples_from else None)
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
        own = {int(x) for x in _LC_NUM.findall(question.split("\n\n")[0])}
        if card.type == "qa":
            note = genanki.Note(
                model=qa_model,
                fields=[_html(question), _html(answer, related, own) + footer, crumb],
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
