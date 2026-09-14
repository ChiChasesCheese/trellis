"""Triage: deciding what a codebase's artefacts should become.

Triage never writes into the vault. It prepares a prompt naming every artefact
and every leaf it could attach to, an LLM answers with a proposal, and the
proposal is validated against the skeletons before a single file appears —
the same all-or-nothing contract the card importer already uses.

An artefact that cannot be placed is not an error. It is a proposal to grow a
skeleton, which is the whole reason the skeletons are authored independently
of the codebases mapped onto them.
"""

from __future__ import annotations

import json
import re

import yaml
from pathlib import Path

from .cases import CASES_DIRNAME, write_case
from .codebases import Artefact, Codebase
from .skeleton import Skeleton

VERDICTS = ("case", "reading", "skip", "gap")
_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

PROMPT = """\
You are triaging a codebase into a study system. For each artefact below decide
what it should become, and answer with one JSON object (no prose).

## Codebase
{codebase} at {sha}, cached read-only at {cache}

## Lenses and their leaves
{inventory}

## Artefacts
{artefacts}

## Verdicts
- `case` — the artefact records a DECISION that is an instance of something a
  leaf already teaches. Rewrite it in that lens's vocabulary: what problem it
  solves, what it forbids, what it costs. Never restate it as "we chose X";
  a reader who does not know this codebase must still learn something.
- `reading` — the artefact is SUBJECT MATTER for a leaf: it teaches a topic
  rather than recording a choice.
- `gap` — the artefact clearly belongs to one of these lenses but no leaf fits.
  Propose the leaf that is missing. This is a wanted outcome, not a failure.
- `skip` — housekeeping, duplication, or specific to this codebase in a way
  that teaches nothing transferable.

## Rules
- `nodes` must be leaf ids of the lens you chose, copied exactly from above.
- `slug` must be unique, lowercase-hyphenated, and start with `{prefix}`.
- `body` is markdown, 100-250 words, written for someone who has never seen
  this repository. State the mechanism and the trade-off, not the conclusion.
- Be strict. An artefact that teaches nothing transferable is a `skip`, and
  skipping is cheaper than diluting the deck.

## Answer format
{{"codebase": "{codebase}", "ref": "{sha}", "items": [
  {{"artefact": "decisions:0004-...", "verdict": "case", "lens": "system-design",
   "nodes": ["async.log"], "slug": "{prefix}-...", "title": "...",
   "body": "...", "confidence": "high"}},
  {{"artefact": "subject:...", "verdict": "gap", "lens": "quant-infra",
   "proposed_leaf": "data.point-in-time", "why": "..."}},
  {{"artefact": "subject:...", "verdict": "skip", "why": "..."}}
]}}
"""


def leaf_inventory(skeletons: dict[str, Skeleton]) -> str:
    lines: list[str] = []
    for domain, skeleton in skeletons.items():
        lines.append(f"### {domain}")
        for leaf in skeleton.leaves():
            crumb = " › ".join(n.title for n in leaf.path()[:-1])
            lines.append(f"- `{leaf.id}` — {crumb}: {leaf.summary or leaf.title}")
    return "\n".join(lines)


def triage_prompt(
    codebase: Codebase,
    sha: str,
    artefacts: list[Artefact],
    skeletons: dict[str, Skeleton],
    prefix: str = "",
) -> str:
    listed = "\n".join(
        f"- `{a.id}` ({a.kind}"
        + (f", suggested lens {a.lens}" if a.lens else "")
        + f") — {a.rel}"
        + (f"\n  > {a.excerpt}" if a.excerpt else "")
        for a in artefacts
    )
    return PROMPT.format(
        codebase=codebase.name,
        sha=sha[:12],
        cache=codebase.cache(Path(".")),
        inventory=leaf_inventory(skeletons),
        artefacts=listed,
        prefix=prefix or codebase.name.split("-")[0][:2] or "cb",
    )


