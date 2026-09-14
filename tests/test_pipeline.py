"""End-to-end tests over a tiny fixture project, plus a guard that the
real repo content always validates and builds."""

import json
import sqlite3
import zipfile
from pathlib import Path

import pytest

from trellis.build import build_package
from trellis.cards import load_cards
from trellis.clippings import CLIP_SUFFIX, CLIPPINGS_DIRNAME
from trellis.readings import load_readings
from trellis.scaffold import import_cards, scaffold_prompt
from trellis.skeleton import load_skeleton
from trellis.sync import BEGIN, END, sync
from trellis.validate import validate

REPO = Path(__file__).resolve().parent.parent

SKELETON = """
domain: demo
title: Demo
nodes:
  - id: beta
    title: Beta
  - id: alpha
    title: Alpha
    children:
      - id: alpha.one
        title: One
        summary: First topic.
      - id: alpha.two
        title: Two
        requires: [beta]
"""

CARD = """---
id: alpha-sample
node: alpha.one
type: qa
---
## Q
What is X?

## A
`X` is **Y**.
"""


@pytest.fixture
def project(tmp_path):
    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "demo.yaml").write_text(SKELETON, encoding="utf-8")
    cards_dir = tmp_path / "vault" / "demo" / "cards" / "alpha"
    cards_dir.mkdir(parents=True)
    (cards_dir / "alpha-sample.md").write_text(CARD, encoding="utf-8")
    return tmp_path


def load(project):
    skeleton = load_skeleton(project / "skeleton" / "demo.yaml")
    cards, errors = load_cards(project / "vault" / "demo" / "cards")
    return skeleton, cards, errors


def test_validate_flags_unknown_node_and_filename_mismatch(project):
    skeleton, cards, errors = load(project)
    assert validate(skeleton, cards, errors).ok
    bad = project / "vault" / "demo" / "cards" / "alpha" / "wrong-name.md"
    bad.write_text(CARD.replace("alpha-sample", "other-id")
                       .replace("alpha.one", "ghost.node"), encoding="utf-8")
    report = validate(*load(project))
    assert any("not in skeleton" in e for e in report.errors)
    assert any("filename must equal card id" in e for e in report.errors)


def test_sync_is_idempotent_and_preserves_user_text(project):
    skeleton, cards, _ = load(project)
    vault = project / "vault" / "demo"
    first = sync(skeleton, cards, vault)
    assert (vault / "Demo MOC.md").exists()
    node_note = vault / "map" / "alpha.one.md"
    body = node_note.read_text(encoding="utf-8")
    assert BEGIN in body and END in body and "First topic." in body
    assert "[[alpha-sample]]" in body

    node_note.write_text(body + "\nmy own notes\n", encoding="utf-8")
    second = sync(skeleton, cards, vault)
    assert second["written"] == []  # nothing changed -> nothing rewritten
    assert "my own notes" in node_note.read_text(encoding="utf-8")


def test_build_produces_apkg_with_stable_guid(project):
    skeleton, cards, _ = load(project)
    out = project / "dist" / "demo.apkg"
    result = build_package(skeleton, cards, out)
    assert result["notes"] == 1
    with zipfile.ZipFile(out) as z, open(project / "c.db", "wb") as f:
        f.write(z.read("collection.anki2"))
    db = sqlite3.connect(project / "c.db")
    guids = [r[0] for r in db.execute("select guid from notes")]
    decks = json.loads(db.execute("select decks from col").fetchone()[0])
    names = {d["name"] for d in decks.values()}
    assert len(guids) == 1
    assert "Demo::02 Alpha::One" in names
    # rebuild -> same guid (safe re-import)
    build_package(skeleton, cards, out)
    with zipfile.ZipFile(out) as z, open(project / "c2.db", "wb") as f:
        f.write(z.read("collection.anki2"))
    guids2 = [r[0] for r in sqlite3.connect(project / "c2.db").execute("select guid from notes")]
    assert guids == guids2


