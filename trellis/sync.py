"""Sync: project the skeleton into the Obsidian vault as linked notes.

Generates one note per skeleton node (vault/map/<node-id>.md) plus a root
map-of-content note, so Obsidian's graph view and backlinks mirror the
skeleton. Each generated note owns only the region between

    %% trellis:begin %%  ...  %% trellis:end %%

(`%%` is Obsidian's comment syntax, so the markers are invisible in
preview). Anything outside the markers — your own notes — is preserved
across syncs. Deleting a node from the skeleton leaves its note behind;
sync reports such orphans instead of deleting user content.
"""

from __future__ import annotations

import re
from pathlib import Path

from .cards import Card
from .clippings import Clipping, canonical_url
from .readings import Reading
from .sequence import core_leaves, sequence
from .skeleton import Node, Skeleton

BEGIN = "%% trellis:begin %%"
END = "%% trellis:end %%"
_BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)


def _link(node: Node, prefix: str = "") -> str:
    """Path-qualified wikilink. Node ids such as `round` or `rules` repeat across domains
    (narrative and code-core both have `round.formats`), and a bare `[[round]]` is ambiguous
    in one Obsidian vault holding every domain — so links carry the domain's folder:
    `[[interviews/rounds/code-core/map/round|Round]]`. Unique names resolve the same way."""
    return f"[[{prefix}{node.id}|{node.title}]]"


def _prefix(skeleton: Skeleton) -> str:
    return f"{skeleton.folder}/map/" if skeleton.folder else "map/"


def _moc_body(skeleton: Skeleton) -> str:
    lines = [f"# {skeleton.title}", ""]
    prefix = _prefix(skeleton)

    def visit(node: Node, depth: int) -> None:
        lines.append("    " * depth + f"- {_link(node, prefix)}")
        for child in node.children:
            visit(child, depth + 1)

    for root in skeleton.roots:
        visit(root, 0)
    return "\n".join(lines)


def _node_body(
    skeleton: Skeleton,
    node: Node,
    cards: list[Card],
    readings: list[Reading],
    drills: list[Reading],
    cases: list[Reading],
) -> str:
    crumbs = " / ".join(n.title for n in node.path()[:-1])
    prefix = _prefix(skeleton)
    lines = [f"# {node.title}"]
    if crumbs:
        lines.append(f"*{crumbs}*")
    if node.summary:
        lines += ["", node.summary]
    if node.is_leaf and node.id in core_leaves(skeleton):
        lines += ["", "**Core** — part of the first pass through this subject."]
    if node.requires:
        lines += ["", "**Requires:** " + ", ".join(
            _link(skeleton.by_id[r], prefix) for r in node.requires
        )]
    if node.children:
        lines += ["", "## Topics"]
        lines += [f"- {_link(c, prefix)}" for c in node.children]
    dependents = [n for n in skeleton.walk() if node.id in n.requires]
    if dependents:
        lines += ["", "**Unlocks:** " + ", ".join(_link(d, prefix) for d in dependents)]
    node_readings = [r for r in readings if node.id in r.nodes]
    if node_readings:
        lines += ["", "## Readings"]
        lines += [f"- [[{r.link_target}|{r.title}]]" for r in node_readings]
    node_cases = [c for c in cases if node.id in c.nodes]
    if node_cases:
        lines += ["", "## Cases"]
        lines += [f"- [[{c.path.stem}|{c.title}]] — `{c.extra.get('codebase')}`"
                  for c in node_cases]
    node_drills = [d for d in drills if node.id in d.nodes]
    if node_drills:
        lines += ["", "## Drills"]
        lines += [f"- [[{d.link_target}|{d.title}]]" for d in node_drills]
    # Numbered, because this is the order they will be met in (their `step`,
    # then the rest, grown cards last) — the same order Anki deals them.
    node_cards = [c for c in sequence(skeleton, cards) if c.node == node.id]
    if node_cards:
        lines += ["", f"## Cards ({len(node_cards)})"]
        lines += [f"{i}. [[{c.id}]]" for i, c in enumerate(node_cards, start=1)]
    return "\n".join(lines)


def write_managed(path: Path, body: str) -> bool:
    """Insert or replace the managed block in path. Returns True if the
    file changed."""
    block = f"{BEGIN}\n{body}\n{END}"
    if path.exists():
        old = path.read_text(encoding="utf-8")
        if _BLOCK_RE.search(old):
            new = _BLOCK_RE.sub(lambda _: block, old, count=1)
        else:
            new = old.rstrip("\n") + "\n\n" + block + "\n"
    else:
        new = block + "\n\n## Notes\n"
    if path.exists() and new == old:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new, encoding="utf-8")
    return True


def _reading_body(reading: Reading, clip: "Clipping | None") -> str:
    """The managed tail of a reading note: where the card lands, and where
    the archived article is embedded so it reads inside Obsidian."""
    lines = ["## Source", f"[Open the original ↗]({reading.url})"] if reading.url else []
    if clip is not None:
        lines += ["", "## Archived copy", f"![[{clip.path.stem}]]"]
    return "\n".join(lines)


def sync(
    skeleton: Skeleton,
    cards: list[Card],
    vault_dir: str | Path,
    readings: list[Reading] | None = None,
    drills: list[Reading] | None = None,
    cases: list[Reading] | None = None,
    clippings: dict[str, "Clipping"] | None = None,
) -> dict:
    """Regenerate map notes and the managed tail of each reading note.
    Returns {'written': [...], 'orphans': [...]}."""
    readings = readings or []
    drills = drills or []
    cases = cases or []
    clippings = clippings or {}
    vault = Path(vault_dir)
    map_dir = vault / "map"
    written: list[str] = []

    moc_path = vault / f"{skeleton.title} MOC.md"
    if write_managed(moc_path, _moc_body(skeleton)):
        written.append(str(moc_path))

    for node in skeleton.walk():
        path = map_dir / f"{node.id}.md"
        if write_managed(path, _node_body(skeleton, node, cards, readings, drills, cases)):
            written.append(str(path))

    for reading in readings:
        body = _reading_body(reading, clippings.get(canonical_url(reading.url)))
        if body and write_managed(reading.path, body):
            written.append(str(reading.path))

    known = {f"{n.id}.md" for n in skeleton.walk()}
    orphans = sorted(
        str(p) for p in map_dir.glob("*.md") if p.name not in known
    ) if map_dir.exists() else []
    return {"written": written, "orphans": orphans}
