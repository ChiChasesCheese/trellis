"""Atlas scope: what may be published (ADR 0014), decided from `atlas.yaml` and git alone.

`atlas.yaml` lists the domains that are published and what is left out of them: a subtree whose node id names a
company, a subtree listed under `exclude`, and every card whose id names a company. Only files that git tracks are
ever read, so a machine that holds gitignored premium or private cards inside a published domain folder produces the
same output as CI does from the same commit.

The functions here are pure except `tracked_files` (asks git) and `load_published` (reads the tracked files).
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .cards import Card, CardError, parse_card
from .readings import Reading, ReadingError, parse_reading
from .skeleton import Skeleton, SkeletonError, load_skeleton

CONFIG_NAME = "atlas.yaml"
_WORD_SPLIT = re.compile(r"[.\-_]")
CORPUS_KEYS = frozenset({"corpus", "section"})


class AtlasError(ValueError):
    pass


@dataclass
class AtlasConfig:
    companies_from: str = ""
    aliases: dict[str, str] = field(default_factory=dict)
    domains: list[str] = field(default_factory=list)
    exclude: dict[str, list[str]] = field(default_factory=dict)
    allow_nodes: set[str] = field(default_factory=set)      # "<domain>:<node id>"
    allow_domains: set[str] = field(default_factory=set)    # a bare entry: the whole domain
    strip_tags: list[str] = field(default_factory=list)


def load_config(root: str | Path) -> AtlasConfig:
    path = Path(root) / CONFIG_NAME
    if not path.exists():
        raise AtlasError(f"no {CONFIG_NAME} in {root}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise AtlasError(f"{path}: top level must be a mapping")
    config = AtlasConfig(
        companies_from=str(data.get("companies_from") or ""),
        aliases={str(k): str(v) for k, v in (data.get("aliases") or {}).items()},
        domains=[str(d) for d in data.get("domains") or []],
        exclude={str(k): [str(x) for x in v or []] for k, v in (data.get("exclude") or {}).items()},
        strip_tags=[str(t) for t in data.get("strip_tags") or []],
    )
    for entry in data.get("allow") or []:
        entry = str(entry)
        (config.allow_nodes if ":" in entry else config.allow_domains).add(entry.strip())
    return config


# -- git -----------------------------------------------------------------------------------------

def tracked_files(root: str | Path) -> set[str]:
    """Every path git tracks under `root`, as posix paths relative to it."""
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout
    return {p for p in out.decode("utf-8").split("\0") if p}


# -- company words -------------------------------------------------------------------------------

def tokens(ident: str) -> tuple[str, ...]:
    return tuple(t for t in _WORD_SPLIT.split(ident.lower()) if t)


def company_words(config: AtlasConfig, tracked: set[str]) -> set[tuple[str, ...]]:
    """The words that name a company: every folder under `companies_from` that holds a tracked file, plus the
    aliases. A word is a token sequence, so a folder `jane-street` matches `jane-street` inside an id."""
    prefix = config.companies_from.strip("/") + "/"
    folders = {p[len(prefix):].split("/", 1)[0] for p in tracked if p.startswith(prefix) and "/" in p[len(prefix):]}
    words = {tokens(f) for f in folders}
    words |= {tokens(a) for a in config.aliases}
    return {w for w in words if w}


def has_company_word(ident: str, words: set[tuple[str, ...]]) -> bool:
    """A whole-word match inside an id split on `.`, `-`, `_`: `tt` is in `tt` and `hi-tt-lc-x`, not in `button`."""
    toks = tokens(ident)
    for w in words:
        n = len(w)
        if any(toks[i:i + n] == w for i in range(len(toks) - n + 1)):
            return True
    return False


def _under(node_id: str, prefix: str) -> bool:
    return node_id == prefix or node_id.startswith(prefix + ".")


# -- scope ---------------------------------------------------------------------------------------

@dataclass
class Scope:
    """What the Atlas may show, from the config and the company words."""

    config: AtlasConfig
    words: set[tuple[str, ...]]

    def domain_published(self, domain: str) -> bool:
        return domain in self.config.domains and (
            domain in self.config.allow_domains or not has_company_word(domain, self.words))

    def _allowed_prefix(self, domain: str, node_id: str) -> str | None:
        """The longest `allow` entry that covers this node (the node itself or an ancestor)."""
        best = None
        for entry in self.config.allow_nodes:
            d, _, nid = entry.partition(":")
            if d == domain and _under(node_id, nid) and (best is None or len(nid) > len(best)):
                best = nid
        return best

    def node_left_out(self, domain: str, node_id: str) -> str:
        """Why this node alone is left out ('' when it is not): `exclude` or a company word in its id. An allowed
        node, and what hangs under it, only count the part of the id below the allowed node."""
        if any(_under(node_id, p) for p in self.config.exclude.get(domain, [])):
            return "exclude"
        if domain in self.config.allow_domains:
            return ""
        allowed = self._allowed_prefix(domain, node_id)
        rest = node_id if allowed is None else node_id[len(allowed):]
        return "company" if has_company_word(rest, self.words) else ""

    def published(self, skeleton: Skeleton) -> set[str]:
        """Node ids of one skeleton that may be shown: not left out, and no ancestor left out."""
        keep: set[str] = set()
        for node in skeleton.walk():
            if self.node_left_out(skeleton.domain, node.id):
                continue
            if node.parent is not None and node.parent.id not in keep:
                continue
            keep.add(node.id)
        return keep

    def left_out_roots(self, skeleton: Skeleton) -> list[tuple[str, str]]:
        """(node id, reason) of each left-out subtree's top node."""
        keep = self.published(skeleton)
        out = []
        for node in skeleton.walk():
            if node.id in keep or (node.parent is not None and node.parent.id not in keep):
                continue
            out.append((node.id, self.node_left_out(skeleton.domain, node.id) or "parent"))
        return out

    def card_published(self, domain: str, card: Card, nodes: set[str]) -> bool:
        if card.node not in nodes:
            return False
        if domain in self.config.allow_domains or self._allowed_prefix(domain, card.node) is not None:
            return True     # the allowance covers what sits under the allowed node, ids included
        return not has_company_word(card.id, self.words)

    def tags(self, card: Card) -> list[str]:
        return [t for t in card.tags if not any(t.startswith(p) for p in self.config.strip_tags)]


