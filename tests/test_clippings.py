from pathlib import Path

from trellis.clippings import (
    FetchedPage,
    canonical_url,
    load_clippings,
    write_clipping,
)
from trellis.links import go_deeper
from trellis.obsidian import open_uri, vault_name
from trellis.readings import parse_reading
from trellis.skeleton import load_skeleton

SKELETON = """
domain: demo
title: Demo
nodes:
  - id: alpha
    order: 1
    title: Alpha
    children:
      - id: alpha.one
        title: One
"""

READING = """---
nodes: [alpha]
url: https://Example.com/Guide/
---
# The Alpha Guide
"""

# What Obsidian's Web Clipper writes: `source` is the identity we match on.
WEB_CLIPPER_NOTE = """---
title: "The Alpha Guide"
source: "https://example.com/Guide"
author: "Someone"
---
Clipped body.
"""


def _project(tmp_path):
    (tmp_path / "s.yaml").write_text(SKELETON, encoding="utf-8")
    (tmp_path / "the-alpha-guide.md").write_text(READING, encoding="utf-8")
    clips = tmp_path / "clippings"
    clips.mkdir()
    return (
        load_skeleton(tmp_path / "s.yaml"),
        [parse_reading(tmp_path / "the-alpha-guide.md")],
        clips,
    )


def test_canonical_url_ignores_cosmetic_differences():
    assert canonical_url("https://www.Example.com/Guide/") == canonical_url(
        "http://example.com/Guide"
    )
    assert canonical_url("https://x.com/a#frag") == canonical_url("https://x.com/a")
    assert canonical_url("https://x.com/a?p=1") != canonical_url("https://x.com/a")


def test_web_clipper_notes_are_indexed_by_source(tmp_path):
    _, _, clips = _project(tmp_path)
    (clips / "alpha-guide.md").write_text(WEB_CLIPPER_NOTE, encoding="utf-8")
    (clips / "just-a-note.md").write_text("---\ntags: [x]\n---\nnot a clip\n",
                                          encoding="utf-8")
    index = load_clippings(clips)
    assert list(index) == [canonical_url("https://example.com/Guide")]
    # host case and trailing slash are noise; path case is not (paths are
    # case-sensitive on the web, so we must not fold it away)
    assert index[canonical_url("https://WWW.example.com/Guide/")].title == "The Alpha Guide"
    assert canonical_url("https://example.com/guide") not in index


def test_go_deeper_targets_the_reading_note_by_name(tmp_path):
    """Cards link to the reading note by bare name: it is committed (so it
    exists on every device) and a name resolves whatever the vault root is."""
    skeleton, readings, _ = _project(tmp_path)

    links = go_deeper(skeleton, readings, "alpha.one", "myvault")
    assert links[0].is_local
    assert links[0].href == open_uri("myvault", "the-alpha-guide")
    assert links[0].web_href == "https://Example.com/Guide/"  # original kept

    # without a vault there is nothing local to point at
    assert go_deeper(skeleton, readings, "alpha.one")[0].href.startswith("https://")


def test_pdf_clipping_is_embedded_not_converted(tmp_path):
    page = FetchedPage(title="Raft", pdf=b"%PDF-1.4 fake")
    path = write_clipping(tmp_path, "raft-paper", "https://x.com/raft.pdf", page,
                          "2026-08-15")
    assert (tmp_path / "raft-paper-clip.pdf").read_bytes() == b"%PDF-1.4 fake"
    assert "![[raft-paper-clip.pdf]]" in path.read_text(encoding="utf-8")
    # and it is still indexable as a clipping
    assert canonical_url("https://x.com/raft.pdf") in load_clippings(tmp_path)


def test_open_uri_escapes_paths():
    uri = open_uri("my vault", "a b/c d.md")
    assert uri == "obsidian://open?vault=my%20vault&file=a%20b%2Fc%20d"


def test_vault_name_is_the_directory_name(tmp_path):
    assert vault_name(tmp_path / "vault") == "vault"


def test_navigation_only_pages_score_as_no_prose():
    """The guard that stops a page of pure chrome (a video page, a docs
    shell) from being saved as if it were an article."""
    from trellis.clippings import _prose_length

    nav = "\n".join(f"[Link {i}](https://example.com/{i})" for i in range(40))
    assert _prose_length(nav) < 100
    assert _prose_length("Real prose. " * 60) > 400


