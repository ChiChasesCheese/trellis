"""网约车参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import datetime, timedelta, UTC
from fractions import Fraction

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T0 = datetime(2026, 9, 20, 8, 0, tzinfo=UTC)


def make_clock(start: datetime = T0):
    """一个可以手动拨动的假时钟：`clock()` 读当前值，`advance()` 往前拨。"""
    state = {"now": start}

    def clock() -> datetime:
        return state["now"]

    def advance(delta: timedelta) -> None:
        state["now"] += delta

    return clock, advance


def build(clock, drivers=(("d1", 1.0, 0.0, 5.0, 4), ("d2", 3.0, 0.0, 5.0, 4)),
          match=None, surge=None, offer_ttl=timedelta(seconds=15),
          fares=None, max_detour_km=2.0, online=True):
    """造一个司机都已上线的派单服务，返回 (service, pool)。"""
    pool = impl.DriverPool(clock=clock)
    for driver_id, x, y, rating, seats in drivers:
        pool.register(driver_id, rating=rating, seats=seats)
        if online:
            pool.go_online(driver_id, impl.Location(x, y))
    service = impl.DispatchService(
        clock=clock, pool=pool,
        fares=fares or impl.FareTable(base=1000, per_km=200, per_minute=50),
        match=match or impl.nearest_driver, surge=surge or impl.no_surge,
        offer_ttl=offer_ttl, max_detour_km=max_detour_km)
    return service, pool


def ride(rider_id="r1", pickup=(0.0, 0.0), dropoff=(3.0, 4.0), seats=1):
    return impl.RideRequest(rider_id, impl.Location(*pickup), impl.Location(*dropoff), seats)


def matched(service, request):
    """叫车并让被要约的那位司机立刻接单，返回行程。"""
    trip = service.request_ride(request)
    service.accept(service.open_offer(trip.id).id)
    return trip


# ---- 第 1 关：要约、状态机 ---------------------------------------------------


def test_a_new_request_is_offered_to_one_driver_and_not_assigned():
    """叫车之后行程还在 REQUESTED：司机只是"被问到了"，没有被分配。"""
    clock, _ = make_clock()
    service, pool = build(clock)
    trip = service.request_ride(ride())
    offer = service.open_offer(trip.id)
    assert trip.state is impl.TripState.REQUESTED
    assert offer is not None and offer.driver_id == "d1"
    assert pool.driver("d1").status is impl.DriverStatus.OFFERED
    assert pool.driver("d2").status is impl.DriverStatus.AVAILABLE
    assert trip.driver_id is None


def test_an_offered_driver_is_held_exclusively_and_cannot_be_offered_twice():
    """要约敞开期间司机被独占，第二位乘客拿不到他——这是本题最核心的不变量。"""
    clock, _ = make_clock()
    service, pool = build(clock, drivers=(("d1", 1.0, 0.0, 5.0, 4),))
    service.request_ride(ride("r1"))
    with pytest.raises(impl.NoDriverAvailableError):
        service.request_ride(ride("r2"))
    assert pool.available_count == 0


def test_accept_matches_the_trip_and_puts_the_driver_on_trip():
    clock, _ = make_clock()
    service, pool = build(clock)
    trip = service.request_ride(ride())
    trip = service.accept(service.open_offer(trip.id).id)
    assert trip.state is impl.TripState.MATCHED
    assert trip.driver_id == "d1"
    assert pool.driver("d1").status is impl.DriverStatus.ON_TRIP
    assert pool.driver("d1").trip_id == trip.id
    assert service.open_offer(trip.id) is None
    assert service.open_offer_count == 0


def test_the_whole_lifecycle_is_recorded_in_order():
    clock, advance = make_clock()
    service, pool = build(clock)
    trip = matched(service, ride())
    service.driver_arrived(trip.id)
    advance(timedelta(minutes=3))
    service.start_trip(trip.id)
    advance(timedelta(minutes=12))
    trip = service.complete_trip(trip.id)
    assert trip.state is impl.TripState.COMPLETED
    assert [c.current for c in trip.history] == [
        impl.TripState.MATCHED, impl.TripState.ARRIVED,
        impl.TripState.IN_PROGRESS, impl.TripState.COMPLETED]
    assert pool.driver("d1").status is impl.DriverStatus.AVAILABLE
    assert pool.driver("d1").location == impl.Location(3.0, 4.0)


def test_illegal_transitions_raise_instead_of_being_ignored():
    """状态机跳步必须报错——被吞掉的非法转移会让调用方以为车已经开了。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    trip = matched(service, ride())
    with pytest.raises(impl.IllegalTransitionError):
        service.start_trip(trip.id)          # 还没到达
    with pytest.raises(impl.IllegalTransitionError):
        service.complete_trip(trip.id)       # 还没上车
    assert trip.state is impl.TripState.MATCHED


