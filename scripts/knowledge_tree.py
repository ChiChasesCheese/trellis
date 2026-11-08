"""Write each domain's knowledge tree as an Obsidian outline note, to be viewed as a mind map (Mindmap NextGen plugin).

    uv run python scripts/knowledge_tree.py                 # every domain with a skeleton
    uv run python scripts/knowledge_tree.py hello-interview  # some domains
    uv run python scripts/knowledge_tree.py --depth 2 sysdesign   # only the top levels (the merged view holds local-only maps)

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

# No YAML frontmatter: on mobile the plugin's YAML parser reads process.env and the map renders blank. Folding is set
# per node with markmap's inline comment instead, which works on every platform.
FOLD = " <!-- markmap: fold -->"
FOLD_FROM = 1  # depth from which a node with children starts folded: decks and their sections show, the rest on tap


def card_nodes(folder: Path) -> Counter:
    per = Counter()
    for f in folder.rglob("*.md"):
        head = f.read_text(encoding="utf-8", errors="replace")[:400]
        m = re.search(r"^node: (\S+)$", head, re.M)
        if m:
            per[m.group(1)] += 1
    return per


def write(domain: str, max_depth: int = 0) -> Path | None:
    sk = load_skeleton(ROOT / "skeleton" / f"{domain}.yaml")
    vault = ROOT / "vault" / sk.folder
    if not vault.is_dir():
        return None
    direct = card_nodes(vault)
    for extra in sk.include:  # a merged view counts the folders it owns too
        direct.update(card_nodes(ROOT / "vault" / extra))
    total: dict[str, int] = {}

    def count(n) -> int:
        total[n.id] = direct.get(n.id, 0) + sum(count(k) for k in n.children)
        return total[n.id]

    lines = [f"# {sk.title}", ""]

    def emit(n, depth: int) -> None:
        if total[n.id] == 0 or (max_depth and depth >= max_depth):
            return
        deeper = any(total[k.id] for k in n.children) and not (max_depth and depth + 1 >= max_depth)
        fold = FOLD if depth >= FOLD_FROM and deeper else ""
        lines.append("  " * depth + f"- {n.title} · {total[n.id]}{fold}")
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
    args = sys.argv[1:]
    depth = 0
    if "--depth" in args:
        i = args.index("--depth")
        depth = int(args[i + 1])
        del args[i:i + 2]
    domains = args or sorted(p.stem for p in (ROOT / "skeleton").glob("*.yaml"))
    for d in domains:
        try:
            out = write(d, depth)
        except Exception as e:  # noqa: BLE001 - one bad skeleton must not stop the rest
            print(f"{d}: skipped ({e})")
            continue
        if out:
            print(f"{d}: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
