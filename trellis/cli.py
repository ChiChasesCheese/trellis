"""CLI. Layout convention (one repo, many domains):

    skeleton/<domain>.yaml      the mind map
    vault/<domain>/             Obsidian content for that domain
    vault/<domain>/cards/       cards (leaves)
    vault/<domain>/readings/    long-form notes, multi-node
    vault/<domain>/drills/      design/coding exercises, multi-node
    corpora/<id>.yaml           a book or series registered for digestion
    codebases/<name>.yaml       a repository studied as a learning target
    dist/<domain>.apkg          build output

Open vault/ itself as the Obsidian vault so wikilinks work across domains.
--domain is optional while the repo has one skeleton; --all runs
validate/sync/build/stats/path over every domain.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from .build import build_package
from .clippings import (
    CLIPPINGS_DIRNAME,
    ClipError,
    canonical_url,
    fetch_page,
    write_clipping,
)
from .codebases import CodebaseError, artefacts, fetch, load_codebase
from .corpus import CORPORA_DIRNAME, Corpus, CorpusError, load_corpora, load_corpus, load_outline
from .obsidian import vault_name
from .path import study_path
from .project import Project, all_skeletons, domains, load_project, vault_note_names
from .scaffold import import_cards, scaffold_prompt
from .skeleton import SkeletonError
from .sync import sync, write_managed
from .triage import (
    accept,
    accept_corpus,
    codebase_index,
    corpus_triage_prompt,
    section_artefacts,
    triage_prompt,
)


def _fail(msg: str) -> "sys.NoReturn":
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def _resolve_domains(root: Path, args) -> list[str]:
    available = domains(root)
    if not available:
        _fail(f"no skeleton files in {root / 'skeleton'}")
    if getattr(args, "all", False):
        return available
    if args.domain:
        if args.domain not in available:
            _fail(f"no skeleton/{args.domain}.yaml")
        return [args.domain]
    if len(available) > 1:
        _fail("multiple domains found, pass --domain or --all: "
              + ", ".join(available))
    return available


def _load(root: Path, domain: str) -> Project:
    try:
        return load_project(root, domain)
    except SkeletonError as exc:
        _fail(str(exc))


def _print_report(report) -> None:
    for w in report.warnings:
        print(f"warning: {w}")
    for e in report.errors:
        print(f"error: {e}", file=sys.stderr)


def _checked(project: Project, action: str) -> None:
    report = project.report()
    if not report.ok:
        _print_report(report)
        _fail(f"fix validation errors before {action}")


def _corpus(root: Path, name: str) -> Corpus:
    path = root / CORPORA_DIRNAME / f"{name}.yaml"
    if not path.exists():
        known = ", ".join(load_corpora(root)) or "none"
        _fail(f"no {path.relative_to(root)} (declared corpora: {known})")
    try:
        return load_corpus(path)
    except CorpusError as exc:
        _fail(str(exc))


def _outline(root: Path, corpus: Corpus):
    path = corpus.outline_path(root)
    if not path.exists():
        _fail(f"{corpus.id} has no outline yet — run `trellis ingest {corpus.id}`")
    return load_outline(path)


def cmd_validate(args, project: Project) -> int:
    report = project.report()
    _print_report(report)
    s = project.skeleton
    print(f"{s.title}: {len(s.walk())} nodes, {len(project.cards)} cards, "
          f"{len(project.readings)} readings, {len(project.drills)} drills, "
          f"{len(project.cases)} cases, "
          f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 0 if report.ok else 1


def cmd_sync(args, project: Project) -> int:
    from .digest import corpus_note
    _checked(project, "syncing")
    result = sync(project.skeleton, project.cards, project.content_dir(args.root),
                  project.readings, project.drills, project.cases,
                  project.clippings)
    print(f"{project.skeleton.domain}: updated {len(result['written'])} note(s)")
    for orphan in result["orphans"]:
        print(f"warning: orphan map note (node no longer in skeleton): {orphan}")
    # One note per corpus that lands on this domain: its outline, annotated.
    for corpus in load_corpora(args.root).values():
        if corpus.domain != project.skeleton.domain or not corpus.outline_path(args.root).exists():
            continue
        note = args.root / "vault" / "Corpora" / f"{corpus.id}.md"
        if write_managed(note, corpus_note(project, corpus, load_outline(corpus.outline_path(args.root)))):
            print(f"  corpus note: {note.relative_to(args.root)}")
    return 0


def cmd_build(args, project: Project) -> int:
    _checked(project, "building")
    cards = project.cards
    suffix = ""
    if args.corpus:
        corpus = _corpus(args.root, args.corpus)
        cards = [c for c in cards if c.source == corpus.id]
        suffix = "." + corpus.id
        if not cards:
            if getattr(args, "all", False):
                print(f"{project.skeleton.domain}: no cards from {corpus.id}")
                return 0
            _fail(f"{project.skeleton.domain}: no cards carry source: {corpus.id}")
    if not cards:
        # A skeleton with no cards yet is the normal early state of a new
        # domain, not an error: the map and its sources are authored first
        # and cards are grown branch by branch.
        if getattr(args, "all", False):
            print(f"{project.skeleton.domain}: skeleton only, no cards to build yet")
            return 0
        _fail(f"{project.skeleton.domain}: no cards to build")
    if args.lang == project.skeleton.lang:
        _fail(f"{project.skeleton.domain} is written in {args.lang} — build it "
              "without --lang; a translation is something appended to another language")
    if args.lang:
        from .cards import suspect_translations
        suspect = [c for c in cards if args.lang in suspect_translations(c)]
        if suspect and not args.force:
            for card in suspect[:5]:
                print(f"  {card.path.name}", file=sys.stderr)
            more = f" (and {len(suspect) - 5} more)" if len(suspect) > 5 else ""
            _fail(
                f"{len(suspect)} card(s){more} have a {args.lang} translation that "
                "looks rewritten rather than translated — repair them, or pass "
                "--force to ship the deck anyway"
            )
    out = args.output or args.root / "dist" / f"{project.skeleton.domain}{suffix}.apkg"
    result = build_package(
        project.skeleton, cards, out, project.readings,
        vault=args.vault_name or vault_name(args.root / "vault"),
        clippings=project.clippings,
        cases=project.cases,
        lang=args.lang,
    )
    print(f"wrote {result['path']}: {result['notes']} notes in {result['decks']} decks")
    return 0


def cmd_stats(args, project: Project) -> int:
    from .links import coverage, leaves_without_readable_source
    s = project.skeleton
    per_node = Counter(c.node for c in project.cards)
    linked_all, total_all = coverage(s, project.cards, project.readings)
    pct = f"{linked_all / total_all:.0%}" if total_all else "n/a"
    hunting = leaves_without_readable_source(s, project.readings, project.clippings)
    readable = len(s.leaves()) - len(hunting)
    print(f"{s.title} ({s.lang}) — {len(project.cards)} cards, {len(project.readings)} readings, "
          f"{len(project.drills)} drills, link coverage {pct}, "
          f"readable sources {readable}/{len(s.leaves())} leaves, "
          f"{len(project.card_errors)} unparseable")
    from .cards import suspect_translations
    flagged = Counter(lang for c in project.cards for lang in suspect_translations(c))
    for lang, n in sorted(flagged.items()):
        print(f"  warning: {n} {lang} translation(s) look rewritten rather than "
              f"translated — `build --lang {lang}` refuses until repaired")
    langs = Counter(lang for c in project.cards for lang in c.tr)
    for lang, n in sorted(langs.items()):
        print(f"  translated into {lang}: {n}/{len(project.cards)} cards "
              f"({n / len(project.cards):.0%})")
    sources = Counter(c.source for c in project.cards if c.source)
    for source, n in sources.most_common():
        print(f"  from {source}: {n} cards")
    for root_node in s.roots:
        subtree = [root_node] + [n for n in s.walk()
                                 if n.id.startswith(root_node.id + ".")]
        branch_cards = [c for c in project.cards
                        if c.node in {n.id for n in subtree}]
        leaves = [n for n in subtree if n.is_leaf]
        covered = sum(1 for n in leaves if per_node.get(n.id))
        linked, total = coverage(s, branch_cards, project.readings)
        link_pct = f"{linked / total:>4.0%}" if total else " n/a"
        print(f"  {root_node.title:<28} {total:>4} cards   "
              f"{covered:>2}/{len(leaves):<2} leaves   links {link_pct}")
    return 0


def cmd_path(args, project: Project) -> int:
    _checked(project, "generating the path")
    body = study_path(project.skeleton, project.cards, weeks=args.weeks)
    out = project.content_dir(args.root) / "Study Path.md"
    changed = write_managed(out, body)
    print(f"{'updated' if changed else 'unchanged'}: {out}")
    return 0


def cmd_scaffold(args, project: Project) -> int:
    if args.node not in project.skeleton.by_id:
        _fail(f"unknown node {args.node!r}")
    prompt = scaffold_prompt(project.skeleton, args.node, project.cards,
                             count=args.count)
    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(prompt)
    return 0


def cmd_import(args, project: Project) -> int:
    if project.card_errors:
        for e in project.card_errors:
            print(f"error: {e}", file=sys.stderr)
        _fail("fix existing card errors before importing")
    written, errors = import_cards(
        project.skeleton, project.cards, args.file,
        project.content_dir(args.root) / "cards",
    )
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        _fail("nothing imported")
    for path in written:
        print(f"wrote {path}")
    print(f"imported {len(written)} card(s); run `trellis sync` to refresh map notes")
    return 0


def cmd_clip(args, project: Project) -> int:
    """Archive readings' pages into the vault so they can be read in
    Obsidian offline. Already-clipped readings are skipped, so this is
    safe to re-run; pages the Web Clipper saved are recognised too."""
    from datetime import date

    dest = project.content_dir(args.root) / CLIPPINGS_DIRNAME
    today = date.today().isoformat()
    todo = [
        r for r in project.readings
        if r.url and canonical_url(r.url) not in project.clippings
    ]
    if args.node:
        todo = [r for r in todo if any(n.startswith(args.node) for n in r.nodes)]
    if not todo:
        print(f"{project.skeleton.domain}: every reading is already clipped")
        return 0

    clipped, failed = 0, []
    for reading in todo:
        try:
            page = fetch_page(reading.url)
        except ClipError as exc:
            failed.append((reading.path.stem, str(exc)))
            continue
        if not page.title:
            page.title = reading.title
        path = write_clipping(dest, reading.path.stem, reading.url, page, today)
        print(f"clipped {path.name}  <- {reading.url}")
        clipped += 1
    print(f"{project.skeleton.domain}: {clipped} clipped, {len(failed)} skipped")
    for slug, why in failed:
        print(f"  skipped {slug}: {why}")
    return 0


def cmd_anki_push(args, project: Project) -> int:
    """Build is a file; push is that file reaching the phone."""
    from .anki import AnkiConnectError, push

    if args.apkg:
        apkg = args.apkg
        if not Path(apkg).exists():
            _fail(f"{apkg} does not exist")
    else:
        # Build here rather than trusting dist/. Anki updates a note only
        # when the incoming one is newer, so re-importing a package built
        # before the collection last changed silently leaves those notes
        # stale — which is exactly what happens when you switch languages
        # and push again.
        _checked(project, "publishing")
        apkg = args.root / "dist" / (
            f"{project.skeleton.domain}"
            f"{'.' + args.lang if args.lang else ''}.apkg")
        result = build_package(
            project.skeleton, project.cards, apkg, project.readings,
            vault=vault_name(args.root / "vault"),
            clippings=project.clippings, cases=project.cases, lang=args.lang,
        )
        print(f"  built {result['notes']} notes in {result['decks']} decks")
    try:
        result = push(project.skeleton, Path(apkg), url=args.anki_url)
    except AnkiConnectError as exc:
        _fail(str(exc))
    for step in result["steps"]:
        print(f"  {step}")
    for name in result["deleted"]:
        print(f"  deleted stale deck: {name}")
    print(f"{project.skeleton.domain}: published")
    return 0


def cmd_anki_align(args, project: Project) -> int:
    from .anki import AnkiConnectError, align
    try:
        result = align(project.skeleton, url=args.anki_url)
    except AnkiConnectError as exc:
        _fail(str(exc))
    print(f"{project.skeleton.domain}: moved {result['moved']} card(s), "
          f"deleted {len(result['deleted'])} stale deck(s)")
    for name in result["deleted"]:
        print(f"  deleted: {name}")
    return 0


# --------------------------------------------------------------------------
# Cross-domain commands: a corpus or a codebase names its own domain.

def cmd_ingest(args) -> int:
    from .ingest import IngestError, ingest
    corpus = _corpus(args.root, args.corpus)
    try:
        result = ingest(corpus, args.root, retry=args.retry)
    except IngestError as exc:
        _fail(str(exc))
    outline = result.outline
    where = corpus.text_dir(args.root).relative_to(args.root)
    kept = "committed" if corpus.is_free else "gitignored — a book you own stays on this machine"
    print(f"{corpus.id}: {len(outline.sections)} section(s) -> {where}/ ({kept})")
    print(f"  outline: {corpus.outline_path(args.root).relative_to(args.root)}")
    for note in result.notes:
        print(f"  note: {note}")
    return 0


def cmd_seed(args) -> int:
    from .seed import seed_prompt
    corpus = _corpus(args.root, args.corpus)
    if (args.root / "skeleton" / f"{corpus.domain}.yaml").exists():
        _fail(f"skeleton/{corpus.domain}.yaml exists — triage the corpus onto it; "
              "seeding is for a subject with no skeleton yet")
    outline = _outline(args.root, corpus)
    prompt = seed_prompt(corpus, outline)
    out = args.output or args.root / "proposals" / f"{corpus.id}.seed.prompt.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prompt, encoding="utf-8")
    print(f"{corpus.id}: {len(outline.sections)} section(s) -> {out}")
    print(f"  answer with JSON, then: trellis accept proposals/{corpus.id}.seed.json")
    return 0


def cmd_triage(args) -> int:
    root = args.root
    if (root / "codebases" / f"{args.name}.yaml").exists():
        return _triage_codebase(args)
    corpus = _corpus(root, args.name)
    outline = _outline(root, corpus)
    if corpus.domain not in domains(root):
        _fail(f"no skeleton/{corpus.domain}.yaml — run `trellis seed {corpus.id}` first")
    skeleton = _load(root, corpus.domain).skeleton
    found = section_artefacts(corpus, outline, root)
    prompt = corpus_triage_prompt(corpus, outline, found, skeleton, root, prefix=args.prefix)
    out = args.output or root / "proposals" / f"{corpus.id}.prompt.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prompt, encoding="utf-8")
    print(f"{len(found)} section(s) beside {len(skeleton.leaves())} leaves -> {out}")
    return 0


def _triage_codebase(args) -> int:
    try:
        codebase = load_codebase(args.root / "codebases" / f"{args.name}.yaml")
    except CodebaseError as exc:
        _fail(str(exc))
    print(f"fetching {codebase.repo}@{codebase.ref} ...", file=sys.stderr)
    try:
        sha = fetch(codebase, args.root)
    except CodebaseError as exc:
        _fail(str(exc))
    found = artefacts(codebase, args.root)
    if args.kinds:
        wanted = set(args.kinds.split(","))
        found = [a for a in found if a.kind in wanted]
    if not found:
        _fail("no artefacts matched")
    skeletons = all_skeletons(args.root)
    if args.lens:
        skeletons = {k: v for k, v in skeletons.items() if k in args.lens.split(",")}
    prompt = triage_prompt(codebase, sha, found, skeletons, prefix=args.prefix)
    out = args.output or args.root / "proposals" / f"{codebase.name}.prompt.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prompt, encoding="utf-8")
    print(f"{len(found)} artefact(s) at {sha[:12]} -> {out}")
    return 0


def cmd_accept(args) -> int:
    """One command for every proposal shape: a seeded skeleton, a corpus's
    readings, or a codebase's cases — told apart by the keys they carry."""
    import re
    root = args.root
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "",
                 Path(args.file).read_text(encoding="utf-8"))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _fail(f"{args.file}: invalid JSON: {exc}")
    if not isinstance(data, dict):
        _fail(f"{args.file}: a proposal is a JSON object")
    if "skeleton" in data:
        from .seed import accept_seed
        if "deck" in data:
            # A skeleton drafted from an Anki deck's inventory: the deck
            # stands where a corpus would, and there is nothing to ingest.
            domain = str(data["skeleton"].get("domain", "")) if isinstance(data["skeleton"], dict) else ""
            corpus = Corpus(id=f"anki:{data['deck']}", title=str(data["deck"]),
                            license="commercial", domain=domain,
                            lang=str(data["skeleton"].get("lang", "zh")) if isinstance(data["skeleton"], dict) else "zh")
        else:
            corpus = _corpus(root, str(data.get("corpus", "")))
        path, errors, uncovered = accept_seed(args.file, root, corpus)
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        if errors:
            _fail("skeleton not written")
        print(f"wrote {path}")
        for leaf in uncovered:
            print(f"uncovered: {leaf}")
        following = (f"trellis adopt {corpus.domain} --anki \"{corpus.title}\""
                     if corpus.id.startswith("anki:") else f"trellis triage {corpus.id}")
        print(f"seeded skeleton/{corpus.domain}.yaml with {len(uncovered)} leaf/leaves the "
              f"source does not cover; next: {following}")
        return 0
    if "corpus" in data:
        corpus = _corpus(root, str(data["corpus"]))
        outline = _outline(root, corpus)
        skeleton = _load(root, corpus.domain).skeleton
        written, errors, gaps = accept_corpus(
            args.file, root, corpus, outline, skeleton, vault_note_names(root))
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        if errors:
            _fail("nothing accepted")
        for path in written:
            print(f"wrote {path.relative_to(root)}")
        for gap in gaps:
            print(f"gap: {corpus.domain} needs {gap.get('proposed_leaf')!r} "
                  f"— {gap.get('why', '')}")
        print(f"accepted {len(written)} file(s), {len(gaps)} skeleton gap(s) proposed; "
              f"next: trellis digest {corpus.id} --status")
        return 0
    skeletons = all_skeletons(root)
    written, errors, gaps = accept(args.file, root, skeletons, vault_note_names(root))
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        _fail("nothing accepted")
    for path in written:
        print(f"wrote {path}")
    for gap in gaps:
        print(f"gap: {gap.get('lens')} needs {gap.get('proposed_leaf')!r} "
              f"— {gap.get('why', '')}")
    if written:
        name = data["codebase"]
        index = root / "vault" / "Codebases" / f"{name}.md"
        index.parent.mkdir(parents=True, exist_ok=True)
        write_managed(index, codebase_index(root, name, domains(root)))
        print(f"index: {index}")
    print(f"accepted {len(written)} case(s), {len(gaps)} skeleton gap(s) proposed")
    return 0


