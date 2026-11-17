"""Render LeetCode Project quick cards to HTML with the real Anki templates and CSS, for a phone-size look.

    uv run python scripts/lcp_preview.py <slug> <kp-suffix> [...] [-o /tmp/lcp-preview]   # one page per card, back side

Writes <out>/<kp>.html (local, never committed: the cards quote LeetCode workspaces). Screenshot them at 390 px wide.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lcp_quick as lq  # noqa: E402
import quick_deck as qd  # noqa: E402


def render(template: str, fields: dict[str, str]) -> str:
    """Enough of Anki's mustache: {{#F}}…{{/F}}, {{^F}}…{{/F}}, {{F}} and {{text:F}}."""
    def section(m: re.Match) -> str:
        neg, name, body = m.group(1) == "^", m.group(2), m.group(3)
        return body if bool(fields.get(name, "").strip()) != neg else ""
    out = template
    for _ in range(3):
        out = re.sub(r"\{\{([#^])([^}]+)\}\}(.*?)\{\{/\2\}\}", section, out, flags=re.S)
    out = re.sub(r"\{\{cloze:([^}]+)\}\}", lambda m: re.sub(r"\{\{c\d::(.*?)(::[^}]*)?\}\}", r'<span class="cloze">\1</span>', fields.get(m.group(1), "")), out)
    return re.sub(r"\{\{(?:text:)?([^}#^/]+)\}\}", lambda m: fields.get(m.group(1).strip(), ""), out)


def main() -> int:
    args = sys.argv[1:]
    out = Path("/tmp/lcp-preview")
    if "-o" in args:
        i = args.index("-o")
        out = Path(args[i + 1])
        del args[i:i + 2]
    slug, wanted = args[0], args[1:]
    cards, _ = lq.load(slug, verified_only=False)
    names = lq.titles()
    out.mkdir(parents=True, exist_ok=True)
    sides = qd.templates()
    for c in cards:
        if wanted and not any(c["kp"].endswith(w) for w in wanted):
            continue
        key, vals = qd.fields(c, {"topic_title": names.get(slug, slug), "title": c["_point"]["title"]})
        fields = dict(zip(qd.MODELS[key][1], vals))
        body = render(sides[key][1], fields)
        page = (f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
                f'<style>{qd.css()}</style></head><body class="card"><div id="qa">{body}</div></body></html>')
        (out / f"{c['kp']}.html").write_text(page, encoding="utf-8")
        print(out / f"{c['kp']}.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
