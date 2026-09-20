"""在线购物（Online Shopping）的验收测试：`IMPL=solution` 全绿，`IMPL=starter` 全红。"""

from __future__ import annotations

import importlib
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

START = datetime(2026, 5, 1, 10, 0, tzinfo=UTC)


class Clock:
    """注入的时钟：测试自己推时间，不靠 `sleep`。"""

    def __init__(self) -> None:
        self.now = START

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kwargs: float) -> None:
        self.now += timedelta(**kwargs)


class Gateway:
    """可编程的支付网关替身，忠实实现幂等键契约：同一个键只扣一次，
    对没扣过款的键退款是无操作。`outstanding` 是还没退回去的钱。"""

    def __init__(self, decline: bool = False, lose_receipt: bool = False) -> None:
        self.decline = decline
        self.lose_receipt = lose_receipt
        self.charges: list[tuple[str, int]] = []
        self.refunds: list[str] = []
        self._held: dict[str, int] = {}

    def charge(self, idempotency_key: str, amount: int) -> str:
        if self.decline:
            raise impl.PaymentDeclinedError("卡被拒了")
        if idempotency_key not in self._held:
            self._held[idempotency_key] = amount
            self.charges.append((idempotency_key, amount))
        if self.lose_receipt:               # 钱已经扣了，但回执在返回途中丢了
            raise impl.PaymentDeclinedError("扣款成功但回执丢失")
        return f"ch_{idempotency_key}"

    def refund(self, idempotency_key: str) -> None:
        if self._held.pop(idempotency_key, None) is None:
            return                          # 没扣过款，退款是无操作
        self.refunds.append(idempotency_key)

    @property
    def outstanding(self) -> dict[str, int]:
        """扣了还没退的钱；Saga 回滚之后它必须是空的。"""
        return dict(self._held)


class Shipper:
    """可编程的履约替身。"""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.shipments: list[str] = []
        self.cancelled: list[str] = []

    def create_shipment(self, order_id: str) -> str:
        if self.fail:
            raise impl.FulfilmentError("没有可用运力")
        self.shipments.append(order_id)
        return f"sh{len(self.shipments)}"

    def cancel_shipment(self, shipment_id: str) -> None:
        self.cancelled.append(shipment_id)


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.fixture
def catalogue():
    c = impl.Catalogue()
    c.add_product(impl.Product("p1", "机械键盘", "peripherals"))
    c.add_product(impl.Product("p2", "鼠标垫"))
    c.add_listing(impl.Listing("l1", "seller-a", "p1", 39900))
    c.add_listing(impl.Listing("l2", "seller-b", "p1", 36900))
    c.add_listing(impl.Listing("l3", "seller-a", "p2", 4900))
    return c


def make_shop(catalogue, clock, gateway=None, shipper=None, rules=(), ttl=timedelta(minutes=15)):
    inventory = impl.Inventory(clock=clock)
    inventory.receive("l1", 5)
    inventory.receive("l2", 2)
    inventory.receive("l3", 10)
    shop = impl.ShoppingService(catalogue, inventory, gateway or Gateway(), shipper or Shipper(),
                                clock=clock, reservation_ttl=ttl, pricing_rules=rules)
    return shop, inventory


# --------------------------------------------------------------------------
# 第 1 关：目录、购物车、结账产出订单
# --------------------------------------------------------------------------

def test_checkout_turns_a_cart_into_an_order(catalogue, clock):
    shop, inventory = make_shop(catalogue, clock)
    shop.add_to_cart("u1", "l1", 2)
    shop.add_to_cart("u1", "l3", 1)
    order = shop.checkout("u1")
    assert order.state is impl.OrderState.SHIPPED
    assert order.subtotal == 39900 * 2 + 4900
    assert order.total == order.subtotal
    assert {line.listing_id: line.quantity for line in order.lines} == {"l1": 2, "l3": 1}
    assert shop.order(order.id) is order
    assert shop.cart_for("u1").is_empty          # 结完账的购物车是空的


def test_cart_line_disappears_when_its_quantity_reaches_zero(catalogue, clock):
    shop, _ = make_shop(catalogue, clock)
    cart = shop.cart_for("u1")
    cart.add("l1", 2)
    cart.remove("l1", 1)
    assert cart.lines == (impl.CartLine("l1", 1),)
    cart.remove("l1", 5)                         # 减多了
    assert cart.lines == ()                      # 留下的是空车，不是一行 quantity=0
    assert cart.is_empty
    with pytest.raises(impl.UnknownItemError):
        cart.remove("l1")


