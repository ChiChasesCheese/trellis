import importlib
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

NOODLE = impl.Dish("面", 4)
SOUP = impl.Dish("汤", 2)
MENU = [NOODLE, SOUP]
# 默认参数下：面耗电 4*1 + 3*2 = 10，汤耗电 2*1 + 3*2 = 8


def shop(batteries=(100,), **kw):
    cfg = impl.Config(**{k: v for k, v in kw.items() if k != "policy"})
    return impl.Restaurant(MENU, batteries, cfg, **({"policy": kw["policy"]} if "policy" in kw else {}))


def kinds(restaurant, order_id):
    return [e.kind.name for e in restaurant.events if e.order_id == order_id]


# ---- 第 1 关：一台机器人，点单 → 做菜 → 送餐 ----

def test_one_order_goes_pending_cooking_delivering_delivered():
    r = shop()
    oid = r.place_order(3, "面")
    assert r.order_state(oid) is impl.OrderState.PENDING
    r.tick()
    assert r.order_state(oid) is impl.OrderState.COOKING
    for _ in range(4):
        r.tick()
    assert r.order_state(oid) is impl.OrderState.DELIVERING
    for _ in range(3):
        r.tick()
    assert r.order_state(oid) is impl.OrderState.DELIVERED
    assert r.robots[0].state is impl.RobotState.IDLE and r.robots[0].order_id is None


def test_event_log_tells_the_story_with_ticks():
    r = shop()
    oid = r.place_order(1, "汤")
    r.run_until_quiet()
    assert [(e.tick, e.kind.name) for e in r.events if e.order_id == oid] == [
        (1, "ASSIGNED"),
        (3, "COOKED"),
        (6, "DELIVERED"),
    ]


def test_single_robot_serves_orders_one_after_another_in_arrival_order():
    r = shop()
    a, b = r.place_order(1, "面"), r.place_order(2, "汤")
    r.tick()
    assert r.order_state(a) is impl.OrderState.COOKING and r.order_state(b) is impl.OrderState.PENDING
    assert r.pending_count == 1
    r.run_until_quiet()
    assert r.order_state(a) is r.order_state(b) is impl.OrderState.DELIVERED
    delivered = [e.order_id for e in r.events if e.kind is impl.EventKind.DELIVERED]
    assert delivered == [a, b]


def test_unknown_dish_and_unknown_order_are_rejected():
    r = shop()
    with pytest.raises(impl.UnknownDishError):
        r.place_order(1, "龙虾")
    with pytest.raises(impl.UnknownOrderError):
        r.order_state(99)


def test_order_that_no_robot_could_ever_finish_is_rejected_up_front():
    r = shop()
    with pytest.raises(impl.OrderRejectedError):
        impl.Restaurant([impl.Dish("满汉全席", 50)], (100,)).place_order(1, "满汉全席")
    assert r.pending_count == 0


def test_battery_drains_while_working():
    r = shop(batteries=(100,))
    r.place_order(1, "面")
    r.run_until_quiet()
    assert r.robots[0].battery == 90


# ---- 第 2 关：多台机器人与分配策略 ----

def test_two_robots_cook_in_parallel():
    r = shop(batteries=(100, 100))
    a, b = r.place_order(1, "面"), r.place_order(2, "面")
    r.tick()
    assert r.order_state(a) is r.order_state(b) is impl.OrderState.COOKING
    assert {v.order_id for v in r.robots} == {a, b}
    assert r.run_until_quiet() == 7  # 共 1 + 7 = 8 刻，与单台机器人做一份面一样久


def test_first_idle_policy_prefers_the_lowest_id():
    r = shop(batteries=(60, 90), policy=impl.first_idle)
    oid = r.place_order(1, "汤")
    r.tick()
    assert r.robots[0].order_id == oid and r.robots[1].order_id is None


def test_most_battery_policy_prefers_the_fullest_robot():
    r = shop(batteries=(60, 90), policy=impl.most_battery)
    oid = r.place_order(1, "汤")
    r.tick()
    assert r.robots[1].order_id == oid and r.robots[0].order_id is None


def test_custom_policy_is_just_a_function_and_a_bad_answer_is_an_error():
    r = shop(batteries=(100, 100), policy=lambda candidates, dish: 7)
    r.place_order(1, "汤")
    with pytest.raises(impl.PolicyError):
        r.tick()


def test_busy_robot_is_never_a_candidate():
    seen = []

    def spy(candidates, dish):
        seen.append([c.id for c in candidates])
        return min((c.id for c in candidates), default=None)

    r = shop(batteries=(100, 100), policy=spy)
    r.place_order(1, "面")
    r.place_order(2, "面")
    r.place_order(3, "面")
    r.tick()
    assert seen[0] == [0, 1] and seen[1] == [1] and seen[2] == []