def cmd_digest(args) -> int:
    from .digest import digest_prompt, import_digest, plan, status_lines
    root = args.root
    corpus = _corpus(root, args.corpus)
    outline = _outline(root, corpus)
    project = _load(root, corpus.domain)
    if project.card_errors:
        for e in project.card_errors:
            print(f"error: {e}", file=sys.stderr)
        _fail("fix existing card errors before digesting")
    plans = plan(project, corpus, outline)
    if not plans:
        _fail(f"{corpus.id}: no readings carry it yet — triage and accept first")
    by_leaf = {lp.leaf.id: lp for lp in plans}

    if args.import_file:
        if not args.leaf:
            _fail("--import needs --leaf <id>")
        if args.leaf not in by_leaf:
            _fail(f"{args.leaf!r} is not a leaf this corpus reaches")
        written, errors = import_digest(project, corpus, args.leaf, args.import_file,
                                        project.content_dir(root) / "cards")
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        if errors:
            _fail("nothing imported")
        for path in written:
            print(f"wrote {path.relative_to(root)}")
        print(f"{args.leaf}: {len(written)} card(s) from {corpus.id}")
        return 0

    if args.next or args.leaf:
        if args.leaf:
            lp = by_leaf.get(args.leaf)
            if lp is None:
                _fail(f"{args.leaf!r} is not a leaf this corpus reaches")
        else:
            lp = next((lp for lp in plans if not lp.done), None)
            if lp is None:
                print(f"{corpus.id}: every leaf is digested")
                return 0
        prompt = digest_prompt(project, corpus, lp, root, count=args.count, budget=args.budget)
        if args.output:
            Path(args.output).write_text(prompt, encoding="utf-8")
            print(f"{lp.leaf.id}: wrote {args.output}")
        else:
            print(prompt)
        return 0

    for line in status_lines(plans):
        print(line)
    return 0



