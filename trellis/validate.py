"""Cross-validation: every card and reading must hang off the skeleton
correctly."""

from __future__ import annotations

from dataclasses import dataclass, field

from .cards import Card
from .readings import Reading
from .skeleton import Skeleton


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate(
    skeleton: Skeleton,
    cards: list[Card],
    card_errors: list[str],
    readings: list[Reading] | None = None,
    reading_errors: list[str] | None = None,
    drills: list[Reading] | None = None,
    drill_errors: list[str] | None = None,
    clippings: dict | None = None,
    cases: list[Reading] | None = None,
    case_errors: list[str] | None = None,
) -> Report:
    report = Report(
        errors=list(card_errors) + list(reading_errors or []) + list(drill_errors or [])
        + list(case_errors or [])
    )

    for note in list(readings or []) + list(drills or []) + list(cases or []):
        for node_id in note.nodes:
            if node_id not in skeleton.by_id:
                report.errors.append(
                    f"{note.path}: node {node_id!r} not in skeleton"
                )

    seen: dict[str, Card] = {}
    for card in cards:
        if card.path.stem != card.id:
            report.errors.append(
                f"{card.path}: filename must equal card id ({card.id}.md) — "
                "Obsidian wikilinks depend on it"
            )
        if card.id in seen:
            report.errors.append(
                f"duplicate card id {card.id!r}: {seen[card.id].path} and {card.path}"
            )
        else:
            seen[card.id] = card

        node = skeleton.by_id.get(card.node)
        if node is None:
            report.errors.append(f"{card.path}: node {card.node!r} not in skeleton")
        elif not node.is_leaf:
            report.warnings.append(
                f"{card.path}: attached to non-leaf node {card.node!r} "
                "(allowed, but prefer leaves)"
            )

    from .cards import leans_on_source
    leaning = [(c.id, leans_on_source(c.question + " " + c.answer + " " + c.text))
               for c in cards]
    leaning = [(cid, phrase) for cid, phrase in leaning if phrase]
    if leaning:
        shown = ", ".join(f"{cid} ({phrase!r})" for cid, phrase in leaning[:6])
        report.warnings.append(
            f"{len(leaning)} card(s) lean on their source — a reviewer has no book "
            f"open, so state the advice as a fact: {shown}"
            + (" …" if len(leaning) > 6 else ""))

    covered = {c.node for c in cards}
    bare = [n.id for n in skeleton.leaves() if n.id not in covered]
    if bare:
        report.warnings.append(
            f"{len(bare)} leaf node(s) have no cards yet: " + ", ".join(bare)
        )

    # Self-containment. A card is read alone, on a phone, months later —
    # and cards written on another machine and dropped into the vault
    # never passed through the scaffold prompt that asks for that.
    from .cards import not_self_contained
    leaning = [(c, problems) for c in cards
               if (problems := not_self_contained(c))]
    if leaning:
        report.warnings.append(
            f"{len(leaning)} card(s) lean on context they do not carry: "
            + "; ".join(f"{c.path.name if c.path else c.id} — {problems[0]}"
                        for c, problems in leaning[:3])
            + (f"; and {len(leaning) - 3} more" if len(leaning) > 3 else "")
        )

    if cards and clippings is not None:
        from .links import leaves_without_readable_source
        hunting = leaves_without_readable_source(skeleton, readings or [], clippings)
        if hunting:
            report.warnings.append(
                f"{len(hunting)} leaf/leaves have no archived, readable source — "
                "their cards point at a book or an index: " + ", ".join(hunting[:8])
                + (" …" if len(hunting) > 8 else "")
            )

    if cards:
        from .links import LINK_COVERAGE_TARGET, coverage
        linked, total = coverage(skeleton, cards, readings or [])
        if linked / total < LINK_COVERAGE_TARGET:
            report.warnings.append(
                f"link coverage {linked}/{total} ({linked / total:.0%}) is below the "
                f"{LINK_COVERAGE_TARGET:.0%} target — attach readings with URLs to "
                "the uncovered nodes"
            )
    return report
