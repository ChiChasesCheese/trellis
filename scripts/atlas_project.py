"""Write the public projection of a local skeleton: only the nodes that hold a git-tracked card.

    uv run python scripts/atlas_project.py sysdesign      # skeleton/sysdesign.yaml -> atlas/skeletons/sysdesign.yaml

The Atlas (ADR 0014) reads `atlas/skeletons/<domain>.yaml` in place of `skeleton/<domain>.yaml` when it is tracked.
Needed for a merged view such as 系统设计, whose source skeleton stays local because it carries the map of folders that
are never published. Every title and summary is checked against the private terms (as scripts/private_guard.py does);
a match drops the node and its subtree, and only the count is printed. Idempotent.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from trellis.atlas import project_skeleton, projection_header, projection_path, tracked_files  # noqa: E402
from trellis.cards import CardError, parse_card  # noqa: E402


def node_cards(data: dict, root: Path, tracked: set[str]) -> dict[str, set[str]]:
    """node id -> folders holding its cards; an untracked card's folder is written `!<folder>`."""
    out: dict[str, set[str]] = {}
    for folder in [data.get("vault", data["domain"]), *(data.get("include") or [])]:
        base = root / "vault" / folder / "cards"
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            try:
                card = parse_card(path)
            except CardError:
                continue
            mark = folder if path.relative_to(root).as_posix() in tracked else f"!{folder}"
            out.setdefault(card.node, set()).add(mark)
    return out


def private_pattern():
    import private_guard
    return private_guard.pattern(private_guard.terms())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("domain")
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args(argv)
    root = args.root
    src = root / "skeleton" / f"{args.domain}.yaml"
    data = yaml.safe_load(src.read_text(encoding="utf-8"))
    tracked = tracked_files(root)
    proj = project_skeleton(data, node_cards(data, root, tracked), tracked, private_pattern())
    out = root / projection_path(args.domain)
    out.parent.mkdir(parents=True, exist_ok=True)
    body = yaml.safe_dump(proj.data, allow_unicode=True, sort_keys=False, width=1000)
    out.write_text(projection_header(args.domain) + body, encoding="utf-8")
    print(f"{args.domain}: {proj.kept} node(s) kept, {proj.dropped} dropped, {proj.top_level} top-level branch(es) -> {out}")
    for why, n in sorted(proj.dropped_by.items()):
        print(f"    dropped {n}: {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
