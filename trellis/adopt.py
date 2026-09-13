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


# --------------------------------------------------------------------------
# A deck that lives only in Anki.
#
# Some decks were never markdown: another tool wrote them straight into the
# collection, and the only copy of each note is there. Trellis can still
# put them on a skeleton — so their Traces feed the loop and `grow` can
# write beside them — by mirroring every note as an *adopted* card: placed
# on a leaf, tagged in Anki with the id and node Trellis knows it by, and
# never built, pushed or moved. The other tool keeps owning the note.

import html as _html  # noqa: E402
from dataclasses import field  # noqa: E402

from .anki import ADOPTED_TAG  # noqa: E402

CONCEPT_PREFIX = "concept::"
_FAMILY_RE = re.compile(r"^(endlesscheng-[a-z0-9]+)-(.+)$")


@dataclass
class Concept:
    slug: str
    family: str
    notes: int = 0
    samples: list[str] = field(default_factory=list)


@dataclass
class Topic:
    slug: str
    name: str
    notes: int = 0
    samples: list[str] = field(default_factory=list)


@dataclass
class Inventory:
    """What a deck contains, in the terms a skeleton can be drafted from:
    every concept its notes name (a leaf each), and the topics left to
    stand in for notes that name no concept."""

    concepts: list[Concept]
    topics: list[Topic]
    leaf_of: dict[int, str]          # note id -> slug it belongs under


def _field(note: dict, name: str) -> str:
    return (note.get("fields", {}).get(name) or {}).get("value", "") or ""


def _plain(html_text: str, limit: int = 80) -> str:
    text = re.sub(r"<[^>]+>", "", html_text)
    return _html.unescape(" ".join(text.split()))[:limit]


def _concept_of(note: dict) -> tuple[str, str] | None:
    for tag in note.get("tags") or []:
        if tag.startswith(CONCEPT_PREFIX):
            raw = tag[len(CONCEPT_PREFIX):]
            m = _FAMILY_RE.match(raw)
            return (m.group(2), m.group(1)) if m else (raw, "other")
    return None


def _topic_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def deck_inventory(notes: list[dict]) -> Inventory:
    """Concepts first. A note naming none borrows the concept its sibling
    notes (same question) carry; only a question with no concept anywhere
    falls back to its most specific topic — the last one listed."""
    concepts: dict[str, Concept] = {}
    by_question: dict[str, str] = {}
    for note in notes:
        found = _concept_of(note)
        if found is None:
            continue
        slug, family = found
        c = concepts.setdefault(slug, Concept(slug=slug, family=family))
        c.notes += 1
        front = _plain(_field(note, "Front") or _field(note, "Text"))
        if front and len(c.samples) < 2:
            c.samples.append(front)
        qid = _field(note, "QuestionID")
        if qid:
            by_question.setdefault(qid, slug)

    topics: dict[str, Topic] = {}
    leaf_of: dict[int, str] = {}
    for note in notes:
        found = _concept_of(note)
        if found is not None:
            leaf_of[note["noteId"]] = found[0]
            continue
        qid = _field(note, "QuestionID")
        if qid in by_question:
            leaf_of[note["noteId"]] = by_question[qid]
            continue
        names = [t.strip() for t in _field(note, "Topics").split("·") if t.strip()]
        name = names[-1] if names else "uncategorised"
        slug = _topic_slug(name) or "uncategorised"
        t = topics.setdefault(slug, Topic(slug=slug, name=name))
        t.notes += 1
        front = _plain(_field(note, "Front") or _field(note, "Text"))
        if front and len(t.samples) < 2:
            t.samples.append(front)
        leaf_of[note["noteId"]] = slug
    return Inventory(
        concepts=sorted(concepts.values(), key=lambda c: c.slug),
        topics=sorted(topics.values(), key=lambda t: t.slug),
        leaf_of=leaf_of,
    )


DECK_PROMPT = """\
You are drafting the study map (a "skeleton") for a subject, from the
inventory of an Anki deck that already holds its cards. Answer with one JSON
object (no prose).

## Subject
domain slug: `{domain}` — the deck: {deck} ({notes} notes). Cards are in
{lang}; write titles and summaries in {lang}, terms of art in English.

## The deck's inventory
Every line is a slug that MUST appear as the last segment of exactly one
leaf id in your skeleton (`<branch>.<slug>`, the slug unchanged). A family in
brackets is the list the concept came from — concepts sharing a family
usually share a branch, but group by what the concept IS, not by the label.

### Concepts ({n_concepts})
{concepts}

### Topics standing in for notes that name no concept ({n_topics})
{topics}

## What a skeleton is
- A tree: branches at the top, leaves below. ids are dotted lowercase slugs;
  a child's id starts with its parent's id plus a dot. Study order = list
  order — put fundamentals first. `requires` lists ids of nodes that must
  be understood first (cross-branch only, sparse).
- Every node has a one-line `summary` in {lang} saying what the leaf
  teaches. Every leaf listed above must exist; you may add a few leaves the
  deck lacks and list them under `uncovered`.
- Aim for {branches} branches.

## Answer format
{{"deck": "{deck}",
  "skeleton": {{"domain": "{domain}", "title": "...", "lang": "{lang_code}",
    "nodes": [
      {{"id": "window", "title": "...", "summary": "...", "children": [
        {{"id": "window.shrink-window-for-longest", "title": "...", "summary": "..."}}
      ]}}
    ]}},
  "uncovered": []}}
"""


