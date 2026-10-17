import importlib
import itertools
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

PEN = impl.Scope(frozenset({"pen"}))
BOOKS = impl.Scope(categories=frozenset({"books"}))


def cart_of(*rows: tuple) -> "impl.Cart":
    cart = impl.Cart()
    for row in rows:
        cart.add(*row)
    return cart


# ── 第 1 关：算总价的主流程 ──

def test_no_discount_total_is_the_sum():
    receipt = impl.PriceEngine().compute(cart_of(("a", 1000, 2), ("b", 550, 1)))
    assert receipt.subtotal_cents == 2550 and receipt.total_cents == 2550
    assert receipt.discount_cents == 0


def test_percent_off_all_products():
    engine = impl.PriceEngine([impl.PercentOff("九折", "10")])
    receipt = engine.compute(cart_of(("a", 1000, 2), ("b", 550, 1)))
    assert receipt.total_cents == 2295                      # 2550 - round(255)
    assert [a.label for r in receipt.lines for a in r.adjustments] == ["九折", "九折"]


def test_percent_off_respects_scope():
    engine = impl.PriceEngine([impl.PercentOff("图书八折", "20", BOOKS)])
    receipt = engine.compute(cart_of(("pen", 250, 4, "stationery"), ("novel", 1500, 1, "books")))
    assert receipt.total_cents == 1000 + 1200


def test_buy_x_get_y_turns_free_units_into_money():
    engine = impl.PriceEngine([impl.BuyXGetY("买2送1", 2, 1, PEN)])
    # 7 支笔，每 3 支送 1 支：7 // 3 = 2 支免费
    receipt = engine.compute(cart_of(("pen", 250, 7)))
    assert receipt.discount_cents == 500 and receipt.total_cents == 1250


def test_buy_x_get_y_not_eligible_below_group_size():
    engine = impl.PriceEngine([impl.BuyXGetY("买2送1", 2, 1, PEN)])
    receipt = engine.compute(cart_of(("pen", 250, 2)))
    assert receipt.discount_cents == 0 and receipt.lines[0].adjustments == ()


def test_threshold_off_uses_subtotal_after_line_discounts():
    engine = impl.PriceEngine([impl.PercentOff("八折", "20")], [impl.ThresholdOff("满100减10", 10000, 1000)])
    assert engine.compute(cart_of(("a", 12000, 1))).total_cents == 9600   # 折后 96.00 < 100，不触发
    assert engine.compute(cart_of(("a", 13000, 1))).total_cents == 9400   # 折后 104.00 ≥ 100，再减 10


# ── 第 2 关：叠加、顺序、钳位 ──

def test_stacking_is_sequential_on_the_remaining_price():
    engine = impl.PriceEngine([impl.PercentOff("A 九折", "10"), impl.PercentOff("B 九折", "10")])
    receipt = engine.compute(cart_of(("a", 10000, 1)))
    assert [a.cents for a in receipt.lines[0].adjustments] == [1000, 900]   # 不是 2000
    assert receipt.total_cents == 8100


def test_buy_x_get_y_after_percent_gives_free_units_at_discounted_price():
    engine = impl.PriceEngine([impl.PercentOff("八折", "20", PEN), impl.BuyXGetY("买2送1", 2, 1, PEN)])
    receipt = engine.compute(cart_of(("pen", 1000, 3)))
    assert [a.cents for a in receipt.lines[0].adjustments] == [600, 800]    # 送的那件是折后的 8.00
    assert receipt.total_cents == 1600


def test_best_only_takes_the_largest_discount_per_line():
    rules = [impl.PercentOff("九折", "10"), impl.PercentOff("七折", "30"), impl.PercentOff("九五折", "5")]
    receipt = impl.PriceEngine(rules, stacking=impl.Stacking.BEST_ONLY).compute(cart_of(("a", 10000, 1)))
    assert [a.label for a in receipt.lines[0].adjustments] == ["七折"]
    assert receipt.total_cents == 7000


def test_best_only_also_applies_to_cart_discounts():
    cart_rules = [impl.ThresholdOff("满100减5", 10000, 500), impl.ThresholdOff("满100减20", 10000, 2000)]
    receipt = impl.PriceEngine([], cart_rules, impl.Stacking.BEST_ONLY).compute(cart_of(("a", 12000, 1)))
    assert [a.label for a in receipt.cart_adjustments] == ["满100减20"]


def test_discount_never_pushes_a_price_below_zero():
    engine = impl.PriceEngine([impl.PercentOff("全免", "100"), impl.PercentOff("再九折", "10")],
                              [impl.ThresholdOff("无门槛减", 1, 5000)])
    receipt = engine.compute(cart_of(("a", 300, 1)))
    assert receipt.total_cents == 0 and receipt.lines[0].adjustments == (impl.Adjustment("全免", 300),)