def cmd_pull(args, project: Project) -> int:
    """Read this domain's review history out of Anki into traces/."""
    from .anki import AnkiConnectError, pull
    from .traces import save_traces, traces_path
    try:
        file = pull(project.skeleton, url=args.anki_url)
    except AnkiConnectError as exc:
        _fail(str(exc))
    path = save_traces(traces_path(args.root, project.skeleton.domain), file)
    seen = sum(1 for t in file.traces.values() if t.seen)
    print(f"{project.skeleton.title}: {len(file.traces)} card(s) traced, "
          f"{seen} reviewed → {path}")
    if file.unmapped:
        print(f"  warning: {file.unmapped} note(s) carry no id:: tag and were "
              f"skipped — run `trellis --domain {project.skeleton.domain} "
              f"anki-push` to tag them")
    return 0


def _read_loop(root: Path, names: list[str]):
    from .project import load_loop
    try:
        return load_loop(root, names)
    except SkeletonError as exc:
        _fail(str(exc))


def _assess_all(root: Path, domains: list[str]):
    """The Brief's and the Feed's view: assessments plus what hangs off
    each node to point the reader at."""
    projects, assessments, _, ages = _read_loop(root, domains)
    skeletons, drills, readings = {}, {}, {}
    for domain, project in projects.items():
        skeletons[domain] = project.skeleton
        for drill in project.drills:
            for node_id in drill.nodes:
                drills.setdefault(node_id, []).append(drill)
        for reading in project.readings:
            for node_id in reading.nodes:
                readings.setdefault(node_id, []).append(reading)
    return assessments, skeletons, drills, readings, ages


