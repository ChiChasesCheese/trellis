import dataclasses
import importlib
import json
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

MAX_Q = 1_000_000
MAX_PRICE = 1_000_000


def prod(i, price=100, name=None):
    return impl.Product(f"p{i}", name or f"Item {i}", price)


def cart_of(*prices):
    return impl.ShoppingCart([prod(i + 1, p) for i, p in enumerate(prices)])


def plain(snapshot):
    return dataclasses.asdict(snapshot)


def ids(snapshot):
    return [item.id for item in snapshot.items]


# ---- README 的例子 ----

def test_readme_example_exact_shape():
    cart = impl.ShoppingCart([impl.Product("p1", "Canvas Hat", 1250)])
    cart.addLine("p1")
    cart.updateLine("p1", 3)
    assert plain(cart.snapshot()) == {
        "products": [{"id": "p1", "name": "Canvas Hat", "priceCents": 1250, "cartQuantity": 3}],
        "items": [{"id": "p1", "name": "Canvas Hat", "priceCents": 1250, "quantity": 3, "lineTotalCents": 3750}],
        "totalQuantity": 3,
        "totalPriceCents": 3750,
        "empty": False,
    }
    # 能被 JSON 序列化：HTTP 适配器就是这样把快照发出去的
    assert json.loads(json.dumps(plain(cart.snapshot())))["totalPriceCents"] == 3750


def test_readme_example_remove_then_readd_goes_last():
    cart = cart_of(10, 20)
    cart.addLine("p1")
    cart.addLine("p2")
    cart.updateLine("p1", 0)
    cart.addLine("p1")
    shot = cart.snapshot()
    assert ids(shot) == ["p2", "p1"]
    assert [p.id for p in shot.products] == ["p1", "p2"]  # 目录原序不变


# ---- 顺序规则 ----

def test_existing_line_keeps_position_on_add_and_update():
    cart = cart_of(1, 1, 1)
    for pid in ("p2", "p1", "p3"):
        cart.addLine(pid)
    cart.addLine("p2")  # 已有的行加一：不挪位置
    cart.updateLine("p1", 5)  # 已有的行改量：不挪位置
    shot = cart.snapshot()
    assert ids(shot) == ["p2", "p1", "p3"]
    assert [item.quantity for item in shot.items] == [2, 5, 1]


def test_positive_update_creates_line_at_end():
    cart = cart_of(1, 1, 1)
    cart.addLine("p3")
    cart.updateLine("p1", 4)  # 正数更新可以新建行，落在末尾
    assert ids(cart.snapshot()) == ["p3", "p1"]


def test_zero_update_removes_line_and_absent_is_noop():
    cart = cart_of(5, 7)
    cart.updateLine("p1", 0)  # 不存在：什么都不做
    assert cart.line_count == 0 and cart.snapshot().empty
    cart.updateLine("p2", 2)
    cart.updateLine("p2", 0)
    shot = cart.snapshot()
    assert cart.line_count == 0 and shot.items == [] and shot.empty is True
    assert [p.cartQuantity for p in shot.products] == [0, 0]


def test_update_is_absolute_not_a_delta():
    cart = cart_of(10)
    cart.updateLine("p1", 3)
    cart.updateLine("p1", 3)
    assert cart.snapshot().totalQuantity == 3
    cart.updateLine("p1", 1)
    assert cart.snapshot().items[0].lineTotalCents == 10


def test_remove_and_readd_through_update_also_goes_last():
    cart = cart_of(1, 1, 1)
    for pid in ("p1", "p2", "p3"):
        cart.addLine(pid)
    cart.updateLine("p1", 0)
    cart.updateLine("p1", 2)
    assert ids(cart.snapshot()) == ["p2", "p3", "p1"]


# ---- 合计与精确整数 ----

def test_empty_cart_and_empty_catalogue():
    shot = cart_of(1, 2).snapshot()
    assert (shot.totalQuantity, shot.totalPriceCents, shot.empty, shot.items) == (0, 0, True, [])
    nothing = impl.ShoppingCart([]).snapshot()
    assert (nothing.products, nothing.items, nothing.totalQuantity, nothing.totalPriceCents, nothing.empty) == (
        [], [], 0, 0, True)


def test_totals_beyond_32_bit_are_exact_integers():
    # 单行 10**12；一百个商品都满额，总价 100 * 10**12，两者都由常量推出，不是跑出来再抄的
    line_max = MAX_PRICE * MAX_Q
    assert line_max > 2**32
    cart = impl.ShoppingCart([prod(i, MAX_PRICE) for i in range(100)])
    for i in range(100):
        cart.updateLine(f"p{i}", MAX_Q)
    shot = cart.snapshot()
    assert all(item.lineTotalCents == line_max and type(item.lineTotalCents) is int for item in shot.items)
    assert shot.totalPriceCents == 100 * line_max and type(shot.totalPriceCents) is int
    assert shot.totalQuantity == 100 * MAX_Q


