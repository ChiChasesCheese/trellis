"""Write each domain's knowledge tree as an Obsidian outline note, to be viewed as a mind map (Mindmap NextGen plugin).

    uv run python scripts/knowledge_tree.py                 # every domain with a skeleton
    uv run python scripts/knowledge_tree.py hello-interview  # some domains

The skeleton is the tree; this only draws it, so the map never drifts from the Anki decks. Each node shows its card
count (cards under it, its subtree included). The note goes to `vault/<skeleton folder>/<title> 知识树.md`; regenerate it
after the skeleton changes. A domain whose vault folder is gitignored keeps its tree local too.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trellis.skeleton import load_skeleton  # noqa: E402

HEADER = """---
markmap:
  initialExpandLevel: 2
  colorFreezeLevel: 2
  maxWidth: 260
tags: [知识树]
---
"""


def card_nodes(folder: Path) -> Counter:
    per = Counter()
    for f in folder.rglob("*.md"):
        head = f.read_text(encoding="utf-8", errors="replace")[:400]
        m = re.search(r"^node: (\S+)$", head, re.M)
        if m:
            per[m.group(1)] += 1
    return per


def write(domain: str) -> Path | None:
    sk = load_skeleton(ROOT / "skeleton" / f"{domain}.yaml")
    vault = ROOT / "vault" / sk.folder
    if not vault.is_dir():
        return None
    direct = card_nodes(vault)
    total: dict[str, int] = {}

    def count(n) -> int:
        total[n.id] = direct.get(n.id, 0) + sum(count(k) for k in n.children)
        return total[n.id]

    lines = [HEADER, f"# {sk.title}", ""]

    def emit(n, depth: int) -> None:
        if total[n.id] == 0:
            return
        lines.append("  " * depth + f"- {n.title} · {total[n.id]}")
        for k in n.children:
            emit(k, depth + 1)

    for r in sk.roots:
        count(r)
    for r in sk.roots:
        emit(r, 0)
    out = vault / f"{sk.title} 知识树.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> int:
    domains = sys.argv[1:] or sorted(p.stem for p in (ROOT / "skeleton").glob("*.yaml"))
    for d in domains:
        try:
            out = write(d)
        except Exception as e:  # noqa: BLE001 - one bad skeleton must not stop the rest
            print(f"{d}: skipped ({e})")
            continue
        if out:
            print(f"{d}: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
