"""A video is the resource itself: it can never be clipped, so the rules
that reward an archived copy have to know about it, or a domain learned by
watching would report every leaf as sourceless."""

from pathlib import Path

from trellis.clippings import Clipping
from trellis.links import (
    go_deeper,
    is_readable_source,
    is_video,
    leaves_without_readable_source,
    sources_for,
)
from trellis.readings import Reading
from trellis.skeleton import load_skeleton

SKELETON = """
domain: demo
title: Demo
nodes:
  - id: alpha
    title: Alpha
    children:
      - id: alpha.one
        title: One
"""


def skeleton(tmp_path):
    p = tmp_path / "demo.yaml"
    p.write_text(SKELETON, encoding="utf-8")
    return load_skeleton(p)


def reading(tmp_path, name, url, tags=()):
    return Reading(
        path=tmp_path / f"{name}.md",
        title=name.replace("-", " ").title(),
        nodes=["alpha.one"],
        url=url,
        tags=list(tags),
    )


def test_video_reading_is_readable_without_a_clipping(tmp_path):
    video = reading(tmp_path, "drill", "https://youtu.be/abc123", tags=["video"])
    article = reading(tmp_path, "essay", "https://example.com/essay")

    assert is_video(video)
    assert is_readable_source(video, {})
    # An ordinary page still has to be archived to count.
    assert not is_readable_source(article, {})


def test_video_tag_without_a_url_is_not_a_video(tmp_path):
    assert not is_video(reading(tmp_path, "drill", "", tags=["video"]))


def test_a_book_tag_still_wins_over_the_video_tag(tmp_path):
    both = reading(tmp_path, "course", "https://youtu.be/abc123",
                   tags=["video", "book"])
    assert not is_readable_source(both, {})


def test_video_leaf_counts_as_sourced(tmp_path):
    sk = skeleton(tmp_path)
    video = reading(tmp_path, "drill", "https://youtu.be/abc123", tags=["video"])
    assert leaves_without_readable_source(sk, [video], {}) == []
    assert leaves_without_readable_source(sk, [], {}) == ["alpha.one"]


def test_video_ranks_beside_a_clipped_article_not_below_it(tmp_path):
    sk = skeleton(tmp_path)
    video = reading(tmp_path, "drill", "https://youtu.be/abc123", tags=["video"])
    unclipped = reading(tmp_path, "essay", "https://example.com/essay")

    ranked = sources_for(sk, [unclipped, video], "alpha.one")
    assert ranked[0].title == "Drill"


def test_go_deeper_sends_a_video_to_the_footage_not_the_note(tmp_path):
    sk = skeleton(tmp_path)
    video = reading(tmp_path, "drill", "https://youtu.be/abc123", tags=["video"])
    clipped = reading(tmp_path, "essay", "https://example.com/essay")
    clippings = {
        "https://example.com/essay": Clipping(
            path=Path("essay-clip.md"),
            source_url="https://example.com/essay",
            title="Essay",
            prose=9999,
        )
    }

    links = {link.title: link for link in
             go_deeper(sk, [video, clipped], "alpha.one", vault="vault",
                       clippings=clippings)}

    # The video plays on tap; the archived article opens in Obsidian.
    assert links["Drill"].href == "https://youtu.be/abc123"
    assert links["Drill"].is_video
    assert links["Essay"].is_local
    assert not links["Essay"].is_video


# --- an article written in the vault is its own archive ----------------------------
#
# A reading usually points at a page somewhere else, and is only "at hand"
# once that page has been clipped. A solution article written here has no
# page to point at: the note *is* the text. It must count as a readable
# source and the card footer must open it, or the longest thing in the
# vault would be the one thing a card cannot reach.

from trellis.readings import parse_reading  # noqa: E402


def authored(tmp_path, name="solution-demo", prose=3000):
    path = tmp_path / f"{name}.md"
    path.write_text("---\nnodes: [alpha.one]\n---\n# Designing Demo\n\n" + "A real sentence of prose. " * (prose // 26),
                    encoding="utf-8")
    return parse_reading(path)


def test_a_reading_with_no_url_and_real_prose_is_authored(tmp_path):
    assert authored(tmp_path).authored
    assert not authored(tmp_path, "stub", prose=200).authored           # a stub is not an article
    assert not reading(tmp_path, "elsewhere", "https://example.org/x").authored


def test_an_authored_reading_is_a_readable_source_and_ranks_first(tmp_path):
    ours = authored(tmp_path)
    web = reading(tmp_path, "unclipped-page", "https://example.org/page")
    assert is_readable_source(ours, {})
    assert [r.title for r in sources_for(skeleton(tmp_path), [web, ours], "alpha.one")][0] == "Designing Demo"
    assert leaves_without_readable_source(skeleton(tmp_path), [ours], {}) == []


def test_the_footer_opens_an_authored_reading_in_the_vault(tmp_path):
    [link] = go_deeper(skeleton(tmp_path), [authored(tmp_path)], "alpha.one", vault="vault")
    assert link.is_local and "solution-demo" in link.href and link.web_href is None


def test_without_a_vault_an_authored_reading_has_nowhere_to_link(tmp_path):
    assert go_deeper(skeleton(tmp_path), [authored(tmp_path)], "alpha.one") == []