def test_cancel_a_pending_order_but_not_one_a_robot_has_taken():
    r = shop()
    a, b = r.place_order(1, "面"), r.place_order(2, "汤")
    r.tick()
    r.cancel_order(b)
    assert r.order_state(b) is impl.OrderState.CANCELLED and r.pending_count == 0
    with pytest.raises(impl.OrderNotCancellableError):
        r.cancel_order(a)
    with pytest.raises(impl.OrderNotCancellableError):
        r.cancel_order(b)
    r.run_until_quiet()
    assert kinds(r, b) == ["CANCELLED"]


# ---- 第 3 关：电量与充电 ----

def test_idle_robot_below_threshold_goes_to_charge_and_returns_full():
    r = shop(batteries=(20,), charge_rate=40)
    r.tick()
    assert r.robots[0].state is impl.RobotState.CHARGING
    r.tick()
    r.tick()
    assert r.robots[0].state is impl.RobotState.IDLE and r.robots[0].battery == 100
    assert [e.kind.name for e in r.events] == ["CHARGE_STARTED", "CHARGE_DONE"]


def test_robot_finishing_a_job_below_threshold_charges_before_taking_the_next_order():
    r = shop(batteries=(45,), charge_rate=50)
    a = r.place_order(1, "面")  # 45 -> 35
    r.run_until_quiet()
    b = r.place_order(2, "面")  # 35 -> 25，低于 30
    r.run_until_quiet()
    assert r.robots[0].battery == 25 and r.robots[0].state is impl.RobotState.CHARGING
    c = r.place_order(3, "面")
    r.tick()
    assert r.order_state(c) is impl.OrderState.PENDING  # 还在充电，不接单
    r.run_until_quiet()
    assert [r.order_state(i) for i in (a, b, c)] == [impl.OrderState.DELIVERED] * 3
    assert r.robots[0].battery == 90  # 25 充到 75、再充到 100，接 c 后耗 10


def test_only_as_many_robots_charge_as_there_are_chargers_lowest_battery_first():
    r = shop(batteries=(25, 10, 28), chargers=1, charge_rate=5)
    r.tick()
    states = {v.id: v.state for v in r.robots}
    assert states == {0: impl.RobotState.IDLE, 1: impl.RobotState.CHARGING, 2: impl.RobotState.IDLE}


def test_low_battery_robot_with_no_free_charger_still_works_while_it_can_finish_the_job():
    # 机器人 0 占着唯一的桩，机器人 1 电量 25 低于阈值但够做一份汤（耗 8，剩 17 >= 保底 10）
    r = shop(batteries=(5, 25), chargers=1, charge_rate=1)
    oid = r.place_order(1, "汤")
    r.tick()
    assert r.robots[0].state is impl.RobotState.CHARGING
    assert r.robots[1].order_id == oid
    r.run_until_quiet()
    assert r.order_state(oid) is impl.OrderState.DELIVERED
    assert r.robots[1].battery == 17


def test_low_battery_robot_that_cannot_finish_the_job_leaves_the_order_waiting():
    # 电量 12：一份汤耗 8，做完只剩 4 < 保底 10，不能接；又没有桩（桩数 0）
    r = shop(batteries=(12,), chargers=0)
    oid = r.place_order(1, "汤")
    for _ in range(20):
        r.tick()
    assert r.order_state(oid) is impl.OrderState.PENDING
    assert r.robots[0].state is impl.RobotState.IDLE and r.robots[0].battery == 12


def test_battery_never_drops_below_the_reserve():
    rng = random.Random(7)
    r = shop(batteries=(100, 60, 35), chargers=1, charge_rate=15)
    ids = [r.place_order(rng.randint(1, 9), rng.choice(["面", "汤"])) for _ in range(60)]
    for _ in range(5000):
        r.tick()
        assert all(v.battery >= 10 for v in r.robots)
        if all(r.order_state(i) is impl.OrderState.DELIVERED for i in ids):
            break
    assert all(r.order_state(i) is impl.OrderState.DELIVERED for i in ids)


def test_config_rejects_nonsense():
    with pytest.raises(ValueError):
        impl.Config(reserve=40, low_battery=30)
    with pytest.raises(ValueError):
        impl.Config(charge_rate=0)


# ---- 第 4 关：并发 ----

def test_concurrent_orders_are_all_delivered_exactly_once():
    r = shop(batteries=(100, 100, 100), chargers=2, charge_rate=20)
    n_threads, per_thread = 6, 20
    barrier = threading.Barrier(n_threads + 1)
    ids, lock = [], threading.Lock()

    def worker(t):
        barrier.wait()
        for _ in range(per_thread):
            oid = r.place_order(t, "汤")
            with lock:
                ids.append(oid)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    barrier.wait()
    for t in threads:
        while t.is_alive():
            r.tick()
        t.join()
    r.run_until_quiet()
    assert len(ids) == len(set(ids)) == n_threads * per_thread
    delivered = [e.order_id for e in r.events if e.kind is impl.EventKind.DELIVERED]
    assert sorted(delivered) == sorted(ids)
