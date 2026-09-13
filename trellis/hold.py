"""Hold: what the Traces say about how well the skeleton is held.

Everything else in Trellis flows one way — a skeleton decides, content
hangs off it, a deck is built. This module is the way back. Given the
skeleton, the cards, and the Traces pulled out of Anki, it answers the
three questions the loop exists to answer:

  * **Hold** — how well is each node retained? Continuous, never a badge.
  * **Bearing** — how much of the skeleton rests on that node?
  * **Sealed** — is this leaf standing on ground that has not taken?

and ranks the result, so `trellis brief` has something to say.

Nothing here talks to Anki, reads the vault, or writes a file. It is a
pure function of three arguments, which is what makes the whole loop
testable from a fixture and usable on a phone-cloned repo with Anki
nowhere in sight (see docs/adr/0004).

Why Hold is a curve and not a badge
-----------------------------------
Anki's scheduler already maintains, per card, its own estimate of how
long that card will survive: the interval. A card sitting at 60 days is
one the scheduler is confident about; a card knocked back to 1 day after
twenty reviews is one it is not. So Hold does not invent a measure of
knowledge — it reads the one the scheduler already keeps, and normalises
it against Anki's own definition of a mature card (21 days).

The normalisation is logarithmic because the underlying quantity is:
the step from a 1-day to a 7-day interval is real progress, the step
from 300 days to 306 is noise. A log curve says so, and it has no
cliffs — nothing about a card changes discontinuously as it crosses a
threshold, which is the point. Thresholds appear exactly once, at the
edge of the report, to decide what to *print*.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .cards import Card
from .skeleton import Node, Skeleton
from .traces import Trace

# Anki's own definition of a mature card. A card that survives three
# weeks is one you will still have in an interview next month; that is
# the bar Hold is measured against, not some invented scale.
MATURE_DAYS = 21

# Below this, a leaf is worth naming in the Brief. Not a cliff in the
# maths — only in the printing.
WEAK_BELOW = 0.55

# One bad card is bad luck; three is a pattern. Under this many seen
# cards a leaf cannot be called weak, only unproven.
MIN_SEEN = 3

# A leaf is solid enough to build on at this Hold. Deliberately lower
# than "known": prerequisites need to have *taken*, not be perfected,
# or nothing downstream would ever open.
SEALS_AT = 0.45

# Shrinkage strength. A leaf with this many cards seen is trusted half on
# its own evidence and half on its branch's; below it, its branch speaks
# louder. This is the practical shadow of a higher-order latent trait
# model (de la Torre & Douglas 2004), which cannot actually be fitted for
# a single learner — and it fixes the failure that matters most here: a
# leaf where two cards happened to lapse must not be able to shout louder
# than a leaf where forty were measured.
KAPPA = 5.0


def confidence(seen: int) -> float:
    """How much a leaf's own evidence is worth against its branch's, in
    [0, 1). Smooth, so nothing about a leaf changes discontinuously as
    one more card gets reviewed."""
    return seen / (seen + KAPPA)


def card_hold(trace: Trace | None) -> float | None:
    """How well one card is held, in [0, 1] — or None if it has never
    been reviewed, which is an absence of evidence rather than a zero.

    A card the scheduler has parked beyond MATURE_DAYS scores 1.0; one
    it keeps pulling back scores near 0. Lapses discount the result
    rather than dominating it: a card can lapse repeatedly on the way to
    a long interval, and that history is real but it is not failure.
    """
    if trace is None or trace.reps == 0:
        return None
    maturity = math.log1p(max(trace.interval, 0)) / math.log1p(MATURE_DAYS)
    maturity = max(0.0, min(1.0, maturity))
    # A card in the relearning queue is, by definition, not held right
    # now, whatever interval it used to have — so the penalty applies to
    # the clamped score, not to the raw one. Otherwise a card sitting at
    # 400 days would score 0.97 on the day it lapsed.
    if trace.lapsed_recently:
        maturity *= 0.5
    lapse_rate = trace.lapses / trace.reps
    return maturity * (1.0 - 0.5 * min(1.0, lapse_rate))


@dataclass
class LeafStanding:
    """Where one leaf stands in the loop."""

    node: Node
    cards: int = 0
    seen: int = 0                 # cards with at least one review
    hold: float | None = None     # None until something has been seen
    bearing: int = 0
    sealed_by: list[str] = field(default_factory=list)  # unheld prerequisites

    @property
    def uncovered(self) -> bool:
        """Nothing to review here, so nothing can be known about it."""
        return self.cards == 0

    @property
    def unproven(self) -> bool:
        """Cards exist but too few have been seen to judge."""
        return not self.uncovered and self.seen < MIN_SEEN

    @property
    def weak(self) -> bool:
        return (not self.uncovered and not self.unproven
                and self.hold is not None and self.hold < WEAK_BELOW)

    @property
    def sealed(self) -> bool:
        return bool(self.sealed_by)

    @property
    def urgency(self) -> float:
        """How much repairing this leaf would repair. Bearing scales the
        shortfall rather than adding to it, so a load-bearing leaf that
        is merely wobbling outranks an isolated leaf that is gone."""
        if self.hold is None or self.uncovered:
            return 0.0
        return (1.0 - self.hold) * math.log1p(self.bearing + 1)


@dataclass
class Assessment:
    domain: str
    leaves: list[LeafStanding]
    node_hold: dict[str, float]   # every node, leaves rolled up into branches
    reviewed: int                 # cards with at least one review
    total: int

    @property
    def hold(self) -> float | None:
        """The domain's Hold: the mean over every card that has been seen,
        so a domain is not flattered by the cards it has never shown."""
        held = [s.hold for s in self.leaves if s.hold is not None]
        if not held:
            return None
        weights = [s.seen for s in self.leaves if s.hold is not None]
        return sum(h * w for h, w in zip(held, weights)) / sum(weights)

    def weaknesses(self) -> list[LeafStanding]:
        """Weak leaves, worst-and-most-load-bearing first."""
        return sorted((s for s in self.leaves if s.weak),
                      key=lambda s: -s.urgency)

    def uncovered(self) -> list[LeafStanding]:
        """Uncovered leaves, most load-bearing first — where writing pays."""
        return sorted((s for s in self.leaves if s.uncovered),
                      key=lambda s: -s.bearing)

    def sealed(self) -> list[LeafStanding]:
        return [s for s in self.leaves if s.sealed]


def bearing(skeleton: Skeleton) -> dict[str, int]:
    """How many nodes reach each node through `requires`, transitively.

    This is the 80/20: the prerequisite graph already records which
    topics the rest of the subject stands on, and nobody has ever read
    it back. A node with high bearing is one whose collapse takes a
    dozen others down with it.

    Ancestors inherit their descendants' dependents, because requiring a
    leaf is requiring the branch it hangs from.
    """
    nodes = skeleton.walk()
    # direct: node -> nodes that name it in `requires`
    direct: dict[str, set[str]] = {n.id: set() for n in nodes}
    for n in nodes:
        for req in n.requires:
            if req in direct:
                direct[req].add(n.id)

    # A dependent of a node is a dependent of everything that node needs:
    # transitive closure over the reversed edges. The skeleton loader
    # rejects cycles, so this terminates without a visited set, and the
    # memo is therefore sound.
    closure: dict[str, set[str]] = {}

    def reach(node_id: str) -> set[str]:
        if node_id in closure:
            return closure[node_id]
        closure[node_id] = set()  # placeholder; the graph is acyclic
        out: set[str] = set()
        for dep in direct[node_id]:
            out.add(dep)
            out |= reach(dep)
        closure[node_id] = out
        return out

    for n in nodes:
        reach(n.id)

    # Roll down: a branch bears everything its subtree bears.
    result: dict[str, int] = {}
    for n in nodes:
        subtree = {n.id} | {m.id for m in nodes if m.id.startswith(n.id + ".")}
        dependents: set[str] = set()
        for m in subtree:
            dependents |= closure[m]
        result[n.id] = len(dependents - subtree)
    return result


def assess(
    skeleton: Skeleton,
    cards: list[Card],
    traces: dict[str, Trace],
    seals_at: float = SEALS_AT,
) -> Assessment:
    """Read the Traces back onto the skeleton.

    `traces` is keyed by card id, so a card never reviewed simply has no
    entry — the loop degrades to silence rather than to zeros.
    """
    by_node: dict[str, list[Card]] = {}
    for card in cards:
        by_node.setdefault(card.node, []).append(card)

    bear = bearing(skeleton)
    standings: dict[str, LeafStanding] = {}

    raw: dict[str, float] = {}
    for leaf in skeleton.leaves():
        node_cards = by_node.get(leaf.id, [])
        holds = [h for h in (card_hold(traces.get(c.id)) for c in node_cards)
                 if h is not None]
        standings[leaf.id] = LeafStanding(
            node=leaf,
            cards=len(node_cards),
            seen=len(holds),
            bearing=bear[leaf.id],
        )
        if holds:
            raw[leaf.id] = sum(holds) / len(holds)

    # Pass 1: roll raw leaf evidence up into every branch, weighted by
    # cards seen, so a branch's Hold is its content's rather than its
    # shape's — one leaf with 40 reviews outweighs six with one each.
    node_hold: dict[str, float] = {}
    for node in skeleton.walk():
        weighted = [(raw[s.node.id], s.seen) for s in standings.values()
                    if s.node.id in raw
                    and (s.node.id == node.id
                         or s.node.id.startswith(node.id + "."))]
        if weighted:
            total_w = sum(w for _, w in weighted)
            node_hold[node.id] = sum(h * w for h, w in weighted) / total_w

    # Pass 2: shrink each leaf toward its branch. A leaf with plenty of
    # evidence keeps its own number; a barely-reviewed one borrows its
    # branch's, so thin evidence cannot masquerade as a weakness.
    for leaf in skeleton.leaves():
        s = standings[leaf.id]
        if leaf.id not in raw:
            continue
        parent = leaf.parent
        prior = node_hold.get(parent.id) if parent is not None else None
        if prior is None:
            s.hold = raw[leaf.id]
        else:
            w = confidence(s.seen)
            s.hold = w * raw[leaf.id] + (1 - w) * prior

    # Seal a leaf whose prerequisites have not taken. A prerequisite with
    # no evidence does not seal anything: silence is not a failing grade,
    # or a fresh collection would lock the whole skeleton on day one.
    for leaf in skeleton.leaves():
        unheld = [req for req in leaf.requires
                  if node_hold.get(req) is not None and node_hold[req] < seals_at]
        standings[leaf.id].sealed_by = unheld

    ordered = [standings[leaf.id] for leaf in skeleton.leaves()]
    return Assessment(
        domain=skeleton.domain,
        leaves=ordered,
        node_hold=node_hold,
        reviewed=sum(s.seen for s in ordered),
        total=len(cards),
    )
