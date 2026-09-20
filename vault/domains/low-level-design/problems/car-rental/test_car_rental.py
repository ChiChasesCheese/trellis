"""租车系统的验收测试。用 `IMPL=starter` 跑同一套即可验证自己的实现。"""

from __future__ import annotations

import importlib
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

BASE = datetime(2026, 7, 1, 9, 0, tzinfo=UTC)
PVG, HQ, NKG = "SH-PVG", "SH-HQ", "NJ-CN"


def hours(offset: int) -> datetime:
    return BASE + timedelta(hours=offset)


def period(start: int, end: int):
    return impl.RentalPeriod(hours(start), hours(end))


def make_fleet(*specs, turnaround: int = 1):
    """specs: (车牌, 车型, 基地门店)。"""
    vehicles = [impl.Vehicle(plate, category, branch) for plate, category, branch in specs]
    return impl.Fleet(vehicles, turnaround=timedelta(hours=turnaround))


def make_service(fleet, clock, **kwargs):
    components = [
        impl.category_rate({impl.VehicleCategory.SUV: 4000, impl.VehicleCategory.ECONOMY: 1500}),
        impl.one_way_fee(30000),
        impl.extras_fee({"insurance": 500}),
        impl.loyalty_discount({"gold": 10}),
    ]
    return impl.RentalService(fleet, clock=clock, components=components, **kwargs)


def request(category, start, end, pickup=PVG, dropoff=None, **kwargs):
    return impl.RentalRequest(category, period(start, end), pickup, dropoff or pickup, **kwargs)


# ---- 第 1 关：小时粒度的租期与按门店查可用 ------------------------------------

def test_period_is_half_open_and_billed_by_the_ceiling_hour():
    assert period(0, 3).hours == 3
    assert impl.RentalPeriod(BASE, BASE + timedelta(minutes=10)).hours == 1
    assert impl.RentalPeriod(BASE, BASE + timedelta(hours=2, minutes=1)).hours == 3
    with pytest.raises(impl.InvalidPeriodError):
        impl.RentalPeriod(hours(5), hours(5))


def test_available_plates_respects_the_turnaround_gap():
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG), turnaround=2)
    fleet.claim(impl.VehicleCategory.SUV, PVG, period(0, 10), PVG, "R1")
    # 10 点还车 + 2 小时周转 ⇒ 11 点起租排不下，12 点起租可以。
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(11, 20), PVG) == ()
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(12, 20), PVG) == ("A1",)


# ---- 第 2 关：异地还车——可用性取决于车"将会在哪" ------------------------------

def test_a_one_way_rental_moves_the_car_so_the_origin_branch_loses_it():
    """这道题的核心断言：没有任何时间重叠，车却不在这个门店，所以租不到。"""
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    fleet.claim(impl.VehicleCategory.SUV, PVG, period(0, 10), HQ, "R1")
    assert fleet.location_of("A1", hours(20)) == HQ
    # 20–24 点与 R1 毫无重叠，纯重叠判据会放行——但车已经在虹桥了。
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(20, 24), PVG) == ()
    assert fleet.available_plates(impl.VehicleCategory.SUV, HQ, period(20, 24), HQ) == ("A1",)


def test_location_before_a_future_one_way_leg_is_still_the_old_branch():
    """异地还车只从它结束之后才生效：之前在浦东租仍然租得到。"""
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    fleet.claim(impl.VehicleCategory.SUV, PVG, period(100, 110), HQ, "R1")
    assert fleet.location_of("A1", hours(50)) == PVG
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(50, 60), PVG) == ("A1",)


def test_a_new_leg_may_not_break_the_origin_of_a_later_leg():
    """插在两段之间的一段异地租约，会让后一段的取车门店对不上，必须被拒。"""
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    fleet.claim(impl.VehicleCategory.SUV, PVG, period(100, 110), PVG, "R_LATE")
    # 20–30 点把车开去南京，100 点在浦东的那单就没车了 ⇒ 这一单必须排不下。
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(20, 30), NKG) == ()
    # 同样的时段、还回浦东，就排得下。
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(20, 30), PVG) == ("A1",)


def test_cancelling_shrinks_the_timeline_and_gives_the_car_back():
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    fleet.claim(impl.VehicleCategory.SUV, PVG, period(0, 10), HQ, "R1")
    assert fleet.scheduled_leg_count == 1
    assert fleet.release("A1", "R1") is True
    assert fleet.scheduled_leg_count == 0
    assert fleet.location_of("A1", hours(20)) == PVG


