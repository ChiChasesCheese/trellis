"""停车场参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import datetime, timedelta, UTC
from decimal import Decimal

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def make_clock(start: datetime):
    """一个可以手动拨动的假时钟：`clock()` 返回当前值，`advance()` 往前拨。"""
    state = {"now": start}

    def clock() -> datetime:
        return state["now"]

    def advance(delta: timedelta) -> None:
        state["now"] += delta

    return clock, advance


def make_lot(spots, allocate=None, price=None, clock=None):
    allocate = allocate or impl.nearest_first
    price = price or impl.hourly_rate({
        impl.VehicleSize.MOTORCYCLE: Decimal("2"),
        impl.VehicleSize.COMPACT: Decimal("5"),
        impl.VehicleSize.LARGE: Decimal("8"),
    })
    clock = clock or (lambda: datetime(2026, 1, 1, 9, 0, tzinfo=UTC))
    return impl.ParkingLot(spots, allocate=allocate, price=price, clock=clock)


def compact_spots(floor: int, count: int, prefix: str = ""):
    return [impl.ParkingSpot(id=f"{prefix}{floor}-{i}", floor=floor, size=impl.VehicleSize.COMPACT)
            for i in range(count)]


# ---- 第 1 关：单楼层的入场 / 出场 --------------------------------------------


def test_park_assigns_a_free_spot_and_returns_a_ticket():
    lot = make_lot(compact_spots(1, 2))
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    assert ticket.spot.id == "1-0"
    assert ticket.spot.vehicle.plate == "A1"


def test_park_records_entry_time_from_the_injected_clock():
    now = datetime(2026, 3, 1, 8, 30, tzinfo=UTC)
    lot = make_lot(compact_spots(1, 1), clock=lambda: now)
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    assert ticket.entry_time == now


def test_unpark_frees_the_spot():
    lot = make_lot(compact_spots(1, 1))
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    lot.unpark(ticket.id)
    assert ticket.spot.is_free


def test_park_when_full_raises_no_available_spot():
    lot = make_lot(compact_spots(1, 1))
    lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    with pytest.raises(impl.NoAvailableSpotError):
        lot.park(impl.Vehicle(plate="A2", size=impl.VehicleSize.COMPACT))


def test_unpark_with_unknown_ticket_raises_invalid_ticket():
    lot = make_lot(compact_spots(1, 1))
    with pytest.raises(impl.InvalidTicketError):
        lot.unpark("no-such-ticket")


def test_unpark_twice_with_the_same_ticket_fails_the_second_time():
    lot = make_lot(compact_spots(1, 1))
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    lot.unpark(ticket.id)
    with pytest.raises(impl.InvalidTicketError):
        lot.unpark(ticket.id)


def test_motorcycle_may_use_a_large_spot_but_a_large_car_may_not_use_a_compact_spot():
    small_spot = impl.ParkingSpot(id="s", floor=1, size=impl.VehicleSize.COMPACT)
    large_spot = impl.ParkingSpot(id="l", floor=1, size=impl.VehicleSize.LARGE)
    assert large_spot.fits(impl.Vehicle(plate="M1", size=impl.VehicleSize.MOTORCYCLE))
    assert not small_spot.fits(impl.Vehicle(plate="L1", size=impl.VehicleSize.LARGE))


# ---- 第 2 关：可替换的分配策略与计费策略 --------------------------------------


def test_nearest_first_prefers_the_lowest_floor():
    spots = compact_spots(2, 1, prefix="p") + compact_spots(1, 1, prefix="p")
    lot = make_lot(spots, allocate=impl.nearest_first)
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    assert ticket.spot.floor == 1


def test_spread_across_floors_prefers_the_floor_with_more_free_spots():
    spots = compact_spots(1, 1, prefix="p") + compact_spots(2, 3, prefix="p")
    lot = make_lot(spots, allocate=impl.spread_across_floors)
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    assert ticket.spot.floor == 2


def test_hourly_rate_charges_by_ceiling_hours():
    clock, advance = make_clock(datetime(2026, 1, 1, 9, 0, tzinfo=UTC))
    lot = make_lot(compact_spots(1, 1), clock=clock,
                    price=impl.hourly_rate({impl.VehicleSize.COMPACT: Decimal("5")}))
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    advance(timedelta(hours=2, minutes=1))  # 不足 3 小时也要按 3 小时收
    assert lot.unpark(ticket.id) == Decimal("15")


def test_flat_rate_ignores_duration():
    clock, advance = make_clock(datetime(2026, 1, 1, 9, 0, tzinfo=UTC))
    lot = make_lot(compact_spots(1, 1), clock=clock, price=impl.flat_rate(Decimal("20")))
    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    advance(timedelta(hours=10))
    assert lot.unpark(ticket.id) == Decimal("20")


def test_tiered_rate_charges_each_tier_at_its_own_price():
    tiered = impl.TieredRate(tiers=((1, Decimal("0")), (3, Decimal("4")), (24, Decimal("2"))))
    # 第 1 小时免费，第 2~3 小时每小时 4 元，之后每小时 2 元；停 5 小时：
    # 0 + 2*4 + 2*2 = 12
    fee = tiered(impl.VehicleSize.COMPACT, timedelta(hours=5))
    assert fee == Decimal("12")


def test_tiered_rate_breakdown_reports_each_tier_billed():
    tiered = impl.TieredRate(tiers=((1, Decimal("0")), (3, Decimal("4"))))
    breakdown = tiered.breakdown(timedelta(hours=2, minutes=30))  # 收 3 小时
    assert breakdown == [(1, 1, Decimal("0")), (3, 2, Decimal("4"))]


# ---- 第 3 关：多闸机并发 -----------------------------------------------------
#
# "闸机"不是一个类（见题解「核心对象与职责」），并发多闸机就是多个线程各自直接
# 调用同一个 ParkingLot 的 park/unpark。


def test_concurrent_callers_never_double_assign_a_spot():
    lot = make_lot(compact_spots(1, 5))
    results: list = []
    lock = threading.Lock()
    barrier = threading.Barrier(8)

    def worker(plate):
        barrier.wait()
        try:
            ticket = lot.park(impl.Vehicle(plate=plate, size=impl.VehicleSize.COMPACT))
            with lock:
                results.append(ticket)
        except impl.NoAvailableSpotError:
            pass

    threads = [threading.Thread(target=worker, args=(f"V{i}",)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 5  # 只有 5 个车位，正好停满，一个不多一个不少
    assert len({ticket.spot.id for ticket in results}) == 5  # 没有两张票指向同一个车位


def test_concurrent_callers_free_every_spot_exactly_once():
    spots = compact_spots(1, 6)
    lot = make_lot(spots)
    tickets = [lot.park(impl.Vehicle(plate=f"V{i}", size=impl.VehicleSize.COMPACT)) for i in range(6)]
    barrier = threading.Barrier(6)

    def worker(ticket):
        barrier.wait()
        lot.unpark(ticket.id)

    threads = [threading.Thread(target=worker, args=(t,)) for t in tickets]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(spot.is_free for spot in spots)  # 六个车位全部释放，没有漏放也没有重复释放


# ---- 第 4 关：展示牌、新车型/车位类型，以及不能被绕过的公开接口 -----------------


def test_display_board_updates_on_park_and_unpark_without_touching_parking_lot():
    lot = make_lot(compact_spots(1, 2) + compact_spots(2, 1, prefix="p"))
    board = impl.DisplayBoard(lot)
    assert dict(board.free_by_floor) == {1: 2, 2: 1}

    ticket = lot.park(impl.Vehicle(plate="A1", size=impl.VehicleSize.COMPACT))
    assert board.free_by_floor[ticket.spot.floor] == 1

    lot.unpark(ticket.id)
    assert board.free_by_floor[ticket.spot.floor] == 2


def test_display_board_matches_a_full_recount_after_a_park_and_unpark_storm():
    spots = compact_spots(1, 4) + compact_spots(2, 4, prefix="p")
    lot = make_lot(spots, allocate=impl.nearest_first)
    board = impl.DisplayBoard(lot)

    entry_barrier = threading.Barrier(8)
    tickets: list = [None] * 8

    def enter(i):
        entry_barrier.wait()
        tickets[i] = lot.park(impl.Vehicle(plate=f"V{i}", size=impl.VehicleSize.COMPACT))

    entry_threads = [threading.Thread(target=enter, args=(i,)) for i in range(8)]
    for t in entry_threads:
        t.start()
    for t in entry_threads:
        t.join()
    assert all(tickets)  # 8 个车位、8 辆车，正好停满

    exit_barrier = threading.Barrier(4)

    def leave(ticket):
        exit_barrier.wait()
        lot.unpark(ticket.id)

    exit_threads = [threading.Thread(target=leave, args=(tickets[i],)) for i in range(0, 8, 2)]
    for t in exit_threads:
        t.start()
    for t in exit_threads:
        t.join()

    # 风暴（并发的 park + unpark）过后，不管事件通知的相对顺序是什么，展示牌的
    # 计数必须和直接数一遍车位算出来的结果完全一致——见题解里"为什么增量计数在
    # 静止状态下总是对的"。
    recount: dict[int, int] = {}
    for spot in spots:
        recount[spot.floor] = recount.get(spot.floor, 0) + (1 if spot.is_free else 0)
    assert dict(board.free_by_floor) == recount


def test_callers_cannot_mutate_the_lot_through_its_public_api():
    lot = make_lot(compact_spots(1, 2))
    snapshot = lot.free_counts_by_floor()
    assert dict(snapshot) == {1: 2}
    with pytest.raises(TypeError):
        snapshot[1] = 99  # 快照是只读的，改不了停车场的真实状态
    assert not hasattr(lot, "spots_by_floor")  # 内部的车位列表/字典不通过任何公开属性泄漏


def test_a_new_vehicle_size_works_with_the_existing_allocation_and_pricing_code():
    # 模拟新增一种比 LARGE 还大的车型（比如大巴），不改 VehicleSize、fits、
    # nearest_first 或任何计价函数——只要遵守"数值越大占地越大"的约定即可。
    bus_size = int(impl.VehicleSize.LARGE) + 1
    bus_spot = impl.ParkingSpot(id="bus-1", floor=1, size=bus_size)
    bus = impl.Vehicle(plate="BUS1", size=bus_size)
    assert bus_spot.fits(bus)

    lot = make_lot([bus_spot], allocate=impl.nearest_first,
                    price=impl.flat_rate(Decimal("50")))
    ticket = lot.park(bus)
    assert ticket.spot.id == "bus-1"