# -- loading the tracked content -----------------------------------------------------------------

@dataclass
class PublishedDomain:
    skeleton: Skeleton
    nodes: set[str]                                         # published node ids
    cards: list[Card] = field(default_factory=list)         # published cards
    readings: list[Reading] = field(default_factory=list)
    # for `export --check`
    left_out: list[tuple[str, str, int]] = field(default_factory=list)   # (node id, reason, cards inside)
    card_ids_left_out: list[str] = field(default_factory=list)
    cards_left_out: int = 0                                 # tracked cards dropped by a company word in their id
    cards_orphan: int = 0                                   # tracked cards whose node is not in the skeleton
    untracked_cards: int = 0                                # card files on disk that git does not track


def _content_folders(skeleton: Skeleton) -> list[str]:
    return [f"vault/{skeleton.folder}"] + [f"vault/{extra}" for extra in skeleton.include]


def _tracked_md(tracked: set[str], prefix: str) -> list[str]:
    return sorted(p for p in tracked if p.startswith(prefix) and p.endswith(".md"))


def load_published(root: str | Path, scope: Scope, tracked: set[str],
                   count_untracked: bool = False) -> tuple[dict[str, PublishedDomain], list[str]]:
    """Every published domain with its published nodes, cards and readings, read from tracked files only.
    Returns (domains by id, notes) where notes say why a listed domain was skipped."""
    root = Path(root)
    out: dict[str, PublishedDomain] = {}
    notes: list[str] = []
    for domain in scope.config.domains:
        rel = f"skeleton/{domain}.yaml"
        proj = projection_path(domain)
        if proj in tracked:
            rel = proj      # a projection (atlas/skeletons/) stands in for a local skeleton
        else:
            if (root / proj).exists():
                notes.append(f"{domain}: {proj} exists but is not tracked by git; using skeleton/{domain}.yaml")
            if rel not in tracked:
                notes.append(f"{domain}: skeleton/{domain}.yaml is not tracked by git; domain skipped")
                continue
        if not scope.domain_published(domain):
            notes.append(f"{domain}: the domain name itself names a company; domain skipped")
            continue
        try:
            skeleton = load_skeleton(root / rel)
        except SkeletonError as exc:
            notes.append(f"{domain}: {exc}")
            continue
        nodes = scope.published(skeleton)
        pub = PublishedDomain(skeleton=skeleton, nodes=nodes)
        seen_ids: set[str] = set()
        per_node: dict[str, int] = {}
        for folder in _content_folders(skeleton):
            for rel_path in _tracked_md(tracked, folder + "/cards/"):
                try:
                    card = parse_card(root / rel_path)
                except CardError:
                    continue
                if card.id in seen_ids:
                    continue
                seen_ids.add(card.id)
                if card.node not in skeleton.by_id:
                    pub.cards_orphan += 1
                    continue
                per_node[card.node] = per_node.get(card.node, 0) + 1
                if scope.card_published(domain, card, nodes):
                    card.tags = scope.tags(card)
                    pub.cards.append(card)
                elif card.node in nodes:
                    pub.cards_left_out += 1
                    pub.card_ids_left_out.append(card.id)
            for rel_path in _tracked_md(tracked, folder + "/readings/"):
                try:
                    reading = parse_reading(root / rel_path, CORPUS_KEYS)
                except ReadingError:
                    continue
                if any(n in nodes for n in reading.nodes):
                    pub.readings.append(reading)
            if count_untracked:
                disk = (root / folder / "cards")
                if disk.exists():
                    pub.untracked_cards += sum(1 for p in disk.rglob("*.md")
                                               if p.relative_to(root).as_posix() not in tracked)
        for node_id, reason in scope.left_out_roots(skeleton):
            inside = sum(n for nid, n in per_node.items() if _under(nid, node_id))
            pub.left_out.append((node_id, reason, inside))
        out[domain] = pub
    return out, notes


