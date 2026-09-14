"""Readings: long-form notes attached to the same skeleton.

Cards are for fragments of spare time; readings are for systematic,
authoritative material — saved articles, paper notes, guided links to
engineering blogs. A reading lives under vault/<folder>/readings/ and
attaches to one or more skeleton nodes:

    ---
    nodes: [distributed.consensus, distributed.replication]
    url: https://raft.github.io/raft.pdf
    ---
    # In Search of an Understandable Consensus Algorithm
    Why read: ...

Readings and cards reference each other with ordinary Obsidian wikilinks
(filenames are the identities); `trellis sync` lists both on each node's
map note, so the graph connects topic <-> reading <-> card.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


class ReadingError(ValueError):
    """Raised for a reading file that violates the format."""


@dataclass
class Reading:
    path: Path
    title: str
    nodes: list[str]
    url: str = ""
    tags: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    @property
    def link_target(self) -> str:
        return self.path.stem


def parse_reading(path: str | Path, allowed_extra: frozenset[str] = frozenset()) -> Reading:
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ReadingError(f"{path}: missing YAML frontmatter")
    try:
        _, fm, body = raw.split("---\n", 2)
    except ValueError:
        raise ReadingError(f"{path}: unterminated frontmatter") from None
    meta = yaml.safe_load(fm)
    if not isinstance(meta, dict):
        raise ReadingError(f"{path}: frontmatter must be a mapping")

    nodes = meta.get("nodes")
    if isinstance(nodes, str):
        nodes = [nodes]
    if not (isinstance(nodes, list) and nodes and all(isinstance(n, str) for n in nodes)):
        raise ReadingError(f"{path}: 'nodes' must be a node id or non-empty list of node ids")
    tags = meta.get("tags", []) or []
    if not (isinstance(tags, list) and all(isinstance(t, str) for t in tags)):
        raise ReadingError(f"{path}: tags must be a list of strings")
    unknown = set(meta) - {"nodes", "url", "tags", "title"} - set(allowed_extra)
    if unknown:
        raise ReadingError(f"{path}: unknown frontmatter keys {sorted(unknown)}")

    title = meta.get("title") or ""
    if not title:
        match = _H1_RE.search(body)
        title = match.group(1).strip() if match else path.stem
    return Reading(
        path=path,
        title=str(title),
        nodes=list(nodes),
        url=str(meta.get("url", "") or ""),
        tags=list(tags),
        extra={k: meta[k] for k in allowed_extra if k in meta},
    )


def load_readings(readings_dir: str | Path,
                  allowed_extra: frozenset[str] = frozenset(),
                  ) -> tuple[list[Reading], list[str]]:
    readings: list[Reading] = []
    errors: list[str] = []
    for path in sorted(Path(readings_dir).rglob("*.md")):
        try:
            readings.append(parse_reading(path, allowed_extra))
        except ReadingError as exc:
            errors.append(str(exc))
    return readings, errors