def accept(
    proposal_path: str | Path,
    root: Path,
    skeletons: dict[str, Skeleton],
    existing_names: set[str],
) -> tuple[list[Path], list[str], list[dict]]:
    """Validate a proposal and write what it accepts. All-or-nothing:
    any error means nothing is written. Returns (written, errors, gaps)."""
    raw = Path(proposal_path).read_text(encoding="utf-8")
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [], [f"{proposal_path}: invalid JSON: {exc}"], []
    codebase, ref = data.get("codebase", ""), data.get("ref", "")
    if not codebase or not ref:
        return [], [f"{proposal_path}: proposal must name its codebase and ref"], []

    errors: list[str] = []
    gaps: list[dict] = []
    staged: list[tuple[Path, dict]] = []
    taken = set(existing_names)

    for i, item in enumerate(data.get("items") or []):
        where = f"item[{i}] {item.get('artefact', '?')}"
        verdict = item.get("verdict")
        if verdict not in VERDICTS:
            errors.append(f"{where}: verdict must be one of {VERDICTS}")
            continue
        if verdict == "skip":
            continue
        if verdict == "gap":
            gaps.append(item)
            continue

        lens = item.get("lens")
        skeleton = skeletons.get(lens)
        if skeleton is None:
            errors.append(f"{where}: unknown lens {lens!r}")
            continue
        nodes = item.get("nodes") or []
        if not nodes:
            errors.append(f"{where}: needs at least one node")
            continue
        for node in nodes:
            if node not in skeleton.by_id:
                errors.append(f"{where}: {lens} has no node {node!r}")
            elif not skeleton.by_id[node].is_leaf:
                errors.append(f"{where}: {node!r} is not a leaf")
        slug = item.get("slug", "")
        if not _SLUG_RE.match(slug):
            errors.append(f"{where}: invalid slug {slug!r}")
            continue
        if slug in taken:
            errors.append(f"{where}: slug {slug!r} already exists in the vault "
                          "(note names must be unique — card links resolve by name)")
            continue
        taken.add(slug)
        if not item.get("title") or not item.get("body"):
            errors.append(f"{where}: needs a title and a body")
            continue
        if verdict == "case" and item.get("artefact") is None:
            errors.append(f"{where}: a case must name the artefact it came from")
            continue
        if verdict == "reading" and not item.get("path"):
            errors.append(f"{where}: a reading must name the artefact's path "
                          "in the codebase, so its text can be clipped")
            continue
        staged.append((lens, item))

    if errors:
        return [], errors, gaps

    written: list[Path] = []
    for lens, item in staged:
        content = root / "vault" / lens
        if item["verdict"] == "case":
            written.append(write_case(
                content / CASES_DIRNAME, item["slug"],
                title=item["title"], nodes=item["nodes"],
                codebase=codebase, ref=ref, artefact=item["artefact"],
                body=item["body"],
            ))
        else:
            written += _write_reading_with_clipping(
                content, root, codebase, ref, item)
    return written, [], gaps


def _write_reading_with_clipping(
    content: Path, root: Path, codebase: str, ref: str, item: dict
) -> list[Path]:
    """Subject matter from a codebase becomes a reading like any other,
    with the file itself clipped beside it — the same shape a clipped web
    article takes, so map notes and card footers need no special case."""
    from .clippings import CLIPPINGS_DIRNAME

    slug, path_in_repo = item["slug"], item["path"]
    url = (f"https://github.com/{item.get('repo', codebase)}/blob/{ref}/"
           f"{path_in_repo}")

    reading = content / "readings" / f"{slug}.md"
    reading.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(
        {"nodes": item["nodes"], "title": item["title"], "url": url,
         "tags": item.get("tags") or ["codebase"]},
        allow_unicode=True, sort_keys=False,
    )
    reading.write_text(f"---\n{front}---\n\n# {item['title']}\n\n{item['body'].strip()}\n",
                       encoding="utf-8")

    written = [reading]
    source = root / ".trellis" / "codebases" / codebase / path_in_repo
    if source.exists():
        clip = content / CLIPPINGS_DIRNAME / f"{slug}-clip.md"
        clip.parent.mkdir(parents=True, exist_ok=True)
        body = source.read_text(encoding="utf-8")
        if body.startswith("---\n"):  # drop the source file's own frontmatter
            parts = body.split("---\n", 2)
            body = parts[2] if len(parts) == 3 else body
        clip_front = yaml.safe_dump(
            {"title": item["title"], "source": url, "codebase": codebase,
             "clipped": ref[:12]},
            allow_unicode=True, sort_keys=False,
        )
        clip.write_text(f"---\n{clip_front}---\n\n{body.strip()}\n", encoding="utf-8")
        written.append(clip)
    return written


