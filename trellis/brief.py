"""Brief: the one note that says what to do next.

There is exactly one Brief and it spans every domain. That is the whole
point of it. A per-domain report would be a better dashboard and a worse
instrument: it would let you sink into the subject you are already best
at, which is the failure mode this is here to prevent. So the Brief
ranks across domains, and caps how much of it any one domain may occupy
— a domain with 465 cards cannot crowd out one with 30.

It opens with a single move, not a table. Everything below the first
line is optional reading. The counts live at the bottom, because a
backlog number at the top of a page is the fastest way to make someone
close it.
"""

from __future__ import annotations

from .hold import Assessment, LeafStanding
from .skeleton import Skeleton

# No domain may take more than this many rows in a section. Breadth is a
# constraint on the report, not a suggestion in it.
PER_DOMAIN_CAP = 3

# Sections stop here whether or not there is more to say. A Brief you can
# read standing up is one you read; a complete one is one you skim.
SECTION_LIMIT = 8


def _bar(value: float | None, width: int = 10) -> str:
    """Hold as a bar, because a number between 0 and 1 means nothing at a
    glance and a bar means everything."""
    if value is None:
        return "·" * width
    filled = round(value * width)
    return "█" * filled + "░" * (width - filled)


def _link(domain: str, standing: LeafStanding) -> str:
    return f"[[{standing.node.id}|{standing.node.title}]]"


def _interleave(
    rows: list[tuple[str, LeafStanding]],
    cap: int = PER_DOMAIN_CAP,
    limit: int = SECTION_LIMIT,
) -> list[tuple[str, LeafStanding]]:
    """Take the best rows overall, then enforce the cap by dealing them
    out domain by domain — so the head of the list is always a mix even
    when one domain owns the top ten on merit."""
    by_domain: dict[str, list[tuple[str, LeafStanding]]] = {}
    for domain, standing in rows:
        by_domain.setdefault(domain, []).append((domain, standing))

    out: list[tuple[str, LeafStanding]] = []
    for round_no in range(cap):
        for domain in sorted(by_domain):
            queue = by_domain[domain]
            if round_no < len(queue):
                out.append(queue[round_no])
    # rows arrived sorted; dealing them out shuffled that, so restore it
    order = {id(r[1]): i for i, r in enumerate(rows)}
    out.sort(key=lambda r: order[id(r[1])])
    return out[:limit]


def _opening_move(
    weak: list[tuple[str, LeafStanding]],
    uncovered: list[tuple[str, LeafStanding]],
    drills_by_node: dict[str, list],
    readings_by_node: dict[str, list],
) -> str:
    """One sentence naming one thing. If there is nothing to repair, say
    so plainly rather than inventing an errand."""
    if weak:
        domain, s = weak[0]
        because = (f"holding {s.hold:.0%}" if not s.bearing else
                   f"holding {s.hold:.0%}, and {s.bearing} "
                   f"topic{'s' if s.bearing != 1 else ''} stand"
                   f"{'' if s.bearing != 1 else 's'} on it")
        bits = [f"**Open with** {_link(domain, s)} — {because}."]
        onward = []
        for drill in drills_by_node.get(s.node.id, [])[:1]:
            onward.append(f"drill [[{drill.link_target}|{drill.title}]]")
        for reading in readings_by_node.get(s.node.id, [])[:1]:
            onward.append(f"read [[{reading.link_target}|{reading.title}]]")
        if onward:
            bits.append("→ " + " · ".join(onward))
        else:
            bits.append(f"→ nothing to practise on it yet: "
                        f"`trellis scaffold {s.node.id}`")
        return "\n".join(bits)
    if uncovered:
        domain, s = uncovered[0]
        because = (f"{s.bearing} topics stand on it and it has no cards"
                   if s.bearing else "it has no cards yet")
        return (f"**Open with** writing for {_link(domain, s)} — {because}.\n"
                f"→ `trellis --domain {domain} scaffold {s.node.id}`")
    return ("**Nothing is slipping.** Everything reviewed is holding, and "
            "every leaf has cards. Pull again after your next session.")


def brief_body(
    assessments: dict[str, Assessment],
    skeletons: dict[str, Skeleton],
    drills_by_node: dict[str, list] | None = None,
    readings_by_node: dict[str, list] | None = None,
    stale_days: dict[str, float | None] | None = None,
) -> str:
    """Render the Brief. Pure: takes assessments, returns markdown."""
    drills_by_node = drills_by_node or {}
    readings_by_node = readings_by_node or {}
    stale_days = stale_days or {}

    weak = _interleave(sorted(
        ((d, s) for d, a in assessments.items() for s in a.weaknesses()),
        key=lambda r: -r[1].urgency,
    ))
    uncovered = _interleave(sorted(
        ((d, s) for d, a in assessments.items() for s in a.uncovered()),
        key=lambda r: -r[1].bearing,
    ))
    sealed = [(d, s) for d, a in assessments.items() for s in a.sealed()][:SECTION_LIMIT]

    lines = ["# Brief", ""]
    lines += [_opening_move(weak, uncovered, drills_by_node, readings_by_node), ""]

    if weak:
        lines += ["## Slipping", "",
                  "| | topic | hold | bears |", "|---|---|---|---|"]
        for domain, s in weak:
            lines.append(f"| {skeletons[domain].title} | {_link(domain, s)} "
                         f"| `{_bar(s.hold)}` {s.hold:.0%} | {s.bearing} |")
        lines.append("")

    if uncovered:
        lines += ["## Worth writing", ""]
        for domain, s in uncovered:
            lines.append(f"- {_link(domain, s)} — {s.bearing} topics stand on it, "
                         f"no cards yet · `trellis --domain {domain} "
                         f"scaffold {s.node.id}`")
        lines.append("")

    if sealed:
        lines += ["## Sealed", "",
                  "*Cards exist but are held back until the ground under them "
                  "takes.*", ""]
        for domain, s in sealed:
            waiting = ", ".join(
                f"[[{r}|{skeletons[domain].by_id[r].title}]]" for r in s.sealed_by)
            lines.append(f"- {_link(domain, s)} — waiting on {waiting}")
        lines.append("")

    lines += ["---", ""]
    for domain in sorted(assessments):
        a = assessments[domain]
        hold = f"{a.hold:.0%}" if a.hold is not None else "—"
        age = stale_days.get(domain)
        when = "never pulled" if age is None else (
            "pulled today" if age < 1 else f"pulled {age:.0f}d ago")
        lines.append(f"- **{skeletons[domain].title}** — {a.reviewed}/{a.total} "
                     f"cards seen, hold {hold} · {when}")
    return "\n".join(lines)
