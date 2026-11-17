"""Render vault cards (## Q / ## A) to phone-preview HTML with the real Anki build's HTML and CSS.

    uv run python scripts/card_preview.py <card.md> [...] [-o /tmp/card-preview]   # then screenshot at 390 px

Writes <out>/<id>.html (question, then answer, as the back of the card shows them).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from trellis import build  # noqa: E402


def main() -> int:
    args = sys.argv[1:]
    out = Path("/tmp/card-preview")
    if "-o" in args:
        i = args.index("-o")
        out = Path(args[i + 1])
        del args[i:i + 2]
    out.mkdir(parents=True, exist_ok=True)
    for f in map(Path, args):
        text = f.read_text(encoding="utf-8")
        q = re.search(r"^## Q\n(.*?)^## A\n", text, re.S | re.M).group(1)
        a = text.split("\n## A\n", 1)[1]
        node = (re.search(r"^node: (\S+)", text, re.M) or [None, ""])[1]
        body = (f'<div class="crumb">{node}</div>{build._html(q)}<hr id="answer">'
                f'{build._html(a, fold=False, links={}, node=node)}')
        page = (f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
                f'<style>{build.CSS}</style></head><body class="card">{body}</body></html>')
        dest = out / f"{f.stem}.html"
        dest.write_text(page, encoding="utf-8")
        print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
