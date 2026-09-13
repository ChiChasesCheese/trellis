"""Adopt: turn a correctly-shaped pile of content into a domain.

Trellis discovers domains from `skeleton/*.yaml` and nowhere else, which
means content authored somewhere the repo is not — another machine, an
afternoon in Obsidian on a phone, an import from a course — is invisible
to every command no matter how correct its format is. The vault grows a
folder; the tool sees nothing; the folder never gets built, never gets
reviewed, and never enters the loop.

`trellis adopt` closes that. It reads the `node:` lines the cards already
carry, reconstructs the tree those dotted ids imply, and writes the
skeleton that was latent in them all along. Nothing is invented: every
node in the output is a prefix of an id some real card claimed.

What it cannot recover is **study order**, because nothing in a pile of
cards records it. Children come out sorted, and the header says so. That
is the one thing to fix by hand afterwards, and it is a five-minute job
on a file that would otherwise not exist.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

_HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_SKIP_DIRS = {"clippings", "cards", "readings", "drills", "cases", "map"}


@dataclass
class Adoptable:
    """A vault folder holding content that no skeleton claims."""

    name: str
    path: Path
    cards: int
    readings: int
    node_ids: set[str]


def _frontmatter_nodes(path: Path) -> list[str]:
    """Every node id a content file claims, without going through the
    strict parsers — adoption has to tolerate what it finds."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return []
    if not raw.startswith("---\n"):
        return []
    try:
        _, fm, _ = raw.split("---\n", 2)
        meta = yaml.safe_load(fm)
    except (ValueError, yaml.YAMLError):
        return []
    if not isinstance(meta, dict):
        return []
    out: list[str] = []
    if isinstance(meta.get("node"), str):
        out.append(meta["node"])
    nodes = meta.get("nodes")
    if isinstance(nodes, list):
        out += [n for n in nodes if isinstance(n, str)]
    return out


def find_adoptable(root: str | Path) -> list[Adoptable]:
    """Vault folders with content but no skeleton — the whole point being
    that the tool should say so rather than silently ignore them."""
    root = Path(root)
    vault = root / "vault"
    if not vault.exists():
        return []
    known = {f.stem for f in (root / "skeleton").glob("*.yaml")}
    found: list[Adoptable] = []
    for folder in sorted(p for p in vault.iterdir() if p.is_dir()):
        if folder.name.startswith(".") or folder.name in known:
            continue
        cards = sorted((folder / "cards").rglob("*.md")) if (folder / "cards").exists() else []
        readings = sorted((folder / "readings").glob("*.md")) if (folder / "readings").exists() else []
        node_ids: set[str] = set()
        for path in cards + readings:
            node_ids.update(_frontmatter_nodes(path))
        if node_ids:
            found.append(Adoptable(folder.name, folder, len(cards),
                                   len(readings), node_ids))
    return found


def _titles_from_map(content_dir: Path) -> dict[str, str]:
    """Map notes already carry the human name of every node they mirror.
    When a folder was built by hand in the shape of a domain, this is
    where its titles are, and reusing them is the difference between
    `Stripe.Algorithms` and `算法套路`."""
    titles: dict[str, str] = {}
    map_dir = content_dir / "map"
    if not map_dir.exists():
        return titles
    for path in sorted(map_dir.glob("*.md")):
        match = _HEADING_RE.search(path.read_text(encoding="utf-8"))
        if match:
            titles[path.stem] = match.group(1).strip()
    return titles


def _titleize(node_id: str) -> str:
    return node_id.rsplit(".", 1)[-1].replace("-", " ").title()


def derive_skeleton(
    node_ids: set[str],
    domain: str,
    content_dir: Path,
    title: str | None = None,
) -> str:
    """The YAML that was latent in the cards. Every ancestor of a claimed
    id becomes a node, because a dotted id is a path and a path with a
    missing segment is not a tree."""
    titles = _titles_from_map(content_dir)

    full: set[str] = set()
    for node_id in node_ids:
        parts = node_id.split(".")
        for i in range(1, len(parts) + 1):
            full.add(".".join(parts[:i]))

    children: dict[str, list[str]] = {n: [] for n in full}
    roots: list[str] = []
    for node_id in sorted(full):
        parent = node_id.rsplit(".", 1)[0] if "." in node_id else None
        if parent is None:
            roots.append(node_id)
        else:
            children[parent].append(node_id)

    def emit(node_id: str, depth: int, ordinal: int | None) -> list[str]:
        pad = "  " * depth
        lines = [f"{pad}- id: {node_id}"]
        if ordinal is not None:
            lines.append(f"{pad}  order: {ordinal}")
        name = titles.get(node_id) or _titleize(node_id)
        lines.append(f"{pad}  title: {yaml.safe_dump(name).strip()}"
                     if ":" in name or name.startswith(("&", "*", "!"))
                     else f"{pad}  title: {name}")
        kids = children[node_id]
        if kids:
            lines.append(f"{pad}  children:")
            for kid in kids:
                lines += emit(kid, depth + 2, None)
        return lines

    header = [
        f"# Derived by `trellis adopt {domain}` from the node ids the cards",
        f"# in vault/{domain}/ already carried. Every node here is a prefix of",
        "# an id a real card claimed — nothing was invented.",
        "#",
        "# STUDY ORDER IS NOT RECOVERABLE from a pile of cards, so children are",
        "# sorted. Reorder them into the order you would learn them, add",
        "# `summary:` lines, and add `requires:` edges — those three edits are",
        "# what turn a valid skeleton into a useful one.",
        f"domain: {domain}",
        f"title: {title or _titleize(domain)}",
        "nodes:",
    ]
    body: list[str] = []
    for i, root in enumerate(roots, start=1):
        body += emit(root, 1, i if len(roots) > 1 else 1)
    return "\n".join(header + body) + "\n"
