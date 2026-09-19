"""The loop, end to end: review → pull → brief → grow → push → review → pull.

Every other test holds one arc of the loop still. This one lets time pass:
the same collection is pushed to, reviewed in, and pulled from more than
once, so what is under test is whether the loop *closes* — whether the
cards it wrote come back as evidence, and whether it waits for that
evidence before writing again.

Only Anki is replaced, by `fake_anki.FakeAnki`, which opens the .apkg `build`
really produced and keeps the notes it finds the way the importer does.
Reviews are then played onto those notes by card id.
"""

from __future__ import annotations

import json

import pytest
import yaml

from fake_anki import FakeAnki
from trellis import cli
from trellis.cli import main

SKELETON = {
    "domain": "demo", "title": "Demo", "lang": "en",
    "nodes": [
        {"id": "base", "title": "Base", "order": 1, "children": [
            {"id": "base.one", "title": "One", "summary": "The first thing."},
            {"id": "base.two", "title": "Two", "summary": "The second thing."},
        ]},
    ],
}

CARD = "---\nid: {id}\nnode: {node}\ntype: qa\n---\n## Q\n{q}\n\n## A\n{a}\n"


@pytest.fixture
def anki(monkeypatch):
    fake = FakeAnki()
    monkeypatch.setattr(cli, "_anki_call", lambda url: fake)
    return fake


@pytest.fixture
def root(tmp_path):
    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "demo.yaml").write_text(yaml.safe_dump(SKELETON), encoding="utf-8")
    for leaf in ("one", "two"):
        for i in range(3):
            path = tmp_path / "vault" / "demo" / "cards" / "base" / f"{leaf}-{i}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(CARD.format(id=f"{leaf}-{i}", node=f"base.{leaf}",
                                        q=f"Question {leaf}-{i}?", a=f"Answer {leaf}-{i}."),
                            encoding="utf-8")
    return tmp_path


def run(root, *argv):
    return main(["--root", str(root), *argv])


def out_of(capsys, root, *argv) -> str:
    capsys.readouterr()
    assert run(root, *argv) == 0
    return capsys.readouterr().out


GROWN = [
    {"id": f"one-angle-{i}", "type": "qa",
     "q": f"A scenario that reaches One from another side, number {i}?",
     "a": f"The mechanism of One, seen from side {i}."}
    for i in range(3)
]


def study_until_one_is_a_weakness(root, anki, capsys):
    """Push the deck, review it badly on One and well on Two, pull."""
    assert run(root, "anki-push") == 0
    for i in range(3):
        anki.review(f"one-{i}", reps=6, lapses=4, interval=1)
        anki.review(f"two-{i}", reps=4, lapses=0, interval=30)
    assert run(root, "pull") == 0


def grow_one_and_push(root, anki, capsys):
    prompt = root / "prompt.md"
    assert "demo:base.one (weakness" in out_of(capsys, root, "grow", "--next", "-o", str(prompt))
    assert "one-0" in prompt.read_text(encoding="utf-8")      # aimed at what slipped
    answer = root / "answer.json"
    answer.write_text(json.dumps(GROWN), encoding="utf-8")
    assert run(root, "grow", "--import", str(answer), "--leaf", "demo:base.one") == 0
    assert run(root, "anki-push") == 0
    assert anki.tagged("grown") == ["one-angle-0", "one-angle-1", "one-angle-2"]


def test_the_loop_waits_for_its_own_cards_before_writing_again(root, anki, capsys):
    study_until_one_is_a_weakness(root, anki, capsys)
    assert "**先做** [[base.one|One]]" in out_of(capsys, root, "brief", "--print")

    grow_one_and_push(root, anki, capsys)

    # Nothing has been reviewed since. One is exactly as weak as it was —
    # and the loop must not answer the same evidence with more cards.
    assert run(root, "pull") == 0
    listing = out_of(capsys, root, "grow")
    assert "demo:base.one" not in listing
    assert "1 weak leaf is waiting on grown cards" in listing
    assert "nothing to grow" in out_of(capsys, root, "grow", "--next")

    brief = out_of(capsys, root, "brief", "--print")
    assert "**先复习** [[base.one|One]]" in brief
    assert "3 张新卡" in brief and "tag:demo::base::one tag:grown" in brief
    assert "trellis grow --leaf demo:base.one" not in brief


def test_grown_cards_that_take_are_reported_and_the_leaf_recovers(root, anki, capsys):
    study_until_one_is_a_weakness(root, anki, capsys)
    grow_one_and_push(root, anki, capsys)
    for i in range(3):
        anki.review(f"one-angle-{i}", reps=4, lapses=0, interval=12)
        anki.review(f"one-{i}", reps=9, lapses=4, interval=9)   # the second route helped the first
    assert run(root, "pull") == 0

    brief = out_of(capsys, root, "brief", "--print")
    assert "长住了" in brief and "[[base.one|One]]" in brief
    assert "**先做** [[base.one|One]]" not in brief
    assert "demo:base.one" not in out_of(capsys, root, "grow")


def test_grown_cards_that_slip_put_the_leaf_back_with_a_different_move(root, anki, capsys):
    study_until_one_is_a_weakness(root, anki, capsys)
    grow_one_and_push(root, anki, capsys)
    for i in range(3):
        anki.review(f"one-angle-{i}", reps=5, lapses=2, interval=1, type=3)
    assert run(root, "pull") == 0

    brief = out_of(capsys, root, "brief", "--print")
    assert "没长住" in brief and "[[base.one|One]]" in brief
    # The leaf is a target again, and the prompt now shows the grown cards
    # that failed too: the third route must differ from the first two.
    prompt = root / "again.md"
    assert "demo:base.one (weakness" in out_of(capsys, root, "grow", "--next", "-o", str(prompt))
    assert "one-angle-" in prompt.read_text(encoding="utf-8")
