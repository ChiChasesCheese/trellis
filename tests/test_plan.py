from trellis.plan import CardInfo, Edge, card_mastery, plan, topic_weights
from trellis.traces import Trace

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
