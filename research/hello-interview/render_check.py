"""Render Hello Interview cards to one page as Anki shows them, to check figures and layout on a phone width in dark mode.

    uv run python research/hello-interview/render_check.py <card files...>   # writes /private/tmp/hi_preview_<pid>.html and prints the path
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from trellis import build as B  # noqa: E402
from trellis.cards import load_cards  # noqa: E402
from trellis.skeleton import load_skeleton  # noqa: E402


def main() -> None:
    sk = load_skeleton(ROOT / "skeleton/hello-interview.yaml")
    cards, _ = load_cards(ROOT / "vault/domains/hello-interview/cards")
    links = B._link_index(sk, cards, [], None)
    related = {}
    for folder in sk.examples_from.split(","):
        if folder:
            related.update(B.load_related(ROOT / "vault" / folder))
    wanted = {Path(x).stem for x in sys.argv[1:]}
    out = ['<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">',
           f"<style>{B._qa_model().css}</style></head>",
           '<body class="card nightMode night_mode" style="max-width:414px;margin:0 auto;padding:12px;background:#000">']
    for c in cards:
        if c.id in wanted:
            q, a = c.render(None)
            out.append(B._html(q) + "<hr>" + B._html(a, related, set(), fold=sk.fold, fold_code=sk.fold_code, links=links, node=c.node) + "<hr>")
    target = Path(f"/private/tmp/hi_preview_{os.getpid()}.html")
    target.write_text("".join(out) + "</body></html>", encoding="utf-8")
    print("wrote", target, len(out) - 3, "cards")


if __name__ == "__main__":
    main()