def test_unknown_listing_and_empty_cart_are_rejected(catalogue, clock):
    shop, _ = make_shop(catalogue, clock)
    with pytest.raises(impl.UnknownItemError):
        shop.add_to_cart("u1", "nope")
    with pytest.raises(impl.EmptyCartError):
        shop.checkout("u1")
    with pytest.raises(impl.UnknownItemError):
        catalogue.add_listing(impl.Listing("l9", "seller-c", "ghost", 100))


def test_order_line_price_is_a_snapshot(catalogue, clock):
    """下单那一刻的单价被抄进订单行；卖家事后改价不追溯已下的单。"""
    shop, _ = make_shop(catalogue, clock)
    shop.add_to_cart("u1", "l2", 1)
    order = shop.checkout("u1")
    catalogue.add_listing(impl.Listing("l2", "seller-b", "p1", 99900))   # 同 id 改价
    assert order.lines[0].unit_price == 36900
    assert order.total == 36900


def test_updating_a_listing_does_not_duplicate_the_secondary_index(catalogue):
    """回归测试：同一个 id 再写一次是改价，不该让这个卖家在同款列表里出现两次；
    改挂到另一件商品下时要从原来那一格摘掉，空了的那一格整格删除。"""
    catalogue.add_listing(impl.Listing("l2", "seller-b", "p1", 30900))
    assert [l.id for l in catalogue.listings_for("p1")] == ["l2", "l1"]
    catalogue.add_listing(impl.Listing("l1", "seller-a", "p2", 100))     # 改挂到别的商品
    assert [l.id for l in catalogue.listings_for("p1")] == ["l2"]
    assert [l.id for l in catalogue.listings_for("p2")] == ["l1", "l3"]


# --------------------------------------------------------------------------
# 第 2 关：库存预留与过期
# --------------------------------------------------------------------------

def test_adding_to_cart_does_not_reserve_stock(catalogue, clock):
    """刻意的取舍：加购不锁货，所以两个人可以同时把最后两件加进购物车。"""
    shop, inventory = make_shop(catalogue, clock)
    shop.add_to_cart("u1", "l2", 2)
    shop.add_to_cart("u2", "l2", 2)
    assert inventory.available("l2") == 2
    shop.checkout("u1")
    assert inventory.available("l2") == 0
    with pytest.raises(impl.SagaFailure) as caught:
        shop.checkout("u2")
    assert isinstance(caught.value.cause, impl.OutOfStockError)


def test_reservation_is_all_or_nothing(catalogue, clock):
    shop, inventory = make_shop(catalogue, clock)
    with pytest.raises(impl.OutOfStockError):
        inventory.reserve({"l2": 1, "l1": 99}, timedelta(minutes=15))
    assert inventory.available("l2") == 2        # 够的那一行也没有被部分预留
    assert inventory.open_reservations == 0


def test_a_reservation_expires_on_the_injected_clock(catalogue, clock):
    shop, inventory = make_shop(catalogue, clock)
    reservation = inventory.reserve({"l2": 2}, timedelta(minutes=15))
    assert inventory.available("l2") == 0
    clock.advance(minutes=16)
    assert inventory.available("l2") == 2        # 额度自己回来了
    assert inventory.open_reservations == 0      # 过期的预留真的被删掉了，不是留着不算
    with pytest.raises(impl.OutOfStockError):    # 过期之后不能再提交
        inventory.commit(reservation.id)
    assert inventory.on_hand("l2") == 2


def test_release_is_idempotent(catalogue, clock):
    _, inventory = make_shop(catalogue, clock)
    reservation = inventory.reserve({"l1": 3}, timedelta(minutes=15))
    inventory.release(reservation.id)
    inventory.release(reservation.id)            # 补偿动作可能被重复调用
    inventory.release("R-never-existed")
    inventory.release("")
    assert inventory.available("l1") == 5
    assert inventory.open_reservations == 0


