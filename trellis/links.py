"""Links: every card should lead somewhere deeper.

A card counts as linked when its body carries an inline markdown link, or
when its node (or any ancestor) has readings with URLs — those readings
are rendered as a clickable "Sources" footer on the Anki card. Coverage
of that property is a first-class metric: the project's job is to be the
authoritative index, so a card without a road onward is a gap.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .cards import Card
from .clippings import Clipping, canonical_url
from .obsidian import open_uri
from .readings import Reading
from .skeleton import Skeleton

_INLINE_LINK_RE = re.compile(r"\[[^\]]+\]\(https?://")

LINK_COVERAGE_TARGET = 0.7


def has_inline_link(card: Card) -> bool:
    return bool(_INLINE_LINK_RE.search(card.question + card.answer + card.text))


# Tags that mark a reading as a pointer rather than something you can sit
# down and read: a book you must own, an index you must navigate.
_POINTER_TAGS = {"book", "index"}

# A video is the resource itself, not a page about one. It can never be
# clipped — extracting a watch page yields chrome — but tapping it puts the
# material in front of you as directly as an archived article does, so it
# counts as readable and is not ranked below clipped prose. In a domain
# learned by watching (a movement, a drill, a defensive rotation), the video
# is the primary source and the writing about it is the summary.
VIDEO_TAG = "video"


def sources_for(
    skeleton: Skeleton,
    readings: list[Reading],
    node_id: str,
    limit: int = 3,
    clippings: dict[str, Clipping] | None = None,
) -> list[Reading]:
    """Readings attached to the node or an ancestor, best first.

    "Best" is by what it costs the reader to get the information: an
    archived article you can read on the spot beats a web page, which beats
    a book's homepage or a docs index. Proximity to the node breaks ties,
    so a leaf's own source still wins among equals.
    """
    node = skeleton.by_id.get(node_id)
    if node is None:
        return []
    clippings = clippings or {}
    distance = {n.id: d for d, n in enumerate(reversed(node.path()))}

    candidates: dict[str, tuple[tuple, Reading]] = {}
    for reading in readings:
        if not reading.url and not reading.authored:
            continue
        near = min((distance[n] for n in reading.nodes if n in distance), default=None)
        if near is None:
            continue
        clip = clippings.get(canonical_url(reading.url)) if reading.url else None
        at_hand = reading.authored or (clip is not None and clip.is_substantive) \
            or is_video(reading)
        rank = (
            # A book or an index is last whatever else is true of it: its
            # homepage archiving cleanly does not put the chapter in your
            # hands. Tag a genuine full chapter `canonical`, not `book`.
            1 if _POINTER_TAGS & set(reading.tags) else 0,
            0 if at_hand else 1,
            near,
            # among equals, what was written for this leaf beats what was found for it
            0 if reading.authored else 1,
        )
        key = canonical_url(reading.url) if reading.url else f"vault:{reading.path.stem}"
        if key not in candidates or rank < candidates[key][0]:
            candidates[key] = (rank, reading)
    return [r for _, r in sorted(candidates.values(), key=lambda x: x[0])][:limit]


@dataclass
class GoDeeper:
    """One entry of a card's further-reading footer."""

    title: str
    href: str            # obsidian:// when a clipping exists, else the web URL
    web_href: str | None  # the original URL, kept as a fallback when href is local
    is_video: bool = False

    @property
    def is_local(self) -> bool:
        return self.href.startswith("obsidian://")


def go_deeper(
    skeleton: Skeleton,
    readings: list[Reading],
    node_id: str,
    vault: str | None = None,
    clippings: dict[str, Clipping] | None = None,
    cases: list[Reading] | None = None,
) -> list[GoDeeper]:
    """Footer links for a card on `node_id`.

    The obsidian:// target is always the *reading note* — addressed by name
    alone, never by path. Two reasons: the note is committed, so it exists
    on every device, and a bare name resolves wherever the vault root
    happens to sit (the phone clones the whole repo; the desktop opens
    `vault/`). The clipped article rides along embedded inside that note.
    """
    out: list[GoDeeper] = []
    # Cases come first: "a real system did this, and here is what it cost"
    # is what makes the leaf's principle stick. They are vault notes, so
    # they are addressed by name like everything else.
    if vault:
        out += [GoDeeper(c.title, open_uri(vault, c.path.stem), None)
                for c in cases or [] if node_id in c.nodes]
    for reading in sources_for(skeleton, readings, node_id, clippings=clippings):
        video = is_video(reading)
        if reading.authored and not vault:
            continue                     # it lives only in the vault; no vault, no link
        if vault and not video:
            out.append(
                GoDeeper(reading.title, open_uri(vault, reading.path.stem), reading.url or None)
            )
        else:
            # A video has nothing embedded in its note to open — send the tap
            # straight to the footage.
            out.append(GoDeeper(reading.title, reading.url, None, is_video=video))
    return out


def is_video(reading: Reading) -> bool:
    """A reading whose material is the footage itself."""
    return VIDEO_TAG in reading.tags and bool(reading.url)


def is_readable_source(reading: Reading, clippings: dict[str, Clipping]) -> bool:
    """True when this reading is something you can actually sit down and
    take in: archived in the vault with real prose, or a video that plays
    on tap — and not a pointer at a book you must own or an index you must
    navigate."""
    if _POINTER_TAGS & set(reading.tags):
        return False
    if is_video(reading) or reading.authored:
        return True
    clip = clippings.get(canonical_url(reading.url))
    return clip is not None and clip.is_substantive


def leaves_without_readable_source(
    skeleton: Skeleton, readings: list[Reading], clippings: dict[str, Clipping]
) -> list[str]:
    """Leaves whose best source is still a book, an index, or a page that
    would not archive — the cards there send you hunting instead of
    reading."""
    return [
        leaf.id
        for leaf in skeleton.leaves()
        if not any(
            is_readable_source(r, clippings)
            for r in sources_for(skeleton, readings, leaf.id, clippings=clippings)
        )
    ]


def coverage(skeleton: Skeleton, cards: list[Card],
             readings: list[Reading]) -> tuple[int, int]:
    """(linked_cards, total_cards)."""
    linked = sum(
        1 for c in cards
        if has_inline_link(c) or sources_for(skeleton, readings, c.node)
    )
    return linked, len(cards)
