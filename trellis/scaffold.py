"""Scaffold: the LLM content loop, with the skeleton as the contract.

`trellis scaffold <node>` emits a self-contained prompt for any LLM. The
prompt carries the node's context (path, summary, prerequisites, sibling
topics, existing card fronts) so generated cards stay atomic, in-scope,
and non-duplicative. The LLM answers with JSON; `trellis import` validates
that JSON against the skeleton and existing cards, then writes normal card
markdown files. The LLM never touches the vault directly.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .cards import _CLOZE_RE, _ID_RE, Card
from .skeleton import Skeleton

PROMPT_TEMPLATE = """\
You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
{crumb}
{summary}

## Position in the knowledge map
{context}

## Rules
- Write {count} cards for THIS topic only. Sibling topics listed above are
  out of scope — never restate their material.
- One card = one retrievable fact, mechanism, trade-off, or number. If an
  answer needs more than ~4 sentences, split the card.
- Prefer questions that force discrimination ("when would you choose X
  over Y") over definitions, except for terms of art.
- Use `type: "cloze"` with {{{{c1::...}}}} syntax for formulas, sequences,
  and lists; `type: "qa"` otherwise.
- Markdown allowed in q/a/text (code spans, tables, lists).
- id: lowercase-hyphenated slug, unique, descriptive, stable.
{avoid}
## Output format (JSON array only, no prose)
[
  {{"id": "example-qa-card", "node": "{node_id}", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []}},
  {{"id": "example-cloze-card", "node": "{node_id}", "type": "cloze",
    "text": "The formula is {{{{c1::W + R > N}}}}.", "tags": []}}
]
"""


def scaffold_prompt(skeleton: Skeleton, node_id: str, cards: list[Card], count: int = 8) -> str:
    node = skeleton.by_id[node_id]
    crumb = " › ".join(n.title for n in node.path())

    context_lines: list[str] = []
    if node.requires:
        context_lines.append("Prerequisites (assume known):")
        for req in node.requires:
            r = skeleton.by_id[req]
            context_lines.append(f"  - {r.title}: {r.summary or '(no summary)'}")
    parent = node.parent
    siblings = [s for s in (parent.children if parent else skeleton.roots) if s is not node]
    if siblings:
        context_lines.append("Sibling topics (OUT of scope):")
        context_lines += [f"  - {s.title}: {s.summary or ''}".rstrip(": ") for s in siblings]
    if node.children:
        context_lines.append("Subtopics covered by their own cards (stay above them):")
        context_lines += [f"  - {c.title}" for c in node.children]

    existing = [c for c in cards if c.node == node_id]
    avoid = ""
    if existing:
        fronts = "\n".join(
            f"  - {(c.question or c.text).splitlines()[0][:100]}" for c in existing
        )
        avoid = f"- Existing cards on this topic — do NOT duplicate them:\n{fronts}\n"

    return PROMPT_TEMPLATE.format(
        crumb=crumb,
        summary=node.summary or "",
        context="\n".join(context_lines) or "(top-level topic)",
        count=count,
        node_id=node_id,
        avoid=avoid,
    )


def import_cards(
    skeleton: Skeleton,
    existing: list[Card],
    json_path: str | Path,
    cards_dir: str | Path,
) -> tuple[list[Path], list[str]]:
    """Validate an LLM's JSON and write card files. All-or-nothing:
    any error means nothing is written. Returns (written_paths, errors)."""
    json_path = Path(json_path)
    raw = json_path.read_text(encoding="utf-8")
    # Tolerate a ```json fence around the array — LLMs love those.
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw)
    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [], [f"{json_path}: invalid JSON: {exc}"]
    if not isinstance(items, list):
        return [], [f"{json_path}: expected a JSON array of cards"]

    errors: list[str] = []
    taken = {c.id for c in existing}
    staged: list[tuple[Path, str]] = []
    for i, item in enumerate(items):
        where = f"{json_path}[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: not an object")
            continue
        card_id = item.get("id", "")
        node_id = item.get("node", "")
        ctype = item.get("type", "qa")
        if not isinstance(card_id, str) or not _ID_RE.match(card_id):
            errors.append(f"{where}: invalid id {card_id!r}")
            continue
        if card_id in taken:
            errors.append(f"{where}: id {card_id!r} already exists")
            continue
        taken.add(card_id)
        node = skeleton.by_id.get(node_id)
        if node is None:
            errors.append(f"{where}: unknown node {node_id!r}")
            continue

        meta = [f"id: {card_id}", f"node: {node_id}", f"type: {ctype}"]
        tags = item.get("tags") or []
        if tags:
            meta.append("tags: [" + ", ".join(map(str, tags)) + "]")
        if item.get("source"):
            meta.append(f"source: {item['source']}")
        header = "---\n" + "\n".join(meta) + "\n---\n"

        if ctype == "qa":
            q, a = item.get("q", ""), item.get("a", "")
            if not q or not a:
                errors.append(f"{where}: qa card missing q or a")
                continue
            body = f"## Q\n{q}\n\n## A\n{a}\n"
            # A translation travels beside the card, never instead of it.
            if item.get("q_zh") and item.get("a_zh"):
                body += f"\n## Q zh\n{item['q_zh']}\n\n## A zh\n{item['a_zh']}\n"
        elif ctype == "cloze":
            text = item.get("text", "")
            if not text or not _CLOZE_RE.search(text):
                errors.append(f"{where}: cloze card missing text or {{{{c1::...}}}}")
                continue
            body = text.rstrip() + "\n"
            if item.get("text_zh"):
                body += f"\n## zh\n{str(item['text_zh']).rstrip()}\n"
        else:
            errors.append(f"{where}: bad type {ctype!r}")
            continue

        branch = node.path()[0].id
        staged.append((Path(cards_dir) / branch / f"{card_id}.md", header + body))

    if errors:
        return [], errors
    written: list[Path] = []
    for path, content in staged:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written, []