def test_cart_threshold_is_rechecked_after_an_earlier_cart_discount():
    cart_rules = [impl.ThresholdOff("满100减30", 10000, 3000), impl.ThresholdOff("满100减10", 10000, 1000)]
    receipt = impl.PriceEngine([], cart_rules).compute(cart_of(("a", 11000, 1)))
    assert receipt.total_cents == 8000 and len(receipt.cart_adjustments) == 1   # 减完剩 80，第二条不再满足


# ── 钱与舍入 ──

def test_money_is_exact_integer_cents():
    assert impl.to_cents("0.10") + impl.to_cents("0.20") == impl.to_cents("0.30") == 30
    assert impl.to_cents("19.99") == 1999 and impl.format_cents(1999) == "19.99"
    assert impl.format_cents(5) == "0.05"


def test_percent_rounds_half_up_once_per_line():
    engine = impl.PriceEngine([impl.PercentOff("8.5%", "8.5")])
    receipt = engine.compute(cart_of(("a", 199, 1)))        # 199 * 8.5% = 16.915 → 17
    assert receipt.lines[0].adjustments[0].cents == 17
    assert engine.compute(cart_of(("b", 105, 1))).lines[0].adjustments[0].cents == 9   # 8.925 → 9


# ── 失败路径 ──

def test_invalid_cart_and_rules_raise():
    cart = impl.Cart()
    with pytest.raises(impl.InvalidCartError):
        cart.add("a", 100, 0)
    cart.add("a", 100, 1)
    with pytest.raises(impl.InvalidCartError):
        cart.add("a", 200, 1)
    with pytest.raises(impl.InvalidCartError):
        cart.remove("zzz")
    with pytest.raises(impl.InvalidRuleError):
        impl.PercentOff("x", "0")
    with pytest.raises(impl.InvalidRuleError):
        impl.PercentOff("x", "120")
    with pytest.raises(impl.InvalidRuleError):
        impl.BuyXGetY("x", 0, 1)


def test_a_discount_that_returns_a_negative_amount_is_rejected():
    class Cheat(impl.LineDiscount):
        def apply(self, line, remaining_cents):
            return -100                                      # 想让总价变高
    with pytest.raises(impl.InvalidRuleError):
        impl.PriceEngine([Cheat("cheat")]).compute(cart_of(("a", 1000, 1)))


# ── 第 3 关：新规则只加类、引擎不动 ──

def test_new_discount_is_one_subclass_and_engine_is_untouched():
    class FixedOffPerUnit(impl.LineDiscount):
        def __init__(self, label, cents):
            super().__init__(label)
            self.cents = cents

        def apply(self, line, remaining_cents):
            return self.cents * line.qty

    receipt = impl.PriceEngine([FixedOffPerUnit("每件减1元", 100)]).compute(cart_of(("a", 500, 3)))
    assert receipt.total_cents == 1200


def test_same_sku_merges_and_cart_returns_snapshots():
    cart = cart_of(("a", 100, 1), ("a", 100, 2))
    snapshot = cart.lines
    cart.add("b", 50, 1)
    assert len(snapshot) == 1 and snapshot[0].qty == 3 and len(cart.lines) == 2
    cart.remove("a")
    assert [l.sku for l in cart.lines] == ["b"]


# ── 属性：账单永远自洽 ──

def test_receipt_is_always_consistent_over_random_carts():
    rng = random.Random(7)
    rules = [impl.PercentOff("p10", "10"), impl.PercentOff("p33", "33.3", BOOKS),
             impl.BuyXGetY("b2g1", 2, 1), impl.BuyXGetY("b1g1", 1, 1, PEN)]
    cart_rules = [impl.ThresholdOff("t50", 5000, 700), impl.ThresholdOff("t200", 20000, 3000)]
    for seed, mode in itertools.product(range(60), impl.Stacking):
        cart = impl.Cart()
        for i in range(rng.randint(1, 5)):
            cart.add(f"s{i}", rng.randint(0, 9999), rng.randint(1, 9), rng.choice(["books", "pen", ""]))
        cart.add("pen", rng.randint(1, 500), rng.randint(1, 9), "stationery")
        receipt = impl.PriceEngine(rules, cart_rules, mode).compute(cart)
        assert 0 <= receipt.total_cents <= receipt.subtotal_cents
        assert receipt.subtotal_cents - receipt.discount_cents == receipt.total_cents
        assert all(r.final_cents >= 0 for r in receipt.lines)
        assert all(a.cents > 0 for r in receipt.lines for a in r.adjustments)


# ── 第 4 关：并发 ──

def test_engine_is_shareable_and_cart_adds_do_not_lose_updates():
    cart = impl.Cart()
    engine = impl.PriceEngine([impl.PercentOff("九折", "10")])
    barrier = threading.Barrier(8)

    def worker() -> None:
        barrier.wait()
        for _ in range(200):
            cart.add("a", 100, 1)
            engine.compute(cart)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert cart.lines[0].qty == 1600
    assert engine.compute(cart).total_cents == 1600 * 100 - 16000
