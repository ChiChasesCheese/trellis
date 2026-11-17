"""活动推荐规则的测试：每条产品规则至少一个用例，再加一个端到端的完整例子。

日期都是 2026 年 11 月，周几由 `datetime.weekday()` 算出（见 test_calendar_used_by_the_tests）：
11-02 周一、11-05 周四、11-07 周六、11-08 周日、11-09 周一、11-14 周六、11-15 周日。
"""

import importlib
import itertools
import math
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

Coordinates, Customer, Event = impl.Coordinates, impl.Customer, impl.Event
Inventory, Listing, Campaign = impl.Inventory, impl.Listing, impl.Campaign
LocationService, RecommendationContext = impl.LocationService, impl.RecommendationContext

CITIES = {
    "seattle": Coordinates(47.6062, -122.3321),
    "bellevue": Coordinates(47.6101, -122.2015),
    "redmond": Coordinates(47.6740, -122.1215),
    "tacoma": Coordinates(47.2529, -122.4443),
    "olympia": Coordinates(47.0379, -122.9007),
    "portland": Coordinates(45.5152, -122.6784),
    "spokane": Coordinates(47.6588, -117.4260),
}
# 西雅图—贝尔维尤、贝尔维尤—雷德蒙德相邻；故意把一对写成反方向。"springfield" 没有坐标，但有邻居
LOCATIONS = LocationService(
    CITIES,
    [("seattle", "bellevue"), ("redmond", "bellevue"), ("springfield", "shelbyville")],
)
PAT = Customer("pat", home_city="seattle")  # 住西雅图，没分享位置
SAM = Customer("sam", location=CITIES["spokane"])  # 只有精确位置（在斯波坎）
KIM = Customer("kim", home_city="seattle", location=CITIES["spokane"])  # 住西雅图，此刻人在斯波坎
NOBODY = Customer("nobody")
FAR_HOME = Customer("far", home_city="atlantis")  # 家所在的城市位置服务不认识


def at(day, hour=0, minute=0, second=0, microsecond=0, month=11, year=2026):
    return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=UTC)


NOW = at(5, 9)  # 周四 09:00


def show(event_id, city, starts_at):
    return Event(event_id, f"show {event_id}", city, starts_at)


def context(customer, now=NOW, listings=()):
    return RecommendationContext(customer, now, LOCATIONS, Inventory(listings))


def with_tickets(events, price_cents=3000, quantity=5):
    return Inventory(Listing(item.id, price_cents, quantity) for item in events)


def recommender(events, inventory=None):
    return impl.Recommender(events, inventory or with_tickets(events), LOCATIONS)


# ---------- 端到端的例子 ----------


def test_calendar_used_by_the_tests():
    names = {day: at(day).strftime("%a") for day in (2, 5, 7, 8, 9, 14, 15)}
    assert names == {2: "Mon", 5: "Thu", 7: "Sat", 8: "Sun", 9: "Mon", 14: "Sat", 15: "Sun"}


def test_worked_example_from_the_article():
    places = LocationService(
        {"seattle": CITIES["seattle"], "bellevue": CITIES["bellevue"]}, [("seattle", "bellevue")]
    )
    events = [Event("c1", "Harbor Lights Concert", "bellevue", at(8, 20))]
    rec = impl.Recommender(events, Inventory([Listing("c1", 4200, 8)]), places)
    close = impl.any_of(impl.within_miles(25), impl.in_metro_area())
    weekend = Campaign(
        "weekend-picks",
        [impl.all_of(impl.this_weekend(), close), impl.all_of(impl.within_days(14), close)],
        3,
    )
    assert rec.recommend(PAT, weekend, NOW) == ["c1"]


# ---------- 位置规则 ----------


def test_shared_location_beats_home_city():
    spokane_show = show("b", "spokane", at(12, 19))
    philly_show = show("p", "seattle", at(12, 19))
    rule = impl.within_miles(10)
    assert rule.matches(spokane_show, context(KIM)) is True  # 人在斯波坎，用精确位置
    assert rule.matches(philly_show, context(KIM)) is False  # 不再按家所在城市算
    assert rule.matches(philly_show, context(PAT)) is True  # 没分享位置才用家


