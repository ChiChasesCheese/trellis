"""配送员薪资的 pytest 套件：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os
from datetime import datetime, time, timedelta, UTC
from decimal import Decimal as D

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
E = impl.EventType
S = impl.State

RATES = {S.TO_RESTAURANT: D("0.25"), S.WAITING: D("0.10"), S.DELIVERING: D("0.30")}
DAY = datetime(2026, 1, 5, 0, 0, tzinfo=UTC)


def at(hour: int, minute: int = 0, second: int = 0, day: int = 0) -> datetime:
    return DAY + timedelta(days=day, hours=hour, minutes=minute, seconds=second)


def peaks_plan(**kw):
    return impl.PayPlan(RATES, peaks=(
        impl.PeakWindow(time(11), time(14), D("1.5")),
        impl.PeakWindow(time(17), time(21), D("2")),
    ), **kw)


def deliver(p, delivery, driver, accept, arrive, pickup, dropoff):
    for event, when in ((E.ACCEPT, accept), (E.ARRIVE, arrive), (E.PICKUP, pickup), (E.DROPOFF, dropoff)):
        p.record(driver, delivery, event, when)


def plain():
    return impl.Payroll(impl.PayPlan(RATES))


# ---- 第 1 关：事件与基础计价 ---------------------------------------------------------


def test_part1_full_delivery_pays_each_state_at_its_own_rate():
    p = plain()
    deliver(p, "x", "d1", at(12), at(12, 10), at(12, 15), at(12, 35))
    assert p.delivery_pay("x") == D("9.00")      # 10x0.25 + 5x0.10 + 20x0.30


def test_part1_seconds_count_and_rounding_happens_once_per_delivery():
    p = plain()
    deliver(p, "x", "d1", at(12), at(12, 0, 30), at(12, 1, 45), at(12, 2, 10))
    # 三段各 0.125，合计 0.375 -> 0.38（若每段先舍入会得到 0.39）
    assert p.delivery_pay("x") == D("0.38")


def test_part1_only_segments_with_both_ends_known_are_paid():
    p = plain()
    p.record("d1", "x", E.ACCEPT, at(12))
    assert p.delivery_pay("x") == D("0.00")
    p.record("d1", "x", E.ARRIVE, at(12, 10))
    assert p.delivery_pay("x") == D("2.50")
    p.record("d1", "x", E.PICKUP, at(12, 15))
    assert p.delivery_pay("x") == D("3.00")


def test_part1_events_may_arrive_out_of_order():
    p = plain()
    p.record("d1", "x", E.DROPOFF, at(12, 35))
    p.record("d1", "x", E.PICKUP, at(12, 15))
    assert p.delivery_pay("x") == D("6.00")      # 只有取餐到送达这一段两端都已知
    p.record("d1", "x", E.ACCEPT, at(12))
    assert p.delivery_pay("x") == D("6.00")
    p.record("d1", "x", E.ARRIVE, at(12, 10))
    assert p.delivery_pay("x") == D("9.00")


def test_part1_duplicate_report_is_ignored_and_conflicting_report_is_rejected():
    p = plain()
    deliver(p, "x", "d1", at(12), at(12, 10), at(12, 15), at(12, 35))
    p.record("d1", "x", E.ARRIVE, at(12, 10))
    assert p.delivery_pay("x") == D("9.00")
    with pytest.raises(impl.ConflictingEventError):
        p.record("d1", "x", E.ARRIVE, at(12, 11))
    assert p.delivery_pay("x") == D("9.00")


def test_part1_timeline_must_follow_the_lifecycle_and_failures_change_nothing():
    p = plain()
    p.record("d1", "x", E.ARRIVE, at(12, 10))
    with pytest.raises(impl.InconsistentTimelineError):
        p.record("d1", "x", E.PICKUP, at(12, 5))        # 取餐早于到店
    with pytest.raises(impl.InconsistentTimelineError):
        p.record("d1", "x", E.ACCEPT, at(12, 20))       # 接单晚于到店
    with pytest.raises(impl.InconsistentTimelineError):
        p.record("d1", "x", E.DROPOFF, at(12, 1))       # 与不相邻的事件比较也要矛盾
    p.record("d1", "x", E.PICKUP, at(12, 10))           # 允许相等
    p.record("d1", "x", E.ACCEPT, at(12))
    assert p.delivery_pay("x") == D("2.50")


def test_part1_an_order_belongs_to_the_first_driver_who_reports_it():
    p = plain()
    p.record("d1", "x", E.ACCEPT, at(12))
    with pytest.raises(impl.DriverMismatchError):
        p.record("d2", "x", E.ARRIVE, at(12, 10))
    p.record("d1", "x", E.ARRIVE, at(12, 10))
    assert p.driver_payout("d2") == D("0.00")
    assert p.driver_payout("d1") == D("2.50")


def test_part1_driver_payout_sums_orders_and_unknown_things_are_handled():
    p = plain()
    deliver(p, "x", "d1", at(12), at(12, 10), at(12, 15), at(12, 35))
    deliver(p, "y", "d1", at(14), at(14, 4), at(14, 6), at(14, 16))
    deliver(p, "z", "d2", at(12), at(12, 10), at(12, 15), at(12, 35))
    assert p.driver_payout("d1") == D("9.00") + D("1.00") + D("0.20") + D("3.00")
    assert p.driver_payout("nobody") == D("0.00")
    with pytest.raises(impl.UnknownDeliveryError):
        p.delivery_pay("nope")


def test_part1_plan_validation():
    bad_rates = [
        {S.TO_RESTAURANT: D("1"), S.WAITING: D("1")},
        {**RATES, S.WAITING: D("-0.1")},
    ]
    for rates in bad_rates:
        with pytest.raises(ValueError):
            impl.PayPlan(rates)


# ---- 第 2 关：高峰倍率 ----------------------------------------------------------------


def peak_payroll(**kw):
    return impl.Payroll(peaks_plan(**kw))


def test_part2_a_delivery_entirely_inside_a_peak_window():
    p = peak_payroll()
    deliver(p, "x", "d1", at(12), at(12, 10), at(12, 15), at(12, 35))
    assert p.delivery_pay("x") == D("13.50")      # 9.00 x 1.5


def test_part2_segment_straddling_the_start_and_the_end_of_a_window():
    p = peak_payroll()
    p.record("d1", "a", E.ACCEPT, at(10, 50))
    p.record("d1", "a", E.ARRIVE, at(11, 10))
    assert p.delivery_pay("a") == D("6.25")       # 10 分钟 x1 + 10 分钟 x1.5，单价 0.25
    p.record("d1", "b", E.PICKUP, at(13, 50))
    p.record("d1", "b", E.DROPOFF, at(14, 10))
    assert p.delivery_pay("b") == D("7.50")       # 10 x1.5 + 10 x1，单价 0.30


def test_part2_a_segment_spanning_a_whole_window_and_two_days():
    p = peak_payroll()
    p.record("d1", "a", E.ARRIVE, at(10))
    p.record("d1", "a", E.PICKUP, at(15))
    assert p.delivery_pay("a") == D("39.00")      # (60 + 180x1.5 + 60) x 0.10
    p.record("d1", "b", E.ARRIVE, at(10))
    p.record("d1", "b", E.PICKUP, at(10, day=1))
    assert p.delivery_pay("b") == D("177.00")     # (1020 + 180x1.5 + 240x2) x 0.10


def test_part2_adjacent_windows_with_different_multipliers():
    plan = impl.PayPlan(RATES, peaks=(impl.PeakWindow(time(9), time(12), D("2")),
                                      impl.PeakWindow(time(12), time(15), D("3"))))
    p = impl.Payroll(plan)
    p.record("d1", "x", E.PICKUP, at(11))
    p.record("d1", "x", E.DROPOFF, at(13))
    assert p.delivery_pay("x") == D("90.00")      # (60x2 + 60x3) x 0.30


def test_part2_windows_ending_at_midnight_cover_the_day_boundary():
    plan = impl.PayPlan(RATES, peaks=(impl.PeakWindow(time(22), time(0), D("2")),
                                      impl.PeakWindow(time(0), time(2), D("2"))))
    p = impl.Payroll(plan)
    p.record("d1", "x", E.PICKUP, at(23, 30))
    p.record("d1", "x", E.DROPOFF, at(0, 30, day=1))
    assert p.delivery_pay("x") == D("36.00")      # 60 x2 x 0.30


def test_part2_window_edges_are_half_open():
    p = peak_payroll()
    p.record("d1", "a", E.PICKUP, at(10, 30))
    p.record("d1", "a", E.DROPOFF, at(11))        # 恰好在窗口开始处结束：全程不涨
    assert p.delivery_pay("a") == D("9.00")
    p.record("d1", "b", E.PICKUP, at(11))
    p.record("d1", "b", E.DROPOFF, at(11, 30))    # 从窗口开始处开始：全程涨
    assert p.delivery_pay("b") == D("13.50")
    p.record("d1", "c", E.PICKUP, at(14))
    p.record("d1", "c", E.DROPOFF, at(14, 30))    # 从窗口结束处开始：不涨
    assert p.delivery_pay("c") == D("9.00")
    p.record("d1", "z", E.PICKUP, at(12))
    p.record("d1", "z", E.DROPOFF, at(12))        # 零长度
    assert p.delivery_pay("z") == D("0.00")


def test_part2_peak_windows_are_validated():
    bad = [
        (impl.PeakWindow(time(12), time(11), D("2")),),
        (impl.PeakWindow(time(12), time(12), D("2")),),
        (impl.PeakWindow(time(11), time(14), D("0")),),
        (impl.PeakWindow(time(11), time(14), D("2")), impl.PeakWindow(time(13), time(15), D("2"))),
    ]
    for peaks in bad:
        with pytest.raises(ValueError):
            impl.PayPlan(RATES, peaks=peaks)
    impl.PayPlan(RATES, peaks=(impl.PeakWindow(time(23), time(0), D("2")),))


def test_part2_multipliers_work_with_out_of_order_events():
    p = peak_payroll()
    p.record("d1", "x", E.DROPOFF, at(12, 35))
    p.record("d1", "x", E.PICKUP, at(12, 15))
    assert p.delivery_pay("x") == D("9.00")       # 20 x0.30 x1.5


# ---- 第 3 关：保底与结算周期 -----------------------------------------------------------


def test_part3_minimum_applies_to_completed_deliveries_only():
    p = impl.Payroll(impl.PayPlan(RATES, min_delivery_pay=D("3.00")))
    deliver(p, "x", "d1", at(12), at(12, 2), at(12, 3), at(12, 6))    # 0.50+0.10+0.90 = 1.50
    assert p.delivery_pay("x") == D("3.00")
    p.record("d1", "y", E.ACCEPT, at(13))
    p.record("d1", "y", E.ARRIVE, at(13, 2))
    assert p.delivery_pay("y") == D("0.50")                           # 还没送完：不保底
    deliver(p, "z", "d1", at(14), at(14, 10), at(14, 15), at(14, 35))
    assert p.delivery_pay("z") == D("9.00")                           # 本来就高于保底


def test_part3_minimum_kicks_in_when_the_last_missing_event_arrives():
    p = impl.Payroll(impl.PayPlan(RATES, min_delivery_pay=D("3.00")))
    p.record("d1", "x", E.DROPOFF, at(12, 6))
    p.record("d1", "x", E.PICKUP, at(12, 3))
    p.record("d1", "x", E.ARRIVE, at(12, 2))
    assert p.delivery_pay("x") == D("1.00")
    p.record("d1", "x", E.ACCEPT, at(12))
    assert p.delivery_pay("x") == D("3.00")


def test_part3_minimum_compares_against_the_peak_adjusted_amount():
    p = impl.Payroll(peaks_plan(min_delivery_pay=D("3.00")))
    deliver(p, "x", "d1", at(12), at(12, 4), at(12, 5), at(12, 6))    # (1.00+0.10+0.30) x1.5 = 2.10
    assert p.delivery_pay("x") == D("3.00")
    deliver(p, "y", "d1", at(12), at(12, 4), at(12, 5), at(12, 8))    # (1.00+0.10+0.90) x1.5 = 3.00
    assert p.delivery_pay("y") == D("3.00")


def test_part3_driver_payout_includes_the_minimum():
    p = impl.Payroll(impl.PayPlan(RATES, min_delivery_pay=D("3.00")))
    deliver(p, "x", "d1", at(12), at(12, 2), at(12, 3), at(12, 6))
    deliver(p, "y", "d1", at(14), at(14, 10), at(14, 15), at(14, 35))
    assert p.driver_payout("d1") == D("12.00")


def test_part3_period_payout_counts_orders_by_dropoff_time_half_open():
    p = plain()
    deliver(p, "a", "d1", at(8), at(8, 10), at(8, 15), at(8, 35))        # 送达 08:35
    deliver(p, "b", "d1", at(23, 50), at(23, 55), at(23, 58), at(0, 18, day=1))   # 跨天，送达次日 00:18
    deliver(p, "c", "d1", at(0, 8, day=1), at(0, 9, day=1), at(0, 10, day=1), at(0, 20, day=1))
    deliver(p, "d", "d2", at(8), at(8, 10), at(8, 15), at(8, 35))
    p.record("d1", "e", E.ACCEPT, at(9))                                 # 没送完的单不进周期结算
    p.record("d1", "e", E.ARRIVE, at(9, 10))
    day1 = p.payout("d1", at(0), at(0, day=1))
    day2 = p.payout("d1", at(0, day=1), at(0, day=2))
    assert day1 == D("9.00")
    assert day2 == p.delivery_pay("b") + p.delivery_pay("c")
    assert day1 + day2 == p.payout("d1", at(0), at(0, day=2))
    assert p.payout("d1", at(8, 35), at(8, 36)) == D("9.00")             # 起点包含
    assert p.payout("d1", at(8), at(8, 35)) == D("0.00")                 # 终点不包含
    assert p.payout("nobody", at(0), at(0, day=9)) == D("0.00")


# ---- 第 4 关：更正与明细 ---------------------------------------------------------------


def test_part4_correcting_a_timestamp_changes_the_pay_without_recomputing_anything_else():
    p = plain()
    deliver(p, "x", "d1", at(12), at(12, 10), at(12, 15), at(12, 35))
    p.correct_event("x", E.ACCEPT, at(11, 50))
    assert p.delivery_pay("x") == D("11.50")      # 去餐厅这段变成 20 分钟
    p.correct_event("x", E.ACCEPT, at(12))
    assert p.delivery_pay("x") == D("9.00")


def test_part4_correction_moves_an_order_between_settlement_periods():
    p = plain()
    deliver(p, "x", "d1", at(23), at(23, 10), at(23, 15), at(23, 55))
    assert p.payout("d1", at(0, day=1), at(0, day=2)) == D("0.00")
    p.correct_event("x", E.DROPOFF, at(0, 5, day=1))
    assert p.payout("d1", at(0), at(0, day=1)) == D("0.00")
    assert p.payout("d1", at(0, day=1), at(0, day=2)) == p.delivery_pay("x")


def test_part4_bad_corrections_are_rejected_and_change_nothing():
    p = plain()
    deliver(p, "x", "d1", at(12), at(12, 10), at(12, 15), at(12, 35))
    with pytest.raises(impl.InconsistentTimelineError):
        p.correct_event("x", E.PICKUP, at(12, 5))
    with pytest.raises(impl.InconsistentTimelineError):
        p.correct_event("x", E.DROPOFF, at(12, 14))
    p2 = plain()
    p2.record("d1", "y", E.ACCEPT, at(12))
    with pytest.raises(impl.MissingEventError):
        p2.correct_event("y", E.PICKUP, at(12, 5))
    with pytest.raises(impl.UnknownDeliveryError):
        p2.correct_event("nope", E.ACCEPT, at(12))
    assert p.delivery_pay("x") == D("9.00")


def test_part4_a_corrected_event_is_the_one_that_later_reports_are_compared_with():
    p = plain()
    p.record("d1", "x", E.ACCEPT, at(12))
    p.correct_event("x", E.ACCEPT, at(11))
    p.record("d1", "x", E.ACCEPT, at(11))                     # 与更正后一致：幂等
    with pytest.raises(impl.ConflictingEventError):
        p.record("d1", "x", E.ACCEPT, at(12))


def test_part4_breakdown_splits_at_peak_boundaries():
    p = peak_payroll()
    deliver(p, "x", "d1", at(10, 50), at(11, 10), at(11, 20), at(11, 40))
    rows = p.delivery_breakdown("x")
    assert [(r.state, r.start, r.end, r.multiplier, r.amount) for r in rows] == [
        (S.TO_RESTAURANT, at(10, 50), at(11), D("1"), D("2.5000")),
        (S.TO_RESTAURANT, at(11), at(11, 10), D("1.5"), D("3.7500")),
        (S.WAITING, at(11, 10), at(11, 20), D("1.5"), D("1.5000")),
        (S.DELIVERING, at(11, 20), at(11, 40), D("1.5"), D("9.0000")),
    ]
    assert sum(r.amount for r in rows) == D("16.7500")
    assert p.delivery_pay("x") == D("16.75")


def test_part4_breakdown_skips_unknown_segments_and_unknown_orders():
    p = plain()
    p.record("d1", "x", E.ACCEPT, at(12))
    p.record("d1", "x", E.PICKUP, at(12, 15))
    assert p.delivery_breakdown("x") == []
    with pytest.raises(impl.UnknownDeliveryError):
        p.delivery_breakdown("nope")
