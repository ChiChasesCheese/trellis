"""Grow: the loop's verdicts become new cards.

`pull` brings the review history back, `brief` says which leaves are weak
and which are uncovered. Grow is what happens next: for each such leaf a
prompt aimed at exactly what the loop found, and an importer that lands
the answer where the loop will see it on the next pull.

Two kinds of target, two different prompts:

- A **Weakness** already has cards, and they are not holding. The prompt
  carries the ones held least — front and back — and asks for cards that
  reach the same mechanism from another angle: a scenario, a contrast, a
  failure story, a number. Restating a card that already failed teaches
  the same failure twice.
- An **uncovered** leaf has nothing. The prompt is the scaffold's, grounded
  in whatever the vault already holds for the leaf: the sections of a
  corpus that reaches it (then growing is digesting, and the cards carry
  the corpus as provenance), or the clipped readings on it.

Every card grown here is tagged `grown`, so the next Brief can say
whether the repair took. Nothing is recorded that can be derived: the
targets are read off the Traces and the vault each time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .brief import interleave_by_domain
from .cards import Card
from .clippings import Clipping, canonical_url
from .corpus import Corpus, Outline, Section, load_corpora, load_outline
from .digest import (SOURCE_HEADER, embed, import_leaf, language_rules,
                     plan as digest_plan, section_blocks)
from .hold import Assessment, LeafStanding, card_hold
from .project import Project
from .readings import Reading
from .scaffold import scaffold_prompt
from .traces import Trace

GROWN_TAG = "grown"
SLIPPED_SHOWN = 5

SLIPPED = """
## What is not holding
This topic has cards already, and they are not holding — the scheduler keeps
pulling them back to short intervals, whether or not they have formally
lapsed. Here are the ones held least, with their answers; they are evidence
of *where* the idea is not landing, not a template:
{cards}

