"""Seed: a corpus's outline becomes a skeleton draft for a subject that has
none yet.

ADR 0002 forbids deriving a skeleton from a codebase, because the result has
exactly the author's blind spots. A canonical book is field evidence rather
than one team's shape, so it may seed a draft — but the draft is judged the
way ADR 0002 demands: as an opinion about the *subject*, with the leaves the
book never covers added by that review and listed back as `uncovered`. The
corpus is then triaged onto the skeleton like any other source, so what it
left empty shows up as gaps instead of disappearing (ADR 0006).

The contract is the one every LLM step here has: a prompt out, JSON back,
validated all-or-nothing before a file is written.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from .corpus import Corpus, Outline
from .skeleton import SkeletonError, load_skeleton

PROMPT = """\
You are drafting the study map (a "skeleton") for a subject, using a book's
table of contents as evidence of what the field contains. Answer with one
JSON object (no prose).

## Subject
domain slug: `{domain}` — the book: {title}{author}
Cards written for this domain will be in: {lang}.

## The book's outline
{outline}

## What a skeleton is
- A tree of topics. Top-level nodes are branches; a node with no children
  is a LEAF, and a leaf is ONE probe: narrow enough that "I'm weak here"
  names something specific to drill, wide enough to carry 3-6 cards.
- ids are dotted lowercase slugs; a child's id starts with its parent's id
  plus a dot (`producer.acks`). Study order = list order. `requires` lists
  ids of nodes that must be understood first (cross-branch edges only;
  a parent is implied). No node may be ordered before one it requires.
- Every node has a one-line `summary` in {lang} naming what the leaf
  teaches, not what the chapter is called.

## Rules
- Map the SUBJECT, not the book. Merge chapters that teach one thing;
  split a chapter that teaches several. Drop front matter, installation
  walkthroughs, and anything that teaches nothing an engineer must know.
- Then add what the field considers canon that this edition omits or
  treats lightly (newer mechanisms, superseded ones the reader will meet
  in the wild, the questions an interviewer asks). List those leaf ids
  under `uncovered` — they are the reader's reading list, not padding.
- Aim for {branches} branches and {leaves} leaves. Titles in {lang}
  with the term of art in English where one exists.

## Answer format
{{"corpus": "{corpus}",
  "skeleton": {{"domain": "{domain}", "title": "...", "lang": "{lang_code}",
    "nodes": [
      {{"id": "producer", "title": "...", "summary": "...", "children": [
        {{"id": "producer.acks", "title": "...", "summary": "...",
          "requires": ["replication.isr"]}}
      ]}}
    ]}},
  "uncovered": ["controller.kraft"]}}
"""

LANG_NAMES = {"en": "English", "zh": "Chinese (简体中文)"}


def outline_text(outline: Outline) -> str:
    lines = []
    for section in outline.sections:
        indent = "  " * (section.level - 1)
        lines.append(f"{indent}- `{section.id}` {section.title}")
        for child in section.children:
            lines.append(f"{indent}    - {child}")
    return "\n".join(lines)


def seed_prompt(corpus: Corpus, outline: Outline, branches: str = "8-14",
                leaves: str = "40-70") -> str:
    return PROMPT.format(
        domain=corpus.domain, title=corpus.title,
        author=f" by {corpus.author}" if corpus.author else "",
        lang=LANG_NAMES.get(corpus.lang, corpus.lang), lang_code=corpus.lang,
        outline=outline_text(outline), branches=branches, leaves=leaves,
        corpus=corpus.id,
    )


def accept_seed(proposal_path: str | Path, root: Path, corpus: Corpus,
                ) -> tuple[Path | None, list[str], list[str]]:
    """Validate the drafted skeleton with the real loader and write it.
    Returns (path, errors, uncovered). All-or-nothing."""
    raw = Path(proposal_path).read_text(encoding="utf-8")
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, [f"{proposal_path}: invalid JSON: {exc}"], []
    skeleton = data.get("skeleton")
    if not isinstance(skeleton, dict):
        return None, [f"{proposal_path}: no 'skeleton' object"], []
    domain = skeleton.get("domain")
    if domain != corpus.domain:
        return None, [f"{proposal_path}: skeleton domain {domain!r} is not the "
                      f"corpus's domain {corpus.domain!r}"], []
    dest = Path(root) / "skeleton" / f"{domain}.yaml"
    if dest.exists():
        return None, [f"{dest} already exists — seeding is for a subject with no "
                      "skeleton; grow an existing one by hand from the gaps"], []
    skeleton.setdefault("lang", corpus.lang)
    header = (f"# {skeleton.get('title', domain)}: seeded from the outline of "
              f"`{corpus.id}` ({corpus.title}), then reviewed as a map of the\n"
              f"# subject — see ADR 0006. Leaves the source does not cover are the\n"
              f"# reading list, not a defect.\n")
    body = header + yaml.safe_dump(skeleton, allow_unicode=True, sort_keys=False, width=100)
    # Validate exactly what will be written, with the loader that will read it.
    tmp = dest.with_suffix(".yaml.proposed")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(body, encoding="utf-8")
    try:
        load_skeleton(tmp)
    except SkeletonError as exc:
        tmp.unlink()
        return None, [str(exc).replace(str(tmp), str(dest))], []
    tmp.rename(dest)
    uncovered = [str(u) for u in (data.get("uncovered") or [])]
    return dest, [], uncovered
