"""A view of the LeetCode knowledge tree: every problem carrying a tag, as a sprint-deck plan (Chi, 2026-11-14).

    uv run python scripts/lc_view.py 公司::Amazon -o sources/local/plan/views/amazon.json
    uv run python scripts/lc_view.py 榜单::Top_Interview_150 -o …   # any 榜单:: / 公司:: / 必读 tag

Every problem has one card, on its tree leaf (`lct-<slug>`), tagged with the lists and companies it belongs to
(scripts/lc_tags.py). A view is the tagged problems in the tree's order, one sub-deck per top-level list of the tree;
deal it with scripts/company_deck.py (config `company`: add {"deck": "8 Amazon 力扣", "plan": <file>, "new_per_day": 10}),
and `release` it when done: the cards go back to the tree. For a quick look without a deck, search the tag in Anki.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anki_refresh import call  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def tree_order() -> list[tuple[str, str]]:
    """(top-level list title, card id) for every problem card, in the tree's order."""
    sk = yaml.safe_load((ROOT / "skeleton/leetcode-tree.yaml").read_text(encoding="utf-8"))
    cards = ROOT / "vault/interviews/core/leetcode/tree/cards"
    by_leaf: dict[str, list[tuple[int, str]]] = {}
    for f in cards.rglob("lct-*.md"):
        if f.name.startswith("lct-learn-"):
            continue
        head = f.read_text(encoding="utf-8")[:400]
        node = next(line[6:] for line in head.splitlines() if line.startswith("node: "))
        step = next((int(line[6:]) for line in head.splitlines() if line.startswith("step: ")), 99)
        by_leaf.setdefault(node, []).append((step, f.stem))
    out = []

    def walk(n: dict, top: str) -> None:
        for _, cid in sorted(by_leaf.get(n["id"], [])):
            out.append((top, cid))
        for k in n.get("children") or []:
            walk(k, top)

    for top in sk["nodes"]:
        walk(top, top["title"])
    return out


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 2
    tag = a[0]
    nids = call("findNotes", query=f'"tag:{tag}"')
    tagged = set()
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            tagged |= {t[4:] for t in n["tags"] if t.startswith("id::lct-")}
    parts: dict[str, list[str]] = {}
    for top, cid in tree_order():
        if cid in tagged:
            parts.setdefault(top, []).append(cid)
    plan = [{"label": f"{i:02d} {top}", "ids": ids} for i, (top, ids) in enumerate(parts.items(), 1)]
    if "-o" in a:
        out = ROOT / a[a.index("-o") + 1]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{tag}: {sum(len(p['ids']) for p in plan)} problems in {len(plan)} parts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