def test_commit_deducts_and_clears_the_reservation(catalogue, clock):
    _, inventory = make_shop(catalogue, clock)
    reservation = inventory.reserve({"l1": 3}, timedelta(minutes=15))
    inventory.commit(reservation.id)
    assert inventory.on_hand("l1") == 2
    assert inventory.available("l1") == 2
    assert inventory.open_reservations == 0


# --------------------------------------------------------------------------
# 第 3 关：订单状态机与 Saga 补偿
# --------------------------------------------------------------------------

def test_illegal_transitions_raise_instead_of_being_ignored(catalogue, clock):
    order = impl.Order("O1", "u1", [impl.OrderLine("l1", "键盘", 100, 1)], 0, START)
    assert order.state is impl.OrderState.CREATED
    with pytest.raises(impl.IllegalTransitionError):
        order.transition_to(impl.OrderState.SHIPPED, START)      # 没付款不能发货
    order.transition_to(impl.OrderState.PAID, START)
    order.transition_to(impl.OrderState.SHIPPED, START)
    order.transition_to(impl.OrderState.DELIVERED, START)
    with pytest.raises(impl.IllegalTransitionError):
        order.transition_to(impl.OrderState.CANCELLED, START)    # 终态没有出边
    assert [(c.from_state, c.to_state) for c in order.history] == [
        (impl.OrderState.CREATED, impl.OrderState.PAID),
        (impl.OrderState.PAID, impl.OrderState.SHIPPED),
        (impl.OrderState.SHIPPED, impl.OrderState.DELIVERED),
    ]


def test_declined_payment_releases_the_reservation(catalogue, clock):
    gateway = Gateway(decline=True)
    shop, inventory = make_shop(catalogue, clock, gateway=gateway)
    shop.add_to_cart("u1", "l2", 2)
    with pytest.raises(impl.SagaFailure) as caught:
        shop.checkout("u1")
    assert caught.value.step == "扣款"
    assert isinstance(caught.value.cause, impl.PaymentDeclinedError)
    assert inventory.available("l2") == 2        # 预留被补偿掉了
    assert inventory.on_hand("l2") == 2
    assert inventory.open_reservations == 0
    assert gateway.refunds == []                 # 根本没扣款，就不该有退款
    assert shop.order("O1").state is impl.OrderState.CANCELLED
    assert not shop.cart_for("u1").is_empty      # 购物车保留，用户可以重试


def test_failed_shipment_refunds_and_restocks(catalogue, clock):
    gateway, shipper = Gateway(), Shipper(fail=True)
    shop, inventory = make_shop(catalogue, clock, gateway=gateway, shipper=shipper)
    shop.add_to_cart("u1", "l2", 2)
    with pytest.raises(impl.SagaFailure) as caught:
        shop.checkout("u1")
    assert caught.value.step == "发货"
    assert caught.value.compensation_errors == ()
    assert gateway.charges == [("O1", 73800)]                # 钱扣了
    assert gateway.refunds == ["O1"] and gateway.outstanding == {}   # 又退了
    assert inventory.on_hand("l2") == 2                      # 货补回来了
    assert inventory.available("l2") == 2
    assert inventory.open_reservations == 0
    assert shipper.cancelled == []                           # 运单没建成，不必取消
    assert shop.order("O1").state is impl.OrderState.CANCELLED


def test_the_failing_step_compensates_itself(catalogue, clock):
    """回归测试：一个动作不是原子的——钱扣了、回执在返回途中丢了。只补偿"已完成"的
    步骤，或者只凭回执号退款，都会把这笔钱永远留在半路上。失败的那一步自己也要被补偿，
    而且补偿按幂等键（订单号）寻址，不依赖那个根本没拿到的回执。"""
    gateway = Gateway(lose_receipt=True)
    shop, inventory = make_shop(catalogue, clock, gateway=gateway)
    shop.add_to_cart("u1", "l2", 1)
    with pytest.raises(impl.SagaFailure) as caught:
        shop.checkout("u1")
    assert caught.value.step == "扣款"
    assert gateway.charges == [("O1", 36900)]
    assert gateway.refunds == ["O1"]             # 失败那一步的补偿也跑了
    assert gateway.outstanding == {}             # 没有一分钱卡在半路
    assert inventory.available("l2") == 2
    assert inventory.on_hand("l2") == 2          # 而且没有凭空补出库存
    assert shop.order("O1").state is impl.OrderState.CANCELLED