def test_sources_footer_and_link_coverage(project):
    from trellis.links import coverage, sources_for
    from trellis.readings import load_readings as load_r

    readings_dir = project / "vault" / "demo" / "readings"
    readings_dir.mkdir(parents=True)
    (readings_dir / "alpha-guide.md").write_text(
        "---\nnodes: [alpha]\nurl: https://example.com/guide\n---\n# The Alpha Guide\n",
        encoding="utf-8",
    )
    skeleton, cards, _ = load(project)
    readings, _ = load_r(readings_dir)

    # reading attached to the parent branch covers the child's card
    srcs = sources_for(skeleton, readings, "alpha.one")
    assert [r.title for r in srcs] == ["The Alpha Guide"]
    assert coverage(skeleton, cards, readings) == (1, 1)
    assert coverage(skeleton, cards, []) == (0, 1)

    # and the built card carries a clickable footer link
    import sqlite3
    import zipfile
    out = project / "dist" / "demo.apkg"
    build_package(skeleton, cards, out, readings)
    with zipfile.ZipFile(out) as z, open(project / "f.db", "wb") as f:
        f.write(z.read("collection.anki2"))
    flds = sqlite3.connect(project / "f.db").execute("select flds from notes").fetchone()[0]
    assert '<a href="https://example.com/guide">The Alpha Guide</a>' in flds


def test_scaffold_prompt_carries_context(project):
    skeleton, cards, _ = load(project)
    prompt = scaffold_prompt(skeleton, "alpha.two", cards)
    assert "Beta" in prompt            # prerequisite surfaced
    assert "One" in prompt             # sibling marked out of scope
    assert '"node": "alpha.two"' in prompt


def test_import_is_all_or_nothing(project):
    skeleton, cards, _ = load(project)
    cards_dir = project / "vault" / "demo" / "cards"
    good = {"id": "alpha-new", "node": "alpha.two", "type": "qa", "q": "Q?", "a": "A."}
    bad = {"id": "alpha-sample", "node": "alpha.two", "type": "qa", "q": "Q?", "a": "A."}

    batch = project / "batch.json"
    batch.write_text(json.dumps([good, bad]), encoding="utf-8")
    written, errors = import_cards(skeleton, cards, batch, cards_dir)
    assert written == [] and any("already exists" in e for e in errors)
    assert not (cards_dir / "alpha" / "alpha-new.md").exists()

    batch.write_text("```json\n" + json.dumps([good]) + "\n```", encoding="utf-8")
    written, errors = import_cards(skeleton, cards, batch, cards_dir)
    assert errors == [] and len(written) == 1
    reloaded, parse_errors = load_cards(cards_dir)
    assert parse_errors == []
    assert {c.id for c in reloaded} == {"alpha-sample", "alpha-new"}


DRILL = """---
nodes: [alpha.one, beta]
---
# Drill: build the thing
Constraints... [[alpha-sample]]
"""


def test_drills_and_path(project):
    drills_dir = project / "vault" / "demo" / "drills"
    drills_dir.mkdir(parents=True)
    (drills_dir / "build-the-thing.md").write_text(DRILL, encoding="utf-8")

    from trellis.cli import main
    root = ["--root", str(project)]
    assert main(root + ["validate"]) == 0
    assert main(root + ["sync"]) == 0
    node_note = (project / "vault" / "demo" / "map" / "alpha.one.md").read_text(encoding="utf-8")
    assert "## Drills" in node_note and "[[build-the-thing|Drill: build the thing]]" in node_note

    assert main(root + ["path", "--weeks", "2"]) == 0
    path_note = (project / "vault" / "demo" / "Study Path.md").read_text(encoding="utf-8")
    assert "Week 1" in path_note and "[[alpha.one|One]]" in path_note
    assert "needs: Beta" in path_note

    # bad drill node -> validate fails
    (drills_dir / "bad.md").write_text(DRILL.replace("beta]", "ghost]"), encoding="utf-8")
    assert main(root + ["validate"]) == 1


def test_all_flag_iterates_domains(project):
    second = (project / "skeleton" / "other.yaml")
    second.write_text(SKELETON.replace("demo", "other"), encoding="utf-8")
    from trellis.cli import main
    root = ["--root", str(project)]
    assert main(root + ["--all", "validate"]) == 0
    # without --domain/--all, two domains must be an explicit error
    import pytest as _pytest
    with _pytest.raises(SystemExit):
        main(root + ["validate"])


def test_real_repo_content_validates_and_builds(tmp_path):
    skeleton = load_skeleton(REPO / "skeleton" / "system-design.yaml")
    content = REPO / "vault" / skeleton.folder
    cards, errors = load_cards(content / "cards")
    readings, reading_errors = load_readings(content / "readings")
    report = validate(skeleton, cards, errors, readings, reading_errors)
    assert report.errors == []
    assert len(cards) >= 50
    assert len(readings) >= 5
    result = build_package(skeleton, cards, tmp_path / "out.apkg")
    assert result["notes"] == len(cards)


