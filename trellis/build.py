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
from urllib.parse import quote

import genanki
import markdown

from .cards import Card
from .kp_footer import footers as kp_footers
from .links import go_deeper
from .readings import Reading
from .sequence import CORE_FIRST, CORE_TAG, core_leaves, sequence
from .skeleton import Skeleton
from .traces import ID_TAG_PREFIX

_MD = markdown.Markdown(
    extensions=["fenced_code", "tables", "sane_lists", "codehilite", "md_in_html"],
    extension_configs={"codehilite": {"css_class": "hl", "guess_lang": False}},
)

_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")
_TITLE = re.compile(r"^<p><strong>(.+?)</strong>[｜|]\s*(.+?)</p>", re.S)
# A short bold lead such as **思路。** opens a section: render it as a label chip.
_LABEL = re.compile(r"<p><strong>([^<]{1,12}?)[。:：]</strong>\s*")


_CODE_OR_TAG = re.compile(r"(<pre>.*?</pre>|<code>.*?</code>|<svg.*?</svg>|<[^>]+>)", re.S)
# A fenced ```svg block is a diagram: it goes into the card as inline SVG, so it can use the theme's colours.
_SVG_FENCE = re.compile(r"^```svg[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
_MERMAID_FENCE = re.compile(r"^```mermaid[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
_MERMAID_CACHE = Path(__file__).resolve().parents[1] / "sources/local/mermaid-cache"


def _mermaid_svg(src: str) -> str | None:
    """Anki cannot run mermaid: render the diagram to SVG once (cached by content hash) with mermaid-cli. None when
    rendering is unavailable, so the block stays as code rather than failing the build."""
    import hashlib
    import json as _json
    import subprocess
    import tempfile
    key = hashlib.sha1(src.encode("utf-8")).hexdigest()[:16]
    cached = _MERMAID_CACHE / f"{key}.svg"
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        mmd, svg, cfg = Path(tmp) / "d.mmd", Path(tmp) / "d.svg", Path(tmp) / "p.json"
        mmd.write_text(src, encoding="utf-8")
        cfg.write_text(_json.dumps({"args": ["--no-sandbox"]}), encoding="utf-8")
        try:
            subprocess.run(["npx", "-y", "@mermaid-js/mermaid-cli@12.0.0", "-q", "-p", str(cfg), "-t", "neutral",
                            "-b", "transparent", "-i", str(mmd), "-o", str(svg)], capture_output=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if not svg.is_file():
            return None
        out = re.sub(r"<\?xml[^>]*>", "", svg.read_text(encoding="utf-8"))
        out = re.sub(r'(<svg[^>]*?) style="max-width:[^"]*"', r'\1 style="max-width:100%;height:auto;background:#fff;border-radius:8px;padding:6px"', out, count=1)
    _MERMAID_CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_text(out, encoding="utf-8")
    return out
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


_RELATED_LABELS = ("同模式的题", "同模式", "同类", "对应 LeetCode", "相关题", "核心题")
_RELATED_P = re.compile(r'<p>(?:<span class="label">(%s)</span>|<strong>(%s)</strong>[：:])\s*(.*?)</p>'
                        % ("|".join(_RELATED_LABELS), "|".join(_RELATED_LABELS)), re.S)
_LI_LEAD_LC = re.compile(r"<li>((?:<strong>)?LC\s*(\d+)(?![\d]).*?)</li>", re.S)


def load_related(folder: Path) -> dict[int, tuple[str, str]]:
    """LC number -> (title, html with a one-line statement and the main solution) from whole-answer cards."""
    md = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists", "codehilite"],
                           extension_configs={"codehilite": {"css_class": "hl", "guess_lang": False}})
    out: dict[int, tuple[str, str]] = {}
    for f in sorted(folder.glob("**/*.md")):  # whole-answer cards, or the shared problem files they point to
        text = f.read_text(encoding="utf-8")
        q, _, a = text.partition("## A")
        head = re.search(r"^\*\*(LC (\d+) [^*\n]+)\*\*｜", q, re.M)
        # the main solution: the first block after the 「最优解：」 lead when a card opens with a 简单解法
        main = a.split("最优解：", 1)[1] if "最优解：" in a else a
        code = re.search(r"```python\n.*?```", main, re.S)
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
.grade { color: var(--dim); font-size: 12.5px; margin-top: 18px; text-align: center; }
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
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
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
  overflow-wrap: normal;
}
.hl .c, .hl .c1, .hl .cm, .hl .ch { color: #6a9955; font-style: normal; }
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
.ref { color: var(--accent); }
.sources {
  margin-top: 22px; padding-top: 10px; border-top: 1px solid var(--rule);
  font-size: 13px; color: var(--dim);
}
.sources a { color: var(--accent); text-decoration: none; }
.sources a.web { color: var(--dim); font-size: 12px; }
.kpidx { margin-top: 18px; padding-top: 8px; border-top: 1px solid var(--rule); font-size: 13px; line-height: 1.55; color: var(--dim); }
.kpidx p { margin: 3px 0; }
.kpidx b { font-weight: 600; margin-right: 6px; color: var(--ink); }

.fig { margin: 12px 0; text-align: center; }
.fig svg { max-width: 100%; height: auto; color: var(--ink); }
video.clip, img.clip { display: block; width: 100%; max-width: 560px; margin: 8px auto; border-radius: 10px; background: #000; }
details.sec { margin: 6px 0; border-left: 1px solid var(--rule); padding: 0 0 0 10px; }
details.sec > summary { cursor: pointer; font-weight: 600; list-style-position: outside; }
details.sec[open] > summary { margin-bottom: 6px; }
details.pt { margin: 3px 0; }
details.pt > summary { cursor: pointer; }
a.ref { text-decoration: none; }
p.linked { margin: 3px 0; }
details.pt > summary::marker { color: var(--dim); }
details.pt > :not(summary) { margin-left: 10px; color: var(--dim); }
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


_FENCE_LINE = re.compile(r"^\s*```")
_MARKER = re.compile(r"^( *)((?:[-*+]|\d+\.)\s)")
_SECTION = re.compile(r"^\*\*([^*\n]{1,14})。\*\*\s*(.*)$")


def _nested_indent(text: str) -> str:
    """Python-Markdown nests a list only under 4 spaces; cards often indent sub-bullets by 2. Double such indents
    (outside code fences) so a sub-bullet renders as a nested list instead of running into its parent's text."""
    out, fence = [], False
    for line in text.split("\n"):
        if _FENCE_LINE.match(line):
            fence = not fence
        m = None if fence else _MARKER.match(line)
        if m and m.group(1) and len(m.group(1)) % 4:
            line = " " * (len(m.group(1)) * 2) + line[len(m.group(1)):]
        out.append(line)
    return "\n".join(out)


def _inline(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r'&lt;(/?)span( class="ref")?&gt;', r"<\1span\2>", s)  # wikilinks already rendered as references
    s = re.sub(r'&lt;a class="ref" href="([^"]*)"&gt;', r'<a class="ref" href="\1">', s).replace("&lt;/a&gt;", "</a>")
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


PHRASE_MAX = 24  # a bullet's head is a phrase to recite from; longer than this and it needs writing, never cutting
_TAG = re.compile(r"<[^>]+>")
_OPEN = {"（": "）", "(": ")", "「": "」", "《": "》", "`": "`", "<": ">", "“": "”"}


def _width(text: str) -> int:
    return len(re.sub(r"【[^】]*】", "", _TAG.sub("", text)).replace("*", "").replace("`", ""))  # a priority tag is not part of the phrase


def _split_at(text: str, seps: str) -> tuple[str, str] | None:
    """The first separator that sits outside brackets, code and tags, as (before, after)."""
    closer = None
    span = 0
    bold = False
    i = 0
    while i < len(text):
        c = text[i]
        if not closer and text.startswith("**", i):  # never split inside bold: its markers would come apart
            bold = not bold
            i += 2
            continue
        if text.startswith(("<span", "<a "), i):
            span += 1
        elif text.startswith(("</span>", "</a>"), i):
            span -= 1
        if closer:
            if c == closer:
                closer = None
        elif c in _OPEN:
            closer = _OPEN[c]
        elif not span and not bold and c in seps:
            return text[:i], text[i + 1:]
        i += 1
    return None


def _head(text: str) -> tuple[str, str]:
    """Split one bullet into (phrase, rest). Nothing is cut and nothing is repeated: a bullet with no phrase stays whole."""
    text = text.strip()
    whole = re.fullmatch(r"\*\*([^*\n]+?)[：:。，,]?\*\*", text)
    if whole:  # a bullet that is all bold is itself the phrase; what folds under it is its sub-list
        return whole.group(1), ""
    m = re.match(r"^\*\*(.+?)\*\*\s*[：:。，,]?\s*(.*)$", text, re.S)
    if m and m.group(2) and _width(m.group(1)) <= PHRASE_MAX + 12:  # an author's own bold cue may run a little long
        return m.group(1).rstrip("：:。，, "), m.group(2)
    if "→" in text:
        before, after = text.split("→", 1)
        before = before.strip()
        if _width(before) <= PHRASE_MAX + 6 or (before.endswith(("？", "?")) and _width(before) <= 44):  # a question is a fine phrase
            return before.strip(), after.strip()
    for seps in ("：:", "，,；;。"):
        parts = _split_at(text, seps)
        if parts and parts[1].strip() and 2 <= _width(parts[0]) <= PHRASE_MAX:
            return parts[0].strip(), parts[1].strip()
    return text, ""


def _outline(text: str) -> str:
    """Long answers as an outline (skeleton `fold: true`): every labelled section folds to its label and gist, and
    every top-level bullet inside folds to its head. The reader sees the structure first and opens what to recall."""
    lines, fence, sections, cur = text.split("\n"), False, [], None
    pre: list[str] = []
    for line in lines:
        if _FENCE_LINE.match(line):
            fence = not fence
        m = None if fence else _SECTION.match(line)
        if m:
            cur = [m.group(1), m.group(2), []]
            sections.append(cur)
        elif cur is None:
            pre.append(line)
        else:
            cur[2].append(line)
    if len(sections) < 3:  # a short card has no outline to fold, but its bullets are still phrases to recite from
        return _fold_bullets(text)
    out = ["\n".join(pre)]
    for label, first, body in sections:
        if label in _RELATED_LABELS:  # expands into the problems it names, so it must stay one paragraph
            out.append(f"**{label}。** {first}")
            continue
        body_md = _fold_bullets("\n".join(body).strip("\n"))
        gist, rest = (first, "") if _width(first) <= PHRASE_MAX else _head(first)
        if _width(gist) > PHRASE_MAX:  # no phrase to lead with: the label stands alone and the prose goes inside
            gist, rest = "", first
        body_md = "\n\n".join(x for x in (rest, body_md) if x.strip())
        if not body_md.strip():
            out.append(f'<p><span class="label">{label}</span>{_inline(gist)}</p>')
            continue
        # Chi (2026-11-04): recite from the phrases, so sections stay open and the details behind each phrase stay closed
        opened = "" if "```" in body_md else " open"
        out.append(f'<details class="sec"{opened} markdown="1"><summary><span class="label">{label}</span>{_inline(gist)}</summary>'
                   f"\n\n{body_md}\n\n</details>")
    return "\n\n".join(out)


def _fold_bullets(md: str) -> str:
    """Each top-level bullet with more than a line of content becomes a foldable item: its head, then the rest."""
    lines, fence, items, buf = md.split("\n"), False, [], []
    for line in lines:
        if _FENCE_LINE.match(line) and not line.startswith(" "):
            fence = not fence
        if not fence and re.match(r"^(?:[-*+]|\d+\.)\s", line):
            items.append(buf)
            buf = [line]
        elif not fence and buf and buf[0] and re.match(r"^(?:[-*+]|\d+\.)\s", buf[0]) and line and not line.startswith(" ") \
                and not _FENCE_LINE.match(line):
            items.append(buf)  # a paragraph after the list ends the item
            buf = [line]
        else:
            buf.append(line)
    items.append(buf)
    out = []
    for item in items:
        if not item:
            continue
        m = re.match(r"^((?:[-*+]|\d+\.)\s+)(.*)$", item[0])
        cont, in_code, base = [], False, 0
        for l in item[1:]:  # undo the list indent, but never eat a code block's own indentation
            if _FENCE_LINE.match(l):
                if not in_code:
                    base = min(len(l) - len(l.lstrip()), 4)
                in_code = not in_code
                cont.append(l[base:])
            else:
                cont.append(l[base:] if in_code else re.sub(r"^ {1,4}", "", l))
        if not m:
            out.append("\n".join(item))
            continue
        text = m.group(2)
        head, rest = _head(text)
        if not rest and not any(c.strip() for c in cont):
            out.append(item[0])
            continue
        num = m.group(1).strip() if m.group(1)[0].isdigit() else ""
        body = "\n".join([rest] + cont if rest else cont).strip("\n")
        out.append(f'<details class="pt" markdown="1"><summary>{num + " " if num else ""}{_inline(head)}</summary>\n\n{body}\n\n</details>')
    return "\n\n".join(o.strip("\n") for o in out if o.strip())


_EMBED = re.compile(r"!\[\[([^\]|]+\.(mp4|webm|mov|gif|png|jpe?g|webp))(?:\|[^\]]*)?\]\]", re.I)
_MEDIA_USED: set[Path] = set()   # media files the current build embedded; build_package ships them in the .apkg
_VAULT_MEDIA: dict[str, Path] = {}


def _media_index() -> dict[str, Path]:
    if not _VAULT_MEDIA:
        vault = Path(__file__).resolve().parents[1] / "vault"
        for f in vault.rglob("*"):
            if f.suffix.lower() in (".mp4", ".webm", ".mov", ".gif", ".png", ".jpg", ".jpeg", ".webp"):
                _VAULT_MEDIA.setdefault(f.name, f)
    return _VAULT_MEDIA


def _embed(m: re.Match) -> str:
    """Obsidian embeds (`![[clip.mp4]]`) become playable media in Anki; the file travels inside the package."""
    name, ext = m.group(1).rsplit("/", 1)[-1], m.group(2).lower()
    f = _media_index().get(name)
    if f is None:
        return f'<span class="ref">{name}</span>'
    _MEDIA_USED.add(f)
    if ext in ("mp4", "webm", "mov"):
        return (f'<video class="clip" src="{name}" controls playsinline loop preload="metadata"></video>')
    return f'<img class="clip" src="{name}">'


CODE_COLUMNS = 44  # what fits a phone at the card's code size
_COMMENT_MARK = {"python": "#", "py": "#", "bash": "#", "sh": "#", "shell": "#", "yaml": "#", "ruby": "#",
                 "java": "//", "go": "//", "cpp": "//", "c": "//", "js": "//", "ts": "//", "javascript": "//",
                 "typescript": "//", "rust": "//", "kotlin": "//", "sql": "--", "lua": "--"}
_CODE_FENCE = re.compile(r"^(```)([A-Za-z0-9+]+)[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)


def _columns(text: str) -> int:
    return sum(2 if ord(c) > 0x2E7F else 1 for c in text)


def _comment_at(line: str, mark: str) -> int:
    """Where a trailing comment starts, skipping strings. -1 if the line has none, or is only a comment."""
    quote = None
    i = 0
    while i < len(line):
        c = line[i]
        if quote:
            if c == "\\":
                i += 1
            elif c == quote:
                quote = None
        elif c in "\"'`":
            quote = c
        elif line.startswith(mark, i):
            return i if line[:i].strip() else -1
        i += 1
    return -1


def _lift_comments(code: str, mark: str) -> str:
    """A trailing comment that would run off a phone moves to its own line above; aligned padding collapses."""
    out = []
    for line in code.split("\n"):
        at = _comment_at(line, mark)
        if at < 0:
            out.append(line)
            continue
        body, comment = line[:at].rstrip(), line[at:].rstrip()
        if _columns(body) + 2 + _columns(comment) <= CODE_COLUMNS:
            out.append(f"{body}  {comment}")
        else:
            out.append(" " * (len(body) - len(body.lstrip())) + comment)
            out.append(body)
    return "\n".join(out)


def _fit_code(text: str) -> str:
    def fit(m: re.Match) -> str:
        mark = _COMMENT_MARK.get(m.group(2).lower())
        return f"```{m.group(2)}\n{_lift_comments(m.group(3), mark) if mark else m.group(3)}```"
    return _CODE_FENCE.sub(fit, text)


_LC_TITLES: dict[str, str] = {}
_LC_MENTION = re.compile(r"LC\s*(\d+)((?:[、,，/]\s*(?:LC\s*)?\d+)*)")


def _lc_titles() -> dict[str, str]:
    if not _LC_TITLES:
        folder = Path(__file__).resolve().parents[1] / "vault/interviews/core/leetcode/problems"
        for f in folder.glob("*.md"):
            m = re.search(r"^\*\*LC (\d+) ([^*\n｜]+)\*\*", f.read_text(encoding="utf-8"), re.M)
            if m:
                _LC_TITLES.setdefault(m.group(1), m.group(2).strip())
    return _LC_TITLES


def _name_problems(text: str) -> str:
    """`LC 787、743` says nothing on a phone: give each number its title, unless the title already follows."""
    titles = _lc_titles()

    def name(m: re.Match) -> str:
        nums = re.findall(r"\d+", m.group(0))
        after = text_part[m.end():m.end() + 40].lstrip()
        if len(nums) == 1 and titles.get(nums[0]) and after.startswith(titles[nums[0]][:3]):
            return m.group(0)
        if len(nums) == 1 and re.match(r"[\u4e00-\u9fffA-Za-z]", after) and after[0] not in "的和与或里中是就也用这那等及":
            return m.group(0)  # followed by the author's own name for it
        return "、".join(f"LC {n} {titles[n]}" if n in titles else f"LC {n}" for n in nums)

    parts = _CODE_SPANS.split(text)
    for i in range(0, len(parts), 2):
        text_part = parts[i]
        parts[i] = _LC_MENTION.sub(name, text_part)
    return "".join(parts)


_CODE_BLOCK = re.compile(r'<div class="hl"><pre>.*?</pre></div>', re.S)


def _fold_long_code(html: str, limit: int) -> str:
    """A code block longer than `limit` lines (skeleton `fold_code`) opens on a tap, so a phone card stays readable."""
    def wrap(m: re.Match) -> str:
        n = m.group(0).count("\n")
        return m.group(0) if n <= limit else f'<details class="inline-example"><summary>代码（{n} 行）</summary>{m.group(0)}</details>'
    return _CODE_BLOCK.sub(wrap, html)


_BASIC_ANSWER = re.compile(r"\*\*基本回答。\*\*(.*?)(?=\n\*\*[^*\n]{1,8}。\*\*|\Z)", re.S)


def _link_index(skeleton: Skeleton, cards: list[Card], readings: list, lang: str | None) -> dict[str, dict]:
    """Everything a wikilink can name in this domain -> where it opens: the Anki tag, and a short answer to show in place."""
    first: dict[str, Card] = {}
    for card in sorted(cards, key=lambda c: (c.step or 0)):
        first.setdefault(card.node, card)
    index: dict[str, dict] = {}

    def add(name: str, node_id: str) -> None:
        card = first.get(node_id) or next((c for n, c in first.items() if n.startswith(node_id + ".")), None)
        if card is None:
            return
        m = _BASIC_ANSWER.search(card.render(lang)[1])
        index.setdefault(name, {"node": node_id, "tag": f"{skeleton.domain}::{node_id.replace('.', '::')}", "answer": m.group(1).strip() if m else ""})

    for node_id in skeleton.by_id:
        add(node_id, node_id)
        add(node_id.rsplit(".", 1)[-1], node_id)  # a design question is linked by its slug
    for r in readings:  # a course page is linked by its reading note; open the page, not one of its parts
        nodes = list(getattr(r, "nodes", []) or [])
        course = next((n.rsplit(".", 1)[0] for n in nodes if n.endswith(".notes")), nodes[0] if nodes else None)
        if course:
            add(Path(r.path).stem, course)
    return index


def _anchor(tag: str, text: str) -> str:
    return f'<a class="ref" href="anki://x-callback-url/search?query={quote("tag:" + tag, safe="")}">{text}</a>'


def _html(text: str, related: dict | None = None, own: set[int] | None = None, fold: bool = False, fold_code: int = 0,
          links: dict | None = None, node: str = "") -> str:
    # Obsidian wikilinks have nowhere to point inside Anki; render the
    # display text as a styled reference instead.
    # (only outside code: `[[0]] * 3` in a code span is Python, not a link)
    text = _fit_code(text)
    if links is not None:  # answers only: a title in a question's header is already named
        text = _name_problems(text)
    parts = _CODE_SPANS.split(text)
    parts = [p if i % 2 else _EMBED.sub(lambda m: "\n\n" + _embed(m) + "\n\n", p) for i, p in enumerate(parts)]
    used: dict[str, tuple[str, str]] = {}

    def _ref(m: re.Match) -> str:
        name, label = m.group(1).rstrip("\\"), m.group(2) or m.group(1)
        target = (links or {}).get(name)
        if not target:
            return f'<span class="ref">{label}</span>'
        if target["node"] != node and not node.startswith(target["node"] + "."):
            used.setdefault(target["node"], (label, name))
        return _anchor(target["tag"], label)
    text = "".join(p if i % 2 else _WIKILINK_RE.sub(_ref, p) for i, p in enumerate(parts))
    svgs: list[str] = []

    def _stash(m: re.Match) -> str:
        svgs.append(m.group(1).strip())
        return f"\n\nTRELLISSVG{len(svgs) - 1}\n\n"
    text = _SVG_FENCE.sub(_stash, text)

    def _mermaid(m: re.Match) -> str:
        svg = _mermaid_svg(m.group(1))
        if svg is None:
            return m.group(0)
        svgs.append(svg)
        return f"\n\nTRELLISSVG{len(svgs) - 1}\n\n"
    text = _MERMAID_FENCE.sub(_mermaid, text)
    text = _nested_indent(text)
    if fold:
        text = _outline(text)
    _MD.reset()
    html = _MD.convert(_blank_before_lists(text))
    for i, svg in enumerate(svgs):
        html = html.replace(f"<p>TRELLISSVG{i}</p>", f'<div class="fig">{svg}</div>')
    html = _TITLE.sub(lambda m: f'<p class="title">{m.group(1)}<span class="meta">{m.group(2)}</span></p>', html, count=1)
    html = _LABEL.sub(lambda m: f'<p><span class="label">{m.group(1)}</span>', html)
    html = _fold_examples(html)
    if fold_code:
        html = _fold_long_code(html, fold_code)
    if related:
        html = _expand_related(html, related, own or set())
    return _break_semicolons(html) + _related_notes(used, links or {})


def _related_notes(used: dict[str, tuple[str, str]], links: dict) -> str:
    """The cards this answer points at, at its end: open in place on any device, or jump where Anki allows it."""
    if not used:
        return ""
    rows = []
    for label, name in used.values():
        target = links[name]
        jump = _anchor(target["tag"], "跳转")
        if target["answer"]:
            body = _html(target["answer"])
            rows.append(f'<details class="pt"><summary>{label} · {jump}</summary>{body}</details>')
        else:
            rows.append(f'<p class="linked">{label} · {jump}</p>')
    return f'<details class="sec related-notes"><summary><span class="label">相关知识点</span></summary>{"".join(rows)}</details>'


_GRADE = '<div class="grade">说全了 Good · 卡壳或漏要点 Hard · 想不起来 Again · 第一次学不按 Easy</div>'


def _qa_model() -> genanki.Model:
    return genanki.Model(
        _stable_id("trellis:model:qa"),
        "Trellis QA",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Crumb"}],
        templates=[{
            "name": "QA",
            "qfmt": '<div class="crumb">{{Crumb}}</div>{{Question}}',
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}' + _GRADE,
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
            "afmt": '<div class="crumb">{{Crumb}}</div>{{cloze:Text}}' + _GRADE,
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
    _MEDIA_USED.clear()
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
    related = None
    if skeleton.examples_from:  # comma-separated folders; the first card found for an LC number wins
        related = {}
        for folder in skeleton.examples_from.split(","):
            for n, v in load_related(Path(__file__).resolve().parents[1] / "vault" / folder).items():
                related.setdefault(n, v)
    # The Sequence leaves out adopted cards — building one would put a second
    # copy of a note another tool owns into the collection. A card's place in
    # it is its new-card position: what a first import studies in. A
    # collection that already has the card keeps its old position through an
    # import, which is why `anki-push` sets it again afterwards (ADR 0010).
    links = _link_index(skeleton, cards, readings, lang) if skeleton.fold else {}
    index = kp_footers(skeleton, cards)
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
                fields=[_html(question), _html(answer, related, own, fold=skeleton.fold, fold_code=skeleton.fold_code, links=links, node=card.node) + index.get(card.id, "") + footer, crumb],
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
    package = genanki.Package(list(decks.values()))
    package.media_files = sorted(str(f) for f in _MEDIA_USED)
    package.write_to_file(out_path)
    return {"notes": note_count, "decks": len(decks), "path": str(out_path)}