# ---- 第 2 关：拒单、超时、不把乘客晾着 ---------------------------------------


def test_a_declining_driver_is_released_and_the_next_one_is_offered():
    clock, _ = make_clock()
    service, pool = build(clock)
    trip = service.request_ride(ride())
    first = service.open_offer(trip.id)
    service.decline(first.id)
    second = service.open_offer(trip.id)
    assert second is not None and second.driver_id == "d2"
    assert pool.driver("d1").status is impl.DriverStatus.AVAILABLE
    assert trip.state is impl.TripState.REQUESTED
    assert service.open_offer_count == 1


def test_a_declined_driver_is_never_offered_the_same_trip_again():
    """排除集必须存在：否则打分最高的那位会被反复骚扰，乘客永远等不到车。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    trip = service.request_ride(ride())
    seen = []
    while (offer := service.open_offer(trip.id)) is not None:
        seen.append(offer.driver_id)
        service.decline(offer.id)
    assert seen == ["d1", "d2"]
    assert len(set(seen)) == len(seen)


def test_when_every_driver_declines_the_trip_is_cancelled_by_the_system():
    """候选耗尽就给一个确定的失败，而不是把行程永远停在"正在找车"。"""
    clock, _ = make_clock()
    service, pool = build(clock)
    trip = service.request_ride(ride())
    service.decline(service.open_offer(trip.id).id)
    service.decline(service.open_offer(trip.id).id)
    assert trip.state is impl.TripState.CANCELLED
    assert trip.history[-1].by is impl.Party.SYSTEM
    assert trip.history[-1].reason is not None
    assert service.open_offer_count == 0
    assert pool.available_count == 2


def test_a_silent_driver_times_out_and_the_ride_moves_on():
    clock, advance = make_clock()
    service, pool = build(clock, offer_ttl=timedelta(seconds=15))
    trip = service.request_ride(ride())
    advance(timedelta(seconds=16))
    assert service.expire_offers() == 1
    assert service.open_offer(trip.id).driver_id == "d2"
    assert pool.driver("d1").status is impl.DriverStatus.AVAILABLE
    assert trip.state is impl.TripState.REQUESTED


def test_an_expired_offer_is_refused_even_before_the_sweep_runs():
    """过期是惰性判断的，所以正确性不依赖清扫任务跑没跑。"""
    clock, advance = make_clock()
    service, _ = build(clock, offer_ttl=timedelta(seconds=15))
    trip = service.request_ride(ride())
    offer = service.open_offer(trip.id)
    advance(timedelta(seconds=30))
    with pytest.raises(impl.OfferExpiredError):
        service.accept(offer.id)
    assert service.open_offer(trip.id).driver_id == "d2"


def test_accepting_an_offer_twice_fails_the_second_time():
    clock, _ = make_clock()
    service, _ = build(clock)
    trip = service.request_ride(ride())
    offer = service.open_offer(trip.id)
    service.accept(offer.id)
    with pytest.raises(impl.OfferExpiredError):
        service.accept(offer.id)


# ---- 取消规则 ---------------------------------------------------------------


def test_a_rider_may_cancel_before_pickup_and_the_driver_goes_back_to_the_pool():
    clock, _ = make_clock()
    service, pool = build(clock)
    trip = matched(service, ride())
    service.driver_arrived(trip.id)
    trip = service.cancel_trip(trip.id, impl.Party.RIDER, "changed my mind")
    assert trip.state is impl.TripState.CANCELLED
    assert pool.driver("d1").status is impl.DriverStatus.AVAILABLE
    assert pool.driver("d1").trip_id is None


def test_nobody_can_cancel_a_trip_in_progress():
    """上车之后"取消"不再有意义；要的是"提前结束并按已走里程计费"，那是另一个动作。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    trip = matched(service, ride())
    service.driver_arrived(trip.id)
    service.start_trip(trip.id)
    for party in (impl.Party.RIDER, impl.Party.DRIVER, impl.Party.SYSTEM):
        with pytest.raises(impl.CancellationNotAllowedError):
            service.cancel_trip(trip.id, party)
    assert trip.state is impl.TripState.IN_PROGRESS


