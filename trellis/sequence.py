"""Sequence: the one order in which a domain's new cards are introduced.

Anki shows new cards by *position*, a number every new card carries. Until
now that number was an accident: the order notes happened to sit in the
package the first time they were imported, never revised afterwards, and
inside a leaf simply alphabetical by file name. This module decides it, from
the vault alone, so that `build` can write it and `anki-push` can correct it
in a collection that already exists (ADR 0010).

Two decisions make a Sequence:

* **Which leaf first.** The Core — the leaves the rest of the subject stands
  on — then everything else. Each pass runs in the skeleton's own order,
  which validation already guarantees never puts a leaf before what it
  requires; and the Core is closed under `requires`, so neither pass can.
  This is the 80/20 made operational: one short pass through what matters
  most, in textbook order, before the long one.
* **Which card first inside a leaf.** The `step` its author gave it; then
  cards without one; grown cards last, since a second route is only useful
  after the first has been tried. File name breaks ties, so the order is
  stable across machines.

Nothing here talks to Anki or reads a file.
"""

from __future__ import annotations

from .cards import Card
from .hold import GROWN_TAG, bearing
from .skeleton import Node, Skeleton

CORE_FIRST, SKELETON_ORDER = "core-first", "skeleton"
ORDERS = (CORE_FIRST, SKELETON_ORDER)

# On every card of a Core leaf, so the Core is something Anki can be asked
# for — a search, a filtered deck — and not only an order it is shown in.
CORE_TAG = "trellis::core"


def _leaves_under(skeleton: Skeleton, node_id: str) -> list[Node]:
    return [n for n in skeleton.leaves()
            if n.id == node_id or n.id.startswith(node_id + ".")]


def core_leaves(skeleton: Skeleton) -> set[str]:
    """The Core: leaves declared `core` (themselves or through a branch),
    leaves something else stands on, and whatever those in turn require.

    Bearing is computed and declaration is asserted, and both are needed:
    a `requires` graph is only as complete as someone made it, and where it
    is silent it must not be read as "nothing here matters".
    """
    bear = bearing(skeleton)
    core: set[str] = set()
    pending = [leaf for leaf in skeleton.leaves()
               if bear[leaf.id] > 0 or any(n.core for n in leaf.path())]
    while pending:
        leaf = pending.pop()
        if leaf.id in core:
            continue
        core.add(leaf.id)
        for node in leaf.path():                 # a branch's requires bind its leaves
            for req in node.requires:
                pending += _leaves_under(skeleton, req)
    return core


def sequence(skeleton: Skeleton, cards: list[Card], order: str = CORE_FIRST) -> list[Card]:
    """Every card Trellis owns, in the order it should first be shown.
    Adopted cards are left out: their positions belong to whoever owns them."""
    core = core_leaves(skeleton) if order == CORE_FIRST else set()
    place = {leaf.id: i for i, leaf in enumerate(skeleton.leaves())}
    own = [c for c in cards if not c.adopted and c.node in place]
    return sorted(own, key=lambda c: (
        c.node not in core if core else False,
        place[c.node],
        c.step is None, c.step or 0,
        GROWN_TAG in c.tags,
        c.path.name if c.path else c.id,
    ))
