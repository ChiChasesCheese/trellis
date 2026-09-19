"""Graft: what reviewing the grown cards has shown.

`grow` writes cards where the loop pointed and tags them. A Graft is the
loop reading that tag back: have the new cards been seen, and did they
take? Derived from the tag and the Traces each time, recorded nowhere.
"""

from __future__ import annotations

import pytest
import yaml

from trellis.cards import Card
from trellis.hold import assess
from trellis.skeleton import load_skeleton
from trellis.traces import TYPE_RELEARNING, Trace

SKELETON = {
    "domain": "demo", "title": "Demo",
    "nodes": [{"id": "base", "title": "Base", "children": [
        {"id": "base.one", "title": "One"},
        {"id": "base.two", "title": "Two"},
    ]}],
}


@pytest.fixture
def skeleton(tmp_path):
    path = tmp_path / "demo.yaml"
    path.write_text(yaml.safe_dump(SKELETON), encoding="utf-8")
    return load_skeleton(path)


def card(card_id: str, node: str = "base.one", grown: bool = False) -> Card:
    return Card(id=card_id, node=node, type="qa", path=None, tags=["grown"] if grown else [])


# base.one as the loop first found it: three cards, all lapsing.
FIRST_ROUTE = [card(f"one-{i}") for i in range(3)]
FAILING = {f"one-{i}": Trace(f"one-{i}", reps=6, lapses=4, interval=1) for i in range(3)}
SECOND_ROUTE = [card(f"angle-{i}", grown=True) for i in range(3)]


def standing(skeleton, cards, traces, leaf="base.one"):
    return next(s for s in assess(skeleton, cards, traces).leaves if s.node.id == leaf)


def test_a_leaf_nothing_was_grown_on_has_no_graft(skeleton):
    assert standing(skeleton, FIRST_ROUTE, FAILING).graft is None


def test_a_graft_is_settling_until_its_cards_have_been_seen(skeleton):
    s = standing(skeleton, FIRST_ROUTE + SECOND_ROUTE, FAILING)
    assert (s.graft.grown, s.graft.unseen) == (3, 3)
    assert s.graft.state == "settling"
    assert s.weak and s.settling        # still weak — and the loop is waiting on it


def test_a_grown_card_seen_once_is_young_and_young_is_not_a_verdict(skeleton):
    # Answered correctly yesterday: the interval is a day because the card
    # is new, not because it failed. Calling that "slipped" would have the
    # loop writing a third route before the second was a week old.
    seen_once = {f"angle-{i}": Trace(f"angle-{i}", reps=1, interval=1) for i in range(3)}
    s = standing(skeleton, FIRST_ROUTE + SECOND_ROUTE, FAILING | seen_once)
    assert (s.graft.young, s.graft.taken, s.graft.slipped) == (3, 0, 0)
    assert s.graft.state == "settling" and s.settling


def test_a_graft_took_when_most_of_its_cards_hold(skeleton):
    grown = {"angle-0": Trace("angle-0", reps=4, interval=12),
             "angle-1": Trace("angle-1", reps=4, interval=9),
             "angle-2": Trace("angle-2", reps=5, lapses=2, interval=1, type=TYPE_RELEARNING)}
    s = standing(skeleton, FIRST_ROUTE + SECOND_ROUTE, FAILING | grown)
    assert (s.graft.taken, s.graft.slipped) == (2, 1)
    assert s.graft.state == "took" and not s.settling


def test_a_graft_slipped_when_its_cards_fail_like_the_first_ones_did(skeleton):
    grown = {f"angle-{i}": Trace(f"angle-{i}", reps=5, lapses=2, interval=1, type=TYPE_RELEARNING)
             for i in range(3)}
    s = standing(skeleton, FIRST_ROUTE + SECOND_ROUTE, FAILING | grown)
    assert s.graft.state == "slipped"
    assert s.weak and not s.settling    # a Weakness again, open to another route


def test_a_small_graft_is_judged_on_all_of_its_cards(skeleton):
    # Two grown cards can never show three verdicts; both holding is enough.
    grown = {f"angle-{i}": Trace(f"angle-{i}", reps=4, interval=12) for i in range(2)}
    s = standing(skeleton, FIRST_ROUTE + SECOND_ROUTE[:2], FAILING | grown)
    assert s.graft.state == "took"


def test_first_cards_on_an_uncovered_leaf_are_a_graft_but_not_a_second_route(skeleton):
    s = standing(skeleton, [card(f"two-{i}", "base.two", grown=True) for i in range(3)], {},
                 leaf="base.two")
    assert s.graft.first_cards and s.graft.state == "settling"
    assert not s.settling               # unproven, not weak: nothing is being waited out


# --- the Brief says what happened to what it asked for -----------------------

from trellis.brief import brief_body  # noqa: E402


def brief(skeleton, cards, traces) -> str:
    return brief_body({"demo": assess(skeleton, cards, traces)}, {"demo": skeleton})


def test_the_brief_opens_with_reviewing_the_new_cards_not_with_writing_more(skeleton):
    text = brief(skeleton, FIRST_ROUTE + SECOND_ROUTE, FAILING)
    opening = text.split("\n\n")[1]
    assert opening.startswith("**先复习** [[base.one|One]]")
    assert "3 张新卡" in opening and "`tag:demo::base::one tag:grown`" in opening
    assert "trellis grow --leaf demo:base.one" not in text
    assert "## 新卡" in text and "还在长" in text


def test_the_brief_says_a_graft_took(skeleton):
    grown = {f"angle-{i}": Trace(f"angle-{i}", reps=4, interval=12) for i in range(3)}
    text = brief(skeleton, FIRST_ROUTE + SECOND_ROUTE, FAILING | grown)
    assert "长住了：[[base.one|One]]" in text


def test_the_brief_says_a_graft_slipped_and_points_somewhere_other_than_more_cards(skeleton):
    grown = {f"angle-{i}": Trace(f"angle-{i}", reps=5, lapses=2, interval=1, type=TYPE_RELEARNING)
             for i in range(3)}
    text = brief(skeleton, FIRST_ROUTE + SECOND_ROUTE, FAILING | grown)
    line = next(l for l in text.splitlines() if "没长住" in l)
    assert "[[base.one|One]]" in line and "3 张新卡里 3 张又滑了" in line
    assert text.split("\n\n")[1].startswith("**先做** [[base.one|One]]")


def test_first_cards_are_not_reported_as_a_second_route(skeleton):
    firsts = [card(f"two-{i}", "base.two", grown=True) for i in range(3)]
    took = {f"two-{i}": Trace(f"two-{i}", reps=4, interval=12) for i in range(3)}
    assert "## 新卡" not in brief(skeleton, firsts, took)
