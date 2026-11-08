import sys
from pathlib import Path

from trellis.plan import CardInfo, Edge, PointModel, card_mastery, plan, topic_weights
from trellis.traces import Trace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import plan_kp  # noqa: E402

DAY = 86_400_000


def test_weight_flows_from_questions_to_the_concepts_they_need():
    w = topic_weights({"q.a": 1.0, "q.b": 1.0, "c.shared": 0.0, "c.only-a": 0.0},
                      [Edge("q.a", "c.shared", 1.0), Edge("q.b", "c.shared", 1.0), Edge("q.a", "c.only-a", 1.0)], {})
    assert abs(sum(w.values()) - 1) < 1e-9
    assert w["c.shared"] > w["c.only-a"]  # two questions lean on it


def test_boost_multiplies_a_weak_spot():
    w0 = topic_weights({"a": 1.0, "b": 1.0}, [], {})
    w1 = topic_weights({"a": 1.0, "b": 1.0}, [], {"a": 2.0})
    assert w1["a"] > w0["a"]


def test_mastery_is_zero_unseen_and_decays_when_overdue():
    now = 100 * DAY
    assert card_mastery(None, now) == 0.0
    fresh = Trace("c", reps=5, interval=20, type=2, last_review=now - 10 * DAY)
    stale = Trace("c", reps=5, interval=20, type=2, last_review=now - 80 * DAY)
    assert card_mastery(fresh, now) > card_mastery(stale, now) > 0


def test_pick_keeps_leaf_order_and_puts_prerequisites_first():
    cards = [CardInfo("q2", "q.leaf", "q", 2, "必会"), CardInfo("q1", "q.leaf", "q", 1, "必会"),
             CardInfo("c1", "c.leaf", "c", 1, "必会")]
    p = plan(cards, {}, {"q": 1.0}, [Edge("q", "c", 1.0)], {}, now_ms=0, budget=3)
    assert p.picked.index("q1") < p.picked.index("q2")
    assert p.picked.index("c1") < p.picked.index("q1")


def test_studied_cards_are_not_picked_and_held_counts_them():
    cards = [CardInfo("a", "l", "t", 1, "必会"), CardInfo("b", "l", "t", 2, "必会")]
    traces = {"a": Trace("a", reps=6, interval=30, type=2, last_review=0)}
    p = plan(cards, traces, {"t": 1.0}, [], {}, now_ms=DAY, budget=5)
    assert p.picked == ["b"]
    assert 0 < p.held < 1


def test_a_second_card_on_one_exam_point_waits_behind_a_different_point():
    a = [CardInfo(f"a{i}", f"l{i}", "t", 1, "必会", graded=True, point="same") for i in range(2)]
    b = CardInfo("b", "l9", "t", 1, "必会", graded=True, point="other", freq=0.8)
    p = plan([*a, b], {}, {"t": 1.0}, [], {}, now_ms=0, budget=2)
    assert "b" in p.picked  # a second card on "same" loses to a slightly lighter card on a new point


def test_exam_point_weight_follows_role_and_question_frequency():
    pts = plan_kp.Points(
        meta={k: {"id": k, "title": k, "topic": "t", "core": False} for k in ("must", "probe", "bonus", "never")},
        card={"c1": ["must"], "c2": ["must", "probe"], "c3": ["bonus"]},
        needs={"q": [{"kp": "must", "role": "必讲"}, {"kp": "probe", "role": "追问"}, {"kp": "bonus", "role": "加分"}]},
        own={"q": []})
    w = plan_kp.weights(pts, {"q": 1.0}, {}, spread=0.7)
    assert w["must"] > w["probe"] > w["bonus"] > w["never"] > 0
    v = plan_kp.card_values(pts, w)
    assert v["c1"] > v["c3"]  # shared by two cards, "must" is still worth more per card than "bonus"
    m = plan_kp.mastery(pts, {"c1": 1.0, "c2": 0.0})
    assert abs(m["must"] - 0.5) < 1e-9


def test_coverage_is_measured_on_points_and_a_card_adds_only_what_is_not_held():
    cards = [CardInfo(c, "l", "t", i, "必会") for i, c in enumerate(("a1", "a2", "a3", "a4", "b1"))]
    model = PointModel({"big": 3.0, "small": 1.0}, {"a1": ["big"], "a2": ["big"], "a3": ["big"], "a4": ["big"], "b1": ["small"]})
    held = {c: Trace(c, reps=9, interval=30, type=2, last_review=DAY) for c in ("a1", "a2", "a3")}
    p = plan(cards, held, {"t": 1.0}, [], {}, now_ms=2 * DAY, budget=1, points=model)
    assert abs(p.held - 0.75) < 0.01  # three held cards hold "big"; a fourth unseen card does not count against it
    assert p.card_value["a4"] < p.card_value["b1"]  # another card on a held point adds less than the first on a new one


def test_oral_counts_add_weight_to_points_no_question_needs():
    pts = plan_kp.Points(meta={"a": {"topic": "t"}, "b": {"topic": "t"}}, oral={"a": 3.0})
    w = plan_kp.weights(pts, {"q": 1.0}, {}, 0.7)
    assert w["a"] > w["b"]
    assert abs(w["a"] - w["b"] - plan_kp.ORAL_SHARE) < 1e-9
