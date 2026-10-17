import importlib
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def menu():
    return impl.default_menu()


def pizza(size="M", crust="thin", *toppings):
    b = impl.PizzaBuilder(menu()).size(size).crust(crust)
    for t in toppings:
        b.topping(t)
    return b.build()


def line(p, qty=1):
    return impl.OrderLine(p, qty)


# ── 第 1 关：菜单与定价 ──

def test_plain_pizza_price_is_base_price():
    assert pizza("S").unit_cents == 800
    assert pizza("L").unit_cents == 1200


def test_crust_and_topping_prices_depend_on_size():
    assert pizza("L", "thick", "pepperoni", "mushroom").unit_cents == 1200 + 100 + 250 + 150
    assert pizza("S", "thin", "pepperoni").unit_cents == 800 + 150
    assert pizza("M", "stuffed").unit_cents == 1000 + 250


def test_toppings_are_order_independent():
    a = pizza("M", "thin", "olive", "mushroom")
    b = pizza("M", "thin", "mushroom", "olive")
    assert a == b and hash(a) == hash(b) and a.sku == b.sku == "M/thin/mushroom+olive"


def test_default_crust_is_thin():
    assert impl.PizzaBuilder(menu()).size("M").build().crust == "thin"


def test_new_topping_is_data_only():
    m = menu()
    m.toppings["jalapeno"] = impl.ToppingSpec({"S": 100, "M": 100, "L": 100})
    p = impl.PizzaBuilder(m).size("S").topping("jalapeno").build()
    assert p.unit_cents == 900


def test_money_helpers_avoid_float():
    assert impl.to_cents("19.99") == 1999
    assert impl.to_cents("0.285") == 29
    assert impl.format_cents(1905) == "19.05"


# ── 第 2 关：校验 ──

@pytest.mark.parametrize("build", [
    lambda b: b,                                              # 没选尺寸
    lambda b: b.size("XL"),                                   # 未知尺寸
    lambda b: b.size("M").crust("deep"),                      # 未知饼底
    lambda b: b.size("S").crust("stuffed"),                   # 小号做不了芝心
    lambda b: b.size("M").topping("anchovy"),                 # 未知配料
    lambda b: b.size("M").topping("olive").topping("olive"),  # 重复配料
    lambda b: b.size("M").topping("cheese").topping("vegan_cheese"),   # 互斥
])
def test_invalid_choices_are_rejected(build):
    with pytest.raises(impl.InvalidChoiceError):
        build(impl.PizzaBuilder(menu())).build()


def test_topping_limit():
    names = ["cheese", "pepperoni", "mushroom", "olive", "pineapple"]
    b = impl.PizzaBuilder(menu()).size("L")
    for n in names:
        b.topping(n)
    assert len(b.build().toppings) == 5
    m = menu()
    m.toppings["ham"] = impl.ToppingSpec({"S": 1, "M": 1, "L": 1})
    b = impl.PizzaBuilder(m).size("L")
    for n in names + ["ham"]:
        b.topping(n)
    with pytest.raises(impl.InvalidChoiceError):
        b.build()


def test_builder_is_reusable_and_failed_build_leaves_no_trace():
    b = impl.PizzaBuilder(menu()).size("M").topping("olive")
    first = b.build()
    second = b.build()
    assert first == second
    b.topping("olive")
    with pytest.raises(impl.InvalidChoiceError):
        b.build()


def test_unit_price_is_frozen_at_build_time():
    m = menu()
    p = impl.PizzaBuilder(m).size("M").build()
    m.base["M"] = 9999
    assert p.unit_cents == 1000


# ── 第 3 关：折扣 ──

def test_no_rules_total_is_subtotal():
    r = impl.PriceEngine().price([line(pizza("M"), 2), line(pizza("L"))])
    assert r.subtotal_cents == 3200 and r.total_cents == 3200 and r.discount_cents == 0


def test_percent_off_scoped_by_size_rounds_once():
    engine = impl.PriceEngine([impl.PercentOff("小号九折", "10", frozenset({"S"}))])
    r = engine.price([line(pizza("S", "thin", "cheese"), 1), line(pizza("L"), 1)])
    assert [a.cents for a in r.lines[0].adjustments] == [90]
    assert r.lines[1].adjustments == ()
    assert r.total_cents == 900 + 1200 - 90
    odd = impl.PriceEngine([impl.PercentOff("8.5%", "8.5")]).price([line(pizza("S", "thin", "cheese"))])
    assert odd.discount_cents == 77                           # 900 * 8.5% = 76.5 → 77，只舍入一次


def test_buy_x_get_y_uses_remaining_price_after_percent():
    engine = impl.PriceEngine([impl.PercentOff("九折", "10"), impl.BuyXGetY("买二送一", 2, 1)])
    r = engine.price([line(pizza("M"), 3)])
    assert [a.cents for a in r.lines[0].adjustments] == [300, 900]   # 3000 → 九折减 300 → 剩 2700，送 1/3 = 900
    assert r.total_cents == 1800


def test_buy_x_get_y_needs_full_group():
    r = impl.PriceEngine([impl.BuyXGetY("买二送一", 2, 1)]).price([line(pizza("M"), 2)])
    assert r.discount_cents == 0


