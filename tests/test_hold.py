"""The loop: Traces in, Hold / Bearing / Sealed out."""

from __future__ import annotations

import pytest
import yaml

from trellis.brief import brief_body
from trellis.cards import Card
from trellis.feed import interleave, plan
from trellis.hold import (MATURE_DAYS, assess, bearing, card_hold,
                          confidence)
from trellis.skeleton import load_skeleton
from trellis.traces import (Trace, TraceFile, card_id_from_tags, load_traces,
                            save_traces)

SKELETON = {
    "domain": "demo",
    "title": "Demo",
    "nodes": [
        {"id": "base", "title": "Base", "children": [
            {"id": "base.one", "title": "One"},
            {"id": "base.two", "title": "Two"},
        ]},
        {"id": "mid", "title": "Mid", "children": [
            {"id": "mid.a", "title": "A", "requires": ["base.one"]},
            {"id": "mid.b", "title": "B", "requires": ["mid.a"]},
        ]},
        {"id": "top", "title": "Top", "requires": ["mid.b"]},
    ],
}


@pytest.fixture
def skeleton(tmp_path):
    path = tmp_path / "demo.yaml"
    path.write_text(yaml.safe_dump(SKELETON), encoding="utf-8")
    return load_skeleton(path)


def card(card_id: str, node: str) -> Card:
    return Card(id=card_id, node=node, type="qa", path=None)


def trace(card_id: str, **kw) -> Trace:
    return Trace(card_id=card_id, **kw)


# --- card_hold ------------------------------------------------------------

def test_an_unreviewed_card_has_no_hold_rather_than_a_hold_of_zero():
    assert card_hold(None) is None
    assert card_hold(trace("x", reps=0, interval=99)) is None


def test_hold_rises_with_the_interval_the_scheduler_trusts():
    short = card_hold(trace("x", reps=5, interval=1))
    long = card_hold(trace("x", reps=5, interval=14))
    assert short < long < 1.0


def test_a_mature_card_is_fully_held():
    assert card_hold(trace("x", reps=5, interval=MATURE_DAYS)) == pytest.approx(1.0)
    assert card_hold(trace("x", reps=5, interval=400)) == pytest.approx(1.0)


def test_relearning_halves_the_hold_whatever_the_interval_says():
    steady = card_hold(trace("x", reps=6, interval=30, type=2))
    relearning = card_hold(trace("x", reps=6, interval=30, type=3))
    assert relearning == pytest.approx(steady * 0.5)


def test_lapses_discount_the_hold_without_dominating_it():
    clean = card_hold(trace("x", reps=10, interval=30, lapses=0))
    lapsed = card_hold(trace("x", reps=10, interval=30, lapses=5))
    assert 0 < lapsed < clean
    # a card that lapsed half the time still scores above nothing, because
    # reaching a 30-day interval anyway is real evidence
    assert lapsed > 0.5 * clean


# --- bearing --------------------------------------------------------------

def test_bearing_counts_transitive_dependents(skeleton):
    bear = bearing(skeleton)
    # base.one <- mid.a <- mid.b <- top
    assert bear["base.one"] == 3
    assert bear["mid.a"] == 2
    assert bear["mid.b"] == 1
    assert bear["top"] == 0


def test_a_branch_bears_what_its_leaves_bear(skeleton):
    bear = bearing(skeleton)
    # `base` inherits base.one's dependents, minus anything in its subtree
    assert bear["base"] == 3
    assert bear["base.two"] == 0


def test_a_skeleton_with_no_requires_edges_has_no_bearing(tmp_path):
    flat = {"domain": "flat", "title": "Flat",
            "nodes": [{"id": "a", "title": "A"}, {"id": "b", "title": "B"}]}
    path = tmp_path / "flat.yaml"
    path.write_text(yaml.safe_dump(flat), encoding="utf-8")
    assert set(bearing(load_skeleton(path)).values()) == {0}


# --- assess ---------------------------------------------------------------

def test_a_leaf_with_no_cards_is_uncovered_not_weak(skeleton):
    a = assess(skeleton, [], {})
    for standing in a.leaves:
        assert standing.uncovered and not standing.weak
    assert a.hold is None
    assert [s.node.id for s in a.uncovered()][0] == "base.one"  # most bearing


def test_thin_evidence_is_unproven_rather_than_weak(skeleton):
    cards = [card("c1", "base.one"), card("c2", "base.one")]
    traces = {"c1": trace("c1", reps=4, interval=1, lapses=3)}
    a = assess(skeleton, cards, traces)
    standing = next(s for s in a.leaves if s.node.id == "base.one")
    assert standing.seen == 1
    assert standing.unproven and not standing.weak


def test_a_well_measured_failing_leaf_is_weak(skeleton):
    cards = [card(f"c{i}", "base.one") for i in range(6)]
    traces = {c.id: trace(c.id, reps=8, interval=1, lapses=4) for c in cards}
    a = assess(skeleton, cards, traces)
    standing = next(s for s in a.leaves if s.node.id == "base.one")
    assert standing.weak
    assert a.weaknesses()[0].node.id == "base.one"