# ---- 第 3 关：取还车状态机与现实中的失败 --------------------------------------

def test_pick_up_and_return_walk_the_state_machine():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now)
    booking = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    assert booking.status is impl.RentalStatus.RESERVED
    service.pick_up(booking.id)
    assert service.reservation(booking.id).status is impl.RentalStatus.PICKED_UP
    with pytest.raises(impl.InvalidTransitionError):
        service.cancel(booking.id)
    now = hours(10)
    outcome = service.return_vehicle(booking.id)
    assert outcome.late_hours == 0 and outcome.charges == ()
    assert service.reservation(booking.id).status is impl.RentalStatus.RETURNED
    with pytest.raises(impl.InvalidTransitionError):
        service.return_vehicle(booking.id)


def test_a_late_return_charges_and_displaces_the_next_reservation():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now, late_fee_per_hour=1000)
    first = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    second = service.reserve("lee", request(impl.VehicleCategory.SUV, 12, 20))
    assert second.plate == "A1"
    service.pick_up(first.id)
    now = hours(15)
    outcome = service.return_vehicle(first.id)
    assert outcome.late_hours == 5
    assert outcome.charges == (impl.Charge("late", 5000),)
    # 车队只有一辆车 ⇒ 第二单救不回来，但单子还在，只是没车。
    assert outcome.unassigned == (second.id,)
    assert service.reservation(second.id).plate is None
    assert service.reservation(second.id).status is impl.RentalStatus.RESERVED
    with pytest.raises(impl.NoVehicleAvailableError):
        service.pick_up(second.id)


def test_a_displaced_reservation_is_reassigned_when_another_car_is_free():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG), ("A2", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now)
    first = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    second = service.reserve("lee", request(impl.VehicleCategory.SUV, 12, 20))
    # 车队会先把车排满：两单都落在 A1 上，A2 完全空着。
    assert first.plate == second.plate == "A1"
    service.pick_up(first.id)
    now = hours(15)
    outcome = service.return_vehicle(first.id)
    assert outcome.reassigned == (second.id,) and outcome.unassigned == ()
    assert service.reservation(second.id).plate == "A2"
    assert fleet.scheduled_leg_count == 2


def test_damage_at_return_blocks_the_car_for_repair():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now, repair=timedelta(hours=48))
    first = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    later = service.reserve("lee", request(impl.VehicleCategory.SUV, 30, 40))
    service.pick_up(first.id)
    now = hours(10)
    outcome = service.return_vehicle(first.id, damaged=True)
    assert outcome.unassigned == (later.id,)
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(30, 40), PVG) == ()
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(60, 70), PVG) == ("A1",)


def test_returning_to_the_wrong_branch_is_charged_and_moves_the_car():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now, wrong_branch_fee=7777)
    booking = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    service.pick_up(booking.id)
    now = hours(10)
    outcome = service.return_vehicle(booking.id, branch=NKG)
    assert impl.Charge("wrong_branch", 7777) in outcome.charges
    assert fleet.location_of("A1", hours(11)) == NKG


def test_no_show_releases_the_car_only_after_the_grace_period():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now, grace=timedelta(hours=2), no_show_fee=4200)
    booking = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    now = hours(1)
    with pytest.raises(impl.InvalidTransitionError):
        service.mark_no_show(booking.id)
    now = hours(3)
    service.mark_no_show(booking.id)
    assert service.reservation(booking.id).status is impl.RentalStatus.NO_SHOW
    assert service.reservation(booking.id).total == booking.quote.total + 4200
    assert fleet.scheduled_leg_count == 0


def test_pick_up_is_refused_when_the_car_is_no_longer_at_the_branch():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now)
    booking = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    # 运营把车调去了南京（用一段维修/调拨封锁表达），取车时必须当场发现。
    fleet.block("A1", period(-5, -1), NKG, "TRANSFER")
    with pytest.raises(impl.NoVehicleAvailableError):
        service.pick_up(booking.id)


# ---- 第 4 关：计费与并发 -------------------------------------------------------