def deck_prompt(domain: str, deck: str, inv: Inventory, notes: int, lang: str = "zh") -> str:
    from .seed import LANG_NAMES
    concepts = "\n".join(
        f"- `{c.slug}` [{c.family}] — {c.notes} note(s)"
        + (f" · e.g. “{c.samples[0]}”" if c.samples else "")
        for c in inv.concepts)
    topics = "\n".join(
        f"- `{t.slug}` ({t.name}) — {t.notes} note(s)"
        + (f" · e.g. “{t.samples[0]}”" if t.samples else "")
        for t in inv.topics)
    n = len(inv.concepts) + len(inv.topics)
    return DECK_PROMPT.format(
        domain=domain, deck=deck, notes=notes, lang=LANG_NAMES.get(lang, lang),
        lang_code=lang, concepts=concepts, n_concepts=len(inv.concepts),
        topics=topics or "(none)", n_topics=len(inv.topics),
        branches="8-14" if n < 60 else "14-24",
    )


def _mirror_id(prefix: str, note: dict) -> str:
    raw = _field(note, "CardID") or f"note-{note['noteId']}"
    parts = [p for p in raw.split(":") if p]
    kind = parts[0][:1] if parts else "n"
    name = parts[1] if len(parts) > 1 else parts[0]
    ctype = parts[2] if len(parts) > 2 and parts[2] != "concept-cloze" else ""
    slug = "-".join(x for x in (prefix, kind, name, ctype) if x)
    return re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")


def _mirror_body(note: dict) -> tuple[str, str]:
    """(type, body) for the card file, from the note's fields."""
    from .ingest import html_to_markdown as md
    if _field(note, "Text"):
        body = md(_field(note, "Text"))
        extra = md(_field(note, "Extra"))
        if extra:
            body += "\n\n" + extra
        kind = "cloze"
    else:
        q = md(_field(note, "Front"))
        a = md(_field(note, "Back"))
        body = f"## Q\n{q}\n\n## A\n{a}\n"
        kind = "qa"
    evidence = md(_field(note, "Evidence"))
    if evidence:
        body = body.rstrip("\n") + "\n\n**Evidence**\n\n" + evidence + "\n"
    source = _field(note, "Source").strip()
    if source:
        body = body.rstrip("\n") + f"\n\n[原文 ↗]({source})\n"
    return kind, body


@dataclass
class AdoptResult:
    written: list[Path] = field(default_factory=list)
    unmapped: list[str] = field(default_factory=list)
    tagged: int = 0


def adopt_deck(root: str | Path, domain: str, deck: str, call, url: str | None = None,
               prefix: str | None = None, lang: str = "zh") -> Path | AdoptResult:
    """Without a skeleton: write the seed prompt and return its path. With
    one: mirror every note onto its leaf, tag the notes in Anki, and return
    what was written. Reads the deck from Anki both times; nothing is
    cached, because the deck is the source of truth for itself."""
    from .skeleton import load_skeleton
    root = Path(root)
    kwargs = {"url": url} if url else {}
    note_ids = call("findNotes", **kwargs, query=f'deck:"{deck}"')
    notes = call("notesInfo", **kwargs, notes=note_ids) if note_ids else []
    inv = deck_inventory(notes)

    skeleton_path = root / "skeleton" / f"{domain}.yaml"
    if not skeleton_path.exists():
        out = root / "proposals" / f"{domain}.seed.prompt.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(deck_prompt(domain, deck, inv, len(notes), lang), encoding="utf-8")
        return out

    skeleton = load_skeleton(skeleton_path)
    by_suffix: dict[str, list[str]] = {}
    for leaf in skeleton.leaves():
        by_suffix.setdefault(leaf.id.rsplit(".", 1)[-1], []).append(leaf.id)
    result = AdoptResult()
    cards_dir = root / "vault" / domain / "cards"
    prefix = prefix or domain
    to_tag: list[tuple[int, str]] = []
    for note in notes:
        slug = inv.leaf_of.get(note["noteId"])
        leaves = by_suffix.get(slug or "", [])
        if len(leaves) != 1:
            why = "no leaf" if not leaves else f"{len(leaves)} leaves"
            result.unmapped.append(f"note {note['noteId']} ({slug}): {why}")
            continue
        node_id = leaves[0]
        card_id = _mirror_id(prefix, note)
        kind, body = _mirror_body(note)
        tags = [t for t in (note.get("tags") or []) if not t.startswith(CONCEPT_PREFIX)]
        front = [f"id: {card_id}", f"node: {node_id}", f"type: {kind}", f"anki: {note['noteId']}"]
        if tags:
            front.append("tags: [" + ", ".join(tags) + "]")
        path = cards_dir / node_id.split(".")[0] / f"{card_id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + "\n".join(front) + "\n---\n" + body, encoding="utf-8")
        result.written.append(path)
        to_tag.append((note["noteId"],
                       f"id::{card_id} {domain}::{node_id.replace('.', '::')} {ADOPTED_TAG}"))
    for note_id, tags in to_tag:
        call("addTags", **kwargs, notes=[note_id], tags=tags)
        result.tagged += 1
    return result
