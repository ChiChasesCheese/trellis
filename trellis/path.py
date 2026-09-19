"""Study path: flatten the skeleton DAG into a linear curriculum.

Tree order is already a valid topological order (validation guarantees
requires edges never point forward), and the path is the Sequence's leaf
order (`trellis/sequence.py`): the Core in tree order, then the rest in tree
order — the same order Anki deals new cards in, so the note and the phone
agree. --weeks splits it into balanced chunks by card volume.
"""

from __future__ import annotations

import math
from collections import Counter

from .cards import Card
from .sequence import CORE_FIRST, core_leaves
from .skeleton import Skeleton


def study_path(skeleton: Skeleton, cards: list[Card], weeks: int | None = None) -> str:
    per_node = Counter(c.node for c in cards)
    core = core_leaves(skeleton) if skeleton.study.order == CORE_FIRST else set()
    leaves = sorted(skeleton.leaves(), key=lambda n: n.id not in core)   # stable: tree order within
    total = sum(per_node.get(n.id, 0) for n in leaves)

    week_of: dict[str, int] = {}
    if weeks:
        target = total / weeks
        acc, week = 0, 1
        for leaf in leaves:
            # close the week once it has reached its share (never exceed
            # the requested number of weeks)
            if acc >= target * week and week < weeks:
                week += 1
            acc += per_node.get(leaf.id, 0)
            week_of[leaf.id] = week

    lines = [f"# {skeleton.title} — study path", ""]
    if weeks:
        lines.append(f"{total} cards over {weeks} weeks ≈ "
                     f"{math.ceil(total / (weeks * 7))} new cards/day.")
        lines.append("")

    current_branch = None
    current_week = None
    current_pass = None
    for leaf in leaves:
        if core and not weeks and (leaf.id in core) != current_pass:
            current_pass = leaf.id in core
            lines += ["## Core" if current_pass else "## The rest", ""]
            if current_pass:
                lines += [f"*{len(core)} of {len(leaves)} topics: the declared Core and what it "
                          "requires. Anki deals these first.*", ""]
            current_branch = None
        if weeks and week_of[leaf.id] != current_week:
            current_week = week_of[leaf.id]
            lines += [f"## Week {current_week}", ""]
            current_branch = None
        branch = leaf.path()[0]
        if branch.id != current_branch:
            current_branch = branch.id
            lines.append(f"**{branch.title}**")
        count = per_node.get(leaf.id, 0)
        extras = [f"{count} cards"] + (["core"] if weeks and leaf.id in core else [])
        if leaf.requires:
            needs = ", ".join(skeleton.by_id[r].title for r in leaf.requires)
            extras.append(f"needs: {needs}")
        lines.append(f"- [ ] [[{leaf.id}|{leaf.title}]] — {'; '.join(extras)}")
    return "\n".join(lines)
