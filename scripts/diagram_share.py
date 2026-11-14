"""How many cards of each domain carry a diagram (Chi, 2026-11-13: every deck at least 25%).

    uv run python scripts/diagram_share.py                 # every domain
    uv run python scripts/diagram_share.py test-release    # some domains; exit 1 if one is below the floor
    uv run python scripts/diagram_share.py --below         # only domains under the floor

A diagram is a ```mermaid block, an <svg> block (bare, or fenced as ```svg), or an embedded image (![[…]] or ![…](…)) in the card's answer.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FLOOR = 0.25
DIAGRAM = re.compile(r"^```(?:mermaid|svg)\b|^<svg\b|!\[\[[^\]]+\.(?:png|jpe?g|svg|gif|webp)\]\]|!\[[^\]]*\]\([^)]+\)", re.M)


def share(domain: str) -> tuple[int, int] | None:
    d = yaml.safe_load((ROOT / "skeleton" / f"{domain}.yaml").read_text(encoding="utf-8"))
    if not isinstance(d, dict) or not d.get("vault"):
        return None
    base = ROOT / "vault" / d["vault"]
    cards = with_fig = 0
    for f in base.rglob("*.md"):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if not (t.startswith("---") and re.search(r"^id: ", t[:400], re.M) and "## A" in t):
            continue
        cards += 1
        with_fig += bool(DIAGRAM.search(t))
    return (with_fig, cards) if cards else None


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    below = "--below" in sys.argv
    domains = args or sorted(p.stem for p in (ROOT / "skeleton").glob("*.yaml"))
    bad = 0
    for d in domains:
        r = share(d)
        if not r:
            continue
        fig, n = r
        low = fig / n < FLOOR
        bad += low
        if low or not below:
            print(f"{d:22} {fig:5}/{n:<5} {fig / n:6.1%}{'  < 25%' if low else ''}")
    return 1 if args and bad else 0


if __name__ == "__main__":
    sys.exit(main())
