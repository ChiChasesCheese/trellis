"""Digest: cards written leaf by leaf from the sections triaged onto it.

Nothing here is recorded that can be derived. The plan is read off the
readings that carry this corpus as provenance (leaf ← sections), and a
leaf is done when it has cards whose `source:` is this corpus — so three
agents digesting disjoint leaves never share a state file, and a run cut
off anywhere resumes from `--status` alone.

The prompt is `scaffold_prompt` (the card rules, in one place) plus the
sections' text, the language the domain is written in, and the rule that
matters most for a card written from a book: it must teach without the
book. The importer is `import_cards` with the provenance stamped on.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .cards import Card, leans_on_source
from .corpus import Corpus, Outline, Section
from .project import Project
from .readings import Reading
from .scaffold import import_cards, scaffold_prompt
from .seed import LANG_NAMES
from .skeleton import Node

SOURCE_HEADER = """
## Source material
These cards are written from *{title}*. The sections below were judged to
teach this topic. Write from them — not from memory — and only what they
support; if the text is silent on something, leave it to another card.
{sections}
"""

LANGUAGE_RULES = """
## Language and self-containment
- Write every card in {lang}. Terms of art stay in English (the reader will
  meet them in code, configs and docs): write the English term and gloss
  it in {lang} once per card, e.g. `consumer group（消费者群组）`.
- SELF-CONTAINED. A reader who has never heard of {subject} must understand
  the card from the card alone: the question carries the situation it is
  asking about, the answer defines every term it uses and says WHY, not
  only what. Never "as discussed", "the book says", "see chapter 3" — nor
  their equivalents ("书中建议", "本书", "如前所述"): the importer refuses a
  card that leans on its source. State the advice as a fact.
- Prefer questions whose answer is a mechanism or a decision ("what happens
  when…", "why would you set…") over ones whose answer is a name.
- Do not set `source`; the importer records where these cards came from.
"""

SECTION_BLOCK = """
### {title}  (`{id}`)
{text}
"""


@dataclass
class LeafPlan:
    leaf: Node
    sections: list[Section]
    readings: list[Reading]
    cards: list[Card] = field(default_factory=list)

    @property
    def done(self) -> bool:
        return bool(self.cards)


def plan(project: Project, corpus: Corpus, outline: Outline) -> list[LeafPlan]:
    """Leaves this corpus reaches, in study order, each with the sections
    triaged onto it and the cards already written from it."""
    by_section = outline.by_id()
    per_leaf: dict[str, LeafPlan] = {}
    for reading in project.readings:
        if reading.extra.get("corpus") != corpus.id:
            continue
        section = by_section.get(str(reading.extra.get("section", "")))
        for node_id in reading.nodes:
            node = project.skeleton.by_id.get(node_id)
            if node is None:
                continue
            lp = per_leaf.setdefault(node_id, LeafPlan(leaf=node, sections=[], readings=[]))
            lp.readings.append(reading)
            if section is not None and section not in lp.sections:
                lp.sections.append(section)
    for card in project.cards:
        if card.source == corpus.id and card.node in per_leaf:
            per_leaf[card.node].cards.append(card)
    order = {n.id: i for i, n in enumerate(project.skeleton.walk())}
    plans = sorted(per_leaf.values(), key=lambda lp: order[lp.leaf.id])
    for lp in plans:
        lp.sections.sort(key=lambda s: s.ordinal)
    return plans


def status_lines(plans: list[LeafPlan]) -> list[str]:
    done = sum(1 for lp in plans if lp.done)
    lines = [f"{done}/{len(plans)} leaves digested"]
    for lp in plans:
        mark = "done" if lp.done else "todo"
        lines.append(f"  {mark}  {lp.leaf.id:<36} {len(lp.sections)} section(s)"
                     f"  {len(lp.cards)} card(s)")
    return lines


TRANSLATION_RULE = """
- This domain's cards also carry a Chinese translation, and its deck is
  reviewed in Chinese. Give every card one: `q_zh` and `a_zh` (for a cloze,
  `text_zh` with every `{{{{cN::…}}}}` deletion byte-identical), a faithful
  translation of your English — same structure, terms of art kept in
  English, nothing added or dropped.
"""


def language_rules(project: Project) -> str:
    """The rules every card written into this domain follows, whatever it
    is written from: its language, and that it must teach alone. A domain
    whose cards mostly carry a translation asks for one on new cards too,
    or the deck the learner actually reviews would go silently bilingual."""
    lang = LANG_NAMES.get(project.skeleton.lang, project.skeleton.lang)
    rules = LANGUAGE_RULES.format(lang=lang, subject=project.skeleton.title)
    cards = project.cards
    if cards and project.skeleton.lang != "zh":
        translated = sum(1 for c in cards if c.tr.get("zh"))
        if translated / len(cards) >= 0.5:
            rules += TRANSLATION_RULE
    return rules


def embed(blocks: list[tuple[str, str, Path]], root: Path, budget: int) -> str:
    """Source texts for a prompt, within a character budget. Each block is
    (title, id, path-to-markdown). What is cut is said, and every path is
    given, so a reader with a filesystem can open the rest."""
    out: list[str] = []
    remaining = budget
    for i, (title, block_id, path) in enumerate(blocks):
        text = _body_text(path)
        note = f"(full text: `{path.relative_to(root)}`)"
        if len(text) > remaining:
            cut = text[:max(0, remaining)]
            text = cut + f"\n\n[… {len(text) - len(cut)} characters cut for length; {note}]"
        else:
            text = text + f"\n\n{note}"
        remaining -= len(text)
        out.append(SECTION_BLOCK.format(title=title, id=block_id, text=text))
        if remaining <= 0:
            for rest_title, rest_id, rest_path in blocks[i + 1:]:
                out.append(f"\n### {rest_title}  (`{rest_id}`)\n[not embedded — read "
                           f"`{rest_path.relative_to(root)}`]\n")
            break
    return "".join(out)


def section_blocks(corpus: Corpus, sections: list[Section], root: Path,
                   ) -> list[tuple[str, str, Path]]:
    text_dir = corpus.text_dir(root)
    return [(s.title, s.id, text_dir / f"{s.id}.md") for s in sections]


def digest_prompt(project: Project, corpus: Corpus, lp: LeafPlan, root: Path,
                  count: int = 5, budget: int = 24000) -> str:
    """The scaffold prompt for the leaf, grounded in its sections' text."""
    base = scaffold_prompt(project.skeleton, lp.leaf.id, project.cards, count=count)
    sections = embed(section_blocks(corpus, lp.sections, root), root, budget)
    return base + SOURCE_HEADER.format(title=corpus.title, sections=sections) \
        + language_rules(project)


def _body_text(path: Path) -> str:
    if not path.exists():
        return f"[text is not on this machine: {path.name}]"
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---\n"):
        parts = raw.split("---\n", 2)
        raw = parts[2] if len(parts) == 3 else raw
    return raw.strip()


def import_digest(project: Project, corpus: Corpus, leaf_id: str,
                  json_path: str | Path, cards_dir: Path,
                  ) -> tuple[list[Path], list[str]]:
    """`import_cards`, with every card forced onto the leaf it was asked
    for and stamped with the corpus it came from. All-or-nothing."""
    return import_leaf(project, leaf_id, json_path, cards_dir, source=corpus.id)


def import_leaf(project: Project, leaf_id: str, json_path: str | Path,
                cards_dir: Path, source: str = "", tags: tuple[str, ...] = (),
                ) -> tuple[list[Path], list[str]]:
    """Land an answer on one leaf: every card is forced onto it, given the
    provenance and tags asked for, and refused if it leans on its source.
    All-or-nothing."""
    raw = Path(json_path).read_text(encoding="utf-8")
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw)
    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [], [f"{json_path}: invalid JSON: {exc}"]
    if not isinstance(items, list):
        return [], [f"{json_path}: expected a JSON array of cards"]
    errors = []
    for i, item in enumerate(items):
        if isinstance(item, dict):
            if item.get("node") not in (None, leaf_id):
                errors.append(f"{json_path}[{i}]: node {item.get('node')!r} is not the "
                              f"leaf being digested ({leaf_id})")
            leaning = leans_on_source(" ".join(
                str(item.get(k, "")) for k in ("q", "a", "text")))
            if leaning:
                errors.append(f"{json_path}[{i}] {item.get('id', '?')}: leans on the "
                              f"book ({leaning!r}) — a card must teach without it; "
                              "state the advice or the mechanism as a fact")
            item["node"] = leaf_id
            if source:
                item["source"] = source
            if tags:
                item["tags"] = [t for t in (item.get("tags") or []) if t not in tags] + list(tags)
    if errors:
        return [], errors
    stamped = Path(json_path).with_suffix(".stamped.json")
    stamped.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    try:
        return import_cards(project.skeleton, project.cards, stamped, cards_dir)
    finally:
        stamped.unlink(missing_ok=True)


