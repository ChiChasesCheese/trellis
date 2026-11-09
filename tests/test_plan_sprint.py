import sys
from datetime import date
from pathlib import Path

from trellis.plan import HELD_CARDS, CardInfo, PointModel, coverage_order

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import plan_sprint  # noqa: E402

CFG = {"start": "2026-11-09", "days": 7, "new_per_day": 80, "review_budget": 120, "lc_new": 0}


def test_day_of_marks_before_during_and_after():
    assert plan_sprint.day_of(CFG, date(2026, 11, 8)) == 0
    assert plan_sprint.day_of(CFG, date(2026, 11, 9)) == 1
    assert plan_sprint.day_of(CFG, date(2026, 11, 15)) == 7
    assert plan_sprint.day_of(CFG, date(2026, 11, 16)) == -1
    assert plan_sprint.day_of(None, date(2026, 11, 9)) == -1


def test_budgets_apply_only_while_the_sprint_runs():
    before = {"sprint": CFG, "daily_new": 35, "lc_new": 6}
    assert plan_sprint.apply(before, date(2026, 11, 8)) == 0 and before["daily_new"] == 35
    during = {"sprint": CFG, "daily_new": 35, "lc_new": 6}
    assert plan_sprint.apply(during, date(2026, 11, 10)) == 2
    assert (during["daily_new"], during["lc_new"]) == (80, 6)  # each subject keeps its own budget during the sprint
    after = {"sprint": CFG, "daily_new": 35, "lc_new": 6}
    assert plan_sprint.apply(after, date(2026, 11, 16)) == -1 and after["daily_new"] == 35


def test_todays_deal_starts_with_what_is_left_of_earlier_days():
    sprint = {"plan": [{"cards": ["a", "b"]}, {"cards": ["c", "d"]}]}
    assert plan_sprint.deal_today(sprint, {"a", "c"}, 2) == ["b", "d"]


def test_age_hold_grows_with_age_and_stays_below_one():
    holds = [plan_sprint.age_hold(a) for a in range(0, 40)]
    assert all(x <= y for x, y in zip(holds, holds[1:]))
    assert 0 < holds[0] < holds[-1] <= 1


def test_layout_puts_prerequisite_topics_first_and_fills_each_day():
    cards = {f"{t}{i}": CardInfo(f"{t}{i}", t, t, i) for t in "ab" for i in range(2)}
    days = plan_sprint.layout(list(cards), cards, {"a": ["b"]}, {i: 1.0 for i in cards}, [2, 2])
    assert days == [["b0", "b1"], ["a0", "a1"]]


def test_coverage_order_stops_paying_for_a_point_that_is_full():
    n = HELD_CARDS + 3
    cards = [CardInfo(f"a{i}", "a", "a", i) for i in range(n)] + [CardInfo("b0", "b", "b", 0)]
    model = PointModel({"pa": 1.0, "pb": 0.1}, {**{f"a{i}": ["pa"] for i in range(n)}, "b0": ["pb"]})
    order, gain = coverage_order(cards, {}, model, n + 1)
    assert order[:HELD_CARDS] == [f"a{i}" for i in range(HELD_CARDS)]  # the heavy point first, in teaching order
    assert order[HELD_CARDS] == "b0"  # then the light point, not a fourth card on a full one
    assert gain["b0"] > 0
    assert len(order) == HELD_CARDS + 1  # nothing left that adds coverage


def test_coverage_order_prefers_a_short_card_and_leaves_very_long_ones():
    model = PointModel({"a": 1.0, "b": 1.0, "c": 1.0}, {"long": ["a"], "short": ["b"], "huge": ["c"]})
    cards = [CardInfo("long", "l1", "t", 1, length=1600), CardInfo("short", "l2", "t", 1, length=200), CardInfo("huge", "l3", "t", 1, length=4000)]
    order, _ = coverage_order(cards, {}, model, 3)
    assert order == ["short", "long"]


def test_every_domain_gets_a_share_of_the_day():
    from trellis.plan import coverage_by_domain
    model = PointModel({"big": 100.0, "b2": 90.0, "b3": 80.0, "b4": 70.0, "s1": 1.0, "s2": 1.0},
                       {"a": ["big"], "b": ["b2"], "c": ["b3"], "d": ["b4"], "x": ["s1"], "y": ["s2"]})
    cards = [CardInfo(i, "l" + i, "big" if i in "abcd" else "small", 1) for i in ("a", "b", "c", "d", "x", "y")]
    order, _ = coverage_by_domain(cards, {}, model, 4, lambda c: c.topic)
    assert len(order) == 4 and {"x", "y"} & set(order)  # the small domain is not crowded out
