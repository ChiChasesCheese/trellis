"""Skeleton: the YAML mind map that constrains everything else.

Format (skeleton/<domain>.yaml):

    domain: system-design          # slug, used for deck/vault naming
    title: System Design           # display name, Anki root deck
    lang: en                       # language the cards are written in (default en)
    nodes:
      - id: storage                # dotted ids; children repeat the parent prefix
        title: Storage
        summary: one-liner shown in node notes and LLM prompts
        children:
          - id: storage.replication
            title: Replication
            requires: [consistency.cap]   # cross-tree prerequisite edges

Rules enforced here:
  * ids unique, non-empty, and prefixed by their parent's id
  * list order == study order (no explicit order field to drift)
  * `requires` must reference existing nodes and form no cycle
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.[a-z0-9]+(?:-[a-z0-9]+)*)*$")


class SkeletonError(ValueError):
    """Raised when a skeleton file violates the format rules."""


@dataclass
class Node:
    id: str
    title: str
    summary: str = ""
    requires: list[str] = field(default_factory=list)
    children: list["Node"] = field(default_factory=list)
    parent: "Node | None" = None
    order: int | None = None  # stable deck ordinal, top-level only

    @property
    def is_leaf(self) -> bool:
        return not self.children

    def path(self) -> list["Node"]:
        """Ancestors from root to self, inclusive."""
        chain: list[Node] = []
        node: Node | None = self
        while node is not None:
            chain.append(node)
            node = node.parent
        return list(reversed(chain))


@dataclass
class Skeleton:
    domain: str
    title: str
    roots: list[Node]
    by_id: dict[str, Node]
    # The language cards in this domain are written in. A domain studied
    # from a Chinese book is written in Chinese; there is no English
    # original to keep. Terms of art stay English in any language.
    lang: str = "en"

    def leaves(self) -> list[Node]:
        return [n for n in self.walk() if n.is_leaf]

    def walk(self) -> list[Node]:
        """All nodes in study order (depth-first, list order)."""
        out: list[Node] = []

        def visit(node: Node) -> None:
            out.append(node)
            for child in node.children:
                visit(child)

        for root in self.roots:
            visit(root)
        return out

    def deck_name(self, node: Node) -> str:
        """Anki deck path, e.g. 'System Design::04 Storage::Replication'.

        Top-level branches carry a 1-based ordinal so Anki's alphabetical
        deck list follows study order.
        """
        parts = [self.title]
        for n in node.path():
            if n.parent is None:
                # explicit order pins the deck name across future branch
                # insertions — deck names are identities in Anki
                ordinal = n.order if n.order is not None else self.roots.index(n) + 1
                parts.append(f"{ordinal:02d} {n.title}")
            else:
                parts.append(n.title)
        return "::".join(parts)


def _parse_node(raw: object, parent: Node | None, errors: list[str]) -> Node | None:
    if not isinstance(raw, dict):
        errors.append(f"node must be a mapping, got: {raw!r}")
        return None
    node_id = raw.get("id")
    title = raw.get("title")
    if not isinstance(node_id, str) or not _ID_RE.match(node_id):
        errors.append(f"invalid node id: {node_id!r} (want dotted lowercase, e.g. storage.replication)")
        return None
    if parent is not None and not node_id.startswith(parent.id + "."):
        errors.append(f"node {node_id!r} must be prefixed by its parent id {parent.id!r}")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"node {node_id!r}: missing title")
        title = node_id
    unknown = set(raw) - {"id", "title", "summary", "requires", "children", "order"}
    if unknown:
        errors.append(f"node {node_id!r}: unknown keys {sorted(unknown)}")
    order = raw.get("order")
    if order is not None and (parent is not None or not isinstance(order, int)):
        errors.append(f"node {node_id!r}: order must be an integer on top-level nodes only")
        order = None
    requires = raw.get("requires", [])
    if not (isinstance(requires, list) and all(isinstance(r, str) for r in requires)):
        errors.append(f"node {node_id!r}: requires must be a list of node ids")
        requires = []
    node = Node(
        id=node_id,
        title=title.strip(),
        summary=str(raw.get("summary", "") or "").strip(),
        requires=list(requires),
        parent=parent,
        order=order,
    )
    for raw_child in raw.get("children", []) or []:
        child = _parse_node(raw_child, node, errors)
        if child is not None:
            node.children.append(child)
    return node


def load_skeleton(path: str | Path) -> Skeleton:
    """Load and fully validate a skeleton file. Raises SkeletonError with
    every problem found (not just the first)."""
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SkeletonError(f"{path}: top level must be a mapping")

    errors: list[str] = []
    domain = data.get("domain")
    title = data.get("title")
    if not isinstance(domain, str) or not re.match(r"^[a-z0-9-]+$", domain or ""):
        errors.append(f"invalid domain: {domain!r} (want a lowercase slug)")
        domain = "unknown"
    if not isinstance(title, str) or not title.strip():
        errors.append("missing title")
        title = domain

    roots: list[Node] = []
    for raw in data.get("nodes", []) or []:
        node = _parse_node(raw, None, errors)
        if node is not None:
            roots.append(node)
    if not roots:
        errors.append("skeleton has no nodes")

    orders = [n.order for n in roots if n.order is not None]
    if orders and len(orders) != len(roots):
        errors.append("either every top-level node has an order or none do")
    if len(set(orders)) != len(orders):
        errors.append("duplicate top-level order values")

    lang = data.get("lang", "en") or "en"
    if not isinstance(lang, str) or not re.match(r"^[a-z]{2}(-[a-z]{2})?$", lang):
        errors.append(f"invalid lang: {lang!r} (want a language code such as en or zh)")
        lang = "en"

    skeleton = Skeleton(domain=domain, title=title.strip(), roots=roots, by_id={},
                        lang=lang)
    for node in skeleton.walk():
        if node.id in skeleton.by_id:
            errors.append(f"duplicate node id: {node.id!r}")
        skeleton.by_id[node.id] = node

    for node in skeleton.walk():
        for req in node.requires:
            if req not in skeleton.by_id:
                errors.append(f"node {node.id!r}: requires unknown node {req!r}")
            elif req == node.id:
                errors.append(f"node {node.id!r}: requires itself")

    cycle = _find_requires_cycle(skeleton)
    if cycle:
        errors.append("requires cycle: " + " -> ".join(cycle))

    # Study order (tree order) must never contradict the requires edges:
    # a prerequisite has to appear earlier in the walk.
    order = {n.id: i for i, n in enumerate(skeleton.walk())}
    for node in skeleton.walk():
        for req in node.requires:
            if req in order and req != node.id and order[req] >= order[node.id]:
                errors.append(
                    f"node {node.id!r} is ordered before its prerequisite {req!r} "
                    "— move it later in the tree"
                )

    if errors:
        raise SkeletonError(f"{path}:\n  " + "\n  ".join(errors))
    return skeleton


def _find_requires_cycle(skeleton: Skeleton) -> list[str] | None:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n.id: WHITE for n in skeleton.walk()}
    stack: list[str] = []

    def dfs(node_id: str) -> list[str] | None:
        color[node_id] = GRAY
        stack.append(node_id)
        for req in skeleton.by_id[node_id].requires:
            if req not in color:
                continue  # unknown target already reported
            if color[req] == GRAY:
                return stack[stack.index(req):] + [req]
            if color[req] == WHITE:
                found = dfs(req)
                if found:
                    return found
        color[node_id] = BLACK
        stack.pop()
        return None

    for node_id in color:
        if color[node_id] == WHITE:
            found = dfs(node_id)
            if found:
                return found
    return None
