"""在线购物（Online Shopping）——目录、购物车、库存预留、订单状态机与 Saga 补偿的参考实现。

核心思路：价格和库存挂在挂牌（Listing）上而不是商品（Product）上，所以"同一个商品第二个
卖家"只是多一行挂牌，下单流程一行不改。库存不在加购时扣，而在下单时预留一份带过期时间的
Reservation，过期由注入的时钟判定、并且真的从字典里被清掉——超卖与少卖的取舍写在这一处。
订单生命周期是一张显式的转移表，非法转移抛异常而不是被静默忽略。结账跨"预留—扣款—扣减—
发货"四步，用一个通用的 Saga：任何一步失败，已完成的步骤按相反顺序执行各自的补偿动作，
补偿必须幂等。定价规则是一串普通函数，加一条促销不需要新建任何类。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from itertools import count
from threading import RLock
from typing import Protocol


class ShopError(Exception):
    """本设计里所有失败路径的公共基类，方便调用方一次性捕获。"""


class UnknownItemError(ShopError):
    """引用了一个目录里不存在的商品或挂牌。"""


class EmptyCartError(ShopError):
    """对空购物车结账。"""


class OutOfStockError(ShopError):
    """可用库存不足，预留失败。"""


class IllegalTransitionError(ShopError):
    """订单被要求做一次转移表不允许的状态变更。"""


class PaymentDeclinedError(ShopError):
    """支付被拒。"""


class FulfilmentError(ShopError):
    """发货环节失败。"""


# --------------------------------------------------------------------------
# 目录：商品是"卖什么"，挂牌是"谁按什么价卖它"。价格和库存都挂在挂牌上——
# 这是第 4 关"同一个商品出现第二个卖家"唯一需要的准备，代价只是第 1 关多一个字段。
# --------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Product:
    """一件商品：只有描述性信息，没有价格，也没有库存。"""

    id: str
    title: str
    category: str = "misc"


@dataclass(frozen=True, slots=True)
class Listing:
    """某个卖家对某件商品的挂牌：价格（整数最小货币单位）和库存都归它。"""

    id: str
    seller_id: str
    product_id: str
    price: int


class Catalogue:
    """商品目录：按 id 查商品和挂牌，按商品查它的全部挂牌。

    `_by_product` 是一张二级索引，把"这件商品有哪些卖家"从一次全表扫描降到一次字典查找；
    它的代价是每次新增挂牌要同时维护两份结构，因此新增只有 `add_listing` 一个入口。
    """

    def __init__(self) -> None:
        self._products: dict[str, Product] = {}
        self._listings: dict[str, Listing] = {}
        self._by_product: dict[str, list[str]] = {}

    def add_product(self, product: Product) -> None:
        self._products[product.id] = product

    def add_listing(self, listing: Listing) -> None:
        """新增或更新一条挂牌（改价就是用同一个 id 再写一次）。

        二级索引必须跟着一起维护：同一个 id 重复写入不能在索引里留下两份（否则
        `listings_for` 会把同一个卖家报两遍），改挂到另一件商品下时要从原来那一格里
        摘掉，那一格空了就整格删除——索引也是一个必须会缩小的容器。
        """
        if listing.product_id not in self._products:
            raise UnknownItemError(f"未知商品：{listing.product_id}")
        previous = self._listings.get(listing.id)
        if previous is not None and previous.product_id != listing.product_id:
            bucket = self._by_product.get(previous.product_id, [])
            if listing.id in bucket:
                bucket.remove(listing.id)
            if not bucket:
                self._by_product.pop(previous.product_id, None)
            previous = None
        self._listings[listing.id] = listing
        if previous is None:
            self._by_product.setdefault(listing.product_id, []).append(listing.id)

    def product(self, product_id: str) -> Product:
        try:
            return self._products[product_id]
        except KeyError:
            raise UnknownItemError(f"未知商品：{product_id}") from None

    def listing(self, listing_id: str) -> Listing:
        try:
            return self._listings[listing_id]
        except KeyError:
            raise UnknownItemError(f"未知挂牌：{listing_id}") from None

    def listings_for(self, product_id: str) -> tuple[Listing, ...]:
        """这件商品的全部挂牌，按价格从低到高；只给快照，不交出内部列表。"""
        ids = self._by_product.get(product_id, ())
        return tuple(sorted((self._listings[i] for i in ids), key=lambda l: (l.price, l.id)))


# --------------------------------------------------------------------------
# 购物车：一行一个挂牌，数量归零就把这一行删掉。
# --------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CartLine:
    """购物车里的一行：买哪个挂牌、买几件。"""

    listing_id: str
    quantity: int


class Cart:
    """一个用户的购物车。对外只给 `tuple[CartLine, ...]` 快照，内部计数表不外泄。

    数量减到 0 时整行从字典里删掉，而不是留一个 `quantity == 0` 的行——否则一个逛了几个月
    的用户会拖着一串"加了又删"的空行，每次结账都要跳过它们。
    """

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self._quantities: dict[str, int] = {}

    @property
    def lines(self) -> tuple[CartLine, ...]:
        return tuple(CartLine(listing_id=k, quantity=v) for k, v in self._quantities.items())

    @property
    def is_empty(self) -> bool:
        return not self._quantities

    def add(self, listing_id: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ShopError("加购数量必须大于 0")
        self._quantities[listing_id] = self._quantities.get(listing_id, 0) + quantity

    def remove(self, listing_id: str, quantity: int = 1) -> None:
        """减少数量；减到 0 或以下时删掉整行。"""
        if listing_id not in self._quantities:
            raise UnknownItemError(f"购物车里没有这一行：{listing_id}")
        remaining = self._quantities[listing_id] - quantity
        if remaining <= 0:
            del self._quantities[listing_id]
        else:
            self._quantities[listing_id] = remaining

    def clear(self) -> None:
        self._quantities.clear()


# --------------------------------------------------------------------------
# 库存：现货数 + 一组会过期的预留。可用量 = 现货 - 未过期的预留。
# --------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Reservation:
    """一次预留：覆盖一整张订单的若干行，整体成立或整体失败。

    `items` 存成 `tuple` 的键值对而不是字典，因为这个对象要 frozen 且可安全共享；
    `expires_at` 由注入的时钟算出，不是 `time.time()`，测试才能不靠 `sleep` 验证过期。
    """

    id: str
    items: tuple[tuple[str, int], ...]
    expires_at: datetime


class Inventory:
    """库存账：每个挂牌的现货数，以及一组带过期时间的预留。

    不变式：`available(l) == on_hand(l) - 所有未过期预留里 l 的数量之和`，且这个值永不为负。
    过期的预留在每次读写库存时被清扫掉——预留字典是这个设计里唯一会无限增长的容器，
    "谁来删它"必须有答案：过期扫一次、释放删一次、提交删一次，三条路径都会让它缩小。
    """

    def __init__(self, clock: Callable[[], datetime]) -> None:
        self._clock = clock
        self._on_hand: dict[str, int] = {}
        self._reservations: dict[str, Reservation] = {}
        self._reserved: dict[str, int] = {}
        self._ids = (f"R{n}" for n in count(1))
        self._lock = RLock()

    def receive(self, listing_id: str, quantity: int) -> None:
        """入库。"""
        if quantity <= 0:
            raise ShopError("入库数量必须大于 0")
        with self._lock:
            self._on_hand[listing_id] = self._on_hand.get(listing_id, 0) + quantity

    def on_hand(self, listing_id: str) -> int:
        with self._lock:
            return self._on_hand.get(listing_id, 0)

    def available(self, listing_id: str) -> int:
        """当前可卖数量：现货减去尚未过期的预留。"""
        with self._lock:
            self._expire()
            return self._on_hand.get(listing_id, 0) - self._reserved.get(listing_id, 0)

    @property
    def open_reservations(self) -> int:
        """未过期、未结清的预留笔数；在锁内数好再交出去。"""
        with self._lock:
            self._expire()
            return len(self._reservations)

    def reserve(self, items: Mapping[str, int], ttl: timedelta) -> Reservation:
        """为一张订单整体预留；任何一行不够就整笔失败，不做部分预留。"""
        with self._lock:
            self._expire()
            for listing_id, quantity in items.items():
                shortfall = quantity - (self._on_hand.get(listing_id, 0) - self._reserved.get(listing_id, 0))
                if shortfall > 0:
                    raise OutOfStockError(f"库存不足：{listing_id} 还差 {shortfall} 件")
            reservation = Reservation(id=next(self._ids),
                                      items=tuple(sorted(items.items())),
                                      expires_at=self._clock() + ttl)
            self._reservations[reservation.id] = reservation
            for listing_id, quantity in reservation.items:
                self._reserved[listing_id] = self._reserved.get(listing_id, 0) + quantity
            return reservation

    def release(self, reservation_id: str) -> None:
        """放弃一次预留，把额度还回可用量。对已经释放、已经提交或已经过期的预留调用
        是**无操作**——补偿动作必须幂等：Saga 回滚时它可能被重复调用，或者被调用时
        那笔预留已经因为超时自己消失了。"""
        with self._lock:
            self._drop(reservation_id)

    def commit(self, reservation_id: str) -> None:
        """把预留变成真正的扣减：现货减掉，预留行删掉。预留已过期就直接失败——
        这正是"预留有时限"这件事必须被强制的地方，否则超时形同虚设。"""
        with self._lock:
            self._expire()
            reservation = self._reservations.get(reservation_id)
            if reservation is None:
                raise OutOfStockError(f"预留已失效：{reservation_id}")
            for listing_id, quantity in reservation.items:
                self._on_hand[listing_id] = self._on_hand.get(listing_id, 0) - quantity
            self._drop(reservation_id)

    def restock(self, items: Iterable[tuple[str, int]]) -> None:
        """把已经扣减掉的货补回现货——`commit` 的补偿动作。"""
        with self._lock:
            for listing_id, quantity in items:
                self._on_hand[listing_id] = self._on_hand.get(listing_id, 0) + quantity

    def _expire(self) -> None:
        """清掉所有已过期的预留。调用方必须已经持锁。"""
        now = self._clock()
        for reservation_id in [r.id for r in self._reservations.values() if r.expires_at <= now]:
            self._drop(reservation_id)

    def _drop(self, reservation_id: str) -> None:
        """删掉一笔预留并回收它占用的额度；额度归零的挂牌整行删掉。"""
        reservation = self._reservations.pop(reservation_id, None)
        if reservation is None:
            return
        for listing_id, quantity in reservation.items:
            remaining = self._reserved.get(listing_id, 0) - quantity
            if remaining > 0:
                self._reserved[listing_id] = remaining
            else:
                self._reserved.pop(listing_id, None)


# --------------------------------------------------------------------------
# 订单：一张显式的状态转移表，而不是一锅布尔值。
# --------------------------------------------------------------------------

class OrderState(Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


#: 谁能变成谁。表在类外、是模块级常量：它是这台状态机的定义本身，读代码的人
#: 应该一眼看完全部合法转移，而不是去二十个方法里各找一个 `if`。
ALLOWED_TRANSITIONS: Mapping[OrderState, frozenset[OrderState]] = {
    OrderState.CREATED: frozenset({OrderState.PAID, OrderState.CANCELLED}),
    OrderState.PAID: frozenset({OrderState.SHIPPED, OrderState.CANCELLED}),
    OrderState.SHIPPED: frozenset({OrderState.DELIVERED}),
    OrderState.DELIVERED: frozenset(),
    OrderState.CANCELLED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class OrderLine:
    """订单里的一行。价格在下单那一刻被抄下来（snapshot），此后卖家改价不影响这张订单。"""

    listing_id: str
    title: str
    unit_price: int
    quantity: int

    @property
    def subtotal(self) -> int:
        return self.unit_price * self.quantity


@dataclass(frozen=True, slots=True)
class StateChange:
    """一次状态变更：从哪来、到哪去、什么时候。"""

    from_state: OrderState
    to_state: OrderState
    at: datetime


class Order:
    """一张订单。它只拥有一条不变式：状态只能沿着 `ALLOWED_TRANSITIONS` 走。

    `lines` 和 `history` 都只给 `tuple` 快照。`state` 是只读属性，唯一的改法是
    `transition_to`——没有 setter，就没有"从别处偷偷把状态改成 SHIPPED"这条路径。
    """

    def __init__(self, id: str, user_id: str, lines: Sequence[OrderLine],
                 discount: int, created_at: datetime) -> None:
        self.id = id
        self.user_id = user_id
        self._lines = tuple(lines)
        self.discount = discount
        self.created_at = created_at
        self._state = OrderState.CREATED
        self._history: list[StateChange] = []

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        return self._lines

    @property
    def state(self) -> OrderState:
        return self._state

    @property
    def history(self) -> tuple[StateChange, ...]:
        return tuple(self._history)

    @property
    def subtotal(self) -> int:
        return sum(line.subtotal for line in self._lines)

    @property
    def total(self) -> int:
        return self.subtotal - self.discount

    def transition_to(self, state: OrderState, at: datetime) -> None:
        """走一次状态转移；不合法就抛异常，绝不静默忽略——被吞掉的非法转移意味着
        调用方以为自己发货了，而订单其实还没付款。"""
        if state not in ALLOWED_TRANSITIONS[self._state]:
            raise IllegalTransitionError(f"订单 {self.id} 不能从 {self._state.value} 变成 {state.value}")
        self._history.append(StateChange(from_state=self._state, to_state=state, at=at))
        self._state = state


# --------------------------------------------------------------------------
# Saga：跨多个会失败的参与方的一次操作，失败时按相反顺序补偿。
# --------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SagaStep:
    """一步：一个会失败的动作，加一个把它撤销的补偿动作。补偿必须幂等。"""

    name: str
    action: Callable[[], None]
    compensation: Callable[[], None]


@dataclass(frozen=True, slots=True)
class SagaFailure(ShopError):
    """Saga 失败：`step` 是失败在哪一步，`cause` 是原始异常，
    `compensation_errors` 是回滚过程中自己也失败了的补偿——它们不能被吞掉，
    因为它们意味着系统里留下了需要人工处理的残留（比如钱扣了没退）。"""

    step: str
    cause: Exception
    compensation_errors: tuple[tuple[str, Exception], ...] = ()

    def __str__(self) -> str:
        return f"步骤「{self.step}」失败：{self.cause}"


class Saga:
    """按顺序执行若干步；任何一步抛异常，就把失败的那一步和它之前**已经成功**的步骤
    按相反顺序补偿掉。

    为什么不是一个大 `try/except`：补偿的对象是"已经完成了哪几步"，而这件事只有
    执行器知道。写成 `try/except` 时，每加一个参与方都要在 `except` 里多一层嵌套，
    而且极容易补偿一个根本没执行成功的步骤。这里把"做什么"和"怎么撤销"在同一个
    `SagaStep` 里成对声明，顺序和补偿逻辑就只剩下这一处。
    """

    def run(self, steps: Sequence[SagaStep]) -> None:
        done: list[SagaStep] = []
        for step in steps:
            try:
                step.action()
            except Exception as exc:
                # 失败的那一步**自己也要被补偿**，而且排在最前面。一个动作不是原子的：
                # "扣款"可能已经把钱扣走、却在记账那一句抛了异常。只补偿"已完成"的步骤，
                # 就会把这笔钱永远留在半路上。这条规则的代价是补偿可能在动作根本没生效时
                # 被调用，所以每个补偿都必须幂等、且能容忍"什么都还没发生"。
                errors: list[tuple[str, Exception]] = []
                for unwind in [step, *reversed(done)]:
                    try:
                        unwind.compensation()
                    except Exception as comp_exc:  # 补偿失败不能掩盖原始异常
                        errors.append((unwind.name, comp_exc))
                raise SagaFailure(step=step.name, cause=exc,
                                  compensation_errors=tuple(errors)) from exc
            done.append(step)


# --------------------------------------------------------------------------
# 外部参与方：用 Protocol 描述契约，因为确实有多种实现（真网关、测试替身）。
# --------------------------------------------------------------------------

class PaymentGateway(Protocol):
    """支付网关。

    扣款和退款都按**调用方生成的幂等键**（idempotency key，本设计里就是订单号）寻址，
    而不是按网关返回的回执号。理由是补偿动作必须能在"不知道对方到底做成了没有"时被
    正确调用：钱扣了、响应在网络上丢了，回执号就永远拿不到——如果退款只能凭回执号，
    这笔钱就卡在半路上了。契约要求：用同一个键重复扣款只扣一次；对没有扣过款的键
    退款是无操作。
    """

    def charge(self, idempotency_key: str, amount: int) -> str: ...

    def refund(self, idempotency_key: str) -> None: ...


class Fulfilment(Protocol):
    """履约：创建一次发货，或取消它。"""

    def create_shipment(self, order_id: str) -> str: ...

    def cancel_shipment(self, shipment_id: str) -> None: ...


#: 定价规则：给订单行算一笔折扣（整数最小货币单位，非负）。
#: 它是一个普通函数而不是一个 `DiscountStrategy` 抽象基类——规则无状态、只有一个方法、
#: 彼此之间没有可共享的代码，签名本身就是接口。
PricingRule = Callable[[Sequence[OrderLine]], int]


def percentage_off(percent: int, minimum_subtotal: int = 0) -> PricingRule:
    """满 `minimum_subtotal` 减 `percent`% 的一条促销规则；向下取整，绝不多送一分。"""

    def rule(lines: Sequence[OrderLine]) -> int:
        subtotal = sum(line.subtotal for line in lines)
        return subtotal * percent // 100 if subtotal >= minimum_subtotal else 0

    return rule


class ShoppingService:
    """浏览、加购、结账的唯一入口。

    它不做成 Singleton：测试要能开两个互不干扰的商城实例。真需要"整个进程一个商城"时，
    在应用启动处构造一次传下去，而不是让类拦截自己的构造。
    """

    def __init__(self, catalogue: Catalogue, inventory: Inventory,
                 payments: PaymentGateway, fulfilment: Fulfilment,
                 clock: Callable[[], datetime],
                 reservation_ttl: timedelta = timedelta(minutes=15),
                 pricing_rules: Sequence[PricingRule] = ()) -> None:
        self.catalogue = catalogue
        self.inventory = inventory
        self._payments = payments
        self._fulfilment = fulfilment
        self._clock = clock
        self._ttl = reservation_ttl
        self._pricing_rules = tuple(pricing_rules)
        self._carts: dict[str, Cart] = {}
        self._orders: dict[str, Order] = {}
        self._order_ids = (f"O{n}" for n in count(1))
        self._lock = RLock()

    def cart_for(self, user_id: str) -> Cart:
        """取（必要时新建）这个用户的购物车。"""
        with self._lock:
            return self._carts.setdefault(user_id, Cart(user_id))

    def add_to_cart(self, user_id: str, listing_id: str, quantity: int = 1) -> None:
        """加购**不预留库存**：加购的人远多于下单的人，在这里锁库存会让一堆永远不会
        结账的购物车把货占住（少卖）。代价是加购成功不等于买得到，结账时可能失败——
        这正是购物网站上"手慢无"的来源，是一个刻意选择的取舍。"""
        self.catalogue.listing(listing_id)          # 不存在的挂牌当场失败
        self.cart_for(user_id).add(listing_id, quantity)

    def order(self, order_id: str) -> Order:
        with self._lock:
            try:
                return self._orders[order_id]
            except KeyError:
                raise UnknownItemError(f"未知订单：{order_id}") from None

    def checkout(self, user_id: str) -> Order:
        """结账：把购物车变成一张订单，然后跑"预留—扣款—扣减—发货"的 Saga。

        任何一步失败，已完成的步骤都会被补偿掉，订单落到 `CANCELLED`，购物车**原样保留**
        （用户还想再试一次），并把 `SagaFailure` 抛给调用方。
        """
        with self._lock:
            cart = self.cart_for(user_id)
            if cart.is_empty:
                raise EmptyCartError("购物车是空的")
            now = self._clock()
            lines = tuple(self._to_order_line(line) for line in cart.lines)
            discount = sum(rule(lines) for rule in self._pricing_rules)
            order = Order(id=next(self._order_ids), user_id=user_id, lines=lines,
                          discount=discount, created_at=now)
            self._orders[order.id] = order
            items = {line.listing_id: line.quantity for line in lines}

        state: dict[str, str] = {}

        def do_reserve() -> None:
            state["reservation"] = self.inventory.reserve(items, self._ttl).id

        def do_pay() -> None:
            state["receipt"] = self._payments.charge(order.id, order.total)
            order.transition_to(OrderState.PAID, self._clock())

        def do_commit() -> None:
            self.inventory.commit(state["reservation"])
            state["committed"] = "yes"

        def do_ship() -> None:
            state["shipment"] = self._fulfilment.create_shipment(order.id)
            order.transition_to(OrderState.SHIPPED, self._clock())

        def undo_commit() -> None:
            # 只有真的扣减过才补货。补偿会在"这一步自己失败"时也被调用（预留过期导致
            # `commit` 抛异常就是这种情况），那时一件货都没扣，盲目补货会凭空造出库存。
            if state.pop("committed", None):
                self.inventory.restock((line.listing_id, line.quantity) for line in lines)

        def undo_ship() -> None:
            shipment = state.pop("shipment", None)
            if shipment:
                self._fulfilment.cancel_shipment(shipment)

        def undo_pay() -> None:
            # 无条件按订单号退款，不看有没有拿到回执：`charge` 可能已经扣款成功、
            # 却在返回途中失败，这时 `state` 里什么都没有，但钱确实少了一笔。
            # 网关那边"没扣过款的键退款是无操作"，所以这样调用是安全的。
            self._payments.refund(order.id)

        steps = [
            SagaStep("预留库存", do_reserve,
                     lambda: self.inventory.release(state.pop("reservation", ""))),
            SagaStep("扣款", do_pay, undo_pay),
            SagaStep("扣减库存", do_commit, undo_commit),
            SagaStep("发货", do_ship, undo_ship),
        ]
        try:
            Saga().run(steps)
        except SagaFailure:
            order.transition_to(OrderState.CANCELLED, self._clock())
            raise
        with self._lock:
            cart.clear()
            self._carts.pop(user_id, None)      # 结清的购物车不留在内存里
        return order

    def _to_order_line(self, line: CartLine) -> OrderLine:
        listing = self.catalogue.listing(line.listing_id)
        product = self.catalogue.product(listing.product_id)
        return OrderLine(listing_id=listing.id, title=product.title,
                         unit_price=listing.price, quantity=line.quantity)


if __name__ == "__main__":
    from datetime import UTC

    class _Gateway:
        """演示用的内存网关。"""

        def charge(self, idempotency_key: str, amount: int) -> str:
            return f"ch_{idempotency_key}"

        def refund(self, idempotency_key: str) -> None:
            return None

    class _Fulfilment:
        """演示用的内存履约。"""

        def create_shipment(self, order_id: str) -> str:
            return f"sh_{order_id}"

        def cancel_shipment(self, shipment_id: str) -> None:
            return None

    now = datetime(2026, 5, 1, 10, 0, tzinfo=UTC)
    catalogue = Catalogue()
    catalogue.add_product(Product("p1", "机械键盘", "peripherals"))
    catalogue.add_listing(Listing("l1", "seller-a", "p1", 39900))
    catalogue.add_listing(Listing("l2", "seller-b", "p1", 36900))   # 第二个卖家：目录多一行
    inventory = Inventory(clock=lambda: now)
    inventory.receive("l2", 3)
    shop = ShoppingService(catalogue, inventory, _Gateway(), _Fulfilment(),
                           clock=lambda: now, pricing_rules=[percentage_off(10, 30000)])

    print("同款的卖家：", [(l.seller_id, l.price) for l in catalogue.listings_for("p1")])
    shop.add_to_cart("u1", "l2", 2)
    placed = shop.checkout("u1")
    print("订单：", placed.id, placed.state, placed.subtotal, "-", placed.discount, "=", placed.total)
    print("剩余现货：", inventory.on_hand("l2"), "未结清预留：", inventory.open_reservations)
