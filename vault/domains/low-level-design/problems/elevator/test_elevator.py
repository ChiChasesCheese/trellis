"""电梯系统参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。

所有测试都靠 tick 推进，不出现 `time.sleep`，也不依赖真实时间；时间只通过注入的假时钟
进入事件的时间戳。
"""

import importlib
import os
import threading
from datetime import datetime, timedelta, UTC

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

START = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)


def make_clock(start: datetime = START):
    """一个可以手动拨动的假时钟。"""
    state = {"now": start}

    def clock() -> datetime:
        return state["now"]

    def advance(delta: timedelta) -> None:
        state["now"] += delta

    return clock, advance


def make_car(car_id: str = "A", policy=None, floor: int = 1, **kwargs):
    clock, _ = make_clock()
    policy = policy or impl.scan
    return impl.ElevatorCar(car_id, policy=policy, clock=clock, floor=floor, **kwargs)


def make_bank(cars, dispatch=None):
    clock, _ = make_clock()
    return impl.ElevatorBank(cars, dispatch=dispatch or impl.directional_dispatch, clock=clock)


def run(car, ticks: int) -> list:
    """推进若干 tick，收集非空事件。"""
    return [e for _ in range(ticks) if (e := car.step()) is not None]


def opened_floors(events) -> list[int]:
    return [e.floor for e in events if e.kind is impl.EventKind.DOORS_OPENED]


# ---- 第 1 关：一部梯的状态机 -------------------------------------------------


def test_idle_car_moves_to_the_requested_floor_and_opens_its_doors():
    car = make_car(floor=1)
    car.request_floor(3)
    events = run(car, 4)
    assert [e.kind for e in events] == [impl.EventKind.MOVED, impl.EventKind.MOVED,
                                        impl.EventKind.DOORS_OPENED, impl.EventKind.DOORS_CLOSED]
    assert car.current_floor == 3


def test_state_machine_walks_idle_moving_doors_open_idle():
    car = make_car(floor=1)
    assert car.state is impl.CarState.IDLE
    car.request_floor(2)
    car.step()
    assert car.state is impl.CarState.MOVING_UP
    car.step()
    assert car.state is impl.CarState.DOORS_OPEN
    car.step()
    assert car.state is impl.CarState.IDLE


def test_a_car_with_nothing_to_do_stays_idle_and_emits_nothing():
    car = make_car()
    assert car.step() is None
    assert car.state is impl.CarState.IDLE
    assert car.snapshot().sweep is None


def test_moving_down_is_its_own_state():
    car = make_car(floor=5)
    car.request_floor(2)
    car.step()
    assert car.state is impl.CarState.MOVING_DOWN
    assert car.current_floor == 4


def test_holding_the_doors_extends_the_dwell_without_a_new_state():
    car = make_car(floor=1, door_ticks=1)
    car.request_floor(2)
    run(car, 2)  # 走一层 + 开门
    assert car.state is impl.CarState.DOORS_OPEN
    car.hold_doors(2)
    car.step()
    assert car.state is impl.CarState.DOORS_OPEN  # 被挡住，门还没关
    car.step()
    assert car.state is impl.CarState.DOORS_OPEN
    event = car.step()
    assert event.kind is impl.EventKind.DOORS_CLOSED
    assert car.state is impl.CarState.IDLE


def test_holding_the_doors_while_they_are_shut_is_rejected():
    car = make_car()
    with pytest.raises(impl.DoorsNotOpenError):
        car.hold_doors()


def test_events_carry_the_timestamp_from_the_injected_clock():
    clock, advance = make_clock()
    car = impl.ElevatorCar("A", policy=impl.scan, clock=clock, floor=1)
    car.request_floor(2)
    advance(timedelta(seconds=3))
    event = car.step()
    assert event.at == START + timedelta(seconds=3)
    assert event.car_id == "A"


def test_snapshot_does_not_expose_the_internal_stop_sets():
    car = make_car()
    car.request_floor(5)
    snap = car.snapshot()
    assert snap.car_calls == frozenset({5})
    assert isinstance(snap.car_calls, frozenset)
    with pytest.raises(AttributeError):
        snap.car_calls.add(9)  # type: ignore[attr-defined]
    assert car.snapshot().car_calls == frozenset({5})


# ---- 第 2 关：可换的停靠策略 ------------------------------------------------


def test_scan_serves_everything_on_the_way_up_in_floor_order():
    car = make_car(floor=1, policy=impl.scan)
    for floor in (7, 3, 5):
        car.request_floor(floor)
    events = run(car, 30)
    assert opened_floors(events) == [3, 5, 7]


