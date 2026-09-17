#!/usr/bin/env python3
"""Generate bank.json from questions.md (single source of truth for the Chakra bank).

Usage (from the kit root or anywhere):
  python3 loop/rounds/00_ai_screen/build_bank.py          # write bank.json, print the count
  python3 loop/rounds/00_ai_screen/build_bank.py --check  # exit 1 if bank.json is stale

Every markdown table row whose first cell looks like an id (A01, B12, ...) becomes one item:
  {"round": "ai", "id", "segment", "q", "principle", "story", "keys", "source"}
`mock.py bq ai` reads the same fields the other rounds use (q / principle / source) and
prints story + keys when present.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "questions.md"
OUT = HERE / "bank.json"
SEGMENT = {"A": "experience", "B": "scenario", "C": "collaboration", "D": "followup", "E": "wrapup"}
ROW = re.compile(r"^\|\s*([A-E]\d{2})\s*\|")


def split_row(line: str) -> list[str]:
    """Split a markdown table row on unescaped pipes; `\\|` inside a cell is kept as `|`."""
    cells, cur, i = [], [], 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "|":
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells[1:-1]  # drop the empty ends produced by the leading/trailing pipe


def parse() -> list[dict]:
    items = []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if not ROW.match(line):
            continue
        cells = split_row(line)
        if len(cells) != 6:
            sys.exit(f"bad row (expected 6 cells, got {len(cells)}): {line[:80]}")
        id_, q, principle, story, keys, source = cells
        items.append(
            {
                "round": "ai",
                "id": id_,
                "segment": SEGMENT[id_[0]],
                "q": q,
                "principle": principle,
                "story": story,
                "keys": keys,
                "source": source,
            }
        )
    ids = [it["id"] for it in items]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        sys.exit(f"duplicate ids: {sorted(dup)}")
    return items


def main() -> None:
    items = parse()
    text = json.dumps(items, ensure_ascii=False, indent=1) + "\n"
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            sys.exit(f"{OUT.name} is stale — run build_bank.py")
        print(f"{OUT.name} up to date: {len(items)} 题")
        return
    OUT.write_text(text, encoding="utf-8")
    by_seg = {}
    for it in items:
        by_seg[it["segment"]] = by_seg.get(it["segment"], 0) + 1
    print(f"wrote {OUT.relative_to(HERE.parent.parent.parent)}: {len(items)} 题 {by_seg}")


if __name__ == "__main__":
    main()