def test_saga_compensates_in_reverse_order_and_reports_failures():
    log: list[str] = []

    def step(name: str, fail: bool = False, comp_fail: bool = False):
        def action() -> None:
            log.append(f"do-{name}")
            if fail:
                raise ShopBoom(name)

        def compensation() -> None:
            log.append(f"undo-{name}")
            if comp_fail:
                raise ShopBoom(f"undo-{name}")

        return impl.SagaStep(name, action, compensation)

    class ShopBoom(impl.ShopError):
        pass

    steps = [step("a"), step("b", comp_fail=True), step("c", fail=True)]
    with pytest.raises(impl.SagaFailure) as caught:
        impl.Saga().run(steps)
    assert log == ["do-a", "do-b", "do-c", "undo-c", "undo-b", "undo-a"]
    assert caught.value.step == "c"
    assert [name for name, _ in caught.value.compensation_errors] == ["b"]
    assert isinstance(caught.value.cause, ShopBoom)


def test_expired_reservation_is_caught_at_commit(catalogue, clock):
    """预留在扣款途中过期：提交必须失败，钱要退，库存不能凭空多出来。"""
    class SlowGateway(Gateway):
        def charge(self, idempotency_key: str, amount: int) -> str:
            clock.advance(minutes=20)            # 用户在支付页上磨蹭了二十分钟
            return super().charge(idempotency_key, amount)

    gateway = SlowGateway()
    shop, inventory = make_shop(catalogue, clock, gateway=gateway, ttl=timedelta(minutes=15))
    shop.add_to_cart("u1", "l2", 2)
    with pytest.raises(impl.SagaFailure) as caught:
        shop.checkout("u1")
    assert caught.value.step == "扣减库存"
    assert gateway.refunds == ["O1"] and gateway.outstanding == {}
    assert inventory.on_hand("l2") == 2
    assert inventory.available("l2") == 2


def test_no_oversell_under_concurrent_checkout(catalogue, clock):
    """真线程 + 屏障：断言的是不变式（成功笔数 == 库存数、现货不为负），不是时序。"""
    shop, inventory = make_shop(catalogue, clock)
    buyers = 10
    barrier = threading.Barrier(buyers)
    succeeded: list[str] = []
    lock = threading.Lock()

    def buy(i: int) -> None:
        shop.add_to_cart(f"u{i}", "l1", 1)
        barrier.wait()
        try:
            order = shop.checkout(f"u{i}")
        except impl.SagaFailure:
            return
        with lock:
            succeeded.append(order.id)

    threads = [threading.Thread(target=buy, args=(i,)) for i in range(buyers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(succeeded) == 5                   # 只有 5 件现货
    assert inventory.on_hand("l1") == 0
    assert inventory.available("l1") == 0
    assert inventory.open_reservations == 0


# --------------------------------------------------------------------------
# 第 4 关：第二个卖家、促销规则——都不碰下单流程
# --------------------------------------------------------------------------

def test_a_second_seller_is_just_another_listing(catalogue, clock):
    shop, _ = make_shop(catalogue, clock)
    offers = catalogue.listings_for("p1")
    assert [l.seller_id for l in offers] == ["seller-b", "seller-a"]     # 按价格从低到高
    catalogue.add_listing(impl.Listing("l4", "seller-c", "p1", 35900))
    assert [l.seller_id for l in catalogue.listings_for("p1")][0] == "seller-c"
    shop.add_to_cart("u1", "l4", 1)                                     # 下单流程一行没改
    with pytest.raises(impl.SagaFailure):                               # 新卖家还没入库
        shop.checkout("u1")


def test_a_pricing_rule_is_just_a_function(catalogue, clock):
    rules = [impl.percentage_off(10, minimum_subtotal=30000),
             lambda lines: 500 if len(lines) >= 2 else 0]
    shop, _ = make_shop(catalogue, clock, rules=rules)
    shop.add_to_cart("u1", "l3", 1)              # 4900，不满减
    small = shop.checkout("u1")
    assert small.discount == 0 and small.total == 4900

    shop.add_to_cart("u2", "l2", 1)              # 36900 + 4900 = 41800
    shop.add_to_cart("u2", "l3", 1)
    big = shop.checkout("u2")
    assert big.subtotal == 41800
    assert big.discount == 41800 * 10 // 100 + 500
    assert big.total == big.subtotal - big.discount