def test_scan_keeps_its_sweep_direction_across_a_door_cycle():
    car = make_car(floor=1, policy=impl.scan)
    car.accept_hall_call(impl.HallCall(3, impl.Direction.UP))
    car.accept_hall_call(impl.HallCall(6, impl.Direction.UP))
    run(car, 4)  # 走到 3 层并开门
    assert car.current_floor == 3
    car.step()  # 关门
    assert car.snapshot().sweep is impl.Direction.UP  # 停过一次仍然记得在往上走
    events = run(car, 10)
    assert opened_floors(events) == [6]


def test_scan_reverses_only_after_nothing_is_left_ahead():
    car = make_car(floor=5, policy=impl.scan)
    car.accept_hall_call(impl.HallCall(8, impl.Direction.UP))
    car.step()  # 起步上行，这一趟扫描的方向就此确定
    assert car.snapshot().sweep is impl.Direction.UP
    car.accept_hall_call(impl.HallCall(2, impl.Direction.DOWN))
    events = run(car, 40)
    assert opened_floors(events) == [8, 2]  # 先把上行扫完，再掉头


def test_nearest_request_starves_a_far_floor_and_scan_does_not():
    served_by_policy = {}
    for policy in (impl.nearest_request, impl.scan):
        car = make_car(floor=1, policy=policy)
        car.request_floor(20)
        served: list[int] = []
        for _ in range(80):
            event = car.step()
            if event is not None and event.kind is impl.EventKind.DOORS_OPENED:
                served.append(event.floor)
            # 一层和二层的人不停地按，制造源源不断的近处请求
            car.request_floor(1 if car.current_floor >= 2 else 2)
        served_by_policy[policy] = served
    assert 20 not in served_by_policy[impl.nearest_request]
    assert 20 in served_by_policy[impl.scan]


def test_an_up_hall_call_is_not_answered_while_the_car_sweeps_down():
    car = make_car(floor=9, policy=impl.scan)
    car.accept_hall_call(impl.HallCall(1, impl.Direction.DOWN))
    car.accept_hall_call(impl.HallCall(5, impl.Direction.UP))
    events = run(car, 40)
    # 下行途中经过 5 层不停（那里的人要上行），扫到底再掉头回来接
    assert opened_floors(events) == [1, 5]


def test_serving_a_floor_upward_leaves_the_down_call_on_that_floor():
    car = make_car(floor=1, policy=impl.scan)
    car.accept_hall_call(impl.HallCall(4, impl.Direction.UP))
    car.accept_hall_call(impl.HallCall(4, impl.Direction.DOWN))
    run(car, 5)  # 上行到 4 层开门
    snap = car.snapshot()
    assert snap.up_calls == frozenset()
    assert snap.down_calls == frozenset({4})  # 下行的那一拨人还在等


def test_a_car_call_is_served_in_whichever_sweep_reaches_it():
    car = make_car(floor=9, policy=impl.scan)
    car.request_floor(6)  # 车里的人要去 6 层
    car.accept_hall_call(impl.HallCall(9, impl.Direction.UP))
    events = run(car, 30)
    assert 6 in opened_floors(events)
    assert car.snapshot().car_calls == frozenset()


# ---- 第 3 关：一组梯与派梯 --------------------------------------------------


def test_a_hall_call_is_assigned_to_exactly_one_car():
    bank = make_bank([make_car("A", floor=1), make_car("B", floor=10)])
    assert bank.hall_call(2, impl.Direction.UP) == "A"
    holders = [s.car_id for s in bank.snapshots() if 2 in s.up_calls]
    assert holders == ["A"]


def test_pressing_the_same_hall_button_twice_does_not_summon_a_second_car():
    bank = make_bank([make_car("A", floor=1), make_car("B", floor=2)])
    first = bank.hall_call(6, impl.Direction.UP)
    second = bank.hall_call(6, impl.Direction.UP)
    assert first == second
    holders = [s.car_id for s in bank.snapshots() if 6 in s.up_calls]
    assert len(holders) == 1


def test_directional_dispatch_prefers_the_car_already_heading_that_way():
    a, b = make_car("A", floor=1), make_car("B", floor=4)
    bank = make_bank([a, b])
    bank.hall_call(9, impl.Direction.UP)  # A 或 B 起步上行
    bank.step()
    bank.step()
    moving_up = [s for s in bank.snapshots() if s.sweep is impl.Direction.UP]
    assert moving_up, "至少有一部梯在上行"
    chosen = bank.hall_call(7, impl.Direction.UP)
    assert chosen == moving_up[0].car_id