def test_totals_with_odd_prices_have_no_rounding():
    cart = cart_of(1, 999_999, 0)
    cart.updateLine("p1", 7)
    cart.updateLine("p2", 999_999)
    cart.updateLine("p3", 12)  # 价格为 0 的商品也是一行
    shot = cart.snapshot()
    assert [i.lineTotalCents for i in shot.items] == [7, 999_999 * 999_999, 0]
    assert shot.totalPriceCents == 7 + 999_999 * 999_999
    assert shot.totalQuantity == 7 + 999_999 + 12
    assert shot.empty is False


def test_types_are_plain_ints_and_bool():
    cart = cart_of(250)
    cart.addLine("p1")
    shot = cart.snapshot()
    for value in (shot.totalQuantity, shot.totalPriceCents, shot.items[0].quantity, shot.items[0].lineTotalCents,
                  shot.products[0].cartQuantity, shot.products[0].priceCents):
        assert type(value) is int
    assert type(shot.empty) is bool
    assert [f.name for f in dataclasses.fields(shot.items[0])] == ["id", "name", "priceCents", "quantity",
                                                                  "lineTotalCents"]
    assert [f.name for f in dataclasses.fields(shot.products[0])] == ["id", "name", "priceCents", "cartQuantity"]


def test_equal_names_and_prices_are_distinct_products():
    cart = impl.ShoppingCart([impl.Product("a", "Same", 500), impl.Product("b", "Same", 500)])
    cart.addLine("b")
    shot = cart.snapshot()
    assert [p.cartQuantity for p in shot.products] == [0, 1]
    assert ids(shot) == ["b"]


# ---- 隔离 ----

def test_constructor_copies_caller_catalogue():
    products = [prod(1, 100), prod(2, 200)]
    cart = impl.ShoppingCart(products)
    before = [dataclasses.asdict(p) for p in products]
    assert [dataclasses.asdict(p) for p in products] == before  # 构造不修改调用方的对象
    products[0].name = "changed outside"
    products[0].priceCents = 17
    products.clear()
    cart.addLine("p1")
    shot = cart.snapshot()
    assert [p.name for p in shot.products] == ["Item 1", "Item 2"]
    assert shot.items[0].priceCents == 100 and shot.totalPriceCents == 100


def test_old_snapshots_never_change():
    cart = cart_of(10, 20)
    cart.addLine("p1")
    first = cart.snapshot()
    frozen = plain(first)
    cart.addLine("p2")
    cart.updateLine("p1", 9)
    cart.updateLine("p1", 0)
    assert plain(first) == frozen
    assert plain(cart.snapshot()) != frozen


def test_mutating_a_returned_snapshot_cannot_reach_the_cart():
    cart = cart_of(10, 20)
    cart.addLine("p2")
    expected = plain(cart.snapshot())
    victim = cart.snapshot()
    victim.items[0].quantity = 99
    victim.items[0].name = "x"
    victim.products[0].cartQuantity = 5
    victim.products.clear()
    victim.items.clear()
    victim.totalPriceCents = -1
    victim.empty = True
    assert plain(cart.snapshot()) == expected
    assert cart.line_count == 1


def test_two_snapshots_do_not_share_objects():
    cart = cart_of(10)
    cart.addLine("p1")
    a, b = cart.snapshot(), cart.snapshot()
    assert a == b
    assert a.items is not b.items and a.products is not b.products
    assert a.items[0] is not b.items[0] and a.products[0] is not b.products[0]


def test_two_carts_are_independent_even_with_shared_product_objects():
    shared = [prod(1, 100), prod(2, 200)]
    one, two = impl.ShoppingCart(shared), impl.ShoppingCart(shared)
    one.addLine("p1")
    one.updateLine("p2", 3)
    assert two.snapshot().empty and two.line_count == 0
    two.addLine("p2")
    assert ids(one.snapshot()) == ["p1", "p2"] and ids(two.snapshot()) == ["p2"]
    assert one.snapshot().items[1].quantity == 3


# ---- 失败不留痕 ----

def test_unknown_product_raises_and_changes_nothing():
    cart = cart_of(10)
    cart.addLine("p1")
    before = plain(cart.snapshot())
    with pytest.raises(impl.UnknownProductError):
        cart.addLine("nope")
    with pytest.raises(impl.UnknownProductError):
        cart.updateLine("nope", 0)
    with pytest.raises(impl.UnknownProductError):
        cart.updateLine("nope", -1)  # ID 与数量同时有错：先报未知商品
    assert plain(cart.snapshot()) == before