def test_origin_falls_back_to_home_city_only_when_service_knows_it():
    nearby = show("t", "tacoma", at(12, 19))
    rule = impl.within_miles(60)
    assert rule.matches(nearby, context(PAT)) is True  # 西雅图到塔科马约 25 英里
    assert rule.matches(nearby, context(FAR_HOME)) is False  # 家的城市没有坐标：没有出发点
    assert rule.matches(nearby, context(NOBODY)) is False


def test_missing_coordinates_never_match_and_never_raise():
    unknown_city = show("u", "atlantis", at(12, 19))
    for customer in (PAT, SAM, KIM, NOBODY, FAR_HOME):
        assert impl.within_miles(10_000).matches(unknown_city, context(customer)) is False
    home_show = show("h", "seattle", at(12, 19))
    assert impl.within_miles(0).matches(home_show, context(NOBODY)) is False  # 缺信息不等于距离 0


def test_within_miles_boundary_is_inclusive():
    target = show("t", "tacoma", at(12, 19))
    exact = LOCATIONS.distance_miles(CITIES["seattle"], CITIES["tacoma"])
    assert 24 < exact < 25
    assert impl.within_miles(exact).matches(target, context(PAT)) is True
    assert impl.within_miles(math.nextafter(exact, 0)).matches(target, context(PAT)) is False


def test_metro_area_is_home_plus_direct_neighbours_only():
    rule = impl.in_metro_area()
    cases = {"seattle": True, "bellevue": True, "redmond": False, "spokane": False, "atlantis": False}
    for city, expected in cases.items():
        assert rule.matches(show("x", city, at(12, 19)), context(PAT)) is expected, city


def test_metro_area_adjacency_works_both_ways_and_needs_no_coordinates():
    rule = impl.in_metro_area()
    bellevue_home = Customer("c", home_city="bellevue")
    assert rule.matches(show("x", "seattle", at(12, 19)), context(bellevue_home)) is True
    assert rule.matches(show("y", "redmond", at(12, 19)), context(bellevue_home)) is True
    springfield = Customer("s", home_city="springfield")  # 位置服务不认识它的坐标，邻接关系仍然有效
    assert rule.matches(show("z", "shelbyville", at(12, 19)), context(springfield)) is True
    assert rule.matches(show("w", "springfield", at(12, 19)), context(springfield)) is True


def test_metro_area_ignores_shared_location_and_needs_a_home_city():
    rule = impl.in_metro_area()
    assert rule.matches(show("b", "spokane", at(12, 19)), context(SAM)) is False
    assert rule.matches(show("p", "seattle", at(12, 19)), context(NOBODY)) is False


# ---------- 时间规则 ----------


def test_within_days_window_is_closed_on_both_ends():
    rule = impl.within_days(3)
    end = NOW + timedelta(hours=72)
    assert rule.matches(show("a", "spokane", NOW), context(PAT)) is True
    assert rule.matches(show("b", "spokane", end), context(PAT)) is True
    assert rule.matches(show("c", "spokane", end + timedelta(microseconds=1)), context(PAT)) is False
    assert rule.matches(show("d", "spokane", NOW - timedelta(microseconds=1)), context(PAT)) is False
    assert rule.matches(show("e", "spokane", NOW - timedelta(days=1)), context(PAT)) is False  # 过去的不算


def test_within_zero_days_means_exactly_now():
    assert impl.within_days(0).matches(show("a", "spokane", NOW), context(PAT)) is True
    assert impl.within_days(0).matches(show("b", "spokane", NOW + timedelta(seconds=1)), context(PAT)) is False


@pytest.mark.parametrize("day", [2, 3, 4, 5, 6])  # 周一到周五：看的是即将到来的周末
def test_weekdays_look_ahead_to_the_coming_weekend(day):
    rule = impl.this_weekend()
    now = at(day, 9)
    expected = [
        (at(6, 23, 59, 59), False),  # 周五最后一秒
        (at(7), True),  # 周六 00:00（含）
        (at(7, 20), True),
        (at(8, 19), True),  # 周日傍晚
        (at(8, 23, 59, 59), True),  # 周日最后一秒
        (at(9), False),  # 下周一 00:00（不含）
        (at(14, 12), False),  # 再下一个周末不算
    ]
    for starts_at, matches in expected:
        assert rule.matches(show("x", "spokane", starts_at), context(PAT, now)) is matches, (day, starts_at)