# --------------------------------------------------------------------------
# A corpus is triaged the same way: its sections beside the leaves of the
# one skeleton it lands on. No `case` verdict — a book records no decisions
# of its own — and a section that teaches a leaf becomes a reading carrying
# `corpus:` and `section:` as its provenance.

CORPUS_PROMPT = """\
You are triaging a book into a study system. For each section below decide
what it should become, and answer with one JSON object (no prose).

## Corpus
`{corpus}` — {title}. Sections are archived as markdown under `{text_dir}/`
(one file per section id) if you need to read one in full.

## The skeleton it lands on
{inventory}

## Sections
{sections}

## Verdicts
- `reading` — the section TEACHES one or more leaves. `nodes` lists them;
  `title` is the reading's own title; `body` (100-200 words, in {lang})
  says why to read this section and what to take from it, for someone who
  has never opened the book. A section may serve several leaves; a leaf
  may be served by several sections.
- `gap` — the section clearly belongs to this subject but no leaf fits.
  Name the missing leaf under `proposed_leaf`. A wanted outcome.
- `skip` — front matter, installation walkthroughs, summaries, or anything
  that teaches nothing a leaf should carry.

## Rules
- `nodes` must be leaf ids copied exactly from above.
- `slug` must be unique, lowercase-hyphenated, and start with `{prefix}-`.
- Be strict: a `skip` costs nothing, a diluted deck costs every review.

## Answer format
{{"corpus": "{corpus}", "items": [
  {{"section": "032-3-4", "verdict": "reading", "nodes": ["producer.acks"],
   "slug": "{prefix}-producer-config", "title": "...", "body": "..."}},
  {{"section": "001-section", "verdict": "skip", "why": "front matter"}},
  {{"section": "099-x", "verdict": "gap", "proposed_leaf": "ops.tiered-storage", "why": "..."}}
]}}
"""


def section_artefacts(corpus, outline, root: Path) -> list[Artefact]:
    """Every section of an ingested corpus as a triage artefact. Its
    excerpt is the sub-headings first — the best summary a chapter has —
    and then its opening words."""
    from .codebases import excerpt_of
    text_dir = corpus.text_dir(root)
    out: list[Artefact] = []
    for section in outline.sections:
        path = text_dir / f"{section.id}.md"
        head = ("; ".join(section.children) + " — ") if section.children else ""
        out.append(Artefact(
            id=section.id, kind="section", lens=corpus.domain, path=path,
            rel=section.title, excerpt=head + excerpt_of(path, 160),
        ))
    return out


def corpus_triage_prompt(corpus, outline, artefacts: list[Artefact],
                         skeleton: Skeleton, root: Path, prefix: str = "") -> str:
    from .seed import LANG_NAMES
    listed = "\n".join(
        f"- `{a.id}` (L{outline.by_id()[a.id].level}) {a.rel}"
        + (f"\n  > {a.excerpt}" if a.excerpt else "")
        for a in artefacts
    )
    return CORPUS_PROMPT.format(
        corpus=corpus.id, title=corpus.title,
        text_dir=corpus.text_dir(root).relative_to(root),
        inventory=leaf_inventory({skeleton.domain: skeleton}),
        # A reading lives in the domain and is read by its learner, so it is
        # written in the domain's language even when the source text is not.
        sections=listed, lang=LANG_NAMES.get(skeleton.lang, skeleton.lang),
        prefix=prefix or corpus.id.split("-")[0][:8],
    )