def test_built_card_carries_the_obsidian_link_and_a_web_fallback(tmp_path):
    """End to end: what a reviewer actually taps in Anki."""
    import sqlite3
    import zipfile

    from trellis.build import build_package
    from trellis.cards import parse_card

    skeleton, readings, clips = _project(tmp_path)
    write_clipping(clips, "the-alpha-guide", "https://example.com/Guide",
                   FetchedPage(title="The Alpha Guide", markdown="body"), "2026-08-15")
    card_file = tmp_path / "alpha-c.md"
    card_file.write_text(
        "---\nid: alpha-c\nnode: alpha.one\ntype: qa\n---\n## Q\nq?\n\n## A\na.\n",
        encoding="utf-8",
    )

    out = tmp_path / "out.apkg"
    build_package(skeleton, [parse_card(card_file)], out, readings, vault="vault")

    with zipfile.ZipFile(out) as z:
        (tmp_path / "c.db").write_bytes(z.read("collection.anki2"))
    flds = sqlite3.connect(tmp_path / "c.db").execute(
        "select flds from notes").fetchone()[0]
    assert 'href="obsidian://open?vault=vault&file=the-alpha-guide"' in flds
    assert 'href="https://Example.com/Guide/" class="web"' in flds


def test_a_book_pointer_does_not_count_as_a_readable_source(tmp_path):
    """The guard behind 'go deeper' actually going somewhere useful: a
    book's homepage is a pointer, not something you can read now."""
    from trellis.clippings import MIN_PROSE
    from trellis.links import is_readable_source, leaves_without_readable_source

    skeleton, readings, clips = _project(tmp_path)
    (tmp_path / "the-book.md").write_text(
        "---\nnodes: [alpha.one]\nurl: https://example.com/book\ntags: [book]\n---\n# A Book\n",
        encoding="utf-8",
    )
    book = parse_reading(tmp_path / "the-book.md")

    # even fully archived, a `book` reading stays a pointer
    write_clipping(clips, "the-book", "https://example.com/book",
                   FetchedPage(title="A Book", markdown="prose. " * MIN_PROSE),
                   "2026-08-15")
    index = load_clippings(clips)
    assert not is_readable_source(book, index)
    assert leaves_without_readable_source(skeleton, [book], index) == ["alpha.one"]

    # a plain article of real length does count
    write_clipping(clips, "the-alpha-guide", "https://example.com/Guide",
                   FetchedPage(title="The Alpha Guide", markdown="prose. " * MIN_PROSE),
                   "2026-08-15")
    index = load_clippings(clips)
    assert is_readable_source(readings[0], index)
    assert leaves_without_readable_source(skeleton, readings, index) == []


def test_a_reading_marked_no_archive_is_linked_but_never_copied_into_the_vault(tmp_path, monkeypatch, capsys):
    """The repository is public. A page we may link to is not thereby a page
    we may republish, and the tag lets a reading say so."""
    import yaml
    from trellis import cli
    from trellis.clippings import FetchedPage as Page

    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "demo.yaml").write_text(yaml.safe_dump({
        "domain": "demo", "title": "Demo",
        "nodes": [{"id": "alpha", "title": "Alpha", "children": [{"id": "alpha.one", "title": "One"}]}],
    }), encoding="utf-8")
    readings = tmp_path / "vault" / "demo" / "readings"
    readings.mkdir(parents=True)
    (readings / "open-post.md").write_text(
        "---\nnodes: [alpha.one]\nurl: https://example.org/open\n---\n# Open post\nWhy read.\n", encoding="utf-8")
    (readings / "paid-course.md").write_text(
        "---\nnodes: [alpha.one]\nurl: https://example.com/course\ntags: [no-archive]\n---\n# Paid course\nWhy read.\n",
        encoding="utf-8")
    fetched = []
    monkeypatch.setattr(cli, "fetch_page", lambda url: fetched.append(url) or Page(
        title="Open post", markdown="Real prose. " * 400))
    assert cli.main(["--root", str(tmp_path), "clip"]) == 0
    assert fetched == ["https://example.org/open"]
    assert "1 kept as a link only (no-archive)" in capsys.readouterr().out
