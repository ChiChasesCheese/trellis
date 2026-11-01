"""Fill the LeetCode Tops topic decks with whole cards that already exist in the current style.

    uv run python research/leetcode-tops/adopt_cards.py      # writes cards/<branch>/tlc-tops-<slug>-0-whole.md

Every card is a stub over the shared problem file `vault/interviews/core/leetcode/problems/<slug>.md` (one body per
problem, see scripts/lc_problems.py) with this deck's id, node and header meta (difficulty · company-tag rank · lists).
Existing tops cards are never overwritten.
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "vault/interviews/core/leetcode/tops/cards"


def header(p: dict, m: dict) -> str:
    bits = [m["difficulty"]] + ([f"全公司热度第 {p['rank']} 名"] if p["rank"] else []) + (["、".join(p["lists"])] if p["lists"] else [])
    return f"**LC {m['id']} {m['title_zh']}**｜" + " · ".join(bits)


def main() -> None:
    sel = json.loads((ROOT / "research/leetcode-tops/selection.json").read_text(encoding="utf-8"))
    meta = json.loads((ROOT / "research/leetcode-tops/meta.json").read_text(encoding="utf-8"))
    made = 0
    for p in sel:
        s, b = p["slug"], p["branch"]
        dest = OUT / b / f"tlc-tops-{s}-0-whole.md"
        if dest.exists():
            continue
        if not (ROOT / f"vault/interviews/core/leetcode/problems/{s}.md").exists():
            continue  # no shared body yet: a card agent writes it
        text = (f"---\nid: tlc-tops-{s}-0-whole\nnode: {b}.{s}\ntype: qa\nbody: interviews/core/leetcode/problems/{s}\n"
                f"meta: {json.dumps(header(p, meta[s]).split('｜', 1)[1], ensure_ascii=False)}\n---\n")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        made += 1
    print(made, "cards adopted")


if __name__ == "__main__":
    main()
