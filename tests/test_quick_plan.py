import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import quick_plan as qp  # noqa: E402

CFG = dict(qp.DEFAULTS, per_day=100)
HOUR, DAY = 3600_000, 86400_000
T0 = 1_800_000_000_000


def seen(kp, ease, topic="t.a", fmt="qa", at=T0, secs=8.0, later=()):
    sights = [qp.Sight(at, ease, secs)] + [qp.Sight(at + gap, e, secs) for gap, e in later]
    return qp.Card(kp, fmt, topic, 0.001, new=False, sights=sights)


def unseen(kp, topic="t.a", fmt="qa", weight=0.001):
    return qp.Card(kp, fmt, topic, weight)


def test_a_slow_right_answer_scores_less_than_a_quick_one():
    cards = [seen(f"k{i}", 3) for i in range(9)] + [seen("slow", 3, secs=45.0)]
    s = qp.first_scores(cards)
    assert s["k0"] == 0.8 and s["slow"] < 0.8


def test_a_miss_fades_with_later_right_answers_and_with_time():
    fresh = seen("a", 1)
    assert qp.open_miss(fresh, T0) == 1.0
    assert qp.open_miss(seen("a", 1, later=[(2 * HOUR, 3)]), T0 + 2 * HOUR) < 0.55
    assert qp.open_miss(seen("a", 1, later=[(60_000, 3)]), T0 + 60_000) > 0.99  # a minute later is not memory
    assert 0.45 < qp.open_miss(fresh, T0 + 4 * DAY) < 0.55
    assert qp.open_miss(seen("a", 2), T0) == 0.5
    assert qp.open_miss(seen("a", 3, later=[(3 * HOUR, 1)]), T0 + 3 * HOUR) == 1.0  # forgotten later counts in full
    assert qp.open_miss(seen("a", 4), T0) == 0.0


def test_one_answer_moves_a_topic_a_little_and_many_move_it_a_lot():
    base = [seen(f"g{i}", 3, topic="t.other") for i in range(20)]
    one = base + [seen("m1", 1, topic="t.weak")]
    many = base + [seen(f"m{i}", 1, topic="t.weak") for i in range(10)]
    target = [unseen("x", topic="t.weak")]
    p_one, _ = qp.predict(one + target, {}, qp.first_scores(one))
    p_many, _ = qp.predict(many + target, {}, qp.first_scores(many))
    p_none, _ = qp.predict(base + target, {}, qp.first_scores(base))
    assert p_none["x"] > p_one["x"] > p_many["x"]
    assert p_none["x"] - p_one["x"] < 0.25 and p_none["x"] - p_many["x"] > 0.35


def test_a_miss_brings_its_prerequisite_and_its_topic_forward_and_holds_what_builds_on_it():
    cards = [seen("missed", 1, topic="t.a"), unseen("pre", topic="t.b"), unseen("same", topic="t.a"), unseen("after", topic="t.c"),
             unseen("far", topic="t.d")]
    prereq = {"missed": ["pre"], "after": ["missed"]}
    pr, parts = qp.priorities(cards, prereq, T0, CFG)
    why = parts["why"]
    assert why["pre"]["related"] > why["same"]["related"] > why["far"]["related"] == 1.0
    assert why["after"]["hold"] < 1.0 == why["far"]["hold"]
    assert pr["pre"] > pr["far"] > pr["after"]


def test_too_easy_brings_harder_cards_forward_and_too_hard_brings_easier_ones():
    easy_run = [seen(f"e{i}", 4, topic=f"t.{i}") for i in range(20)]
    hard_run = [seen(f"h{i}", 1 if i % 2 else 2, topic=f"t.{i}") for i in range(20)]
    recall, recognise = unseen("recall", topic="t.x", fmt="qa"), unseen("recognise", topic="t.y", fmt="mc")
    _, parts = qp.priorities(easy_run + [recall, recognise], {}, T0, CFG)
    assert parts["tilt"] > 0 and parts["why"]["recall"]["fit"] > 1.0 > parts["why"]["recognise"]["fit"]
    _, parts = qp.priorities(hard_run + [recall, recognise], {}, T0, CFG)
    assert parts["tilt"] < 0 and parts["why"]["recall"]["fit"] < 1.0 < parts["why"]["recognise"]["fit"]


def test_the_dial_waits_for_a_real_sample():
    _, parts = qp.priorities([seen(f"e{i}", 4) for i in range(5)] + [unseen("x")], {}, T0, CFG)
    assert parts["tilt"] == 0.0 and parts["recent"] is None


