"""航班管理参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import date, datetime, time, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

DAY = date(2026, 7, 1)


def make_clock(start: datetime):
    """一个可以手动拨动的假时钟：`clock()` 读当前值，`advance()` 往前拨。"""
    state = {"now": start}

    def clock() -> datetime:
        return state["now"]

    def advance(delta: timedelta) -> None:
        state["now"] += delta

    return clock, advance


def small_aircraft(aircraft_id="T1", economy=4, business=2):
    """一架小飞机：1 排头等舱（AB…）、1 排经济舱（ABCD…），座位数由调用方指定。"""
    letters = "ABCDEFGH"
    return impl.Aircraft.layout(aircraft_id, "Test", {
        impl.CabinClass.BUSINESS: (1, letters[:business]),
        impl.CabinClass.ECONOMY: (1, letters[:economy]),
    })


def build(clock=None, overbooking=None, connection=None, fare=None, refund=None,
          hold_ttl=timedelta(minutes=20), check_in_opens=timedelta(hours=24),
          check_in_closes=timedelta(minutes=45), economy=4, business=2):
    """造一条 SHA -> PEK -> HRB 的两段航线，返回 (service, leg1, leg2)。"""
    clock = clock or (lambda: datetime(2026, 6, 30, 9, 0))
    connection = connection or impl.MinimumConnectionTime(timedelta(minutes=45))
    fare = fare or impl.cabin_fare({impl.CabinClass.ECONOMY: 89000, impl.CabinClass.BUSINESS: 268000})
    aircraft = small_aircraft(economy=economy, business=business)
    flight1 = impl.Flight("MU5100", "SHA", "PEK", time(8, 0), timedelta(hours=2), aircraft, "MU",
                          marketed_as=("CZ9001",))
    flight2 = impl.Flight("MU2610", "PEK", "HRB", time(11, 0), timedelta(hours=2), aircraft, "MU")
    leg1 = impl.FlightInstance(flight1, DAY, overbooking=overbooking or impl.no_overbooking)
    leg2 = impl.FlightInstance(flight2, DAY, overbooking=overbooking or impl.no_overbooking)
    service = impl.AirlineService(clock=clock, connection=connection, fare=fare,
                                  refund=refund or impl.no_refund, hold_ttl=hold_ttl,
                                  check_in_opens=check_in_opens, check_in_closes=check_in_closes)
    service.schedule(leg1)
    service.schedule(leg2)
    return service, leg1, leg2


# ---- 第 1 关：航班 / 航班实例 / 航段三层模型 --------------------------------


def test_aircraft_layout_assigns_seats_by_cabin_from_high_to_low():
    aircraft = small_aircraft(economy=4, business=2)
    business_seats = aircraft.seats_in(impl.CabinClass.BUSINESS)
    economy_seats = aircraft.seats_in(impl.CabinClass.ECONOMY)
    assert [s.row for s in business_seats] == [1, 1]
    assert [s.label for s in business_seats] == ["1A", "1B"]
    assert {s.row for s in economy_seats} == {2}
    assert len(economy_seats) == 4


def test_flight_instance_authorized_includes_overbooking_allowance():
    policy = impl.percent_overbooking({impl.CabinClass.ECONOMY: 25})
    service, leg1, _ = build(overbooking=policy, economy=4)
    assert leg1.capacity(impl.CabinClass.ECONOMY) == 4
    assert leg1.authorized(impl.CabinClass.ECONOMY) == 5  # 4 + 25%
    assert leg1.available(impl.CabinClass.ECONOMY) == 5


def test_search_finds_direct_itinerary():
    service, leg1, leg2 = build()
    plans = service.search("SHA", "PEK", DAY, impl.CabinClass.ECONOMY)
    assert len(plans) == 1
    assert plans[0].stops == 0
    assert plans[0].origin == "SHA" and plans[0].destination == "PEK"


def test_search_finds_connecting_itinerary_when_mct_satisfied():
    # leg2 起飞 11:00，leg1 落地 10:00（08:00 + 2h），间隔 60 分钟 ≥ 45 分钟的默认 MCT。
    service, leg1, leg2 = build()
    plans = service.search("SHA", "HRB", DAY, impl.CabinClass.ECONOMY)
    assert len(plans) == 1
    plan = plans[0]
    assert plan.stops == 1
    assert plan.origin == "SHA" and plan.destination == "HRB"
    assert [s.instance.key for s in plan.segments] == [leg1.key, leg2.key]


# ---- 第 2 关：最短衔接时间与跨航段原子订座 ----------------------------------


def test_minimum_connection_time_lives_on_the_airport_not_the_flight():
    mct = impl.MinimumConnectionTime(default=timedelta(minutes=45),
                                     by_airport={"PEK": timedelta(minutes=90)},
                                     carrier_change=timedelta(minutes=30))
    aircraft = small_aircraft()
    same_carrier = impl.Flight("A1", "SHA", "PEK", time(8, 0), timedelta(hours=2), aircraft, "MU")
    onward_same = impl.Flight("A2", "PEK", "HRB", time(9, 45), timedelta(hours=2), aircraft, "MU")
    other_carrier = impl.Flight("A3", "PEK", "HRB", time(9, 45), timedelta(hours=2), aircraft, "CZ")
    arriving = impl.Segment(impl.FlightInstance(same_carrier, DAY), impl.CabinClass.ECONOMY)
    # 同一承运人：PEK 的 90 分钟基准，10:00 落地、9:45(+1) 起飞——这里构造刚好卡边界。
    tail_same = impl.Segment(impl.FlightInstance(onward_same, DAY + timedelta(days=0)), impl.CabinClass.ECONOMY)
    assert mct.required(arriving, tail_same) == timedelta(minutes=90)
    tail_other = impl.Segment(impl.FlightInstance(other_carrier, DAY), impl.CabinClass.ECONOMY)
    assert mct.required(arriving, tail_other) == timedelta(minutes=120)  # 90 + 换承运人再加 30


def test_search_excludes_itinerary_when_connection_too_short():
    # leg2 提前到 08:40 起飞：leg1 10:00 落地，只剩 -80 分钟——接不上，search 不该返回它。
    aircraft = small_aircraft()
    clock = lambda: datetime(2026, 6, 30, 9, 0)
    connection = impl.MinimumConnectionTime(timedelta(minutes=45))
    fare = impl.cabin_fare({impl.CabinClass.ECONOMY: 89000, impl.CabinClass.BUSINESS: 268000})
    flight1 = impl.Flight("MU5100", "SHA", "PEK", time(8, 0), timedelta(hours=2), aircraft, "MU")
    flight2 = impl.Flight("MU2610", "PEK", "HRB", time(10, 10), timedelta(hours=2), aircraft, "MU")
    leg1, leg2 = impl.FlightInstance(flight1, DAY), impl.FlightInstance(flight2, DAY)
    service = impl.AirlineService(clock=clock, connection=connection, fare=fare)
    service.schedule(leg1)
    service.schedule(leg2)
    plans = service.search("SHA", "HRB", DAY, impl.CabinClass.ECONOMY)
    assert plans == ()
    with pytest.raises(impl.InvalidItineraryError):
        service.hold(impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),
                                     impl.Segment(leg2, impl.CabinClass.ECONOMY))), passenger="chi")


def test_hold_is_all_or_nothing_when_second_leg_is_sold_out():
    service, leg1, leg2 = build(economy=1)
    # 先把 leg2 经济舱唯一的座位订满。
    other = service.hold(impl.Itinerary((impl.Segment(leg2, impl.CabinClass.ECONOMY),)), passenger="other")
    assert leg1.available(impl.CabinClass.ECONOMY) == 1
    plan = service.search("SHA", "HRB", DAY, impl.CabinClass.ECONOMY)
    assert plan == ()  # leg2 满员，search 已经把这条行程排除
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),
                                impl.Segment(leg2, impl.CabinClass.ECONOMY)))
    with pytest.raises(impl.NoSeatsAvailableError):
        service.hold(itinerary, passenger="chi")
    # 关键不变量：leg1 完全没被碰过——不是订上一段、另一段失败。
    assert leg1.available(impl.CabinClass.ECONOMY) == 1
    assert leg1.refs_in(impl.CabinClass.ECONOMY) == ()


# ---- 第 3 关：订单生命周期、值机/登机、取消、改签 ---------------------------


def test_lifecycle_held_to_boarded_on_a_direct_flight():
    clock, advance = make_clock(datetime(2026, 7, 1, 5, 0))
    service, leg1, _ = build(clock=clock, check_in_opens=timedelta(hours=6), check_in_closes=timedelta(minutes=30))
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    booking = service.hold(itinerary, passenger="chi")
    assert booking.status is impl.BookingStatus.HELD
    service.ticket(booking.id)
    assert service.booking(booking.id).status is impl.BookingStatus.TICKETED
    advance(timedelta(hours=2))  # 07:00，落在 [02:00, 07:30] 的值机窗口内
    seats = service.check_in(booking.id, {leg1.key: "2A"})
    assert seats[leg1.key] == "2A"
    assert service.booking(booking.id).status is impl.BookingStatus.CHECKED_IN
    denied = service.board(leg1.key)
    assert denied == ()
    assert service.booking(booking.id).status is impl.BookingStatus.BOARDED


def test_invalid_transition_is_rejected():
    service, leg1, _ = build()
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    booking = service.hold(itinerary, passenger="chi")
    service.cancel(booking.id)
    with pytest.raises(impl.InvalidTransitionError):
        service.cancel(booking.id)  # 已取消的订单不能再取消一次


def test_cancel_from_held_releases_seats_with_no_refund_by_default():
    service, leg1, _ = build(economy=1)
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    booking = service.hold(itinerary, passenger="chi")
    assert leg1.available(impl.CabinClass.ECONOMY) == 0
    cancelled = service.cancel(booking.id)
    assert cancelled.status is impl.BookingStatus.CANCELLED
    assert cancelled.refunded == 0
    assert leg1.available(impl.CabinClass.ECONOMY) == 1


def test_cancel_from_ticketed_uses_tiered_refund_policy():
    clock, advance = make_clock(datetime(2026, 6, 20, 9, 0))
    refund = impl.tiered_refund([(timedelta(days=7), 100), (timedelta(hours=24), 50)])
    service, leg1, _ = build(clock=clock, refund=refund)
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    booking = service.hold(itinerary, passenger="chi")
    service.ticket(booking.id)
    advance(timedelta(days=3))  # 距起飞（7 月 1 日）还有 8 天多——落在 100% 档
    cancelled = service.cancel(booking.id)
    assert cancelled.refunded == booking.fare


def test_ticket_after_hold_expires_raises_and_releases_seats():
    clock, advance = make_clock(datetime(2026, 6, 30, 9, 0))
    service, leg1, _ = build(clock=clock, hold_ttl=timedelta(minutes=10), economy=1)
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    booking = service.hold(itinerary, passenger="chi")
    advance(timedelta(minutes=11))
    with pytest.raises(impl.HoldExpiredError):
        service.ticket(booking.id)
    assert service.booking(booking.id).status is impl.BookingStatus.CANCELLED
    assert leg1.available(impl.CabinClass.ECONOMY) == 1


def test_release_expired_holds_sweeps_every_stale_booking():
    clock, advance = make_clock(datetime(2026, 6, 30, 9, 0))
    service, leg1, _ = build(clock=clock, hold_ttl=timedelta(minutes=10), economy=2)
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    b1 = service.hold(itinerary, passenger="a")
    b2 = service.hold(itinerary, passenger="b")
    assert leg1.available(impl.CabinClass.ECONOMY) == 0
    advance(timedelta(minutes=11))
    swept = service.release_expired_holds()
    assert swept == 2
    assert service.booking(b1.id).status is impl.BookingStatus.CANCELLED
    assert service.booking(b2.id).status is impl.BookingStatus.CANCELLED
    assert leg1.available(impl.CabinClass.ECONOMY) == 2


def test_change_keeps_the_shared_leg_seat_untouched():
    service, leg1, leg2 = build(economy=2)
    old_itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),
                                    impl.Segment(leg2, impl.CabinClass.ECONOMY)))
    booking = service.hold(old_itinerary, passenger="chi")
    leg1.assign_seat(booking.id, "2A")
    new_itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))  # 只飞到 PEK 就下机
    changed = service.change(booking.id, new_itinerary)
    assert changed.itinerary.destination == "PEK"
    assert leg1.seat_of(booking.id) == "2A"  # 共用的那一段座位没有被"先放再占"抹掉
    assert leg2.available(impl.CabinClass.ECONOMY) == 2  # 不再需要的那段库存已经还回去
    assert leg2.refs_in(impl.CabinClass.ECONOMY) == ()


def test_change_preserves_old_itinerary_when_new_itinerary_is_unavailable():
    service, leg1, leg2 = build(economy=1)
    old_itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    booking = service.hold(old_itinerary, passenger="chi")
    # 把 leg2 订满，改签目标行程注定订不上。
    service.hold(impl.Itinerary((impl.Segment(leg2, impl.CabinClass.ECONOMY),)), passenger="other")
    new_itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),
                                    impl.Segment(leg2, impl.CabinClass.ECONOMY)))
    with pytest.raises(impl.NoSeatsAvailableError):
        service.change(booking.id, new_itinerary)
    # 改签失败：旅客手里那张老票必须还在，一段都没丢。
    refreshed = service.booking(booking.id)
    assert refreshed.itinerary is old_itinerary
    assert leg1.refs_in(impl.CabinClass.ECONOMY) == (booking.id,)


def test_board_denies_the_passenger_with_no_seat_first():
    policy = impl.percent_overbooking({impl.CabinClass.ECONOMY: 25})  # 4 座 -> 授权卖 5 张
    clock, advance = make_clock(datetime(2026, 7, 1, 5, 0))
    service, leg1, _ = build(clock=clock, overbooking=policy, economy=4,
                             check_in_opens=timedelta(hours=6), check_in_closes=timedelta(minutes=0))
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    bookings = [service.hold(itinerary, passenger=f"p{i}") for i in range(5)]
    for b in bookings:
        service.ticket(b.id)
    advance(timedelta(hours=1))
    for b in bookings:
        service.check_in(b.id)  # 前 4 个拿到座位，第 5 个拿不到（座位已经坐满）
    seatless = [b.id for b in bookings if leg1.seat_of(b.id) is None]
    assert len(seatless) == 1
    denied = service.board(leg1.key)
    assert denied == tuple(seatless)
    assert service.booking(denied[0]).status is impl.BookingStatus.TICKETED  # 拒载退回 TICKETED，票还在
    for b in bookings:
        if b.id not in denied:
            assert service.booking(b.id).status is impl.BookingStatus.BOARDED


# ---- 第 4 关：代码共享、清理与并发 -------------------------------------------


def test_codeshare_alias_resolves_to_the_same_flight_instance():
    service, leg1, _ = build()
    assert service.instance("CZ9001@2026-07-01") is leg1
    booking = service.hold(impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),)), passenger="chi")
    # 共享航班只有一份库存：不管从哪个航班号订，卖的都是同一班的同一批座位。
    assert leg1.refs_in(impl.CabinClass.ECONOMY) == (booking.id,)


def test_purge_flown_before_shrinks_catalogue_and_bookings():
    clock, advance = make_clock(datetime(2026, 6, 30, 9, 0))
    service, leg1, leg2 = build(clock=clock)
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    booking = service.hold(itinerary, passenger="chi")
    service.ticket(booking.id)
    before_instances, before_index = service.instance_count, service.route_index_size
    advance(timedelta(days=2))  # 两段都已经落地
    removed = service.purge_flown_before(clock())
    assert removed == 2  # leg1 和 leg2 都被摘掉（按对象去重，别名不重复计数）
    assert service.instance_count == before_instances - 2
    assert service.route_index_size < before_index
    with pytest.raises(impl.BookingNotFoundError):
        service.booking(booking.id)  # 全程已飞完的订单被一并归档清掉


def test_concurrent_holds_never_oversell_a_cabin():
    policy = impl.percent_overbooking({impl.CabinClass.ECONOMY: 50})  # 2 座 -> 授权卖 3 张
    service, leg1, _ = build(overbooking=policy, economy=2)
    itinerary = impl.Itinerary((impl.Segment(leg1, impl.CabinClass.ECONOMY),))
    n_threads = 12
    barrier = threading.Barrier(n_threads)
    results: list[bool] = [False] * n_threads

    def worker(i: int) -> None:
        barrier.wait()
        try:
            service.hold(itinerary, passenger=f"p{i}")
            results[i] = True
        except impl.NoSeatsAvailableError:
            results[i] = False

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # 授权数是 3（2 座 + 50% 超售 = 1），永远不能被卖穿，也不能少卖。
    assert sum(results) == 3
    assert leg1.available(impl.CabinClass.ECONOMY) == 0
    assert len(leg1.refs_in(impl.CabinClass.ECONOMY)) == 3