def test_nearest_car_ignores_direction_which_is_exactly_its_weakness():
    a = make_car("A", floor=1)
    b = make_car("B", floor=9)
    bank = make_bank([a, b], dispatch=impl.nearest_car)
    bank.hall_call(1, impl.Direction.DOWN)
    bank.step()  # A 开门接人，准备下行
    assert bank.hall_call(3, impl.Direction.UP) == "A"  # 只看楼层差，完全不管 A 在往下走


def test_the_assignment_is_cleared_once_the_call_is_served():
    bank = make_bank([make_car("A", floor=1)])
    call = impl.HallCall(3, impl.Direction.UP)
    assert bank.hall_call(3, impl.Direction.UP) == "A"
    assert bank.assignment_of(call) == "A"
    bank.run_until_idle()
    assert bank.assignment_of(call) is None  # 分派表随完成的外呼缩小
    # 同一层同一方向再按一次，必须还能叫来梯——分派表不缩的话这里会被静默吞掉
    assert bank.hall_call(3, impl.Direction.UP) == "A"


def test_a_call_no_car_can_take_is_queued_and_retried_on_the_next_tick():
    bank = make_bank([make_car("A", floor=1)])
    bank.take_out_of_service("A")
    call = impl.HallCall(4, impl.Direction.UP)
    assert bank.hall_call(4, impl.Direction.UP) is None
    assert call in bank.pending_calls()
    bank.step()
    assert call in bank.pending_calls()  # 仍然没有梯能接，但只排了一份
    assert len(bank.pending_calls()) == 1
    bank.return_to_service("A")
    bank.step()
    assert bank.pending_calls() == frozenset()
    assert bank.assignment_of(call) == "A"


def test_taking_a_car_out_of_service_reassigns_its_hall_calls():
    bank = make_bank([make_car("A", floor=1), make_car("B", floor=2)])
    call = impl.HallCall(5, impl.Direction.UP)
    owner = bank.hall_call(5, impl.Direction.UP)
    stranded = bank.take_out_of_service(owner)
    assert stranded == (call,)
    new_owner = bank.assignment_of(call)
    assert new_owner is not None and new_owner != owner
    holders = [s.car_id for s in bank.snapshots() if 5 in s.up_calls]
    assert holders == [new_owner]


def test_an_out_of_service_car_still_delivers_the_riders_inside_it():
    bank = make_bank([make_car("A", floor=1), make_car("B", floor=9)])
    bank.press_floor("A", 4)
    bank.take_out_of_service("A")
    bank.run_until_idle()
    a = next(s for s in bank.snapshots() if s.car_id == "A")
    assert a.floor == 4 and a.car_calls == frozenset()


def test_dropping_a_hall_call_keeps_a_car_call_for_the_same_floor():
    bank = make_bank([make_car("A", floor=1), make_car("B", floor=2)])
    owner = bank.hall_call(6, impl.Direction.UP)
    bank.press_floor(owner, 6)  # 车里也有人要去 6 层
    bank.take_out_of_service(owner)
    stranded_car = next(s for s in bank.snapshots() if s.car_id == owner)
    assert stranded_car.up_calls == frozenset()      # 外呼被收回
    assert stranded_car.car_calls == frozenset({6})  # 内选原封不动


def test_an_express_car_refuses_a_floor_it_does_not_serve():
    express = make_car("X", floor=1, served_floors=[1, 10, 11, 12])
    with pytest.raises(impl.FloorNotServedError):
        express.request_floor(5)
    bank = make_bank([express, make_car("L", floor=1, served_floors=range(1, 11))])
    assert bank.hall_call(5, impl.Direction.UP) == "L"  # 直达梯不参与低区的外呼


def test_pressing_a_floor_on_an_unknown_car_raises():
    bank = make_bank([make_car("A")])
    with pytest.raises(impl.UnknownCarError):
        bank.press_floor("ghost", 3)


def test_concurrent_hall_calls_are_each_assigned_to_exactly_one_car():
    cars = [make_car("A", floor=1), make_car("B", floor=5), make_car("C", floor=9)]
    bank = make_bank(cars)
    calls = [impl.HallCall(f, impl.Direction.UP) for f in range(1, 9)]
    barrier = threading.Barrier(len(calls))

    def place(call):
        barrier.wait()
        bank.hall_call(call.floor, call.direction)

    threads = [threading.Thread(target=place, args=(c,)) for c in calls]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    holders = [s.up_calls for s in bank.snapshots()]
    total = sum(len(h) for h in holders)
    assert total == len(calls)  # 没有一个外呼被派给两部梯，也没有一个丢掉
    assert set().union(*holders) == {c.floor for c in calls}
    assert all(bank.assignment_of(c) is not None for c in calls)
