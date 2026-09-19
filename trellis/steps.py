"""Steps: giving the cards of a leaf their order.

Which card of a leaf should be met first is a judgement about teaching —
what has to be understood before what — and it cannot be computed from the
cards. So Trellis asks for it the way it asks for everything a model or a
person has to decide: it writes a prompt, hands it to a Runner, and checks
the answer. The check is strict because the answer is mechanical: each leaf
must come back as exactly its own cards, each once.

An accepted answer becomes one `step:` line in each card's frontmatter. The
edit is textual and touches only that line, so comments, key order and
everything else an author wrote in the file survive it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .cards import Card
from .project import Project

RULES = """You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{{
{shape}
}}
"""


def own_cards(project: Project) -> dict[str, list[Card]]:
    """Leaf id -> the cards Trellis owns on it, for every leaf that has any."""
    out: dict[str, list[Card]] = {}
    leaves = {leaf.id for leaf in project.skeleton.leaves()}
    for card in project.cards:
        if not card.adopted and card.node in leaves:
            out.setdefault(card.node, []).append(card)
    return out


def is_ordered(cards: list[Card]) -> bool:
    """A leaf is ordered when its own route is: grown cards arrive later and
    follow the rest by rule, so they never make a leaf unordered."""
    first_route = [c for c in cards if "grown" not in c.tags] or cards
    return all(c.step is not None for c in first_route)


def status_lines(project: Project) -> list[str]:
    by_leaf = own_cards(project)
    pending = [(leaf, cards) for leaf, cards in by_leaf.items() if not is_ordered(cards)]
    lines = [f"{project.skeleton.title}: {len(by_leaf) - len(pending)}/{len(by_leaf)} leaves ordered"]
    lines += [f"  {leaf:<44} {len(cards)} card(s), no order yet" for leaf, cards in pending[:12]]
    if len(pending) > 12:
        lines.append(f"  … and {len(pending) - 12} more")
    return lines


def _front(card: Card) -> str:
    return " ".join((card.question or card.text).split())


def steps_prompt(project: Project, branch: str | None = None, only_pending: bool = False) -> str:
    by_leaf = own_cards(project)
    blocks, shape = [], []
    for leaf in project.skeleton.leaves():
        cards = by_leaf.get(leaf.id)
        if not cards or (branch and not (leaf.id == branch or leaf.id.startswith(branch + "."))) \
                or (only_pending and is_ordered(cards)):
            continue
        lines = [f"## {leaf.id} — {leaf.title}"]
        if leaf.summary:
            lines.append(leaf.summary)
        for card in cards:
            back = " ".join(card.answer.split())[:160]
            lines.append(f"- `{card.id}` Q: {_front(card)}" + (f"\n  A: {back}" if back else ""))
        blocks.append("\n".join(lines))
        shape.append(f'  "{leaf.id}": ["<id shown first>", "…"]')
    return RULES.format(shape=",\n".join(shape[:3] + (["  …"] if len(shape) > 3 else []))) \
        + "\n" + "\n\n".join(blocks) + "\n"


def check(project: Project, answer: object) -> tuple[dict[str, list[Card]], list[str]]:
    """Validate an answer. Returns (leaf -> cards in order, errors); the
    first is empty whenever the second is not."""
    if not isinstance(answer, dict):
        return {}, ["expected a JSON object mapping each leaf id to its card ids in order"]
    by_leaf = own_cards(project)
    leaves = {leaf.id for leaf in project.skeleton.leaves()}
    errors: list[str] = []
    ordered: dict[str, list[Card]] = {}
    for leaf, ids in answer.items():
        if leaf not in leaves:
            errors.append(f"{leaf} is not a leaf of {project.skeleton.domain}")
            continue
        if not (isinstance(ids, list) and all(isinstance(i, str) for i in ids)):
            errors.append(f"{leaf}: expected a list of card ids")
            continue
        mine = {c.id: c for c in by_leaf.get(leaf, [])}
        for card_id in dict.fromkeys(ids):
            if ids.count(card_id) > 1:
                errors.append(f"{leaf}: {card_id} appears twice")
            if card_id not in mine:
                errors.append(f"{leaf}: {card_id} is not a card of {leaf}")
        for card_id in mine:
            if card_id not in ids:
                errors.append(f"{leaf}: the order leaves out {card_id}")
        ordered[leaf] = [mine[i] for i in ids if i in mine]
    return ({}, errors) if errors else (ordered, [])


_STEP_LINE = re.compile(r"^step:.*\n", re.MULTILINE)
_ANCHOR = re.compile(r"^(type|node):.*\n", re.MULTILINE)


def write_step(path: Path, step: int) -> bool:
    """Set the `step:` line of one card file. Returns whether it changed."""
    raw = path.read_text(encoding="utf-8")
    _, front, body = raw.split("---\n", 2)
    line = f"step: {step}\n"
    if _STEP_LINE.search(front):
        new_front = _STEP_LINE.sub(line, front, count=1)
    else:
        anchors = list(_ANCHOR.finditer(front))
        at = anchors[-1].end() if anchors else len(front)
        new_front = front[:at] + line + front[at:]
    if new_front == front:
        return False
    path.write_text(f"---\n{new_front}---\n{body}", encoding="utf-8")
    return True


def import_steps(project: Project, json_path: str | Path, write: bool = True,
                 ) -> tuple[int, list[str]]:
    """Land an answer: all of it or none of it. Returns (files changed,
    errors) — or, with `write` off, (cards the answer orders, errors)."""
    raw = Path(json_path).read_text(encoding="utf-8")
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw)
    try:
        answer = json.loads(raw)
    except json.JSONDecodeError as exc:
        return 0, [f"{json_path}: invalid JSON: {exc}"]
    ordered, errors = check(project, answer)
    if errors:
        return 0, errors
    if not write:
        return sum(len(cards) for cards in ordered.values()), []
    changed = 0
    for cards in ordered.values():
        for step, card in enumerate(cards, start=1):
            changed += write_step(card.path, step)
    return changed, []