@pytest.mark.parametrize("bad", [-1, MAX_Q + 1, True, 1.0, "3", None])
def test_bad_quantity_raises_and_changes_nothing(bad):
    cart = cart_of(10, 20)
    cart.updateLine("p1", 2)
    before = plain(cart.snapshot())
    with pytest.raises(impl.QuantityError):
        cart.updateLine("p2", bad)
    with pytest.raises(impl.QuantityError):
        cart.updateLine("p1", bad)  # 已有的行也不能被坏数量改动
    assert plain(cart.snapshot()) == before


def test_quantity_bounds_are_inclusive_and_add_stops_at_the_cap():
    cart = cart_of(1)
    cart.updateLine("p1", MAX_Q)
    assert cart.snapshot().totalQuantity == MAX_Q
    before = plain(cart.snapshot())
    with pytest.raises(impl.QuantityError):
        cart.addLine("p1")  # 加一会超过上限
    assert plain(cart.snapshot()) == before
    cart.updateLine("p1", MAX_Q - 1)
    cart.addLine("p1")
    assert cart.snapshot().items[0].quantity == MAX_Q
    cart.updateLine("p1", 999)
    cart.addLine("p1")
    assert cart.snapshot().items[0].quantity == 1000


def test_catalogue_with_duplicate_ids_is_rejected():
    with pytest.raises(ValueError):
        impl.ShoppingCart([impl.Product("a", "x", 1), impl.Product("a", "y", 2)])


# ---- 与朴素模型对拍 ----

class NaiveModel:
    """最笨的参考：用一个 (id, 数量) 列表，删除就真的从列表里拿掉，加回来就 append。"""

    def __init__(self, catalogue):
        self.catalogue = catalogue
        self.lines = []

    def find(self, pid):
        return next((i for i, (p, _) in enumerate(self.lines) if p == pid), None)

    def add(self, pid):
        i = self.find(pid)
        if i is None:
            self.lines.append((pid, 1))
        else:
            self.lines[i] = (pid, self.lines[i][1] + 1)

    def update(self, pid, q):
        i = self.find(pid)
        if q == 0:
            if i is not None:
                del self.lines[i]
        elif i is None:
            self.lines.append((pid, q))
        else:
            self.lines[i] = (pid, q)


def test_random_sequences_match_naive_model_for_ten_thousand_calls():
    rng = random.Random(20261116)
    catalogue = {f"p{i}": (rng.randint(0, MAX_PRICE), f"N{i}") for i in range(100)}
    cart = impl.ShoppingCart([impl.Product(pid, name, price) for pid, (price, name) in catalogue.items()])
    model = NaiveModel(catalogue)
    held = []
    for step in range(10_000):  # 合同里每辆购物车至多 10_000 次修改
        pid = f"p{rng.randrange(100)}"
        roll = rng.random()
        at_cap = any(p == pid and q == MAX_Q for p, q in model.lines)
        if roll < 0.5 and at_cap:  # 合同保证调用方不会在上限上再加；这里验证它被拒绝且不留痕
            with pytest.raises(impl.QuantityError):
                cart.addLine(pid)
        elif roll < 0.5:
            model.add(pid)
            cart.addLine(pid)
        elif roll < 0.75:
            model.update(pid, 0)
            cart.updateLine(pid, 0)
        else:
            q = rng.choice([1, 2, 999, 1000, MAX_Q])
            model.update(pid, q)
            cart.updateLine(pid, q)
        if step % 500 == 0:
            shot = cart.snapshot()
            held.append((shot, plain(shot)))
        if step % 97 == 0:
            shot = cart.snapshot()
            assert [(i.id, i.quantity) for i in shot.items] == model.lines
            assert shot.totalQuantity == sum(q for _, q in model.lines)
            assert shot.totalPriceCents == sum(catalogue[p][0] * q for p, q in model.lines)
            assert shot.empty == (not model.lines)
            assert cart.line_count == len(model.lines)
    assert all(plain(shot) == frozen for shot, frozen in held)  # 一路上拿的旧快照一个都没变


def test_quantity_of_and_error_details():
    cart = cart_of(10, 20)
    assert cart.quantityOf("p1") == 0
    cart.updateLine("p1", 4)
    cart.addLine("p1")
    assert cart.quantityOf("p1") == 5 and cart.quantityOf("p2") == 0
    with pytest.raises(impl.UnknownProductError) as unknown:
        cart.quantityOf("zz")
    assert unknown.value.product_id == "zz"
    with pytest.raises(impl.QuantityError) as bad:
        cart.updateLine("p2", -3)
    assert (bad.value.product_id, bad.value.quantity) == ("p2", -3)


def test_free_item_makes_cart_non_empty_with_zero_totals():
    cart = cart_of(0, 500)
    cart.addLine("p1")  # 单价 0：总价是 0，但购物车不空
    shot = cart.snapshot()
    assert shot.totalPriceCents == 0 and shot.totalQuantity == 1
    assert shot.empty is False and ids(shot) == ["p1"]
    assert shot.items[0].lineTotalCents == 0