def check_report(published: dict[str, PublishedDomain], notes: list[str]) -> list[str]:
    """The lines `trellis export --check` prints: everything left out, per domain."""
    lines = list(notes)
    for domain, pub in published.items():
        total = sum(n for _, _, n in pub.left_out)
        lines.append(f"{domain}: {len(pub.nodes)} nodes and {len(pub.cards)} cards published; "
                     f"{len(pub.left_out)} subtree(s) left out ({total} cards), "
                     f"{pub.cards_left_out} card(s) left out by a company word in their id"
                     + (f", {pub.cards_orphan} on no node" if pub.cards_orphan else "")
                     + (f", {pub.untracked_cards} untracked card file(s) ignored" if pub.untracked_cards else ""))
        for node_id, reason, n in pub.left_out:
            lines.append(f"    - {node_id}  [{reason}]  {n} card(s)")
        for card_id in pub.card_ids_left_out:
            lines.append(f"    - card {card_id}  [company word in id]")
    return lines


# -- the projection: a published copy of a local skeleton ----------------------------------------

PROJECTION_DIR = "atlas/skeletons"
_PROJECTION_KEYS = ("domain", "title", "lang", "show", "vault", "include")
_NODE_KEYS = ("id", "title", "summary", "core", "requires", "order")


@dataclass
class Projection:
    data: dict
    kept: int = 0
    dropped: int = 0
    dropped_by: dict[str, int] = field(default_factory=dict)    # why: "untracked:<folder>", "no cards", "private term"
    top_level: int = 0


def projection_path(domain: str) -> str:
    return f"{PROJECTION_DIR}/{domain}.yaml"