def test_saturday_is_the_weekend_in_progress():
    rule = impl.this_weekend()
    now = at(7, 12)
    assert rule.matches(show("a", "spokane", at(7, 11, 59)), context(PAT, now)) is False  # 已经开始
    assert rule.matches(show("b", "spokane", at(7, 12)), context(PAT, now)) is True  # 恰好此刻
    assert rule.matches(show("c", "spokane", at(8, 23, 59, 59)), context(PAT, now)) is True
    assert rule.matches(show("d", "spokane", at(9)), context(PAT, now)) is False
    assert rule.matches(show("e", "spokane", at(14, 12)), context(PAT, now)) is False


def test_sunday_is_still_the_same_weekend_not_the_next_one():
    rule = impl.this_weekend()
    now = at(8, 20)
    assert rule.matches(show("a", "spokane", at(8, 19)), context(PAT, now)) is False
    assert rule.matches(show("b", "spokane", at(8, 21)), context(PAT, now)) is True
    assert rule.matches(show("c", "spokane", at(14, 20)), context(PAT, now)) is False  # 下周六不是"这个周末"


def test_monday_midnight_moves_to_the_next_weekend():
    rule = impl.this_weekend()
    assert rule.matches(show("a", "spokane", at(8, 20)), context(PAT, at(9))) is False
    assert rule.matches(show("b", "spokane", at(14, 20)), context(PAT, at(9))) is True
    assert rule.matches(show("c", "spokane", at(14, 20)), context(PAT, at(8, 23, 59, 59))) is False


def test_weekend_window_across_month_and_year_boundaries():
    rule = impl.this_weekend()
    friday = datetime(2026, 10, 30, 18, tzinfo=UTC)  # 周五；周六是 10-31，周一是 11-02
    assert rule.matches(show("a", "spokane", at(1, 23)), context(PAT, friday)) is True
    assert rule.matches(show("b", "spokane", at(2)), context(PAT, friday)) is False
    new_year = datetime(2026, 12, 30, 9, tzinfo=UTC)  # 周三；周六是 2027-01-02
    jan_2 = datetime(2027, 1, 2, 20, tzinfo=UTC)
    jan_3 = datetime(2027, 1, 3, 20, tzinfo=UTC)
    assert rule.matches(show("c", "spokane", jan_2), context(PAT, new_year)) is True
    assert rule.matches(show("d", "spokane", jan_3), context(PAT, new_year)) is True
    assert rule.matches(show("e", "spokane", datetime(2027, 1, 4, tzinfo=UTC)), context(PAT, new_year)) is False


# ---------- 价格规则 ----------


def test_price_under_needs_one_ticket_that_is_both_cheap_and_buyable():
    listings = [
        Listing("a", 3500, 10),  # 便宜且有货
        Listing("b", 6500, 4),  # 有货但贵
        Listing("c", 2000, 0),  # 便宜但售罄
        Listing("c", 9000, 2),  # 有货但贵：两个条件不能分别由两张票满足
    ]
    rule = impl.price_under(5000)
    ctx = context(PAT, listings=listings)
    assert [rule.matches(show(i, "spokane", at(12)), ctx) for i in "abcd"] == [True, False, False, False]


def test_price_under_is_strict():
    ctx = context(PAT, listings=[Listing("a", 5000, 1), Listing("b", 4999, 1)])
    rule = impl.price_under(5000)
    assert rule.matches(show("a", "spokane", at(12)), ctx) is False
    assert rule.matches(show("b", "spokane", at(12)), ctx) is True


# ---------- 组合 ----------


class Hometown:
    """别处写的规则：只要有 matches(event, context) 就能放进组合。"""

    def __init__(self, name_part):
        self.name_part = name_part

    def matches(self, event, context):
        return self.name_part in event.name


