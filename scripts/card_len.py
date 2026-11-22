"""Length of card answers as the learner reads them: characters of `## A` without code, SVG, HTML tags and whitespace.

    uv run python scripts/card_len.py <card.md> […]            # one line per card: total chars, CJK chars, path
    uv run python scripts/card_len.py --over 700 <card.md> […]  # only cards whose CJK count exceeds the limit; exit 1 if any

Used as the gate when trimming long cards (deck review 2026-11): a trimmed answer should hold at most ~700 CJK characters.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def measure(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    a = text.split("\n## A\n", 1)[1] if "\n## A\n" in text else ""
    a = re.sub(r"```.*?```", "", a, flags=re.S)
    a = re.sub(r"<svg.*?</svg>", "", a, flags=re.S)
    a = re.sub(r"<[^>]+>|\s", "", a)
    return len(a), len(re.findall(r"[一-鿿]", a))


def main() -> int:
    args = sys.argv[1:]
    limit = None
    if args[:1] == ["--over"]:
        limit, args = int(args[1]), args[2:]
    if not args:
        print(__doc__)
        return 2
    bad = 0
    for f in map(Path, args):
        total, cjk = measure(f)
        if limit is None or cjk > limit:
            print(f"{total:6} {cjk:6} {f}")
            bad += limit is not None
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
