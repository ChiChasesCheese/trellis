import importlib
import os
import random
import threading
from datetime import date, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

M = impl.Money
CAR, MOTO, LARGE = impl.VehicleType.CAR, impl.VehicleType.MOTORCYCLE, impl.VehicleType.LARGE
THU = datetime(2026, 10, 15, 0, 0)
FRI = datetime(2026, 10, 16, 0, 0)
SAT = datetime(2026, 10, 17, 0, 0)
SUN = datetime(2026, 10, 18, 0, 0)


def at(day: datetime, h: int, m: int = 0, s: int = 0) -> datetime:
    return day.replace(hour=h, minute=m, second=s)


class Clock:
    def __init__(self, now: datetime) -> None:
        self.now = now

    def __call__(self) -> datetime:
        return self.now


def engine(*adjustments):
    return impl.FeeEngine(impl.default_tariff(), adjustments)


def desk(now: datetime, *adjustments):
    clock = Clock(now)
    return impl.FeeDesk(engine(*adjustments), clock), clock


def fee(vehicle, entered, exited) -> int:
    return sum(d.charged.cents for d in engine().day_charges(vehicle, entered, exited))


# ---- 第 1 关：按车型的小时费率 ----

def test_two_peak_hours_for_a_car():
    assert fee(CAR, at(FRI, 10), at(FRI, 12)) == 800


def test_rate_depends_on_vehicle_type():
    stay = (at(FRI, 10), at(FRI, 12))
    assert [fee(v, *stay) for v in (MOTO, CAR, LARGE)] == [400, 800, 1200]


def test_partial_hours_are_prorated_and_rounded_up_to_the_cent():
    assert fee(CAR, at(FRI, 10), at(FRI, 10, 16)) == 107  # 400 * 16 / 60 = 106.67


def test_grace_period_is_all_or_nothing():
    assert fee(CAR, at(FRI, 10), at(FRI, 10, 15)) == 0
    assert fee(CAR, at(FRI, 10), at(FRI, 10, 15, 1)) == 101  # 400 * 901 / 3600 = 100.1


def test_exit_before_entry_is_rejected():
    with pytest.raises(impl.InvalidStayError):
        engine().day_charges(CAR, at(FRI, 10), at(FRI, 9))


def test_money_formats_and_orders():
    assert str(M(2700)) == "27.00" and str(M(5)) == "0.05" and M(1) < M(2)
    assert M(100) + M(50) - M(25) == M(125)


# ---- 第 2 关：跨费率边界、夜间、周末 ----

def test_stay_crossing_peak_end_is_split_into_two_rates():
    assert fee(CAR, at(FRI, 19, 30), at(FRI, 20, 30)) == 300  # 30 分钟高峰 200 + 30 分钟非高峰 100


def test_overnight_into_weekend_is_billed_per_calendar_day():
    days = engine().day_charges(CAR, at(FRI, 19, 30), at(SAT, 8, 30))
    assert [(d.day, d.charged.cents) for d in days] == [(date(2026, 10, 16), 1000), (date(2026, 10, 17), 1700)]


def test_weekend_is_off_peak_all_day():
    assert fee(CAR, at(SAT, 10), at(SAT, 12)) == 400
    assert fee(CAR, at(SUN, 9), at(SUN, 11)) == 400


def test_peak_window_is_half_open():
    assert fee(CAR, at(FRI, 7), at(FRI, 8)) == 200
    assert fee(CAR, at(FRI, 8), at(FRI, 9)) == 400
    assert fee(CAR, at(FRI, 19), at(FRI, 20)) == 400
    assert fee(CAR, at(FRI, 20), at(FRI, 21)) == 200


def test_rounding_happens_once_per_day_not_once_per_segment():
    days = engine().day_charges(CAR, at(FRI, 19, 59, 59), at(FRI, 20, 15, 4))
    assert days[0].raw == M(51)  # (400 * 1 + 200 * 904) / 3600 = 50.2 → 51；每段各取整会是 1 + 51 = 52


# ---- 第 3 关：每日封顶 ----

def test_daily_cap_limits_a_long_peak_day():
    days = engine().day_charges(CAR, at(FRI, 8), at(FRI, 20))
    assert days[0].raw == M(4800) and days[0].charged == M(2000)


def test_cap_is_per_calendar_day_and_per_vehicle_type():
    days = engine().day_charges(MOTO, at(THU, 8), at(SAT, 8))
    assert [d.charged.cents for d in days] == [1000, 1000, 800]  # 周六 0–8 点非高峰：8 小时 * 100
    assert fee(LARGE, at(FRI, 8), at(FRI, 20)) == 3000


def test_stay_below_the_cap_is_untouched():
    days = engine().day_charges(CAR, at(FRI, 10), at(FRI, 12))
    assert days[0].raw == days[0].charged == M(800)


# ---- 第 4 关：调整、丢票、收据 ----

def test_member_discount_rounds_the_discount_down():
    d, clock = desk(at(FRI, 10), impl.MemberDiscount(10))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 10, 16)  # 107 分，折扣 10.7 → 10
    receipt = d.exit(t.id, member=True)
    assert receipt.total == M(97)
    assert receipt.adjustments == (impl.Line("会员折扣", M(-10)),)


def test_non_member_gets_no_discount_line():
    d, clock = desk(at(FRI, 10), impl.MemberDiscount(10))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 12)
    receipt = d.exit(t.id)
    assert receipt.total == M(800) and receipt.adjustments == ()