def test_all_of_needs_every_rule_not_just_the_first_or_the_last():
    ctx = context(PAT, listings=[Listing("a", 2000, 5)])
    assert impl.all_of(impl.price_under(5000), impl.within_days(7)).matches(show("a", "spokane", at(8)), ctx) is True
    late = show("a", "spokane", at(20))  # 票便宜，但不在 7 天内
    assert impl.all_of(impl.within_days(7), impl.price_under(5000)).matches(late, ctx) is False  # 首条不过、末条过
    assert impl.all_of(impl.price_under(5000), impl.within_days(7)).matches(late, ctx) is False  # 末条不过
    middle = impl.all_of(impl.price_under(5000), impl.within_days(7), impl.price_under(6000))
    assert middle.matches(late, ctx) is False  # 中间不过、首末都过


def test_empty_combinators_are_the_identities():
    ctx = context(NOBODY)
    anything = show("a", "atlantis", at(12))
    assert impl.all_of().matches(anything, ctx) is True
    assert impl.any_of().matches(anything, ctx) is False


def test_combinators_nest_and_accept_foreign_rules():
    ctx = context(PAT, listings=[Listing("jazz", 2500, 3)])
    jazz = Event("jazz", "Jazz night", "bellevue", at(8, 20))
    rule = impl.all_of(
        impl.any_of(impl.within_miles(10), Hometown("Opera")),
        impl.any_of(impl.all_of(impl.this_weekend(), impl.in_metro_area()), impl.price_under(10)),
        Hometown("Jazz"),
    )
    assert rule.matches(jazz, ctx) is True
    assert rule.matches(Event("opera", "Opera night", "spokane", at(8, 20)), ctx) is False
    assert impl.any_of(Hometown("Opera"), Hometown("Jazz")).matches(jazz, ctx) is True


# ---------- 规则可复用 ----------


def test_one_rule_object_answers_each_customer_for_themselves():
    spokane_show = show("b", "spokane", at(12, 19))
    rule = impl.within_miles(100)
    for first, second in itertools.permutations([PAT, SAM, NOBODY, KIM], 2):
        answers = {c.id: rule.matches(spokane_show, context(c)) for c in (first, second)}
        fresh = {c.id: impl.within_miles(100).matches(spokane_show, context(c)) for c in (first, second)}
        assert answers == fresh


def test_one_rule_object_serves_every_call_with_a_different_now():
    rule = impl.this_weekend()
    sunday_show = show("a", "spokane", at(8, 19))  # 周日 19:00
    assert rule.matches(sunday_show, context(PAT, at(5, 9))) is True
    assert rule.matches(sunday_show, context(PAT, at(9, 9))) is False  # 已经是过去
    assert rule.matches(sunday_show, context(PAT, at(5, 9))) is True


def test_one_campaign_sent_to_many_customers_gives_each_their_own_events():
    events = [
        show("p1", "seattle", at(10, 19)),
        show("t1", "tacoma", at(11, 19)),
        show("b1", "spokane", at(12, 19)),
    ]
    campaign = Campaign("close", [impl.within_miles(60)], 5)
    rec = recommender(events)
    assert rec.recommend(PAT, campaign, NOW) == ["p1", "t1"]
    assert rec.recommend(SAM, campaign, NOW) == ["b1"]
    assert rec.recommend(KIM, campaign, NOW) == ["b1"]
    assert rec.recommend(PAT, campaign, NOW) == ["p1", "t1"]  # 回到第一位客户，答案不变


# ---------- 推荐器 ----------


def test_only_upcoming_events_with_tickets_are_eligible_and_sorted_by_start_then_id():
    events = [
        show("b", "spokane", at(12, 19)),
        show("a", "spokane", at(12, 19)),  # 同一时刻，按 id
        show("early", "spokane", at(10, 9)),
        show("past", "spokane", at(4, 19)),  # 已经开始
        show("sold-out", "spokane", at(11, 19)),  # 没有可买的票
        show("unlisted", "spokane", at(11, 20)),  # 没有任何票
    ]
    inventory = Inventory(
        [Listing(e.id, 3000, 5) for e in events if e.id not in ("sold-out", "unlisted")]
        + [Listing("sold-out", 1000, 0)]
    )
    campaign = Campaign("all", [impl.any_of(impl.within_miles(10_000))], 10)
    assert recommender(events, inventory).recommend(SAM, campaign, NOW) == ["early", "a", "b"]


