"""Sequence: the one order in which a domain's new cards are introduced.

Two decisions make it. Which leaves come first — the Core, the few the rest
of the subject stands on, then everything else, each pass in the skeleton's
own order. And which card comes first inside a leaf — the `step` its author
gave it. Both are read from the vault and computed; Anki is only told.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from trellis.cards import Card
from trellis.sequence import core_leaves, sequence
from trellis.skeleton import SkeletonError, load_skeleton

SKELETON = {
    "domain": "demo", "title": "Demo",
    "nodes": [
        {"id": "intro", "title": "Intro", "children": [
            {"id": "intro.history", "title": "History"},
            {"id": "intro.model", "title": "Model"},
        ]},
        {"id": "storage", "title": "Storage", "children": [
            {"id": "storage.log", "title": "Log", "requires": ["intro.model"]},
            {"id": "storage.index", "title": "Index", "core": True},
            {"id": "storage.trivia", "title": "Trivia"},
        ]},
        {"id": "apps", "title": "Apps", "children": [
            {"id": "apps.queue", "title": "Queue", "requires": ["storage.log"]},
        ]},
    ],
}


def load(tmp_path, data=SKELETON):
    path = tmp_path / "demo.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return load_skeleton(path)


def card(card_id: str, node: str, step: int | None = None, grown: bool = False) -> Card:
    return Card(id=card_id, node=node, type="qa", path=Path(f"{card_id}.md"),
                step=step, tags=["grown"] if grown else [])


def test_the_core_is_what_was_declared_plus_what_the_graph_shows_is_stood_on(tmp_path):
    # storage.index is declared; intro.model and storage.log are stood on
    # (apps.queue → storage.log → intro.model); nothing else is core.
    assert core_leaves(load(tmp_path)) == {"intro.model", "storage.log", "storage.index"}


def test_core_leaves_come_first_and_each_pass_keeps_the_skeletons_order(tmp_path):
    cards = [card(f"c-{leaf.id}", leaf.id) for leaf in load(tmp_path).leaves()]
    order = [c.node for c in sequence(load(tmp_path), cards)]
    assert order == ["intro.model", "storage.log", "storage.index",       # the Core
                     "intro.history", "storage.trivia", "apps.queue"]      # then the rest


def test_inside_a_leaf_the_step_decides_then_unstepped_cards_then_grown_ones(tmp_path):
    cards = [card("z-grown", "intro.model", grown=True), card("b-unstepped", "intro.model"),
             card("a-unstepped", "intro.model"), card("y-second", "intro.model", step=2),
             card("z-first", "intro.model", step=1), card("a-grown-stepped", "intro.model", step=3, grown=True)]
    assert [c.id for c in sequence(load(tmp_path), cards)] == [
        "z-first", "y-second", "a-grown-stepped", "a-unstepped", "b-unstepped", "z-grown"]


def test_the_plain_skeleton_order_is_still_there_to_ask_for(tmp_path):
    cards = [card(f"c-{leaf.id}", leaf.id) for leaf in load(tmp_path).leaves()]
    assert [c.node for c in sequence(load(tmp_path), cards, order="skeleton")] == [
        leaf.id for leaf in load(tmp_path).leaves()]


def test_declaring_a_branch_core_covers_its_leaves_and_requiring_a_branch_pulls_them_in(tmp_path):
    data = {"domain": "demo", "title": "Demo", "nodes": [
        {"id": "a", "title": "A", "children": [{"id": "a.one", "title": "1"}, {"id": "a.two", "title": "2"}]},
        {"id": "b", "title": "B", "core": True, "requires": ["a"],
         "children": [{"id": "b.one", "title": "1"}]},
        {"id": "c", "title": "C", "children": [{"id": "c.one", "title": "1"}]},
    ]}
    assert core_leaves(load(tmp_path, data)) == {"a.one", "a.two", "b.one"}


def test_adopted_cards_are_not_sequenced(tmp_path):
    mine, theirs = card("mine", "intro.model"), card("theirs", "intro.model")
    theirs.anki = 12345
    assert [c.id for c in sequence(load(tmp_path), [mine, theirs])] == ["mine"]


def test_core_must_be_a_boolean(tmp_path):
    data = {"domain": "demo", "title": "Demo",
            "nodes": [{"id": "a", "title": "A", "core": "yes"}]}
    with pytest.raises(SkeletonError, match="core must be true or false"):
        load(tmp_path, data)


# --- `step` in a card file ----------------------------------------------------

from trellis.cards import CardError, load_cards, parse_card  # noqa: E402

FILE = "---\nid: {id}\nnode: intro.model\n{extra}---\n## Q\nWhat?\n\n## A\nThat.\n"


def write(tmp_path, card_id, extra=""):
    path = tmp_path / f"{card_id}.md"
    path.write_text(FILE.format(id=card_id, extra=extra), encoding="utf-8")
    return path


def test_a_card_file_can_say_which_step_it_is(tmp_path):
    assert parse_card(write(tmp_path, "first", "step: 1\n")).step == 1
    assert parse_card(write(tmp_path, "unsaid")).step is None


@pytest.mark.parametrize("bad", ["0", "-2", "first", "1.5", "true"])
def test_a_step_is_a_positive_whole_number(tmp_path, bad):
    with pytest.raises(CardError, match="step must be a positive whole number"):
        parse_card(write(tmp_path, "bad", f"step: {bad}\n"))


def test_two_cards_on_one_leaf_cannot_claim_the_same_step(tmp_path):
    write(tmp_path, "one", "step: 1\n")
    write(tmp_path, "also-one", "step: 1\n")
    cards, errors = load_cards(tmp_path)
    assert len(cards) == 2
    assert any("step 1" in e and "intro.model" in e and "also-one" in e and "one" in e for e in errors)


# --- the package carries the Sequence -------------------------------------------

import sqlite3  # noqa: E402
import zipfile  # noqa: E402

from trellis.build import build_package  # noqa: E402


def positions(apkg) -> list[tuple[int, str, bool]]:
    """(position, card id, tagged core) for every card in a built package."""
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", apkg.parent)
    db = sqlite3.connect(apkg.parent / "collection.anki2")
    rows = db.execute("select c.due, n.tags from cards c join notes n on n.id = c.nid").fetchall()
    db.close()
    out = []
    for due, tags in rows:
        card_id = next(t for t in tags.split() if t.startswith("id::")).removeprefix("id::")
        out.append((due, card_id, "trellis::core" in tags.split()))
    return sorted(out)


def test_a_built_package_numbers_its_cards_in_sequence_and_tags_the_core(tmp_path):
    skeleton = load(tmp_path)
    cards = [parse_card(write(tmp_path, cid, extra).rename(tmp_path / f"{cid}.md"))
             for cid, extra in [("model-b", "step: 2\n"), ("model-a", "step: 1\n")]]
    trivia = write(tmp_path, "aaa-trivia")
    trivia.write_text(trivia.read_text().replace("intro.model", "storage.trivia"), encoding="utf-8")
    cards.append(parse_card(trivia))
    build_package(skeleton, cards, tmp_path / "demo.apkg")
    assert positions(tmp_path / "demo.apkg") == [
        (1, "model-a", True), (2, "model-b", True), (3, "aaa-trivia", False)]


# --- `study:` in a skeleton ------------------------------------------------------

def with_study(study):
    return {**SKELETON, "study": study}


def test_a_skeleton_with_no_study_block_asks_for_nothing_but_the_default_order(tmp_path):
    study = load(tmp_path).study
    assert study.order == "core-first" and not study.sets_pace


def test_a_skeleton_can_set_its_pace(tmp_path):
    study = load(tmp_path, with_study({"order": "skeleton", "mix": "new-first",
                                       "new_per_day": 20, "reviews_per_day": 20})).study
    assert (study.order, study.mix, study.new_per_day, study.reviews_per_day) == \
        ("skeleton", "new-first", 20, 20)
    assert study.sets_pace


@pytest.mark.parametrize("study, complaint", [
    ({"order": "random"}, "study.order must be one of"),
    ({"mix": "fifty-fifty"}, "study.mix must be one of"),
    ({"new_per_day": -1}, "study.new_per_day must be a whole number, 0 or more"),
    ({"reviews_per_day": "many"}, "study.reviews_per_day must be a whole number, 0 or more"),
    ({"ratio": 0.5}, "study: unknown keys"),
    ("fast", "study must be a mapping"),
])
def test_a_study_block_is_checked(tmp_path, study, complaint):
    with pytest.raises(SkeletonError, match=complaint):
        load(tmp_path, with_study(study))
