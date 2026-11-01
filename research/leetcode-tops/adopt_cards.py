"""Fill the LeetCode Tops topic decks with whole cards that already exist in the current style.

    uv run python research/leetcode-tops/adopt_cards.py      # writes cards/<branch>/tlc-tops-<slug>-0-whole.md

Source, first found: the classic-lists card (written to the newest rules), else the TikTok whole card. The body is kept;
the id, node and header line are rewritten for this deck (difficulty · company-tag rank · lists). Existing tops cards
are never overwritten.
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
        src = [ROOT / f"vault/interviews/core/leetcode/classic/cards/tlc-classic-{s}-0-whole.md",
               *map(Path, glob.glob(str(ROOT / f"vault/interviews/core/leetcode/tiktok/cards/*/tlc-{s}-0-whole.md")))]
        src = next((f for f in src if f.exists()), None)
        if src is None:
            continue
        text = src.read_text(encoding="utf-8")
        text = re.sub(r"^id: .*$", f"id: tlc-tops-{s}-0-whole", text, count=1, flags=re.M)
        text = re.sub(r"^node: .*$", f"node: {b}.{s}", text, count=1, flags=re.M)
        text = re.sub(r"^\*\*LC [^\n]*?\*\*｜.*$", lambda _: header(p, meta[s]), text, count=1, flags=re.M)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        made += 1
    print(made, "cards adopted")


if __name__ == "__main__":
    main()