# --------------------------------------------------------------------------
# The Corpus note: the book's own outline, annotated with what each section
# became, and underneath it the leaves of the domain the book never reached.

def corpus_note(project: Project, corpus: Corpus, outline: Outline) -> str:
    skeleton = project.skeleton
    readings = [r for r in project.readings if r.extra.get("corpus") == corpus.id]
    by_section: dict[str, list[Reading]] = {}
    for r in readings:
        by_section.setdefault(str(r.extra.get("section", "")), []).append(r)
    cards_by_node: dict[str, int] = {}
    for c in project.cards:
        if c.source == corpus.id:
            cards_by_node[c.node] = cards_by_node.get(c.node, 0) + 1
    reached = {n for r in readings for n in r.nodes}
    leaves = skeleton.leaves()

    lines = [f"# {corpus.title}", ""]
    meta = [corpus.author, corpus.license, f"[[{skeleton.title} MOC|{skeleton.title}]]"]
    lines.append(" · ".join(m for m in meta if m))
    if corpus.home:
        lines.append(f"[Home ↗]({corpus.home})")
    total_cards = sum(cards_by_node.values())
    lines += ["", f"{len(outline.sections)} sections · {len(readings)} readings · "
                  f"{total_cards} cards · {len(reached & {l.id for l in leaves})}/{len(leaves)} leaves reached",
              "", "## Outline"]
    for section in outline.sections:
        indent = "    " * (section.level - 1)
        rs = by_section.get(section.id, [])
        if not rs:
            lines.append(f"{indent}- {section.title} — *skipped*")
            continue
        parts = []
        for r in rs:
            nodes = ", ".join(
                f"[[{n}|{skeleton.by_id[n].title}]]" if n in skeleton.by_id else n
                for n in r.nodes)
            n_cards = sum(cards_by_node.get(n, 0) for n in r.nodes)
            parts.append(f"[[{r.link_target}|{r.title}]] → {nodes}"
                         + (f" · {n_cards} cards" if n_cards else ""))
        lines.append(f"{indent}- **{section.title}** — " + " / ".join(parts))
    missing = [l for l in leaves if l.id not in reached]
    if missing:
        lines += ["", f"## Leaves this corpus never reached ({len(missing)})",
                  "Your reading list: the map says these exist and the book does not teach them."]
        lines += [f"- [[{l.id}|{l.title}]] — {l.summary}" for l in missing]
    return "\n".join(lines)
