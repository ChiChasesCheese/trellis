"""Fold a project's separately written reading/recall cards into its quick-card files.

    uv run python scripts/lcp_merge_read.py <slug> [...]

A reading-card writer that runs while another agent edits `points/<slug>.json` writes `points/<slug>.read.json` and
`cards/<slug>.read.jsonl` instead. This puts those points first (reading, then recall, as LCP_READ_AGENT.md asks),
appends the cards, skips any kp already present, and moves the two side files to ~/.local/state/lcp-merged-read/.
"""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

HOME = Path(__file__).resolve().parents[1] / "sources/local/lc-project/quick"
BACKUP = Path.home() / ".local/state/lcp-merged-read"


def merge(slug: str) -> str:
    side_points, side_cards = HOME / "points" / f"{slug}.read.json", HOME / "cards" / f"{slug}.read.jsonl"
    if not side_points.exists():
        return f"{slug}: no side files"
    main_points, main_cards = HOME / "points" / f"{slug}.json", HOME / "cards" / f"{slug}.jsonl"
    old = json.loads(main_points.read_text(encoding="utf-8")) if main_points.exists() else []
    have = {p["kp"] for p in old}
    new = [p for p in json.loads(side_points.read_text(encoding="utf-8")) if p["kp"] not in have]
    main_points.write_text(json.dumps(new + old, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = main_cards.read_text(encoding="utf-8").splitlines() if main_cards.exists() else []
    card_kps = {json.loads(l)["kp"] for l in lines if l.strip()}
    added = [l for l in side_cards.read_text(encoding="utf-8").splitlines()
             if l.strip() and json.loads(l)["kp"] not in card_kps]
    main_cards.write_text("\n".join([l for l in lines if l.strip()] + added) + "\n", encoding="utf-8")
    dest = BACKUP / f"{slug}-{time.strftime('%Y%m%d-%H%M%S')}"
    dest.mkdir(parents=True, exist_ok=True)
    for f in (side_points, side_cards):
        shutil.move(str(f), dest / f.name)
    return f"{slug}: {len(new)} points first, {len(added)} cards appended; side files in {dest}"


if __name__ == "__main__":
    for s in sys.argv[1:]:
        print(merge(s))