def test_order_puts_prerequisites_first_and_breaks_runs_of_one_topic():
    cards = [unseen("heavy", topic="t.a", weight=0.01), unseen("pre", topic="t.b", weight=0.0001)]
    cards += [unseen(f"a{i}", topic="t.a", weight=0.005) for i in range(6)] + [unseen(f"z{i}", topic=f"t.z{i}", weight=0.0002) for i in range(8)]
    pr = {c.kp: c.weight for c in cards}
    seq = [c.kp for c in qp.order(cards, pr, {"heavy": ["pre"]}, CFG)]
    assert seq[:2] == ["pre", "heavy"]
    assert len(seq) == len(cards) == len(set(seq))
    for i in range(len(seq) - CFG["window"]):
        window = seq[i:i + CFG["window"] + 1]
        if i + CFG["window"] + 1 <= 12:  # while other topics are left to choose from
            assert sum(k == "heavy" or k.startswith("a") for k in window) <= CFG["per_window"] + 1


def test_order_survives_a_prerequisite_cycle():
    cards = [unseen("a"), unseen("b")]
    assert len(qp.order(cards, {"a": 1.0, "b": 0.5}, {"a": ["b"], "b": ["a"]}, CFG)) == 2


def day(new, score=0.8, later=0, later_ok=0, secs_each=10.0, answers=None):
    answers = answers or new * 3
    return {"new": new, "score": score, "later": later, "later_ok": later_ok, "answers": answers, "secs": answers * secs_each}


def test_quota_grows_after_a_finished_day():
    n, why = qp.quota({"d1": day(100)}, {"d1": 100}, 100, due_soon=50, unseen=500, cfg=CFG)
    assert n == 115 and "加量" in why


def test_quota_shrinks_when_cards_seen_again_are_forgotten():
    n, why = qp.quota({"d1": day(100, later=40, later_ok=24)}, {"d1": 100}, 100, due_soon=50, unseen=500, cfg=CFG)
    assert n == 80 and "减量" in why


def test_quota_follows_two_unfinished_days_but_not_one():
    n, _ = qp.quota({"d1": day(100), "d2": day(40)}, {"d1": 100, "d2": 100}, 100, 50, 500, CFG)
    assert n == 100
    n, why = qp.quota({"d1": day(50), "d2": day(40)}, {"d1": 100, "d2": 100}, 100, 50, 500, CFG)
    assert n == 75 and "靠拢" in why


def test_quota_keeps_inside_the_time_budget_and_the_bounds():
    n, why = qp.quota({"d1": day(100, secs_each=30.0)}, {"d1": 100}, 100, due_soon=60, unseen=500, cfg=CFG)
    assert n < 100 and "时间预算" in why  # 90 minutes: 60 due at 30 s, a new card three answers of 30 s
    n, _ = qp.quota({"d1": day(100, secs_each=200.0)}, {"d1": 100}, 100, 60, 500, CFG)
    assert n == CFG["min_new"]
    n, _ = qp.quota({"d1": day(200, secs_each=5.0)}, {"d1": 200}, 200, 0, 500, CFG)
    assert n == CFG["max_new"]
    n, _ = qp.quota({"d1": day(100)}, {"d1": 100}, 100, 0, 12, CFG)
    assert n == 12
    n, why = qp.quota({}, {}, 100, 0, 500, CFG)
    assert n == 100 and "不变" in why


def test_history_splits_days_at_the_rollover_hour():
    from datetime import datetime
    late = int(datetime(2026, 11, 11, 2, 0).timestamp() * 1000)
    noon = int(datetime(2026, 11, 11, 12, 0).timestamp() * 1000)
    days = qp.history([seen("a", 3, at=late), seen("b", 1, at=noon, later=[(2 * HOUR, 3)])], 4)
    assert list(days) == ["2026-11-10", "2026-11-11"]
    assert days["2026-11-10"]["new"] == 1 and days["2026-11-11"]["later"] == 1 and days["2026-11-11"]["later_ok"] == 1


def test_full_cards_pick_the_card_that_teaches_the_missed_point_first():
    card_points = {"c1": ["k.other", "k.missed"], "c2": ["k.missed"], "c3": ["k.missed"], "c4": ["k.second"]}
    got = qp.full_cards(["k.missed", "k.second", "k.none"], card_points, {"c1": 1, "c2": 9, "c3": 4, "c4": 2}, 10)
    assert got == ["c3", "c4"]
    assert qp.full_cards(["k.missed", "k.second"], card_points, {"c1": 1, "c4": 2}, 1) == ["c1"]


def test_only_the_cut_and_the_cards_already_seen_stay_in_the_deck():
    cut, rest, done, stray = unseen("cut"), unseen("rest"), seen("done", 3), seen("stray", 1)
    for c, cid, deck in ((cut, 1, "Q::wait"), (rest, 2, "Q"), (done, 3, "Q"), (stray, 4, "Q::wait")):
        c.cid, c.deck = cid, deck
    assert qp.moves([cut, rest, done, stray], {"cut"}, "Q", "Q::wait") == {"Q": [1, 4], "Q::wait": [2]}
    for c, deck in ((cut, "Q"), (rest, "Q::wait"), (stray, "Q")):
        c.deck = deck
    assert qp.moves([cut, rest, done, stray], {"cut"}, "Q", "Q::wait") == {}