def accept_corpus(
    proposal_path: str | Path, root: Path, corpus, outline, skeleton: Skeleton,
    existing_names: set[str],
) -> tuple[list[Path], list[str], list[dict]]:
    """Validate a corpus proposal and write the readings it accepts, with
    the section's text clipped beside each when the license allows.
    All-or-nothing. Returns (written, errors, gaps)."""
    from .clippings import CLIPPINGS_DIRNAME

    raw = Path(proposal_path).read_text(encoding="utf-8")
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [], [f"{proposal_path}: invalid JSON: {exc}"], []
    if data.get("corpus") != corpus.id:
        return [], [f"{proposal_path}: proposal is for {data.get('corpus')!r}, "
                    f"not {corpus.id!r}"], []
    sections = outline.by_id()
    errors: list[str] = []
    gaps: list[dict] = []
    staged: list[dict] = []
    taken = set(existing_names)
    for i, item in enumerate(data.get("items") or []):
        where = f"item[{i}] {item.get('section', '?')}"
        verdict = item.get("verdict")
        if verdict not in ("reading", "gap", "skip"):
            errors.append(f"{where}: verdict must be reading, gap or skip")
            continue
        if item.get("section") not in sections:
            errors.append(f"{where}: unknown section")
            continue
        if verdict == "skip":
            continue
        if verdict == "gap":
            gaps.append(item)
            continue
        nodes = item.get("nodes") or []
        if not nodes:
            errors.append(f"{where}: needs at least one node")
            continue
        for node in nodes:
            if node not in skeleton.by_id:
                errors.append(f"{where}: {skeleton.domain} has no node {node!r}")
            elif not skeleton.by_id[node].is_leaf:
                errors.append(f"{where}: {node!r} is not a leaf")
        slug = item.get("slug", "")
        if not _SLUG_RE.match(slug):
            errors.append(f"{where}: invalid slug {slug!r}")
            continue
        if slug in taken:
            errors.append(f"{where}: slug {slug!r} already exists in the vault "
                          "(note names must be unique — card links resolve by name)")
            continue
        taken.add(slug)
        if not item.get("title") or not item.get("body"):
            errors.append(f"{where}: needs a title and a body")
            continue
        staged.append(item)
    if errors:
        return [], errors, gaps

    content = root / "vault" / skeleton.domain
    text_dir = corpus.text_dir(root)
    written: list[Path] = []
    for item in staged:
        section = sections[item["section"]]
        slug = item["slug"]
        # A free chapter fetched from the web keeps its own URL, so the
        # existing clipping machinery matches the two; a book you own
        # points at its home page and is tagged as the pointer it is.
        url = section.locator if section.locator.startswith("http") else corpus.home
        tags = ["canonical"] if corpus.is_free and url else ["book"]
        reading = content / "readings" / f"{slug}.md"
        reading.parent.mkdir(parents=True, exist_ok=True)
        front = {"nodes": item["nodes"], "title": item["title"],
                 "corpus": corpus.id, "section": section.id}
        if url:
            front["url"] = url
        front["tags"] = tags
        reading.write_text(
            "---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False)
            + f"---\n\n# {item['title']}\n\n{item['body'].strip()}\n", encoding="utf-8")
        written.append(reading)
        source = text_dir / f"{section.id}.md"
        if corpus.is_free and url and source.exists():
            clip = content / CLIPPINGS_DIRNAME / f"{slug}-clip.md"
            clip.parent.mkdir(parents=True, exist_ok=True)
            body = source.read_text(encoding="utf-8")
            if body.startswith("---\n"):
                parts = body.split("---\n", 2)
                body = parts[2] if len(parts) == 3 else body
            from datetime import date
            clip_front = yaml.safe_dump(
                {"title": section.title, "source": url, "corpus": corpus.id,
                 "section": section.id, "clipped": date.today().isoformat()},
                allow_unicode=True, sort_keys=False)
            clip.write_text(f"---\n{clip_front}---\n\n# {section.title}\n\n{body.strip()}\n",
                            encoding="utf-8")
            written.append(clip)
    return written, [], gaps


def codebase_index(root: Path, name: str, domains: list[str]) -> str:
    """A per-codebase view over material that is stored per domain."""
    from .cases import load_cases

    lines = [f"# {name}", "", "What this codebase contributed, by lens.", ""]
    total = 0
    for domain in domains:
        cases_dir = root / "vault" / domain / CASES_DIRNAME
        if not cases_dir.exists():
            continue
        cases = [c for c in load_cases(cases_dir)[0]
                 if c.extra.get("codebase") == name]
        if not cases:
            continue
        lines.append(f"## {domain}")
        for case in sorted(cases, key=lambda c: c.path.stem):
            nodes = ", ".join(f"[[{n}]]" for n in case.nodes)
            lines.append(f"- [[{case.path.stem}|{case.title}]] — {nodes}"
                         f"  `{case.extra.get('artefact')}` @ `{str(case.extra.get('ref'))[:12]}`")
        lines.append("")
        total += len(cases)
    lines.insert(3, f"{total} case(s) accepted.\n" if total else "Nothing accepted yet.\n")
    return "\n".join(lines)