def test_real_repo_wikilinks_resolve():
    """Every [[wikilink]] in any domain's cards, readings, and drills must
    point at an existing card, reading, drill, or map note. Targets are
    pooled across domains because vault/ is one Obsidian vault."""
    import re
    from trellis.drills import load_drills
    targets: set[str] = set()
    for skel_file in (REPO / "skeleton").glob("*.yaml"):
        skeleton = load_skeleton(skel_file)
        targets |= {n.id for n in skeleton.walk()}
        vault = REPO / "vault" / skeleton.domain
        from trellis.cases import load_cases
        for loader, sub in ((load_cards, "cards"), (load_readings, "readings"),
                            (load_drills, "drills"), (load_cases, "cases")):
            if (vault / sub).exists():
                items, _ = loader(vault / sub)
                targets |= {getattr(i, "id", None) or i.link_target for i in items}
    link_re = re.compile(r"\[\[([^\]|#]+)")
    # Only the content the tool owns is checked: a domain's cards, readings,
    # drills and cases. Map notes, corpus notes and the study path are
    # generated; clippings are other people's pages; and a domain folder
    # may also hold plain notes (handouts, problem archives) whose `[[…]]`
    # is code, not a link.
    content_dirs = [
        REPO / "vault" / load_skeleton(f).domain / sub
        for f in (REPO / "skeleton").glob("*.yaml")
        for sub in ("cards", "readings", "drills", "cases")
    ]
    for path in (p for d in content_dirs if d.exists() for p in d.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        # an adopted card mirrors another tool's note: its text is theirs,
        # and `[[0]*n` in a code block is a list, not a link
        if "\nanki: " in text.split("---", 2)[1] if text.startswith("---") else False:
            continue
        for target in link_re.findall(text):
            target = target.strip()
            # embeds of clipped articles are expected to be missing here:
            # clippings are gitignored, so a clean checkout has none
            if target.endswith(CLIP_SUFFIX) or target.endswith(CLIP_SUFFIX + ".pdf"):
                continue
            assert target in targets, f"{path}: dangling link [[{target}]]"


def test_every_deck_link_resolves_to_exactly_one_note(tmp_path):
    """The property that makes card links work on both a phone (whose vault
    root is the repo) and a laptop (whose vault root is vault/): each link
    names a note, and that name is unique across the whole vault."""
    import re
    from collections import Counter
    from urllib.parse import unquote

    from trellis.clippings import load_clippings
    from trellis.drills import load_drills
    from trellis.obsidian import vault_name

    vault_root = REPO / "vault"
    names = Counter(p.stem for p in vault_root.rglob("*.md"))
    for skel_file in (REPO / "skeleton").glob("*.yaml"):
        skeleton = load_skeleton(skel_file)
        content = vault_root / skeleton.domain
        cards, _ = load_cards(content / "cards")
        readings, _ = load_readings(content / "readings")
        result = build_package(
            skeleton, cards, tmp_path / f"{skeleton.domain}.apkg", readings,
            vault=vault_name(vault_root),
        )
        # adopted cards mirror notes another tool owns and are never built
        assert result["notes"] == sum(1 for c in cards if not c.adopted)

        with zipfile.ZipFile(tmp_path / f"{skeleton.domain}.apkg") as z:
            (tmp_path / "c.db").write_bytes(z.read("collection.anki2"))
        for (flds,) in sqlite3.connect(tmp_path / "c.db").execute("select flds from notes"):
            for match in re.finditer(r"obsidian://open\?vault=[^&]+&file=([^\"]+)", flds):
                target = unquote(match.group(1))
                assert names[target] == 1, f"{target!r} resolves to {names[target]} notes"


def test_build_all_skips_a_skeleton_only_domain(project):
    """A new domain starts as a map with no cards — the normal early state
    of authoring a skeleton first, and not something CI should fail on."""
    from trellis.cli import main

    (project / "skeleton" / "fresh.yaml").write_text(
        "domain: fresh\ntitle: Fresh\nnodes:\n  - id: alpha\n    title: Alpha\n",
        encoding="utf-8",
    )
    assert main(["--root", str(project), "--all", "build"]) == 0
    assert (project / "dist" / "demo.apkg").exists()
    assert not (project / "dist" / "fresh.apkg").exists()