def test_quote_lines_are_itemised_and_the_discount_applies_to_the_subtotal():
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: BASE)
    quote = service.quote(request(impl.VehicleCategory.SUV, 0, 30, dropoff=HQ,
                                  tier="gold", extras=("insurance",)))
    codes = {line.code: line.amount for line in quote.lines}
    # 30 小时 = 1 天（封顶 20 小时）+ 6 小时 = 26 个计费小时。
    assert codes["base"] == 4000 * 26
    assert codes["one_way"] == 30000
    assert codes["extras"] == 500 * 30
    assert codes["loyalty"] == -((codes["base"] + codes["one_way"] + codes["extras"]) * 10 // 100)
    assert quote.total == sum(codes.values())


def test_no_surcharge_lines_appear_for_a_plain_local_rental():
    fleet = make_fleet(("A1", impl.VehicleCategory.ECONOMY, PVG))
    service = make_service(fleet, lambda: BASE)
    quote = service.quote(request(impl.VehicleCategory.ECONOMY, 0, 5))
    assert [line.code for line in quote.lines] == ["base"]


def test_concurrent_reservations_never_oversell_the_last_car():
    """两个客人同时抢同一门店最后一辆车：恰好一个成功，时间轴上恰好一段。"""
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now)
    wanted = request(impl.VehicleCategory.SUV, 0, 10)
    barrier = threading.Barrier(8)
    won: list[str] = []
    lost: list[str] = []
    guard = threading.Lock()

    def attempt(name: str) -> None:
        barrier.wait()
        try:
            booking = service.reserve(name, wanted)
        except impl.NoVehicleAvailableError:
            with guard:
                lost.append(name)
        else:
            with guard:
                won.append(booking.id)

    threads = [threading.Thread(target=attempt, args=(f"c{i}",)) for i in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(won) == 1, f"oversold: {won}"
    assert len(lost) == 7
    assert fleet.scheduled_leg_count == 1


def test_concurrent_cancels_release_the_car_exactly_once():
    now = BASE
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    service = make_service(fleet, lambda: now)
    booking = service.reserve("chi", request(impl.VehicleCategory.SUV, 0, 10))
    barrier = threading.Barrier(6)
    outcomes: list[bool] = []
    guard = threading.Lock()

    def attempt() -> None:
        barrier.wait()
        try:
            service.cancel(booking.id)
        except impl.InvalidTransitionError:
            ok = False
        else:
            ok = True
        with guard:
            outcomes.append(ok)

    threads = [threading.Thread(target=attempt) for _ in range(6)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sum(outcomes) == 1
    assert fleet.scheduled_leg_count == 0


# ---- 时间轴必须会缩 ------------------------------------------------------------

def test_purging_history_absorbs_the_last_known_location():
    """清理历史段之前必须把"车最后停在哪"吸收进起点，否则车会瞬移回基地。"""
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    fleet.claim(impl.VehicleCategory.SUV, PVG, period(0, 10), HQ, "R1")
    fleet.claim(impl.VehicleCategory.SUV, HQ, period(20, 30), NKG, "R2")
    assert fleet.scheduled_leg_count == 2
    assert fleet.purge_before(hours(15)) == 1
    assert fleet.scheduled_leg_count == 1
    assert fleet.location_of("A1", hours(16)) == HQ
    assert fleet.purge_before(hours(100)) == 1
    assert fleet.scheduled_leg_count == 0
    assert fleet.location_of("A1", hours(200)) == NKG
    # 起点前移之后，浦东仍然租不到这辆车——它确实在南京。
    assert fleet.available_plates(impl.VehicleCategory.SUV, PVG, period(200, 210), PVG) == ()


def test_a_long_horizon_of_bookings_costs_only_one_leg_each():
    """小时粒度 + 几个月的排期，代价是「预约条数」而不是「小时格子数」。"""
    fleet = make_fleet(("A1", impl.VehicleCategory.ECONOMY, PVG))
    for index in range(60):
        start = index * 72
        fleet.claim(impl.VehicleCategory.ECONOMY, PVG, period(start, start + 4), PVG, f"R{index}")
    assert fleet.scheduled_leg_count == 60
    assert fleet.purge_before(hours(60 * 72)) == 60
    assert fleet.scheduled_leg_count == 0


def test_public_api_of_the_schedule_is_read_only():
    """时间轴只交出快照；改快照不会改到里面。"""
    fleet = make_fleet(("A1", impl.VehicleCategory.SUV, PVG))
    fleet.claim(impl.VehicleCategory.SUV, PVG, period(0, 10), PVG, "R1")
    schedule = impl.VehicleSchedule(impl.Vehicle("B1", impl.VehicleCategory.SUV, PVG))
    schedule.add(impl.ScheduleLeg("X", period(0, 10), PVG, PVG))
    snapshot = schedule.legs()
    assert isinstance(snapshot, tuple) and schedule.leg_count == 1
    with pytest.raises((AttributeError, TypeError)):
        snapshot[0].destination = NKG  # type: ignore[misc]
