"""酒店预订参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import date, datetime, timedelta, UTC

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

MONDAY = date(2026, 6, 1)  # 2026-06-01 是星期一


def make_clock(start: datetime = datetime(2026, 6, 1, 14, 0, tzinfo=UTC)):
    """一个可以手动拨动的假时钟。"""
    state = {"now": start}

    def clock() -> datetime:
        return state["now"]

    def advance(delta: timedelta) -> None:
        state["now"] += delta

    return clock, advance


def rooms(doubles: int = 2, suites: int = 1):
    return ([impl.Room(number=f"1{i:02d}", type=impl.RoomType.DOUBLE, floor=1)
             for i in range(1, doubles + 1)]
            + [impl.Room(number=f"2{i:02d}", type=impl.RoomType.SUITE, floor=2)
               for i in range(1, suites + 1)])


def flat():
    return impl.flat_nightly({impl.RoomType.SINGLE: 30000, impl.RoomType.DOUBLE: 48000,
                              impl.RoomType.DELUXE: 80000, impl.RoomType.SUITE: 120000})


def build(clock=None, doubles=2, suites=1, rate=None, overbooking=None, city="Sanya"):
    """造一个只有一家酒店的服务，返回 (service, hotel)。"""
    clock = clock or make_clock()[0]
    hotel = impl.Hotel("H1", "Seaside", city, rooms(doubles, suites),
                       overbooking=overbooking or impl.no_overbooking)
    service = impl.HotelService(clock=clock, rate=rate or flat())
    service.register(hotel)
    return service, hotel


def stay(offset_days: int = 0, nights: int = 3) -> "impl.Stay":
    start = MONDAY + timedelta(days=offset_days)
    return impl.Stay(check_in=start, check_out=start + timedelta(days=nights))


# ---- 第 1 关：房型、房间与一段日期的预订 ------------------------------------


def test_a_stay_is_a_half_open_range_of_nights():
    s = impl.Stay(check_in=MONDAY, check_out=MONDAY + timedelta(days=3))
    assert s.nights == 3
    assert list(s.each_night()) == [MONDAY, MONDAY + timedelta(days=1), MONDAY + timedelta(days=2)]
    # 退房当天不算占用：3 号退房和 3 号入住不冲突
    assert not s.overlaps(impl.Stay(check_in=s.check_out, check_out=s.check_out + timedelta(days=1)))
    assert s.overlaps(impl.Stay(check_in=MONDAY + timedelta(days=2), check_out=MONDAY + timedelta(days=9)))


def test_a_stay_must_have_at_least_one_night():
    with pytest.raises(impl.InvalidStayError):
        impl.Stay(check_in=MONDAY, check_out=MONDAY)
    with pytest.raises(impl.InvalidStayError):
        impl.Stay(check_in=MONDAY, check_out=MONDAY - timedelta(days=1))


def test_booking_a_range_consumes_one_room_on_every_night_only():
    service, hotel = build(doubles=2)
    s = stay(nights=3)
    service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_in) == 1
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_out - timedelta(days=1)) == 1
    # 退房当天那一晚完全没有被占
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_out) == 2
    assert hotel.inventory.tracked_nights == 3


def test_a_booking_names_a_room_type_not_a_room_number():
    service, hotel = build(doubles=2, suites=1)
    assert hotel.room_types() == (impl.RoomType.DOUBLE, impl.RoomType.SUITE)
    assert hotel.inventory.capacity_of(impl.RoomType.DOUBLE) == 2
    assert hotel.inventory.capacity_of(impl.RoomType.SINGLE) == 0
    booking = service.book("H1", impl.RoomType.DOUBLE, stay(), guest="chi")
    assert booking.room_type is impl.RoomType.DOUBLE
    assert booking.room_number is None            # 房号要到入住时才定
    assert booking.status is impl.BookingStatus.RESERVED


def test_search_only_returns_hotels_free_on_every_night_of_the_range():
    service, hotel = build(doubles=1, city="Sanya")
    s = stay(nights=3)
    assert [h.id for h in service.search("Sanya", impl.RoomType.DOUBLE, s)] == ["H1"]
    service.book("H1", impl.RoomType.DOUBLE, impl.Stay(check_in=s.check_in + timedelta(days=1),
                                                       check_out=s.check_in + timedelta(days=2)),
                 guest="chi")
    # 中间那一晚满了，整段就搜不到这家店
    assert service.search("Sanya", impl.RoomType.DOUBLE, s) == ()
    assert service.search("Beijing", impl.RoomType.DOUBLE, s) == ()


def test_unknown_hotel_and_unknown_booking_raise():
    service, _ = build()
    with pytest.raises(impl.HotelNotFoundError):
        service.book("NOPE", impl.RoomType.DOUBLE, stay(), guest="chi")
    with pytest.raises(impl.BookingNotFoundError):
        service.booking("R-nope")


# ---- 第 2 关：区间可订量与"多晚预订必须整段原子" ----------------------------


def test_min_available_is_the_tightest_night_not_the_first():
    service, hotel = build(doubles=2)
    s = stay(nights=3)
    tight = impl.Stay(check_in=s.check_in + timedelta(days=1), check_out=s.check_in + timedelta(days=2))
    service.book("H1", impl.RoomType.DOUBLE, tight, guest="chi")
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_in) == 2
    assert hotel.inventory.min_available(impl.RoomType.DOUBLE, s) == 1


def test_a_multi_night_booking_is_all_or_nothing():
    """经典 bug：五晚里前三晚扣成功、第四晚满了，客人被扣了库存却没有订单。"""
    service, hotel = build(doubles=1)
    s = stay(nights=5)
    blocked = impl.Stay(check_in=s.check_in + timedelta(days=3), check_out=s.check_in + timedelta(days=4))
    service.book("H1", impl.RoomType.DOUBLE, blocked, guest="early")
    before = hotel.inventory.tracked_nights
    with pytest.raises(impl.NoAvailabilityError):
        service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    assert hotel.inventory.tracked_nights == before          # 一晚都没被写进去
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_in) == 1


def test_cancelling_returns_every_night_and_leaves_no_zero_buckets():
    service, hotel = build(doubles=1)
    s = stay(nights=4)
    booking = service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    assert hotel.inventory.tracked_nights == 4
    service.cancel(booking.id)
    assert hotel.inventory.min_available(impl.RoomType.DOUBLE, s) == 1
    assert hotel.inventory.tracked_nights == 0               # 归零的格子被删掉，不留空壳


def test_purging_past_nights_shrinks_the_counter_table():
    service, hotel = build(doubles=2)
    s = stay(nights=3)
    service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    assert service.purge_nights_before(s.check_in) == 0
    assert service.purge_nights_before(s.check_in + timedelta(days=1)) == 1
    assert hotel.inventory.tracked_nights == 2
    assert service.purge_nights_before(s.check_out) == 2
    assert hotel.inventory.tracked_nights == 0


def test_cancelling_twice_is_refused_so_inventory_is_returned_once():
    service, hotel = build(doubles=1)
    s = stay(nights=2)
    booking = service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    service.cancel(booking.id)
    with pytest.raises(impl.InvalidTransitionError):
        service.cancel(booking.id)
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_in) == 1


# ---- 第 3 关：并发抢最后一间、入住/退房状态机 -------------------------------


def test_many_threads_racing_for_the_last_room_win_exactly_once():
    service, hotel = build(doubles=1)
    s = stay(nights=3)
    workers = 16
    barrier = threading.Barrier(workers)
    guard = threading.Lock()
    won: list[str] = []

    def book(i: int) -> None:
        barrier.wait()
        try:
            booking = service.book("H1", impl.RoomType.DOUBLE, s, guest=f"g{i}")
        except impl.NoAvailabilityError:
            return
        with guard:
            won.append(booking.id)

    threads = [threading.Thread(target=book, args=(i,)) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(won) == 1
    assert hotel.inventory.min_available(impl.RoomType.DOUBLE, s) == 0


def test_concurrent_overlapping_ranges_never_oversell_any_single_night():
    """每个线程订的区间都不一样，但都压在同一批晚上：任何一晚都不能超过房量。"""
    service, hotel = build(doubles=3)
    workers = 24
    barrier = threading.Barrier(workers)
    guard = threading.Lock()
    booked: list["impl.Stay"] = []

    def book(i: int) -> None:
        s = impl.Stay(check_in=MONDAY + timedelta(days=i % 4),
                      check_out=MONDAY + timedelta(days=i % 4 + 2))
        barrier.wait()
        try:
            service.book("H1", impl.RoomType.DOUBLE, s, guest=f"g{i}")
        except impl.NoAvailabilityError:
            return
        with guard:
            booked.append(s)

    threads = [threading.Thread(target=book, args=(i,)) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    expected: dict[date, int] = {}
    for s in booked:
        for night in s.each_night():
            expected[night] = expected.get(night, 0) + 1
    for offset in range(6):
        night = MONDAY + timedelta(days=offset)
        taken = 3 - hotel.inventory.available_on(impl.RoomType.DOUBLE, night)
        assert taken == expected.get(night, 0)   # 账面和成功的订单逐晚对得上
        assert 0 <= taken <= 3                   # 任何一晚都没有超卖
    assert hotel.inventory.tracked_nights == len(expected)


def test_concurrent_cancels_return_the_inventory_exactly_once():
    service, hotel = build(doubles=1)
    s = stay(nights=2)
    booking = service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    workers = 8
    barrier = threading.Barrier(workers)
    guard = threading.Lock()
    ok: list[int] = []

    def cancel() -> None:
        barrier.wait()
        try:
            service.cancel(booking.id)
        except impl.InvalidTransitionError:
            return
        with guard:
            ok.append(1)

    threads = [threading.Thread(target=cancel) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(ok) == 1
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_in) == 1


def test_check_in_assigns_a_physical_room_and_check_out_gives_it_back():
    clock, _ = make_clock()
    service, hotel = build(clock=clock, doubles=2)
    s = stay(nights=2)
    first = service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    second = service.book("H1", impl.RoomType.DOUBLE, s, guest="lee")
    room_a = service.check_in(first.id)
    room_b = service.check_in(second.id)
    assert room_a.number != room_b.number                    # 两位客人不会被塞进同一间房
    assert room_a.type is impl.RoomType.DOUBLE
    assert hotel.front_desk.occupied_count == 2
    assert service.booking(first.id).room_number == room_a.number
    service.check_out(first.id)
    assert hotel.front_desk.occupied_count == 1
    assert service.booking(first.id).status is impl.BookingStatus.CHECKED_OUT


def test_the_lifecycle_transition_table_refuses_illegal_moves():
    clock, _ = make_clock()
    service, _ = build(clock=clock)
    booking = service.book("H1", impl.RoomType.DOUBLE, stay(nights=2), guest="chi")
    with pytest.raises(impl.InvalidTransitionError):
        service.check_out(booking.id)                        # 没入住不能退房
    service.check_in(booking.id)
    with pytest.raises(impl.InvalidTransitionError):
        service.check_in(booking.id)                         # 不能重复入住
    with pytest.raises(impl.InvalidTransitionError):
        service.cancel(booking.id)                           # 已入住不能取消
    service.check_out(booking.id)
    with pytest.raises(impl.InvalidTransitionError):
        service.check_out(booking.id)


def test_checking_in_outside_the_stay_is_refused():
    clock, advance = make_clock()
    service, hotel = build(clock=clock)
    booking = service.book("H1", impl.RoomType.DOUBLE, stay(offset_days=5, nights=2), guest="chi")
    with pytest.raises(impl.InvalidTransitionError):
        service.check_in(booking.id)                         # 提前五天来办入住
    assert hotel.front_desk.occupied_count == 0              # 也没有白占一间房
    advance(timedelta(days=5))
    assert service.check_in(booking.id).type is impl.RoomType.DOUBLE


def test_check_out_does_not_give_the_nights_back_to_inventory():
    clock, _ = make_clock()
    service, hotel = build(clock=clock, doubles=1)
    s = stay(nights=2)
    booking = service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    service.check_in(booking.id)
    service.check_out(booking.id)
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, s.check_in) == 0
    assert hotel.front_desk.occupied_count == 0


# ---- 第 4 关：超卖政策与按夜动态定价（都没碰库存结构） ---------------------


def test_overbooking_policy_sells_more_than_the_physical_rooms():
    service, hotel = build(doubles=4, overbooking=impl.percent_overbooking(25))
    s = stay(nights=2)
    assert hotel.inventory.min_available(impl.RoomType.DOUBLE, s) == 5   # 4 间 + 25%
    for i in range(5):
        service.book("H1", impl.RoomType.DOUBLE, s, guest=f"g{i}")
    with pytest.raises(impl.NoAvailabilityError):
        service.book("H1", impl.RoomType.DOUBLE, s, guest="late")


def test_overbooking_is_paid_for_at_the_front_desk():
    """超卖的代价不在库存层，而在前台：第 5 位客人没有实体房可分。"""
    clock, _ = make_clock()
    service, _ = build(clock=clock, doubles=4, overbooking=impl.percent_overbooking(25))
    s = stay(nights=2)
    bookings = [service.book("H1", impl.RoomType.DOUBLE, s, guest=f"g{i}") for i in range(5)]
    for booking in bookings[:4]:
        service.check_in(booking.id)
    with pytest.raises(impl.NoRoomToAssignError):
        service.check_in(bookings[4].id)
    assert service.booking(bookings[4].id).status is impl.BookingStatus.RESERVED


def test_weekday_overbooking_only_loosens_monday_to_thursday():
    service, hotel = build(doubles=10, overbooking=impl.weekday_overbooking(20))
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, MONDAY) == 12
    assert hotel.inventory.available_on(impl.RoomType.DOUBLE, MONDAY + timedelta(days=4)) == 10


def test_weekend_uplift_prices_friday_and_saturday_higher():
    rate = impl.weekend_uplift(flat(), 13, 10)
    service, _ = build(rate=rate)
    weekdays = impl.Stay(check_in=MONDAY, check_out=MONDAY + timedelta(days=2))
    weekend = impl.Stay(check_in=MONDAY + timedelta(days=4), check_out=MONDAY + timedelta(days=6))
    assert service.quote("H1", impl.RoomType.DOUBLE, weekdays) == 48000 * 2
    assert service.quote("H1", impl.RoomType.DOUBLE, weekend) == 48000 * 13 // 10 * 2


def test_scarcity_uplift_reads_the_remaining_count_it_is_given():
    rate = impl.scarcity_uplift(flat(), threshold=1, numerator=15, denominator=10)
    service, _ = build(doubles=2, rate=rate)
    s = stay(nights=1)
    assert service.quote("H1", impl.RoomType.DOUBLE, s) == 48000       # 还剩 2 间，原价
    service.book("H1", impl.RoomType.DOUBLE, s, guest="chi")
    assert service.quote("H1", impl.RoomType.DOUBLE, s) == 48000 * 15 // 10   # 只剩 1 间，加价


def test_the_quote_uses_the_availability_before_this_booking_consumes_it():
    """先报价后扣减：自己的这一间不能把自己推进"剩余紧张"的档位。"""
    rate = impl.scarcity_uplift(flat(), threshold=1, numerator=15, denominator=10)
    service, _ = build(doubles=2, rate=rate)
    booking = service.book("H1", impl.RoomType.DOUBLE, stay(nights=1), guest="chi")
    assert booking.amount == 48000