def test_cheapest_free_per_n_groups_by_price():
    ps = [pizza("L", "thin", "pepperoni"), pizza("M"), pizza("S")]       # 1450, 1000, 800
    r = impl.PriceEngine([], [impl.CheapestFreePerN("三送一", 3)]).price([line(p) for p in ps])
    assert r.order_adjustments[0].cents == 800
    four = ps + [pizza("S", "thin", "olive")]                             # 1450, 1000, 900, 800
    r = impl.PriceEngine([], [impl.CheapestFreePerN("三送一", 3)]).price([line(p) for p in four])
    assert r.order_adjustments[0].cents == 900                            # 一组三份，免最便宜的组内一份


def test_cheapest_free_sees_discounted_prices_not_original():
    s, m = pizza("S"), pizza("M")                                         # 800, 1000
    engine = impl.PriceEngine([impl.PercentOff("小号半价", "50", frozenset({"S"}))],
                              [impl.CheapestFreePerN("二送一", 2)])
    r = engine.price([line(s), line(m)])
    assert r.lines[0].final_cents == 400
    assert r.order_adjustments[0].cents == 400                            # 免的是折后 400，不是原价 800
    assert r.total_cents == 1000


def test_threshold_uses_discounted_total():
    engine = impl.PriceEngine([impl.PercentOff("九折", "10")], [impl.ThresholdOff("满30减3", 3000, 300)])
    just_over = engine.price([line(pizza("L"), 3)])                       # 3600 → 3240 ≥ 3000
    assert just_over.order_adjustments[0].cents == 300 and just_over.total_cents == 2940
    under = engine.price([line(pizza("M"), 3)])                           # 3000 → 2700 < 3000
    assert under.order_adjustments == () and under.total_cents == 2700


def test_clamp_and_bad_rules():
    class Greedy(impl.LineRule):
        def apply(self, line, remaining_cents):
            return remaining_cents * 2
    r = impl.PriceEngine([Greedy("全免"), impl.PercentOff("九折", "10")],
                         [impl.ThresholdOff("满减", 100, 500)]).price([line(pizza("S"))])
    assert r.total_cents == 0 and r.lines[0].final_cents == 0 and r.order_adjustments == ()

    class Negative(impl.LineRule):
        def apply(self, line, remaining_cents):
            return -1
    with pytest.raises(impl.InvalidRuleError):
        impl.PriceEngine([Negative("坏")]).price([line(pizza("S"))])
    for bad in (lambda: impl.PercentOff("x", "0"), lambda: impl.PercentOff("x", "120"),
                lambda: impl.BuyXGetY("x", 0, 1), lambda: impl.ThresholdOff("x", 0, 5),
                lambda: impl.CheapestFreePerN("x", 1)):
        with pytest.raises(impl.InvalidRuleError):
            bad()


def test_new_rule_is_one_subclass():
    class FiftyOff(impl.LineRule):
        def apply(self, line, remaining_cents):
            return 50 * line.qty
    r = impl.PriceEngine([FiftyOff("每份减五毛")]).price([line(pizza("M"), 4)])
    assert r.discount_cents == 200 and r.total_cents == 3800


# ── 第 4 关：订单与并发 ──

def test_order_merges_equal_pizzas_and_returns_snapshots():
    order = impl.Order()
    order.add(pizza("M", "thin", "olive"), 1)
    order.add(pizza("M", "thin", "olive"), 2)
    order.add(pizza("L"))
    snap = order.lines
    assert sorted(l.qty for l in snap) == [1, 3]
    order.add(pizza("S"))
    assert len(snap) == 2 and len(order.lines) == 3                       # 旧快照不变


def test_order_rejects_bad_operations():
    order = impl.Order()
    with pytest.raises(impl.InvalidOrderError):
        order.add(pizza("M"), 0)
    with pytest.raises(impl.InvalidOrderError):
        order.remove(pizza("M"))
    order.add(pizza("M"))
    order.remove(pizza("M"))
    assert order.lines == ()


def test_receipt_invariant_over_random_orders():
    rng = random.Random(7)
    sizes, crusts = ["S", "M", "L"], ["thin", "thick"]
    tops = ["pepperoni", "mushroom", "olive", "pineapple"]
    engine = impl.PriceEngine(
        [impl.PercentOff("9折", "10"), impl.BuyXGetY("买二送一", 2, 1), impl.PercentOff("8.5", "8.5", frozenset({"S"}))],
        [impl.CheapestFreePerN("三送一", 3), impl.ThresholdOff("满减", 2500, 700)])
    for _ in range(80):
        lines = [line(pizza(rng.choice(sizes), rng.choice(crusts), *rng.sample(tops, rng.randint(0, 3))), rng.randint(1, 7))
                 for _ in range(rng.randint(1, 5))]
        r = engine.price(lines)
        assert 0 <= r.total_cents <= r.subtotal_cents
        assert r.subtotal_cents - r.discount_cents == r.total_cents
        assert all(x.final_cents >= 0 for x in r.lines)
        assert all(a.cents > 0 for x in r.lines for a in x.adjustments)


def test_concurrent_adds_lose_nothing():
    order, p = impl.Order(), pizza("M", "thin", "olive")
    barrier = threading.Barrier(8)

    def work():
        barrier.wait()
        for _ in range(200):
            order.add(p)
            impl.PriceEngine([impl.PercentOff("九折", "10")]).price(order.lines)

    threads = [threading.Thread(target=work) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert [l.qty for l in order.lines] == [1600]
