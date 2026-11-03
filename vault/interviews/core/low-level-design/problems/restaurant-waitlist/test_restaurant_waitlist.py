"""餐厅候位的 pytest 套件：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os
from datetime import datetime, timedelta, UTC

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T0 = datetime(2026, 1, 1, 18, 0, tzinfo=UTC)


class Clock:
    def __init__(self):
        self.now = T0

    def __call__(self):
        return self.now

    def advance(self, minutes: int):
        self.now += timedelta(minutes=minutes)


def make(tables, **kwargs):
    clock = Clock()
    return impl.Restaurant(tables, clock, **kwargs), clock


def minutes(n: int) -> timedelta:
    return timedelta(minutes=n)


# ---- 第 1 关：入座、排队、离开 ----------------------------------------------------


def test_part1_best_fit_picks_the_smallest_table_that_fits():
    r, _ = make([6, 2, 4])
    assert r.join("a", 3) == 2    # 3 人坐 4 人桌，不占 6 人桌
    assert r.join("b", 2) == 1
    assert r.join("c", 5) == 0


def test_part1_ties_go_to_the_lowest_table_number():
    r, _ = make([4, 4, 4])
    assert r.join("a", 4) == 0
    assert r.join("b", 1) == 1


def test_part1_waiting_parties_queue_in_order():
    r, _ = make([2])
    assert r.join("a", 2) == 0
    assert r.join("b", 2) is None
    assert r.join("c", 1) is None
    assert r.queue() == ["b", "c"]
    assert r.table_of("b") is None and r.table_of("a") == 0


def test_part1_finish_seats_the_first_party_that_fits_and_keeps_the_rest_in_order():
    r, _ = make([2, 4])
    r.join("a", 2)      # 桌 0
    r.join("b", 4)      # 桌 1
    r.join("c", 4)
    r.join("d", 2)
    r.join("e", 1)
    assert r.queue() == ["c", "d", "e"]
    assert r.finish("a") == [("d", 0)]    # 桌 0 容量 2，c 坐不下，d 是第一个坐得下的
    assert r.queue() == ["c", "e"]
    assert r.finish("b") == [("c", 1)]
    assert r.finish("c") == [("e", 1)]
    assert r.finish("d") == []


def test_part1_leave_removes_only_waiting_parties():
    r, _ = make([2])
    r.join("a", 2)
    r.join("b", 2)
    r.join("c", 2)
    r.leave("b")
    assert r.queue() == ["c"]
    with pytest.raises(impl.UnknownPartyError):
        r.leave("b")
    with pytest.raises(impl.UnknownPartyError):
        r.leave("a")        # 已经入座，不是离开队伍
    assert r.join("b", 2) is None   # 同一个 id 可以重新排队，排到队尾
    assert r.queue() == ["c", "b"]


def test_part1_validation_errors_leave_state_unchanged():
    r, _ = make([2, 4])
    r.join("a", 2)
    for size in (0, -3):
        with pytest.raises(impl.InvalidPartyError):
            r.join("x", size)
    with pytest.raises(impl.PartyTooLargeError):
        r.join("x", 5)
    with pytest.raises(impl.DuplicatePartyError):
        r.join("a", 2)          # 正在用餐
    r.join("b", 2)
    r.join("c", 4)
    r.join("d", 4)
    with pytest.raises(impl.DuplicatePartyError):
        r.join("d", 4)          # 正在排队
    assert r.queue() == ["c", "d"]


def test_part1_finish_of_unknown_or_waiting_party_is_an_error():
    r, _ = make([2])
    r.join("a", 2)
    r.join("b", 2)
    with pytest.raises(impl.UnknownPartyError):
        r.finish("b")
    with pytest.raises(impl.UnknownPartyError):
        r.finish("zzz")
    r.finish("a")
    with pytest.raises(impl.UnknownPartyError):
        r.finish("a")           # 同一桌不能结束两次


def test_part1_bad_tables_are_rejected_and_ids_are_reusable_after_finish():
    for bad in ([], [0, 2], [-1]):
        with pytest.raises(ValueError):
            make(bad)
    r, _ = make([2])
    r.join("a", 2)
    r.finish("a")
    assert r.join("a", 1) == 0


# ---- 第 2 关：等位估计 --------------------------------------------------------------


def test_part2_quote_on_an_empty_restaurant_is_zero():
    r, _ = make([2, 4])
    assert r.quote(4) == minutes(0)
    r.join("a", 4)
    assert r.quote(2) == minutes(0)


def test_part2_estimates_follow_the_same_seating_rule_as_the_real_thing():
    r, clock = make([2, 4])             # 用餐 60 分钟
    r.join("a", 2)                      # 桌 0，18:00
    r.join("b", 4)                      # 桌 1，18:00
    r.join("c", 4)
    r.join("d", 2)
    r.join("e", 2)
    assert r.estimate_wait("c") == minutes(60)
    assert r.estimate_wait("d") == minutes(60)      # 18:00 桌 0、桌 1 同时空出，c 占 1，d 占 0
    assert r.estimate_wait("e") == minutes(120)
    clock.advance(30)
    assert r.estimate_wait("c") == minutes(30)
    assert r.estimate_wait("e") == minutes(90)


def test_part2_quote_matches_the_estimate_after_joining():
    r, clock = make([2, 4])
    r.join("a", 2)
    clock.advance(10)
    r.join("b", 4)
    for size in (1, 2, 4):
        quoted = r.quote(size)
        r.join(f"p{size}", size)
        assert r.estimate_wait(f"p{size}") == quoted
    assert r.queue() == ["p1", "p2", "p4"]      # quote 本身没有排过队


def test_part2_seated_party_waits_zero_and_unknown_party_is_an_error():
    r, _ = make([4])
    r.join("a", 4)
    assert r.estimate_wait("a") == minutes(0)
    with pytest.raises(impl.UnknownPartyError):
        r.estimate_wait("nobody")
    with pytest.raises(impl.PartyTooLargeError):
        r.quote(5)


def test_part2_someone_ahead_leaving_shortens_the_wait():
    r, _ = make([4])
    r.join("a", 4)
    r.join("b", 4)
    r.join("c", 4)
    assert r.estimate_wait("c") == minutes(120)
    r.leave("b")
    assert r.estimate_wait("c") == minutes(60)


def test_part2_each_table_uses_its_own_seating_time():
    r, clock = make([4, 4])
    r.join("a", 4)                      # 18:00 -> 19:00 空出
    clock.advance(20)
    r.join("b", 4)                      # 18:20 -> 19:20 空出
    clock.advance(10)
    r.join("c", 4)
    r.join("d", 4)
    assert r.estimate_wait("c") == minutes(30)
    assert r.estimate_wait("d") == minutes(50)
    clock.advance(10)                   # 18:40，a 提前结束
    assert r.finish("a") == [("c", 0)]
    assert r.estimate_wait("d") == minutes(40)   # b 在 19:20 空出，比 c（18:40 入座，19:40 空出）早


def test_part2_overdue_tables_count_as_free_now_and_dining_time_is_configurable():
    r, clock = make([4], dining_time=minutes(30))
    r.join("a", 4)
    r.join("b", 4)
    assert r.estimate_wait("b") == minutes(30)
    clock.advance(45)                   # a 已经超时
    assert r.estimate_wait("b") == minutes(0)


# ---- 第 3 关：防饿死 ----------------------------------------------------------------


def starve_setup(max_overtakes):
    """桌 0 容量 2、桌 1 容量 6。a 占了 6 人桌，b(6) 排队，c(2) 越过 b 坐到桌 0，之后 c 结束。"""
    r, clock = make([2, 6], max_overtakes=max_overtakes)
    assert r.join("a", 6) == 1
    assert r.join("b", 6) is None
    assert r.join("c", 2) == 0
    clock.advance(10)
    return r, clock


def test_part3_unlimited_overtaking_is_the_default():
    r, _ = starve_setup(None)
    r.finish("c")
    assert r.join("d", 2) == 0          # 不限插队：d 直接坐桌 0，b 继续等


def test_part3_a_party_overtaken_too_often_blocks_those_behind_it():
    r, _ = starve_setup(1)              # c 已经插了 b 一次
    assert r.finish("c") == []
    assert r.join("d", 2) is None       # 桌 0 空着，但 b 挡在前面
    assert r.queue() == ["b", "d"]
    assert r.finish("a") == [("b", 1), ("d", 0)]      # b 先入座，同一次调用里 d 也坐下


def test_part3_zero_means_strict_first_come_first_served():
    r, _ = make([2, 4], max_overtakes=0)
    r.join("a", 4)
    assert r.join("b", 4) is None
    assert r.join("c", 2) is None       # 桌 0 空着也不行
    assert r.finish("a") == [("b", 1), ("c", 0)]


def test_part3_overtaking_is_allowed_up_to_the_limit():
    r, clock = make([2, 2, 6], max_overtakes=2)
    r.join("a", 6)
    r.join("b", 6)                      # 排队，被插队 0 次
    assert r.join("c", 2) == 0          # 第 1 次
    assert r.join("d", 2) == 1          # 第 2 次，b 此后挡路
    assert r.join("e", 2) is None
    clock.advance(5)
    assert r.finish("c") == []          # b 挡着，e 不能坐
    assert r.queue() == ["b", "e"]


def test_part3_leaving_blocker_releases_the_queue():
    r, _ = starve_setup(1)
    r.finish("c")
    r.join("d", 2)
    r.leave("b")
    assert r.table_of("d") == 0


def test_part3_estimates_obey_the_blocking_rule():
    r, clock = starve_setup(1)
    r.finish("c")
    r.join("d", 2)
    assert r.estimate_wait("d") == minutes(50)      # a 在 18:00 入座，19:00 空出；现在 18:10
    assert r.estimate_wait("b") == minutes(50)
    assert r.quote(2) == minutes(110)     # b、d 在 19:00 入座，d 在 20:00 才空出桌 0
    free_for_all, _ = starve_setup(None)
    free_for_all.finish("c")
    assert free_for_all.quote(2) == minutes(0)


# ---- 第 4 关：改人数 ----------------------------------------------------------------


def test_part4_shrinking_can_seat_the_party_immediately():
    r, _ = make([2, 4])
    r.join("a", 4)
    r.join("b", 4)
    r.join("c", 4)
    assert r.change_size("c", 2) == [("c", 0)]
    assert r.table_of("c") == 0 and r.queue() == ["b"]


def test_part4_growing_beyond_the_biggest_table_fails_and_keeps_the_party():
    r, _ = make([2, 4])
    r.join("a", 2)
    r.join("b", 4)
    r.join("c", 2)
    for size, error in ((5, impl.PartyTooLargeError), (0, impl.InvalidPartyError)):
        with pytest.raises(error):
            r.change_size("c", size)
    assert r.queue() == ["c"]
    with pytest.raises(impl.UnknownPartyError):
        r.change_size("a", 1)           # 已经入座
    with pytest.raises(impl.UnknownPartyError):
        r.change_size("nobody", 2)


def test_part4_keeps_position_and_changes_the_estimate():
    r, _ = make([2, 4])
    r.join("a", 2)
    r.join("b", 4)
    r.join("c", 4)
    r.join("d", 2)
    assert r.estimate_wait("d") == minutes(60)
    r.change_size("d", 4)
    assert r.queue() == ["c", "d"]
    assert r.estimate_wait("d") == minutes(120)


def test_part4_party_that_blocks_keeps_blocking_after_a_resize():
    r, _ = starve_setup(1)
    r.finish("c")
    r.join("d", 2)
    assert r.change_size("b", 5) == []      # 5 人仍坐不进桌 0，被插队次数还在，d 仍被挡
    assert r.queue() == ["b", "d"]


def test_part4_resize_can_unblock_the_parties_behind():
    r, _ = make([2, 2, 4], max_overtakes=0)
    r.join("a", 4)
    r.join("b", 4)
    r.join("c", 2)
    assert r.queue() == ["b", "c"]
    assert r.change_size("b", 2) == [("b", 0), ("c", 1)]
