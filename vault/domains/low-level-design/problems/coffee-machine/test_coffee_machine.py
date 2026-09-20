"""咖啡机参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

Y = impl.YUAN


def latte():
    return impl.recipe("拿铁", 22 * Y, espresso=30, milk=180)


def americano():
    return impl.recipe("美式", 18 * Y, espresso=30, water=150)


def make_machine(levels=None, low_water=None, outlets=2, brewer=None, recipes=None):
    stock = impl.Inventory(levels if levels is not None else
                           {"espresso": 300, "milk": 1000, "water": 1000},
                           low_water=low_water or {})
    kwargs = {"outlets": outlets}
    if brewer is not None:
        kwargs["brewer"] = brewer
    return impl.CoffeeMachine(stock, recipes or (latte(), americano()), **kwargs), stock


def collector(machine):
    seen, guard = [], threading.Lock()

    def observe(event):
        with guard:
            seen.append(event)

    machine.subscribe(observe)
    return seen


# ---- 第 1 关：配方与原料的原子扣减 ------------------------------------------


def test_brewing_deducts_exactly_what_the_recipe_asks_for():
    machine, stock = make_machine()
    served = machine.brew("拿铁")
    assert served.drink == "拿铁" and served.outlet.startswith("outlet-")
    assert dict(stock.levels()) == {"espresso": 270, "milk": 820, "water": 1000}
    assert machine.served_count == 1


def test_an_unknown_drink_touches_nothing():
    machine, stock = make_machine()
    before = dict(stock.levels())
    with pytest.raises(impl.UnknownDrinkError):
        machine.brew("摩卡")
    assert dict(stock.levels()) == before
    assert machine.served_count == 0


def test_a_short_ingredient_leaves_every_other_ingredient_untouched():
    """全有或全无：牛奶不够时，浓缩一滴都不许被扣掉。"""
    machine, stock = make_machine({"espresso": 300, "milk": 100, "water": 1000})
    with pytest.raises(impl.OutOfIngredientError) as exc:
        machine.brew("拿铁")
    assert exc.value.drink == "拿铁"
    assert dict(exc.value.missing) == {"milk": 80}
    assert dict(stock.levels()) == {"espresso": 300, "milk": 100, "water": 1000}


def test_the_shortfall_names_every_missing_ingredient_at_once():
    machine, stock = make_machine({"espresso": 10, "milk": 10, "water": 1000})
    with pytest.raises(impl.OutOfIngredientError) as exc:
        machine.brew("拿铁")
    assert dict(exc.value.missing) == {"espresso": 20, "milk": 170}


def test_a_failure_halfway_through_brewing_puts_every_ingredient_back():
    def broken_brewer(drink, outlet):
        raise RuntimeError("加热器故障")

    machine, stock = make_machine(brewer=broken_brewer)
    before = dict(stock.levels())
    seen = collector(machine)
    with pytest.raises(impl.BrewingFailedError):
        machine.brew("拿铁")
    assert dict(stock.levels()) == before
    assert machine.served_count == 0
    assert [type(e) for e in seen] == [impl.BrewFailed]
    assert seen[0].drink == "拿铁" and "加热器" in seen[0].reason


def test_an_ingredient_the_machine_never_heard_of_is_a_shortfall_not_a_keyerror():
    machine, _ = make_machine(recipes=(impl.recipe("抹茶拿铁", 26 * Y, matcha=8, milk=200),))
    with pytest.raises(impl.OutOfIngredientError) as exc:
        machine.brew("抹茶拿铁")
    assert dict(exc.value.missing) == {"matcha": 8}


def test_a_recipe_with_a_zero_or_negative_amount_is_refused_at_construction():
    with pytest.raises(impl.InvalidQuantityError):
        impl.recipe("空气", 1 * Y, milk=0)


def test_neither_the_levels_nor_the_menu_hand_out_a_writable_container():
    machine, stock = make_machine()
    with pytest.raises(TypeError):
        stock.levels()["milk"] = 10 ** 9
    with pytest.raises(TypeError):
        machine.menu()["拿铁"] = None


# ---- 第 2 关：多出口并发 ----------------------------------------------------


def test_exactly_as_many_drinks_are_served_as_the_stock_allows():
    """十个线程同时抢只够做四杯的原料：正好四杯成功，库存不为负，账目分毫不差。"""
    machine, stock = make_machine({"espresso": 120, "milk": 720, "water": 0}, outlets=3)
    threads_n = 10
    barrier = threading.Barrier(threads_n)
    served, refused, guard = [], [], threading.Lock()

    def order():
        barrier.wait()
        try:
            drink = machine.brew("拿铁")
        except impl.OutOfIngredientError as exc:
            with guard:
                refused.append(exc)
            return
        with guard:
            served.append(drink)

    threads = [threading.Thread(target=order) for _ in range(threads_n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(served) == 4 and len(refused) == threads_n - 4
    assert machine.served_count == 4
    levels = dict(stock.levels())
    assert all(v >= 0 for v in levels.values())
    assert levels == {"espresso": 0, "milk": 0, "water": 0}


def test_exactly_as_many_brews_run_at_once_as_there_are_outlets():
    """三出口机器发六杯：冲煮里的屏障要求恰好三个线程同时到齐才能继续。

    少于三个并发（比如把库存锁跨到了冲煮上）会让屏障超时，多于三个会把 `peak` 推高——
    断言的是并发度这条不变式本身，没有一句 `sleep`。
    """
    live, peak, guard = 0, 0, threading.Lock()
    rendezvous = threading.Barrier(3, timeout=3)

    def slow_brewer(drink, outlet):
        nonlocal live, peak
        with guard:
            live += 1
            peak = max(peak, live)
        rendezvous.wait()
        with guard:
            live -= 1

    machine, _ = make_machine({"espresso": 3000, "milk": 1000, "water": 5000},
                              outlets=3, brewer=slow_brewer)
    threads = [threading.Thread(target=machine.brew, args=("美式",)) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)
    assert not any(t.is_alive() for t in threads)
    assert peak == 3
    assert machine.served_count == 6


def test_the_inventory_lock_is_not_held_across_the_brew():
    """冲煮正进行时补货必须立刻成功——否则说明临界区把冲煮圈进去了。"""
    brewing, release = threading.Event(), threading.Event()

    def slow_brewer(drink, outlet):
        brewing.set()
        assert release.wait(timeout=2)

    machine, stock = make_machine(outlets=1, brewer=slow_brewer)
    worker = threading.Thread(target=machine.brew, args=("拿铁",))
    worker.start()
    assert brewing.wait(timeout=2)
    assert stock.refill("milk", 500) == 1000 - 180 + 500   # 冲煮中，补货照样立刻返回
    assert dict(stock.levels())["espresso"] == 270         # 读库存也不会被挡住
    release.set()
    worker.join(timeout=5)
    assert machine.served_count == 1


def test_an_outlet_is_returned_even_when_the_brew_blows_up():
    def flaky(drink, outlet):
        if drink.name == "拿铁":
            raise RuntimeError("卡豆")

    machine, _ = make_machine(outlets=1, brewer=flaky)
    for _ in range(3):
        with pytest.raises(impl.BrewingFailedError):
            machine.brew("拿铁")
    assert machine.brew("美式").outlet == "outlet-1"       # 出口没有被漏掉


# ---- 第 3 关：缺料告警与补货 ------------------------------------------------


def test_crossing_the_low_water_mark_publishes_an_event_that_carries_what_happened():
    machine, stock = make_machine({"espresso": 300, "milk": 300, "water": 1000},
                                  low_water={"milk": 150})
    seen = collector(machine)
    machine.brew("拿铁")
    lows = [e for e in seen if isinstance(e, impl.IngredientLow)]
    assert len(lows) == 1
    assert (lows[0].ingredient, lows[0].remaining, lows[0].low_water) == ("milk", 120, 150)


def test_the_alert_does_not_repeat_on_every_later_cup():
    machine, stock = make_machine({"espresso": 300, "milk": 400, "water": 1000},
                                  low_water={"milk": 250})
    seen = collector(machine)
    machine.brew("拿铁")
    machine.brew("拿铁")
    assert len([e for e in seen if isinstance(e, impl.IngredientLow)]) == 1


def test_refilling_above_the_mark_arms_the_alert_again():
    machine, stock = make_machine({"espresso": 300, "milk": 200, "water": 1000},
                                  low_water={"milk": 150})
    seen = collector(machine)
    machine.brew("拿铁")                    # 200 → 20，告警
    stock.refill("milk", 380)               # 20 → 400，解除告警闩
    machine.brew("拿铁")                    # 400 → 220
    machine.brew("拿铁")                    # 220 → 40，再次告警
    lows = [e.remaining for e in seen if isinstance(e, impl.IngredientLow)]
    assert lows == [20, 40]


def test_an_ingredient_that_runs_out_mid_queue_names_itself_in_every_later_refusal():
    machine, stock = make_machine({"espresso": 300, "milk": 180, "water": 1000})
    machine.brew("拿铁")
    assert dict(stock.levels())["milk"] == 0
    for _ in range(3):
        with pytest.raises(impl.OutOfIngredientError) as exc:
            machine.brew("拿铁")
        assert dict(exc.value.missing) == {"milk": 180}
    assert machine.brew("美式").drink == "美式"   # 不用牛奶的饮品照做不误


def test_an_ingredient_at_zero_stays_in_the_table():
    """0 和"这台机器根本没有这种原料"是两件事，运维要看得到前者。"""
    machine, stock = make_machine({"espresso": 300, "milk": 180, "water": 1000})
    machine.brew("拿铁")
    assert dict(stock.levels())["milk"] == 0


def test_a_subscriber_may_call_back_into_the_machine_without_deadlocking():
    """"缺料就自动补货"是最自然的订阅者。事件在锁外投递，所以它不会把机器锁死。"""
    machine, stock = make_machine({"espresso": 300, "milk": 200, "water": 1000},
                                  low_water={"milk": 150})
    refills = []

    def auto_refill(event):
        if isinstance(event, impl.IngredientLow):
            refills.append(stock.refill(event.ingredient, 1000))

    machine.subscribe(auto_refill)
    worker = threading.Thread(target=machine.brew, args=("拿铁",))
    worker.start()
    worker.join(timeout=3)
    assert not worker.is_alive()            # 没死锁
    assert refills == [1020]
    assert dict(stock.levels())["milk"] == 1020


def test_refilling_a_non_positive_amount_is_refused():
    _, stock = make_machine()
    with pytest.raises(impl.InvalidQuantityError):
        stock.refill("milk", 0)


# ---- 第 4 关：新配方与新原料 ------------------------------------------------


def test_a_new_recipe_with_a_brand_new_ingredient_needs_no_change_to_the_brew_path():
    machine, stock = make_machine()
    machine.register(impl.recipe("摩卡", 26 * Y, espresso=30, milk=150, cocoa=20))
    with pytest.raises(impl.OutOfIngredientError) as exc:
        machine.brew("摩卡")               # 菜单先上，原料还没到
    assert dict(exc.value.missing) == {"cocoa": 20}
    stock.refill("cocoa", 100)
    stock.set_low_water("cocoa", 85)
    seen = collector(machine)
    assert machine.brew("摩卡").drink == "摩卡"
    assert dict(stock.levels())["cocoa"] == 80
    machine.brew("摩卡")
    assert [e.ingredient for e in seen if isinstance(e, impl.IngredientLow)] == ["cocoa"]


def test_registering_the_same_name_replaces_the_recipe_and_running_cups_keep_the_old_one():
    machine, stock = make_machine()
    machine.register(impl.recipe("拿铁", 25 * Y, espresso=30, milk=120))
    assert machine.menu()["拿铁"].price == 25 * Y
    machine.brew("拿铁")
    assert dict(stock.levels())["milk"] == 880     # 用的是新配方的 120