def cmd_brief(args) -> int:
    """Write the one note that says what to do next, across every domain."""
    from .brief import brief_body
    names = domains(args.root)
    if not names:
        _fail(f"no skeleton files in {args.root / 'skeleton'}")
    assessments, skeletons, drills, readings, ages = _assess_all(args.root, names)
    if not assessments:
        _fail("no domain has any cards yet — nothing to brief on")
    body = brief_body(assessments, skeletons, drills, readings, ages)
    out = args.root / "vault" / "Brief.md"
    changed = write_managed(out, body)
    print(f"{'updated' if changed else 'unchanged'}: {out}")
    if args.print:
        print()
        print(body)
    return 0


def cmd_feed(args) -> int:
    """Print the filtered-deck recipe for one interleaved cross-domain
    stream — the surface for spare minutes."""
    from .feed import plan
    assessments, _, _, _, _ = _assess_all(args.root, domains(args.root))
    feed = plan(assessments, limit=args.limit, include_sealed=args.include_sealed)
    if not feed.search:
        _fail("no domain has any cards yet")
    print("Anki → Tools → Create Filtered Deck. Paste this search, set the")
    print("card limit, choose 'Random' order, and untick 'Reschedule cards")
    print("based on my answers in this deck' only if you want a pure browse.")
    print()
    for line in feed.as_lines():
        print(line)
    return 0