def test_a_thinly_measured_leaf_is_pulled_toward_its_branch(skeleton):
    """One unlucky card must not be able to shout as loud as forty."""
    cards = [card("solid1", "base.two"), card("solid2", "base.two"),
             card("thin", "base.one")]
    traces = {
        "solid1": trace("solid1", reps=20, interval=90),
        "solid2": trace("solid2", reps=20, interval=90),
        "thin": trace("thin", reps=3, interval=1, lapses=2),
    }
    a = assess(skeleton, cards, traces)
    thin = next(s for s in a.leaves if s.node.id == "base.one")
    raw = card_hold(traces["thin"])
    assert raw < thin.hold, "shrinkage should lift a barely-measured leaf"
    assert thin.hold < a.node_hold["base"]


def test_confidence_is_smooth_and_bounded():
    assert confidence(0) == 0
    assert 0 < confidence(1) < confidence(10) < confidence(100) < 1


# --- sealing --------------------------------------------------------------

def test_a_leaf_is_sealed_when_a_prerequisite_is_not_holding(skeleton):
    cards = [card("weak", "base.one"), card("later", "mid.a")]
    traces = {"weak": trace("weak", reps=10, interval=1, lapses=6)}
    a = assess(skeleton, cards, traces)
    mid_a = next(s for s in a.leaves if s.node.id == "mid.a")
    assert mid_a.sealed and mid_a.sealed_by == ["base.one"]


def test_silence_seals_nothing(skeleton):
    """A prerequisite nobody has reviewed is not a failing grade — or a
    fresh collection would lock the whole skeleton on day one."""
    cards = [card("later", "mid.a")]
    a = assess(skeleton, cards, {})
    assert a.sealed() == []


def test_a_held_prerequisite_opens_what_stands_on_it(skeleton):
    cards = [card("strong", "base.one"), card("later", "mid.a")]
    traces = {"strong": trace("strong", reps=12, interval=60)}
    a = assess(skeleton, cards, traces)
    assert a.sealed() == []


# --- traces round trip ----------------------------------------------------

def test_traces_survive_a_save_and_load(tmp_path):
    path = tmp_path / "traces" / "demo.json"
    original = TraceFile(domain="demo", pulled_at="2026-08-30T06:00:00+00:00",
                         traces={"a": trace("a", reps=3, interval=9, lapses=1)})
    save_traces(path, original)
    back = load_traces(path)
    assert back.domain == "demo"
    assert back.traces["a"].reps == 3
    assert back.traces["a"].interval == 9


def test_a_missing_trace_file_is_absence_not_an_error(tmp_path):
    assert load_traces(tmp_path / "nope.json") is None


def test_saving_twice_produces_an_identical_file(tmp_path):
    """A pull that changed nothing must produce no diff."""
    file = TraceFile(domain="demo", pulled_at="2026-08-30T06:00:00+00:00",
                     traces={"b": trace("b", reps=1), "a": trace("a", reps=2)})
    first = tmp_path / "one.json"
    second = tmp_path / "two.json"
    save_traces(first, file)
    save_traces(second, file)
    assert first.read_text() == second.read_text()


def test_the_card_id_is_read_back_off_the_note_tag():
    assert card_id_from_tags(["demo::base::one", "id::cap-theorem"]) == "cap-theorem"
    assert card_id_from_tags(["demo::base::one"]) is None


# --- brief ----------------------------------------------------------------

def test_no_domain_may_monopolise_the_brief(skeleton):
    """Breadth is a constraint on the report, not a suggestion in it."""
    cards = [card(f"c{i}", "base.one") for i in range(20)]
    traces = {c.id: trace(c.id, reps=8, interval=1, lapses=4) for c in cards}
    a = assess(skeleton, cards, traces)
    body = brief_body({"demo": a, "other": a},
                      {"demo": skeleton, "other": skeleton})
    assert body.count("| Demo |") <= 3


def test_the_brief_opens_with_one_move(skeleton):
    a = assess(skeleton, [], {})
    body = brief_body({"demo": a}, {"demo": skeleton})
    assert body.splitlines()[2].startswith("**Open with**")


# --- feed -----------------------------------------------------------------

def test_the_feed_spans_every_domain_and_withholds_sealed_leaves(skeleton):
    cards = [card("weak", "base.one"), card("later", "mid.a")]
    traces = {"weak": trace("weak", reps=10, interval=1, lapses=6)}
    a = assess(skeleton, cards, traces)
    feed = plan({"demo": a})
    assert "tag:demo::*" in feed.search
    assert "-tag:demo::mid::a" in feed.search
    assert "-is:suspended" in feed.search


def test_including_sealed_leaves_puts_them_back(skeleton):
    cards = [card("weak", "base.one"), card("later", "mid.a")]
    traces = {"weak": trace("weak", reps=10, interval=1, lapses=6)}
    a = assess(skeleton, cards, traces)
    assert "-tag:demo::mid::a" not in plan({"demo": a}, include_sealed=True).search


def test_interleaving_never_repeats_a_subject_while_another_has_cards():
    cards = ([card(f"a{i}", "a") for i in range(3)]
             + [card(f"b{i}", "b") for i in range(3)]
             + [card("c0", "c")])
    order = [c.node for c in interleave(cards, key=lambda c: c.node)]
    # the tail may repeat once one bucket is empty, but the head must not
    assert all(x != y for x, y in zip(order[:5], order[1:6]))
    assert sorted(order) == sorted(c.node for c in cards)
