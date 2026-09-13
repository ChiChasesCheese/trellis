"""Feed: one stream across every domain, ordered so the next card is a
different subject from the last.

The deck tree is how you *author*. It is a bad way to *review*, and it is
a very bad way to review in the four minutes before a train arrives: you
open Anki, you are shown seven decks and a backlog number, and you have
to make a decision before you have learned anything. The Feed removes the
decision.

Interleaving is the rare case where what makes something compelling and
what makes it work are the same mechanism. A short-form feed holds
attention because consecutive items are unalike; retrieval practice sticks
because consecutive items are unalike (mixing topics beats blocking them,
even though blocking *feels* more productive while you do it). So the
ordering that makes a study session feel like scrolling is also the
ordering that teaches better. Nothing here is a trick played on the
learner.

Anki, not a new app
-------------------
A note's cards live in exactly one deck, so a Feed cannot be a second
deck holding copies — it has to be a **filtered deck**, which gathers
cards by search, shows them, and returns them to where they came from.
That keeps one scheduler, one review history, and one thing to sync. What
this module produces is therefore a search string and an order, not a
deck of its own.
"""

from __future__ import annotations

from dataclasses import dataclass

from .cards import Card
from .hold import Assessment, LeafStanding


@dataclass
class FeedPlan:
    """What to put in the filtered deck, and why."""

    search: str
    limit: int
    order: str
    domains: list[str]
    sealed: list[str]        # node ids withheld, and the reason they are
    reasons: list[str]

    def as_lines(self) -> list[str]:
        out = [f"search: {self.search}", f"limit:  {self.limit}",
               f"order:  {self.order}"]
        out += [f"  · {r}" for r in self.reasons]
        return out


def _sealed_tags(assessments: dict[str, Assessment]) -> list[tuple[str, str]]:
    """(tag, why) for every leaf standing on ground that has not taken."""
    out: list[tuple[str, str]] = []
    for domain, assessment in assessments.items():
        for standing in assessment.sealed():
            tag = domain + "::" + standing.node.id.replace(".", "::")
            out.append((tag, f"{standing.node.title} waits on "
                             + ", ".join(standing.sealed_by)))
    return out


def plan(
    assessments: dict[str, Assessment],
    limit: int = 40,
    include_sealed: bool = False,
) -> FeedPlan:
    """The search a filtered deck should run.

    Two things are excluded on purpose. **Sealed** leaves, because
    introducing a topic whose prerequisites have not taken is how a
    smooth curve becomes a cliff — the card is not deleted, it is
    withheld until the ground under it holds. And **suspended** cards,
    because Anki already means something by that.

    Everything else is fair game and deliberately unordered by subject:
    the whole point is that the next card is not more of the last one.
    """
    domains = sorted(assessments)
    if not domains:
        return FeedPlan("", 0, "random", [], [], ["no domains with cards"])

    clauses = ["(" + " OR ".join(f"tag:{d}::*" for d in domains) + ")",
               "-is:suspended"]
    reasons = [f"{len(domains)} domains in one stream — consecutive cards "
               f"come from different subjects, which is both why it holds "
               f"attention and why it teaches better than blocking"]

    sealed = _sealed_tags(assessments)
    if sealed and not include_sealed:
        clauses += [f"-tag:{tag}" for tag, _ in sealed]
        reasons.append(f"{len(sealed)} leaf/leaves withheld: their "
                       f"prerequisites are not holding yet")

    reasons.append(f"capped at {limit} cards — a session that ends is a "
                   f"session you start again tomorrow")

    return FeedPlan(
        search=" ".join(clauses),
        limit=limit,
        order="random",
        domains=domains,
        sealed=[why for _, why in sealed],
        reasons=reasons,
    )


def interleave(cards: list[Card], key) -> list[Card]:
    """Deal cards out one subject at a time, round-robin, so no two
    consecutive cards share a subject while any other subject still has
    cards left. Used for the ordering the build can control; the live
    scheduler owns the rest.
    """
    buckets: dict[str, list[Card]] = {}
    for card in cards:
        buckets.setdefault(key(card), []).append(card)

    out: list[Card] = []
    last: str | None = None
    while any(buckets.values()):
        # take from the fullest bucket that is not the one we just used,
        # which keeps the tail from degenerating into one long run
        candidates = [k for k, v in buckets.items() if v and k != last]
        if not candidates:
            candidates = [k for k, v in buckets.items() if v]
        pick = max(candidates, key=lambda k: len(buckets[k]))
        out.append(buckets[pick].pop(0))
        last = pick
    return out