Do not restate them. Write cards that reach the same mechanism from a
**different angle**: a concrete scenario the reader has to reason through,
a contrast with the thing it is confused with, what goes wrong when it is
misapplied, a number or a threshold that pins it down. A second route in
is what a topic that failed on the first route needs.
"""

CLIPPED_HEADER = """
## Source material
The vault holds these readings for this topic, archived in full. Write from
them — not from memory — and only what they support.
{sections}
"""


@dataclass
class Target:
    """One leaf the loop says is worth writing for, and what to write from."""

    domain: str
    standing: LeafStanding
    kind: str                                   # "weakness" | "uncovered"
    slipped: list[tuple[Card, Trace]] = field(default_factory=list)  # worst first
    corpus: Corpus | None = None
    sections: list[Section] = field(default_factory=list)
    clipped: list[tuple[Reading, Clipping]] = field(default_factory=list)

    @property
    def key(self) -> str:
        return f"{self.domain}:{self.standing.node.id}"

    @property
    def grounding(self) -> str:
        """One phrase saying what the prompt can be written from."""
        if self.sections:
            return f"{self.corpus.id} ({len(self.sections)} section(s))"
        if self.clipped:
            return f"{len(self.clipped)} clipped reading(s)"
        return "ungrounded"


def plan(root: Path, projects: dict[str, Project], assessments: dict[str, Assessment],
         traces: dict[str, dict[str, Trace]]) -> list[Target]:
    """Every leaf worth writing for, weaknesses first (worst and most
    load-bearing first), then uncovered leaves (most load-bearing first)."""
    corpora = [c for c in load_corpora(root).values() if c.outline_path(root).exists()]
    outlines: dict[str, Outline] = {c.id: load_outline(c.outline_path(root)) for c in corpora}

    weak: list[Target] = []
    uncovered: list[Target] = []
    for domain, assessment in assessments.items():
        project = projects[domain]
        domain_traces = traces.get(domain, {})
        reach: dict[str, tuple[Corpus, list[Section]]] = {}
        for corpus in corpora:
            if corpus.domain != domain:
                continue
            for lp in digest_plan(project, corpus, outlines[corpus.id]):
                reach.setdefault(lp.leaf.id, (corpus, lp.sections))

        def target(standing: LeafStanding, kind: str) -> Target:
            leaf_id = standing.node.id
            t = Target(domain=domain, standing=standing, kind=kind)
            if kind == "weakness":
                held = [(c, domain_traces[c.id]) for c in project.cards
                        if c.node == leaf_id and c.id in domain_traces]
                held.sort(key=lambda ct: card_hold(ct[1]) or 0.0)
                t.slipped = held[:SLIPPED_SHOWN]
            if leaf_id in reach:
                t.corpus, t.sections = reach[leaf_id]
            for reading in project.readings:
                if leaf_id not in reading.nodes or not reading.url:
                    continue
                clip = project.clippings.get(canonical_url(reading.url))
                if clip is not None and clip.is_substantive and not clip.is_pdf:
                    t.clipped.append((reading, clip))
            return t

        weak += [target(s, "weakness") for s in assessment.weaknesses()]
        uncovered += [target(s, "uncovered") for s in assessment.uncovered()]
    return weak + uncovered


def shortlist(targets: list[Target], cap: int = 3, limit: int = 8) -> list[Target]:
    """What `grow` lists: the Brief's own breadth rule, so one domain with
    sixty empty leaves cannot crowd out a weakness elsewhere. When the
    learner has already chosen a domain there is nothing to crowd out,
    so the caller lifts the cap."""
    rows = lambda kind: [(t.domain, t) for t in targets if t.kind == kind]
    return [t for _, t in interleave_by_domain(rows("weakness"), cap=cap, limit=limit)] + \
           [t for _, t in interleave_by_domain(rows("uncovered"), cap=cap, limit=limit)]


def status_lines(targets: list[Target]) -> list[str]:
    lines: list[str] = []
    for t in targets:
        s = t.standing
        if t.kind == "weakness":
            names = ", ".join(c.id for c, _ in t.slipped[:3])
            why = f"holds {s.hold:.0%}, {s.seen}/{s.cards} cards seen, weakest: {names}"
        else:
            why = (f"{s.bearing} topic(s) stand on it" if s.bearing else "no cards yet")
            if s.sealed:
                why += " (sealed)"
        lines.append(f"  {t.kind:<10} {t.key:<40} {why}  · {t.grounding}")
    return lines


def grow_prompt(project: Project, t: Target, root: Path, count: int = 5,
                budget: int = 24000) -> str:
    base = scaffold_prompt(project.skeleton, t.standing.node.id, project.cards, count=count)
    parts = [base]
    if t.kind == "weakness" and t.slipped:
        shown = []
        for card, trace in t.slipped:
            front = card.question or card.text
            back = card.answer
            shown.append(f"- **{card.id}** — {trace.reps} reviews, {trace.lapses} lapses, "
                         f"interval {trace.interval} d\n  Q: {front.strip()}\n"
                         + (f"  A: {back.strip()}\n" if back else ""))
        parts.append(SLIPPED.format(cards="\n".join(shown)))
    if t.sections:
        parts.append(SOURCE_HEADER.format(
            title=t.corpus.title,
            sections=embed(section_blocks(t.corpus, t.sections, root), root, budget)))
    elif t.clipped:
        blocks = [(f"{reading.title} — {reading.url}", reading.link_target, clip.path)
                  for reading, clip in t.clipped]
        parts.append(CLIPPED_HEADER.format(sections=embed(blocks, root, budget)))
    parts.append(language_rules(project))
    return "".join(parts)


def import_grown(project: Project, t: Target, json_path: str | Path, cards_dir: Path,
                 ) -> tuple[list[Path], list[str]]:
    return import_leaf(project, t.standing.node.id, json_path, cards_dir,
                       source=t.corpus.id if t.sections else "", tags=(GROWN_TAG,))