def test_event_starting_exactly_now_is_eligible():
    events = [show("now", "spokane", NOW)]
    assert recommender(events).recommend(SAM, Campaign("c", [impl.within_days(1)], 3), NOW) == ["now"]


def test_first_tier_with_a_match_wins_and_later_tiers_are_ignored():
    events = [show("t", "tacoma", at(10, 19)), show("n", "olympia", at(11, 19)), show("w", "portland", at(9, 19))]
    rec = recommender(events)
    campaign = Campaign("c", [impl.within_miles(20), impl.within_miles(100), impl.within_miles(500)], 5)
    assert rec.recommend(PAT, campaign, NOW) == ["t", "n"]  # 第二级命中，第三级（含华盛顿）不用


def test_limit_applies_after_matching_not_before():
    events = [show(f"far{i}", "spokane", at(6 + i, 12)) for i in range(3)]  # 最早的三场都在斯波坎
    events += [show("near1", "tacoma", at(13, 19)), show("near2", "tacoma", at(14, 19))]
    campaign = Campaign("close", [impl.within_miles(60)], 2)
    assert recommender(events).recommend(PAT, campaign, NOW) == ["near1", "near2"]


def test_limit_truncates_the_matches_in_order():
    events = [show(f"e{i}", "tacoma", at(6 + i, 12)) for i in range(5)]
    campaign = Campaign("close", [impl.within_miles(60)], 3)
    assert recommender(events).recommend(PAT, campaign, NOW) == ["e0", "e1", "e2"]


@pytest.mark.parametrize("customer", [PAT, SAM, KIM, NOBODY, FAR_HOME])
def test_last_resort_gives_every_customer_the_soonest_events(customer):
    events = [
        show("f1", "olympia", at(12, 20)),
        show("f2", "portland", at(13, 19)),
        show("f3", "olympia", at(14, 18)),
        show("f0", "portland", at(11, 8)),
    ]
    campaign = Campaign("nowhere", [impl.within_miles(0.5), impl.price_under(1)], 3)
    assert recommender(events).recommend(customer, campaign, NOW) == ["f0", "f1", "f2"]


def test_result_is_empty_only_when_nothing_is_eligible():
    events = [show("past", "spokane", at(1, 9)), show("sold-out", "spokane", at(12, 9))]
    inventory = Inventory([Listing("past", 1000, 5), Listing("sold-out", 1000, 0)])
    campaign = Campaign("c", [impl.within_miles(1000)], 5)
    assert recommender(events, inventory).recommend(PAT, campaign, NOW) == []
    assert recommender([], Inventory()).recommend(NOBODY, campaign, NOW) == []


def test_campaign_with_a_foreign_rule_needs_no_change_to_the_recommender():
    events = [show("x", "spokane", at(12, 20)), Event("y", "Hometown Heroes", "spokane", at(13, 20))]
    campaign = Campaign("hometown", [Hometown("Heroes")], 5)
    assert recommender(events).recommend(NOBODY, campaign, NOW) == ["y"]


def test_returned_list_belongs_to_the_caller():
    events = [show("a", "tacoma", at(10, 19))]
    rec = recommender(events)
    campaign = Campaign("c", [impl.within_miles(60)], 5)
    first = rec.recommend(PAT, campaign, NOW)
    first.append("junk")
    assert rec.recommend(PAT, campaign, NOW) == ["a"]


def test_threads_sharing_one_recommender_and_one_campaign_get_their_own_answers():
    events = [
        show("p", "seattle", at(10, 19)),
        show("t", "tacoma", at(11, 19)),
        show("b", "spokane", at(12, 19)),
    ]
    campaign = Campaign("close", [impl.all_of(impl.within_miles(60), impl.price_under(5000))], 5)
    shared = recommender(events)
    customers = [PAT, SAM, KIM, NOBODY, FAR_HOME, PAT, SAM, KIM]
    expected = [recommender(events).recommend(c, campaign, NOW) for c in customers]
    barrier = threading.Barrier(len(customers))
    results = [None] * len(customers)

    def work(index):
        barrier.wait()
        results[index] = [shared.recommend(customers[index], campaign, NOW) for _ in range(200)]

    threads = [threading.Thread(target=work, args=(i,)) for i in range(len(customers))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert results == [[answer] * 200 for answer in expected]