def _anki_call(url: str):
    """The one AnkiConnect client the CLI hands to modules; tests replace it."""
    from functools import partial
    from .anki import invoke
    return partial(invoke, url=url)


def cmd_adopt(args) -> int:
    """Turn a correctly-shaped folder of content — or a deck that lives
    only in Anki — into a real domain."""
    from .adopt import AdoptResult, adopt_deck, derive_skeleton, find_adoptable
    if args.anki:
        if not args.name:
            _fail("adopt --anki needs the domain slug to adopt the deck as")
        from .anki import AnkiConnectError
        try:
            outcome = adopt_deck(args.root, args.name, args.anki, call=_anki_call(args.anki_url),
                                 prefix=args.prefix)
        except AnkiConnectError as exc:
            _fail(str(exc))
        if not isinstance(outcome, AdoptResult):
            print(f"no skeleton/{args.name}.yaml yet — wrote the seed prompt: "
                  f"{outcome.relative_to(args.root)}")
            print(f"answer it with JSON, then: trellis accept proposals/{args.name}.seed.json, "
                  f"then run this command again")
            return 0
        for line in outcome.unmapped:
            print(f"unmapped: {line}", file=sys.stderr)
        print(f"{args.name}: {len(outcome.written)} note(s) adopted from '{args.anki}', "
              f"{outcome.tagged} tagged in Anki, {len(outcome.unmapped)} unmapped")
        return 0 if not outcome.unmapped else 1
    found = find_adoptable(args.root)
    if args.name is None:
        if not found:
            print("nothing to adopt: every vault folder with content already "
                  "has a skeleton")
            return 0
        print("content in the vault that no skeleton claims:")
        for item in found:
            print(f"  {item.name:<20} {item.cards:>4} cards, "
                  f"{item.readings:>3} readings, {len(item.node_ids)} node id(s)"
                  f"  →  trellis adopt {item.name}")
        return 0
    match = next((f for f in found if f.name == args.name), None)
    if match is None:
        _fail(f"vault/{args.name} has no cards or readings carrying node ids "
              f"(or a skeleton for it already exists)")
    out = args.root / "skeleton" / f"{args.name}.yaml"
    if out.exists() and not args.force:
        _fail(f"{out} already exists; pass --force to overwrite")
    yaml_text = derive_skeleton(match.node_ids, args.name, match.path, args.title)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml_text, encoding="utf-8")
    print(f"wrote {out} — {len(match.node_ids)} node id(s) from "
          f"{match.cards} card(s)")
    print(f"next: trellis --domain {args.name} validate, then put the children "
          f"in study order")
    return 0