def test_a_driver_cannot_cancel_a_trip_that_has_not_been_matched_yet():
    """还没接单的行程上根本没有"这位司机"，所以司机方无权取消它。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    trip = service.request_ride(ride())
    with pytest.raises(impl.CancellationNotAllowedError):
        service.cancel_trip(trip.id, impl.Party.DRIVER)
    trip = service.cancel_trip(trip.id, impl.Party.RIDER)
    assert trip.state is impl.TripState.CANCELLED
    assert service.open_offer_count == 0


def test_a_busy_driver_cannot_go_offline():
    clock, _ = make_clock()
    service, pool = build(clock)
    trip = service.request_ride(ride())
    with pytest.raises(impl.DriverBusyError):
        pool.go_offline("d1")
    service.accept(service.open_offer(trip.id).id)
    with pytest.raises(impl.DriverBusyError):
        pool.go_offline("d1")
    pool.go_offline("d2")
    assert pool.driver("d2").status is impl.DriverStatus.OFFLINE


# ---- 第 3 关：并发 -----------------------------------------------------------


def test_concurrent_riders_never_share_a_driver():
    """二十位乘客、八位司机同时下单：成交数恰好等于司机数，且没有司机跑两趟。"""
    clock, _ = make_clock()
    fleet = tuple((f"d{i}", float(i), 0.0, 5.0, 4) for i in range(8))
    service, pool = build(clock, drivers=fleet)
    barrier = threading.Barrier(20)
    results: list[str | None] = [None] * 20
    errors: list[int] = []

    def rider(index: int) -> None:
        barrier.wait()
        try:
            trip = service.request_ride(ride(f"r{index}"))
            results[index] = service.accept(service.open_offer(trip.id).id).driver_id
        except impl.NoDriverAvailableError:
            errors.append(index)

    threads = [threading.Thread(target=rider, args=(i,)) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    taken = [d for d in results if d is not None]
    assert len(taken) == 8, "八位司机应当正好成交八单"
    assert len(set(taken)) == 8, "同一位司机不可能同时跑两趟"
    assert len(errors) == 12
    assert all(pool.driver(d).status is impl.DriverStatus.ON_TRIP for d, *_ in fleet)


def test_concurrent_expiry_never_strands_a_rider_in_requested():
    """反复超时清扫（多线程同时扫）之后，不变量仍然成立：REQUESTED ⟺ 有一张敞开的要约。"""
    clock, advance = make_clock()
    fleet = (("d1", 1.0, 0.0, 5.0, 4), ("d2", 2.0, 0.0, 5.0, 4), ("d3", 3.0, 0.0, 5.0, 4))
    service, pool = build(clock, drivers=fleet, offer_ttl=timedelta(seconds=15))
    trips = [service.request_ride(ride(f"r{i}")) for i in range(3)]

    for _ in range(4):
        advance(timedelta(seconds=20))
        barrier = threading.Barrier(4)

        def sweep() -> None:
            barrier.wait()
            service.expire_offers()

        threads = [threading.Thread(target=sweep) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        for trip in trips:
            has_offer = service.open_offer(trip.id) is not None
            assert (trip.state is impl.TripState.REQUESTED) == has_offer

    assert all(t.state is impl.TripState.CANCELLED for t in trips)
    assert service.open_offer_count == 0
    assert pool.available_count == 3


# ---- 第 4 关：匹配策略、计价、拼车 -------------------------------------------


def test_the_match_policy_is_a_seam_rating_can_beat_distance():
    clock, _ = make_clock()
    fleet = (("near", 1.0, 0.0, 4.0, 4), ("far", 3.0, 0.0, 5.0, 4))
    service, _ = build(clock, drivers=fleet, match=impl.nearest_driver)
    assert service.open_offer(service.request_ride(ride("r1")).id).driver_id == "near"

    service2, _ = build(clock, drivers=fleet,
                        match=impl.weighted_score(per_km=1.0, per_rating_point=3.0))
    assert service2.open_offer(service2.request_ride(ride("r2")).id).driver_id == "far"


def test_a_driver_idle_longer_wins_a_tie_on_distance_and_rating():
    """只按距离排，等得久的司机永远抢不到单；空闲时长是司机端公平性的最低限度。"""
    clock, advance = make_clock()
    pool = impl.DriverPool(clock=clock)
    pool.register("early")
    pool.go_online("early", impl.Location(1.0, 0.0))
    advance(timedelta(minutes=5))
    pool.register("late")
    pool.go_online("late", impl.Location(-1.0, 0.0))
    advance(timedelta(minutes=5))
    service = impl.DispatchService(
        clock=clock, pool=pool, fares=impl.FareTable(base=1000, per_km=200, per_minute=50),
        match=impl.weighted_score(per_km=1.0, per_rating_point=0.0, per_idle_minute=1.0))
    trip = service.request_ride(ride())
    assert service.open_offer(trip.id).driver_id == "early"


def test_fare_is_base_plus_distance_plus_time_from_pickup_not_from_request():
    """等车的三分钟不计费：计时起点是上车那一刻。"""
    clock, advance = make_clock()
    service, _ = build(clock, fares=impl.FareTable(base=1000, per_km=200, per_minute=50))
    trip = matched(service, ride(dropoff=(3.0, 4.0)))     # 直线 5 公里
    service.driver_arrived(trip.id)
    advance(timedelta(minutes=3))
    service.start_trip(trip.id)
    advance(timedelta(minutes=12))
    trip = service.complete_trip(trip.id)
    fare = trip.fare_for("r1")
    assert (fare.base, fare.distance, fare.time) == (1000, 1000, 600)
    assert fare.total == 2600


def test_the_surge_multiplier_is_locked_in_when_the_ride_is_requested():
    """下单时看到 1.5 倍，结束时就按 1.5 倍收——事后车多了也不追溯。"""
    clock, advance = make_clock()
    service, pool = build(clock, drivers=(("d1", 1.0, 0.0, 5.0, 4),),
                          surge=impl.demand_surge([(Fraction(1), Fraction(3, 2))]))
    trip = matched(service, ride())
    assert trip.legs[0].surge == Fraction(3, 2)
    for extra in ("d2", "d3", "d4"):                      # 车多起来了
        pool.register(extra)
        pool.go_online(extra, impl.Location(0.5, 0.0))
    service.driver_arrived(trip.id)
    service.start_trip(trip.id)
    advance(timedelta(minutes=10))
    trip = service.complete_trip(trip.id)
    assert trip.fare_for("r1").surge == Fraction(3, 2)
    assert trip.fare_for("r1").total == int((1000 + 1000 + 500) * Fraction(3, 2))


def test_pooling_adds_a_leg_without_touching_the_state_machine():
    clock, advance = make_clock()
    service, _ = build(clock, fares=impl.FareTable(base=1000, per_km=200, per_minute=0))
    trip = matched(service, ride("r1", (0.0, 0.0), (10.0, 0.0)))
    service.driver_arrived(trip.id)
    service.start_trip(trip.id)
    history_before = trip.history
    trip = service.join_trip(trip.id, ride("r2", (2.0, 0.0), (8.0, 0.0)))
    assert trip.state is impl.TripState.IN_PROGRESS
    assert trip.history == history_before, "拼车不是一次状态转移"
    assert [leg.rider_id for leg in trip.legs] == ["r1", "r2"]
    assert trip.seats_taken == 2
    advance(timedelta(minutes=10))
    trip = service.complete_trip(trip.id)
    assert trip.fare_for("r1").total == int((1000 + 2000) * Fraction(4, 5))
    assert trip.fare_for("r2").total == int((1000 + 1200) * Fraction(4, 5))


def test_pooling_is_refused_when_the_detour_or_the_seats_do_not_allow_it():
    clock, _ = make_clock()
    service, _ = build(clock, max_detour_km=2.0)
    trip = matched(service, ride("r1", (0.0, 0.0), (10.0, 0.0)))
    with pytest.raises(impl.SeatUnavailableError):
        service.join_trip(trip.id, ride("r2", (0.0, 5.0), (8.0, 0.0)))    # 绕太远
    with pytest.raises(impl.SeatUnavailableError):
        service.join_trip(trip.id, ride("r3", (2.0, 0.0), (8.0, 0.0), seats=4))
    assert [leg.rider_id for leg in trip.legs] == ["r1"]


def test_an_unmatched_trip_takes_no_pool_rider():
    clock, _ = make_clock()
    service, _ = build(clock)
    trip = service.request_ride(ride("r1", (0.0, 0.0), (10.0, 0.0)))
    with pytest.raises(impl.IllegalTransitionError):
        service.join_trip(trip.id, ride("r2", (2.0, 0.0), (8.0, 0.0)))


def test_requesting_with_nobody_online_fails_and_leaves_no_ghost_trip():
    """一位候选都没有时不建行程——否则就留下一个永远没有要约的 REQUESTED 行程。"""
    clock, _ = make_clock()
    service, _ = build(clock, online=False)
    with pytest.raises(impl.NoDriverAvailableError):
        service.request_ride(ride())
    with pytest.raises(impl.UnknownTripError):
        service.trip("T1")
    assert service.open_offer_count == 0


def test_the_snapshots_handed_out_cannot_corrupt_the_trip():
    """对外只给不可变快照：拿到 `legs` 之后再 append，行程不会跟着变。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    trip = matched(service, ride())
    legs = trip.legs
    assert isinstance(legs, tuple)
    with pytest.raises(AttributeError):
        legs[0].seats = 99
    assert trip.seats_taken == 1
