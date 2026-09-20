"""电影订票参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import datetime, timedelta, UTC

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T0 = datetime(2026, 5, 13, 18, 0, tzinfo=UTC)  # 2026-05-13 是星期三


def make_clock(start: datetime = T0):
    """一个可以手动拨动的假时钟：`clock()` 读当前值，`advance()` 往前拨。"""
    state = {"now": start}

    def clock() -> datetime:
        return state["now"]

    def advance(delta: timedelta) -> None:
        state["now"] += delta

    return clock, advance


def default_pricing():
    return impl.by_seat_type({
        impl.SeatType.NORMAL: 4500,
        impl.SeatType.PREMIUM: 6800,
        impl.SeatType.RECLINER: 9900,
    })


def build(clock, rows="AB", seats_per_row=3, starts_in=timedelta(hours=3),
          pricing=None, cancellation=None, hold_ttl=timedelta(minutes=10),
          payment_window=timedelta(minutes=2), types=None):
    """造一个只有一场放映的服务，返回 (service, show)。"""
    screen = impl.Screen.grid("S1", rows=rows, seats_per_row=seats_per_row, types=types or {})
    cinema = impl.Cinema(id="C1", name="Grand", city="Shanghai", screens=(screen,))
    movie = impl.Movie(id="M1", title="Dune", duration=timedelta(minutes=120))
    show = impl.Show("SH1", movie, screen, cinema, starts_at=clock() + starts_in, clock=clock)
    service = impl.BookingService(clock=clock, pricing=pricing or default_pricing(),
                                  cancellation=cancellation or impl.no_refund,
                                  hold_ttl=hold_ttl, payment_window=payment_window)
    service.schedule(show)
    return service, show


def approve(user_id, amount):
    return True


def decline(user_id, amount):
    return False


# ---- 第 1 关：层级模型与一笔选座下单 ----------------------------------------


def test_a_fresh_show_has_every_seat_of_its_screen_available():
    clock, _ = make_clock()
    _, show = build(clock)
    assert show.seat_count == 6
    assert {seat.label for seat in show.available_seats()} == {"A1", "A2", "A3", "B1", "B2", "B3"}
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6


def test_hold_then_confirm_produces_a_booking_priced_from_the_strategy():
    clock, _ = make_clock()
    service, show = build(clock, rows="AB", types={"B": impl.SeatType.PREMIUM})
    receipt = service.hold("SH1", ["A1", "B1"], user_id="u1")
    assert receipt.seat_labels == ("A1", "B1")
    assert show.seat_status("A1") is impl.SeatStatus.HELD
    booking = service.confirm(receipt, pay=approve)
    assert booking.amount == 4500 + 6800
    assert booking.status is impl.BookingStatus.CONFIRMED
    assert show.seat_status("A1") is impl.SeatStatus.BOOKED
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 4


def test_two_shows_on_the_same_screen_keep_independent_seat_state():
    """物理座位被两场共用，但"卖没卖掉"是每场独有的——这道题最常见的建模错误。"""
    clock, _ = make_clock()
    service, early = build(clock)
    late = impl.Show("SH2", early.movie, early.screen, early.cinema,
                     starts_at=clock() + timedelta(hours=6), clock=clock)
    service.schedule(late)
    service.confirm(service.hold("SH1", ["A1"], user_id="u1"), pay=approve)
    assert early.seat_status("A1") is impl.SeatStatus.BOOKED
    assert late.seat_status("A1") is impl.SeatStatus.AVAILABLE


def test_holding_an_unknown_seat_raises_and_changes_nothing():
    clock, _ = make_clock()
    service, show = build(clock)
    with pytest.raises(impl.UnknownSeatError):
        service.hold("SH1", ["A1", "Z9"], user_id="u1")
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6


def test_a_hold_is_all_or_nothing_when_one_seat_is_taken():
    clock, _ = make_clock()
    service, show = build(clock)
    service.hold("SH1", ["A2"], user_id="u1")
    with pytest.raises(impl.SeatNotAvailableError):
        service.hold("SH1", ["A1", "A2", "A3"], user_id="u2")
    assert show.seat_status("A1") is impl.SeatStatus.AVAILABLE
    assert show.seat_status("A3") is impl.SeatStatus.AVAILABLE
    assert show.count_by_status()[impl.SeatStatus.HELD] == 1


def test_shows_in_city_filters_by_city_and_by_movie():
    clock, _ = make_clock()
    service, show = build(clock)
    other_cinema = impl.Cinema(id="C2", name="Palace", city="Beijing", screens=(show.screen,))
    other = impl.Show("SH9", show.movie, show.screen, other_cinema,
                      starts_at=clock() + timedelta(hours=1), clock=clock)
    service.schedule(other)
    assert [s.id for s in service.shows_in_city("Shanghai")] == ["SH1"]
    assert [s.id for s in service.shows_in_city("Beijing", movie_id="M1")] == ["SH9"]
    assert service.shows_in_city("Beijing", movie_id="M-none") == ()


def test_unknown_show_and_unknown_booking_raise():
    clock, _ = make_clock()
    service, _ = build(clock)
    with pytest.raises(impl.ShowNotFoundError):
        service.hold("NOPE", ["A1"], user_id="u1")
    with pytest.raises(impl.BookingNotFoundError):
        service.booking("B-nope")


# ---- 第 2 关：带 TTL 的锁座（不 sleep，全靠注入的时钟） ----------------------


def test_an_expired_hold_frees_the_seats_without_any_sweep():
    """惰性过期：清扫任务一次都没跑，可用座位数也必须已经是对的。"""
    clock, advance = make_clock()
    service, show = build(clock, hold_ttl=timedelta(minutes=10))
    service.hold("SH1", ["A1", "A2"], user_id="u1")
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 4
    advance(timedelta(minutes=10, seconds=1))
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6
    assert show.seat_status("A1") is impl.SeatStatus.AVAILABLE


def test_another_user_can_take_the_seats_of_an_expired_hold():
    clock, advance = make_clock()
    service, show = build(clock)
    stale = service.hold("SH1", ["A1"], user_id="u1")
    advance(timedelta(minutes=11))
    fresh = service.hold("SH1", ["A1"], user_id="u2")
    assert fresh.user_id == "u2"
    with pytest.raises(impl.HoldExpiredError):
        service.confirm(stale, pay=approve)
    assert show.seat_status("A1") is impl.SeatStatus.HELD


def test_release_expired_holds_leaves_no_seat_stuck_in_held():
    clock, advance = make_clock()
    service, show = build(clock)
    service.hold("SH1", ["A1", "A2", "B1"], user_id="u1")
    advance(timedelta(minutes=11))
    assert service.release_expired_holds() == 3
    assert show.count_by_status()[impl.SeatStatus.HELD] == 0
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6
    assert service.release_expired_holds() == 0  # 幂等：再扫一次不会重复计数


def test_releasing_a_hold_returns_the_seats_immediately():
    clock, _ = make_clock()
    service, show = build(clock)
    receipt = service.hold("SH1", ["A1", "A2"], user_id="u1")
    assert service.release(receipt) == 2
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6
    assert service.release(receipt) == 0  # 已经放过的收据再放一次是无害的空操作


def test_declined_payment_releases_the_hold():
    clock, _ = make_clock()
    service, show = build(clock)
    receipt = service.hold("SH1", ["A1"], user_id="u1")
    with pytest.raises(impl.PaymentFailedError):
        service.confirm(receipt, pay=decline)
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6
    assert show.count_by_status()[impl.SeatStatus.HELD] == 0


def test_a_raising_payment_gateway_also_releases_the_hold():
    clock, _ = make_clock()
    service, show = build(clock)
    receipt = service.hold("SH1", ["A1"], user_id="u1")

    def explode(user_id, amount):
        raise RuntimeError("gateway timeout")

    with pytest.raises(RuntimeError):
        service.confirm(receipt, pay=explode)
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6


def test_the_payment_window_keeps_the_seats_past_the_original_ttl():
    """支付在锁外发生；进入支付窗口前持有期被延长，所以途中的清扫抢不走座位。"""
    clock, advance = make_clock()
    service, show = build(clock, hold_ttl=timedelta(minutes=10), payment_window=timedelta(minutes=5))
    receipt = service.hold("SH1", ["A1"], user_id="u1")

    def slow_pay(user_id, amount):
        advance(timedelta(minutes=3))          # 网关花了 3 分钟
        assert service.release_expired_holds() == 0  # 清扫在这期间跑过，什么也没清掉
        return True

    advance(timedelta(minutes=9))               # 原 TTL 只剩 1 分钟
    booking = service.confirm(receipt, pay=slow_pay)
    assert show.seat_status("A1") is impl.SeatStatus.BOOKED
    assert booking.seat_labels == ("A1",)


def test_payment_that_outruns_the_window_refuses_to_steal_someone_elses_seat():
    clock, advance = make_clock()
    service, show = build(clock, payment_window=timedelta(minutes=2))
    receipt = service.hold("SH1", ["A1"], user_id="u1")
    stolen: list[object] = []

    def very_slow_pay(user_id, amount):
        advance(timedelta(minutes=3))
        service.release_expired_holds()
        stolen.append(service.confirm(service.hold("SH1", ["A1"], user_id="u2"), pay=approve))
        return True

    with pytest.raises(impl.HoldExpiredError):
        service.confirm(receipt, pay=very_slow_pay)
    assert show.count_by_status()[impl.SeatStatus.BOOKED] == 1
    assert service.booking(stolen[0].id).user_id == "u2"


# ---- 第 3 关：并发（真线程 + barrier，断言不变量而不是时序） -----------------


def test_many_threads_racing_for_one_seat_sell_it_exactly_once():
    clock, _ = make_clock()
    service, show = build(clock)
    workers = 16
    barrier = threading.Barrier(workers)
    guard = threading.Lock()
    winners: list[str] = []

    def buy(i: int) -> None:
        barrier.wait()
        try:
            receipt = service.hold("SH1", ["A1"], user_id=f"u{i}")
        except impl.SeatNotAvailableError:
            return
        booking = service.confirm(receipt, pay=approve)
        with guard:
            winners.append(booking.id)

    threads = [threading.Thread(target=buy, args=(i,)) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(winners) == 1
    assert show.count_by_status()[impl.SeatStatus.BOOKED] == 1
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 5


def test_concurrent_bookings_never_sell_a_seat_twice_and_never_lose_one():
    """所有线程抢同一场的 6 个座：卖出的座位号必须互不重复，且账面三态相加等于总座数。"""
    clock, _ = make_clock()
    service, show = build(clock)
    labels = ["A1", "A2", "A3", "B1", "B2", "B3"]
    workers = 24
    barrier = threading.Barrier(workers)
    guard = threading.Lock()
    sold: list[str] = []

    def buy(i: int) -> None:
        wanted = [labels[i % len(labels)], labels[(i + 1) % len(labels)]]
        barrier.wait()
        try:
            receipt = service.hold("SH1", wanted, user_id=f"u{i}")
            booking = service.confirm(receipt, pay=approve)
        except impl.BookingError:
            return
        with guard:
            sold.extend(booking.seat_labels)

    threads = [threading.Thread(target=buy, args=(i,)) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(sold) == len(set(sold))                      # 没有一个座位被卖两次
    counts = show.count_by_status()
    assert counts[impl.SeatStatus.BOOKED] == len(sold)
    assert sum(counts.values()) == show.seat_count           # 没有座位凭空消失


def test_concurrent_sweeps_leave_no_seat_held_and_none_double_freed():
    clock, advance = make_clock()
    service, show = build(clock)
    for i, label in enumerate(["A1", "A2", "A3", "B1", "B2", "B3"]):
        service.hold("SH1", [label], user_id=f"u{i}")
    advance(timedelta(minutes=11))
    workers = 8
    barrier = threading.Barrier(workers)
    guard = threading.Lock()
    freed: list[int] = []

    def sweep() -> None:
        barrier.wait()
        n = service.release_expired_holds()
        with guard:
            freed.append(n)

    threads = [threading.Thread(target=sweep) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sum(freed) == 6                                   # 每个座位只被清扫一次
    assert show.count_by_status()[impl.SeatStatus.HELD] == 0
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6


# ---- 第 4 关：定价与退票政策（加进来没碰锁座机器） --------------------------


def test_row_surcharge_stacks_on_top_of_seat_type_pricing():
    clock, _ = make_clock()
    pricing = impl.row_surcharge(default_pricing(), {"A": 500})
    service, _ = build(clock, pricing=pricing, types={"B": impl.SeatType.PREMIUM})
    assert service.quote("SH1", ["A1"]) == 5000
    assert service.quote("SH1", ["B1"]) == 6800
    assert service.quote("SH1", ["A1", "B1"]) == 11800


def test_weekend_pricing_only_applies_to_weekend_shows():
    weekday_clock, _ = make_clock(T0)                                  # 周三
    weekend_clock, _ = make_clock(T0 + timedelta(days=3))              # 周六
    pricing = impl.weekend_multiplier(default_pricing(), 12, 10)
    weekday_service, _ = build(weekday_clock, pricing=pricing)
    weekend_service, _ = build(weekend_clock, pricing=pricing)
    assert weekday_service.quote("SH1", ["A1"]) == 4500
    assert weekend_service.quote("SH1", ["A1"]) == 5400


def test_tiered_refund_pays_less_the_later_you_cancel():
    policy = impl.tiered_refund([(timedelta(hours=4), 100), (timedelta(hours=1), 50)])
    clock, advance = make_clock()
    service, show = build(clock, starts_in=timedelta(hours=5), cancellation=policy)
    booking = service.confirm(service.hold("SH1", ["A1"], user_id="u1"), pay=approve)
    advance(timedelta(hours=2))                              # 离开演还有 3 小时 → 退一半
    cancelled = service.cancel(booking.id)
    assert cancelled.status is impl.BookingStatus.CANCELLED
    assert cancelled.refunded == 2250
    assert show.count_by_status()[impl.SeatStatus.AVAILABLE] == 6


def test_cancelling_twice_is_refused_so_nobody_is_refunded_twice():
    clock, _ = make_clock()
    service, _ = build(clock, cancellation=impl.tiered_refund([(timedelta(0), 100)]))
    booking = service.confirm(service.hold("SH1", ["A1"], user_id="u1"), pay=approve)
    service.cancel(booking.id)
    with pytest.raises(impl.CancellationNotAllowedError):
        service.cancel(booking.id)
    assert service.booking(booking.id).refunded == 4500


def test_cancelling_after_the_show_started_is_refused():
    clock, advance = make_clock()
    service, _ = build(clock, starts_in=timedelta(hours=1))
    booking = service.confirm(service.hold("SH1", ["A1"], user_id="u1"), pay=approve)
    advance(timedelta(hours=1, minutes=1))
    with pytest.raises(impl.CancellationNotAllowedError):
        service.cancel(booking.id)


def test_purging_ended_shows_shrinks_the_catalogue_but_keeps_the_booking_record():
    clock, advance = make_clock()
    service, show = build(clock, starts_in=timedelta(hours=1))
    booking = service.confirm(service.hold("SH1", ["A1"], user_id="u1"), pay=approve)
    advance(timedelta(hours=1))
    assert service.purge_shows_ended_before(clock()) == 0     # 还没散场
    advance(show.movie.duration)
    assert service.purge_shows_ended_before(clock()) == 1
    assert service.shows_in_city("Shanghai") == ()
    assert service.booking(booking.id).seat_labels == ("A1",)
    with pytest.raises(impl.ShowNotFoundError):
        service.hold("SH1", ["A2"], user_id="u2")