def cmd_grow(args) -> int:
    """Write where the loop says it pays: a Weakness gets cards from
    another angle, an uncovered leaf gets its first, each grounded in what
    the vault already holds for it."""
    from .grow import grow_prompt, import_grown, plan, shortlist, status_lines
    root = args.root
    names = domains(root)
    if not names:
        _fail(f"no skeleton files in {root / 'skeleton'}")
    if args.domain:
        # Grow one domain when asked: the Brief's breadth rule is for
        # deciding what to study, not for someone who has decided.
        if args.domain not in names:
            _fail(f"no skeleton/{args.domain}.yaml")
        names = [args.domain]
    projects, assessments, traces, _ = _read_loop(root, names)
    targets = plan(root, projects, assessments, traces)
    by_key = {t.key: t for t in targets}

    target = None
    if args.leaf:
        if ":" not in args.leaf:
            _fail("name the leaf as <domain>:<leaf id>, e.g. kafka:producer.acks")
        target = by_key.get(args.leaf)
        if target is None:
            _fail(f"{args.leaf} is not a leaf the loop wants written for — it is "
                  "neither weak nor uncovered (use `scaffold` or `digest` to add "
                  "cards anywhere)")
    elif args.next or args.import_file:
        if args.import_file:
            _fail("--import needs --leaf <domain>:<leaf id>")
        target = next(iter(shortlist(targets)), None)
        if target is None:
            print("nothing to grow: every reviewed leaf is holding and every leaf has cards")
            return 0

    if args.import_file:
        project = projects[target.domain]
        if project.card_errors:
            for e in project.card_errors:
                print(f"error: {e}", file=sys.stderr)
            _fail("fix existing card errors before growing")
        written, errors = import_grown(project, target, args.import_file,
                                       project.content_dir(root) / "cards")
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        if errors:
            _fail("nothing imported")
        for path in written:
            print(f"wrote {path.relative_to(root)}")
        print(f"{target.key}: {len(written)} card(s) grown"
              + (f" from {target.corpus.id}" if target.sections else ""))
        return 0

    if target is not None:
        prompt = grow_prompt(projects[target.domain], target, root,
                             count=args.count, budget=args.budget)
        if args.output:
            Path(args.output).write_text(prompt, encoding="utf-8")
            print(f"{target.key} ({target.kind}, {target.grounding}): wrote {args.output}")
        else:
            print(prompt)
        return 0

    listed = shortlist(targets)
    weak = sum(1 for t in targets if t.kind == "weakness")
    print(f"{weak} weak leaf/leaves and {len(targets) - weak} uncovered across "
          f"{len(names)} domain(s); showing {len(listed)}:")
    for line in status_lines(listed):
        print(line)
    print("next: trellis grow --next -o prompt.md, answer it, then "
          "trellis grow --import answer.json --leaf <domain>:<leaf>")
    return 0