def test_adjustment_order_matters_penalty_after_discount_is_not_discounted():
    a, ca = desk(at(FRI, 10), impl.MemberDiscount(50), impl.LostTicketPenalty(M(1000)))
    b, cb = desk(at(FRI, 10), impl.LostTicketPenalty(M(1000)), impl.MemberDiscount(50))
    for dd, cc in ((a, ca), (b, cb)):
        dd.enter("A1", CAR)
        cc.now = at(FRI, 12)
    assert a.exit_lost("A1", member=True).total == M(400 + 1000)
    assert b.exit_lost("A1", member=True).total == M((800 + 1000) // 2)


def test_receipt_total_equals_days_plus_adjustment_lines():
    d, clock = desk(at(FRI, 19, 30), impl.MemberDiscount(15), impl.LostTicketPenalty(M(1500)))
    d.enter("A1", CAR)
    clock.now = at(SAT, 8, 30)
    r = d.exit_lost("A1", member=True)
    assert r.total == sum((x.charged for x in r.days), M(0)) + sum((x.amount for x in r.adjustments), M(0))
    assert [x.label for x in r.adjustments] == ["会员折扣", "丢票罚款"]


def test_lost_ticket_is_found_by_plate_and_closes_the_ticket():
    d, clock = desk(at(FRI, 10), impl.LostTicketPenalty(M(1500)))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 12)
    assert d.exit_lost("A1").total == M(800 + 1500)
    with pytest.raises(impl.UnknownTicketError):
        d.exit(t.id)
    with pytest.raises(impl.UnknownTicketError):
        d.exit_lost("A1")


def test_a_normal_exit_has_no_penalty():
    d, clock = desk(at(FRI, 10), impl.LostTicketPenalty(M(1500)))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 12)
    assert d.exit(t.id).total == M(800)


# ---- 票与失败路径 ----

def test_quote_does_not_settle_the_ticket():
    d, clock = desk(at(FRI, 10))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 11)
    assert d.quote(t.id).total == M(400)
    clock.now = at(FRI, 12)
    assert d.exit(t.id).total == M(800)


def test_ticket_cannot_be_paid_twice_and_unknown_ticket_fails():
    d, clock = desk(at(FRI, 10))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 11)
    d.exit(t.id)
    with pytest.raises(impl.UnknownTicketError):
        d.exit(t.id)
    with pytest.raises(impl.UnknownTicketError):
        d.quote("T999")


def test_same_plate_cannot_hold_two_open_tickets_but_can_return_later():
    d, clock = desk(at(FRI, 10))
    t = d.enter("A1", CAR)
    with pytest.raises(impl.DuplicatePlateError):
        d.enter("A1", CAR)
    clock.now = at(FRI, 11)
    d.exit(t.id)
    assert d.enter("A1", CAR).id != t.id


def test_open_tickets_are_released_after_exit():
    d, clock = desk(at(FRI, 10))
    ids = [d.enter(f"P{i}", CAR).id for i in range(5)]
    assert d.open_count == 5
    clock.now = at(FRI, 11)
    for i in ids:
        d.exit(i)
    assert d.open_count == 0


def test_clock_going_backwards_keeps_the_ticket_open():
    d, clock = desk(at(FRI, 10))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 9)
    with pytest.raises(impl.InvalidStayError):
        d.exit(t.id)
    assert d.open_count == 1
    clock.now = at(FRI, 11)
    assert d.exit(t.id).total == M(400)


# ---- 属性：与逐分钟的朴素算法对拍 ----

def brute_force_raw(vehicle, entered, exited):
    """逐分钟累加单价（分/小时），每个日历日 ceil(sum/60)，完全独立于 next_change 的切段。"""
    tariff = impl.default_tariff()
    per_day: dict[date, int] = {}
    cursor = entered
    while cursor < exited:
        per_day[cursor.date()] = per_day.get(cursor.date(), 0) + tariff.rate_at(vehicle, cursor).cents
        cursor += timedelta(minutes=1)
    return {day: -(-total // 60) for day, total in per_day.items()}


@pytest.mark.parametrize("seed", range(25))
def test_matches_minute_by_minute_oracle(seed):
    rng = random.Random(seed)
    entered = FRI + timedelta(minutes=rng.randrange(0, 7 * 24 * 60))
    exited = entered + timedelta(minutes=rng.randrange(16, 4 * 24 * 60))
    vehicle = rng.choice([MOTO, CAR, LARGE])
    days = engine().day_charges(vehicle, entered, exited)
    assert {d.day: d.raw.cents for d in days} == brute_force_raw(vehicle, entered, exited)
    cap = impl.default_tariff().daily_cap[vehicle].cents
    assert all(d.charged.cents == min(d.raw.cents, cap) for d in days)


# ---- 并发 ----

def test_many_exits_of_the_same_ticket_pay_exactly_once():
    d, clock = desk(at(FRI, 10))
    t = d.enter("A1", CAR)
    clock.now = at(FRI, 12)
    barrier = threading.Barrier(16)
    results: list[object] = []

    def worker():
        barrier.wait()
        try:
            results.append(d.exit(t.id))
        except impl.UnknownTicketError as e:
            results.append(e)

    threads = [threading.Thread(target=worker) for _ in range(16)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    receipts = [r for r in results if isinstance(r, impl.Receipt)]
    assert len(results) == 16 and len(receipts) == 1 and receipts[0].total == M(800)


def test_concurrent_entries_get_distinct_ticket_ids():
    d, _ = desk(at(FRI, 10))
    barrier = threading.Barrier(16)
    tickets: list[object] = []

    def worker(i):
        barrier.wait()
        tickets.append(d.enter(f"P{i}", CAR))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(16)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    assert len({t.id for t in tickets}) == 16 and d.open_count == 16