def project_skeleton(data: dict, node_cards: dict[str, set[str]], tracked: set[str],
                     private: "re.Pattern | None" = None) -> Projection:
    """The tracked-only copy of a skeleton mapping (as read from YAML).

    node_cards: node id -> the vault folders (as in `vault:` / `include:`) holding a card of that node, for tracked
    and untracked cards alike, with tracked ones marked by the folder name itself and untracked ones as `!<folder>`.
    A node goes only when cards exist under it and none is tracked (local material); a node with no cards stays, as a
    gap the map shows. Its title and summary must not match
    the private-term pattern (a match drops the whole subtree). `requires` pointing at a dropped node are removed.
    """
    dropped_by: dict[str, int] = {}
    kept_ids: set[str] = set()

    def bump(why: str) -> None:
        dropped_by[why] = dropped_by.get(why, 0) + 1

    def has_tracked(node: dict) -> bool:
        if any(not f.startswith("!") for f in node_cards.get(node["id"], ())):
            return True
        return any(has_tracked(c) for c in node.get("children") or [])

    def only_untracked(node: dict) -> bool:
        """Cards exist under this node and none of them is tracked: the node is someone's local material. A node with
        no cards at all is not: it is a gap in the map and is shown as one (Chi, 2026-11-28)."""
        def has_untracked(n: dict) -> bool:
            return any(f.startswith("!") for f in node_cards.get(n["id"], ())) or \
                any(has_untracked(c) for c in n.get("children") or [])
        return not has_tracked(node) and has_untracked(node)

    def private_hit(node: dict) -> bool:
        return bool(private and (private.search(str(node.get("title", ""))) or private.search(str(node.get("summary", "")))))

    def count_subtree(node: dict, why_of) -> None:
        bump(why_of(node))
        for c in node.get("children") or []:
            count_subtree(c, why_of)

    def reason(node: dict) -> str:
        folders = sorted({f[1:] for f in node_cards.get(node["id"], ()) if f.startswith("!")})
        return f"untracked cards in {'+'.join(folders)}" if folders else "no cards"

    def walk(node: dict) -> dict | None:
        if private_hit(node):
            count_subtree(node, lambda n: "private term")
            return None
        if only_untracked(node):
            count_subtree(node, reason)
            return None
        children = [k for k in (walk(c) for c in node.get("children") or []) if k is not None]
        kept_ids.add(node["id"])
        out = {k: node[k] for k in _NODE_KEYS if k in node and node[k] not in (None, "", [], False)}
        out["_children"] = children
        return out

    roots = [r for r in (walk(n) for n in data.get("nodes") or []) if r is not None]

    def finish(node: dict) -> dict:
        kids = node.pop("_children")
        if "requires" in node:
            node["requires"] = [r for r in node["requires"] if r in kept_ids]
            if not node["requires"]:
                del node["requires"]
        if kids:
            node["children"] = [finish(k) for k in kids]
        return node

    nodes = [finish(r) for r in roots]
    # A skeleton wants an `order` on every top-level node or on none; a kept branch the source left unnumbered would
    # break that, so a mixed set is renumbered in its current sequence.
    if any("order" in n for n in nodes) and not all("order" in n for n in nodes):
        for i, n in enumerate(nodes):
            n["order"] = i
    out = {k: data[k] for k in _PROJECTION_KEYS if k in data and k != "include"}
    include = [f for f in data.get("include") or [] if any(p.startswith(f"vault/{f}/") for p in tracked)]
    if include:
        out["include"] = include
    out["nodes"] = nodes
    return Projection(data=out, kept=len(kept_ids), dropped=sum(dropped_by.values()), dropped_by=dropped_by,
                      top_level=len(nodes))


def projection_header(domain: str) -> str:
    return (f"# Generated by scripts/atlas_project.py from skeleton/{domain}.yaml (a local, gitignored file). Do not edit.\n"
            f"# Only nodes whose subtree holds a git-tracked card are kept; the Atlas reads this file instead of the source.\n")