def cmd_serve(args) -> int:
    """The Workbench: the loop as a page on this machine."""
    from .web import serve
    server = serve(args.root, port=args.port, open_browser=not args.no_open)
    port = server.server_address[1]
    print(f"Trellis 工作台 → http://127.0.0.1:{port}/   (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


CROSS_DOMAIN = {
    "ingest": cmd_ingest, "seed": cmd_seed, "triage": cmd_triage,
    "accept": cmd_accept, "digest": cmd_digest, "grow": cmd_grow,
    "brief": cmd_brief, "adopt": cmd_adopt, "feed": cmd_feed, "serve": cmd_serve,
}

HANDLERS = {
    "clip": cmd_clip,
    "anki-push": cmd_anki_push,
    "anki-align": cmd_anki_align,
    "validate": cmd_validate,
    "sync": cmd_sync,
    "build": cmd_build,
    "stats": cmd_stats,
    "path": cmd_path,
    "scaffold": cmd_scaffold,
    "import": cmd_import,
    "pull": cmd_pull,
}
SINGLE_DOMAIN_ONLY = {"scaffold", "import"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="trellis",
        description="Skeleton-constrained knowledge cards: Obsidian in, Anki out.",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="project root (default: cwd)")
    parser.add_argument("--domain", help="domain slug (default: the only skeleton)")
    parser.add_argument("--all", action="store_true",
                        help="run over every domain in skeleton/")
    sub = parser.add_subparsers(dest="command", required=True)

    # The global options are accepted on either side of the subcommand name:
    # `trellis --all anki-align` and `trellis anki-align --all` both work.
    # The error you get for a multi-domain project tells you to pass --all,
    # so where you type it must not decide whether the command runs.
    # SUPPRESS is what makes this safe: an option left off after the
    # subcommand stays unset instead of overwriting the value given before it.
    after_command = argparse.ArgumentParser(add_help=False)
    after_command.add_argument("--root", type=Path, default=argparse.SUPPRESS)
    after_command.add_argument("--domain", default=argparse.SUPPRESS)
    after_command.add_argument("--all", action="store_true",
                               default=argparse.SUPPRESS)

    def _subcommand(name: str, **kwargs) -> argparse.ArgumentParser:
        return sub.add_parser(name, parents=[after_command], **kwargs)

    _subcommand("validate", help="check skeleton, cards, readings, drills")
    _subcommand("sync", help="regenerate Obsidian map notes and corpus notes")
    p_build = _subcommand("build", help="compile vault into an Anki .apkg")
    p_build.add_argument("-o", "--output", type=Path)
    p_build.add_argument(
        "--force", action="store_true",
        help="build a language even though some translations look rewritten")
    p_build.add_argument(
        "--lang", default="",
        help="render cards in this language where a translation exists "
             "(e.g. zh); card ids are unchanged, so re-importing swaps the "
             "text in place and keeps review history",
    )
    p_build.add_argument(
        "--corpus", default="",
        help="only the cards written from this corpus — the same cards with "
             "the same identities, as dist/<domain>.<corpus>.apkg",
    )
    p_build.add_argument(
        "--vault-name",
        help="Obsidian vault name used in obsidian:// links "
             "(default: the vault directory's name)",
    )
    p_clip = _subcommand(
        "clip",
        help="archive readings' pages as markdown in the vault, so cards can "
             "open them in Obsidian instead of a browser",
    )
    p_clip.add_argument("--node", help="only readings under this node id")
    _subcommand("stats", help="card counts and leaf coverage per branch")
    p_path = _subcommand("path", help="write the linear study path into the vault")
    p_path.add_argument("--weeks", type=int)
    p_scaffold = _subcommand("scaffold", help="emit an LLM prompt for a node")
    p_scaffold.add_argument("node")
    p_scaffold.add_argument("-n", "--count", type=int, default=8)
    p_scaffold.add_argument("-o", "--output", type=Path)

    p_ingest = _subcommand(
        "ingest",
        help="turn a declared corpus (corpora/<id>.yaml: epub, pdf, markdown, "
             "or chapter URLs) into archived sections and an outline",
    )
    p_ingest.add_argument("corpus")
    p_ingest.add_argument("--retry", action="store_true",
                          help="re-attempt chapters that failed to fetch")
    p_seed = _subcommand(
        "seed",
        help="prepare a prompt that drafts a skeleton for a corpus whose "
             "subject has none yet (ADR 0006)",
    )
    p_seed.add_argument("corpus")
    p_seed.add_argument("-o", "--output", type=Path)
    p_triage = _subcommand(
        "triage",
        help="prepare a triage prompt for a declared codebase "
             "(codebases/<name>.yaml) or an ingested corpus (corpora/<id>.yaml)",
    )
    p_triage.add_argument("name")
    p_triage.add_argument("--kinds", help="codebases: only these harvest kinds, comma separated")
    p_triage.add_argument("--lens", help="codebases: only offer these lenses, comma separated")
    p_triage.add_argument("--prefix", default="", help="slug prefix for proposals")
    p_triage.add_argument("-o", "--output", type=Path)
    p_accept = _subcommand(
        "accept", help="validate a proposal (seed, corpus, or codebase) and write what it accepts")
    p_accept.add_argument("file", type=Path)
    p_digest = _subcommand(
        "digest",
        help="write cards from a corpus leaf by leaf: --status, --next (or "
             "--leaf ID) for a grounded prompt, --import FILE --leaf ID to land "
             "the answer",
    )
    p_digest.add_argument("corpus")
    p_digest.add_argument("--status", action="store_true", help="which leaves are done (default)")
    p_digest.add_argument("--next", action="store_true", help="prompt for the next undigested leaf")
    p_digest.add_argument("--leaf", help="the leaf to prompt for or import into")
    p_digest.add_argument("--import", dest="import_file", type=Path,
                          help="a JSON answer to validate and write as cards")
    p_digest.add_argument("-n", "--count", type=int, default=5, help="cards to ask for")
    p_digest.add_argument("--budget", type=int, default=24000,
                          help="max characters of source text embedded in a prompt")
    p_digest.add_argument("-o", "--output", type=Path)

    p_grow = _subcommand(
        "grow",
        help="write cards where the loop says it pays: list the weak and "
             "uncovered leaves; --next / --leaf D:ID for a prompt grounded in "
             "what slipped and what the vault holds; --import FILE --leaf D:ID "
             "to land the answer, tagged `grown`",
    )
    p_grow.add_argument("--next", action="store_true", help="prompt for the top target")
    p_grow.add_argument("--leaf", help="<domain>:<leaf id> to prompt for or import into")
    p_grow.add_argument("--import", dest="import_file", type=Path,
                        help="a JSON answer to validate and write as cards")
    p_grow.add_argument("-n", "--count", type=int, default=5, help="cards to ask for")
    p_grow.add_argument("--budget", type=int, default=24000,
                        help="max characters of source text embedded in a prompt")
    p_grow.add_argument("-o", "--output", type=Path)
    p_serve = _subcommand(
        "serve",
        help="open the Workbench: every domain's Hold, the Brief, grow with "
             "guidance answered by Claude Code, focus in Anki — a local page",
    )
    p_serve.add_argument("--port", type=int, default=8777)
    p_serve.add_argument("--no-open", action="store_true", help="do not open the browser")
    p_import = _subcommand("import", help="import LLM-generated JSON as cards")
    p_import.add_argument("file", type=Path)
    p_push = _subcommand(
        "anki-push",
        help="publish a built deck into the running Anki and out to "
             "AnkiWeb: sync, import, align to the skeleton, sync again",
    )
    p_push.add_argument("--lang", default="", help="publish this language's build")
    p_push.add_argument("--apkg", type=Path, help="override the package path")
    p_push.add_argument("--anki-url", default="http://127.0.0.1:8765")
    p_pull = _subcommand(
        "pull",
        help="read this domain's review history out of Anki into traces/ — "
             "the only command that asks Anki a question (needs desktop "
             "Anki + AnkiConnect)",
    )
    p_pull.add_argument("--anki-url", default="http://127.0.0.1:8765")
    p_brief = _subcommand(
        "brief",
        help="write vault/Brief.md: what to do next, ranked across every "
             "domain, from the Traces `pull` last brought back",
    )
    p_brief.add_argument("--print", action="store_true",
                         help="also print the Brief to stdout")
    p_feed = _subcommand(
        "feed",
        help="print the filtered-deck recipe for one interleaved stream "
             "across every domain — spare-minutes review with no deck to "
             "choose and sealed leaves held back",
    )
    p_feed.add_argument("-n", "--limit", type=int, default=40)
    p_feed.add_argument("--include-sealed", action="store_true",
                        help="do not withhold leaves whose prerequisites are "
                             "not holding")
    p_adopt = _subcommand(
        "adopt",
        help="turn a vault folder of correctly-formatted content into a real "
             "domain by deriving its skeleton from the node ids its cards "
             "carry; with no name, lists what is adoptable",
    )
    p_adopt.add_argument("name", nargs="?",
                         help="the vault/<name> folder to adopt")
    p_adopt.add_argument("--title", help="display name (default: from the name)")
    p_adopt.add_argument("--force", action="store_true",
                         help="overwrite an existing skeleton")
    p_adopt.add_argument("--anki", metavar="DECK",
                         help="adopt a deck that lives only in Anki: first a seed "
                              "prompt for its skeleton, then (once the skeleton "
                              "exists) its notes mirrored onto the leaves as "
                              "adopted cards and tagged in Anki")
    p_adopt.add_argument("--prefix", help="card id prefix for --anki (default: the slug)")
    p_adopt.add_argument("--anki-url", default="http://127.0.0.1:8765")
    p_align = _subcommand(
        "anki-align",
        help="move cards in a live Anki collection to the decks the current "
             "skeleton defines, and delete stale empty decks (run after "
             "importing the new .apkg; needs desktop Anki + AnkiConnect)",
    )
    p_align.add_argument("--anki-url", default="http://127.0.0.1:8765")

    args = parser.parse_args(argv)
    if args.all and args.command in SINGLE_DOMAIN_ONLY:
        _fail(f"{args.command} needs a single domain")
    if args.all and args.command == "build" and args.output:
        _fail("build --all uses dist/<domain>.apkg; drop -o")

    if args.command in CROSS_DOMAIN:
        return CROSS_DOMAIN[args.command](args)

    exit_code = 0
    for domain in _resolve_domains(args.root, args):
        project = _load(args.root, domain)
        exit_code = max(exit_code, HANDLERS[args.command](args, project))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
