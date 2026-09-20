"""在线购物（Online Shopping）——练习骨架：公开 API 与参考解完全一致，方法体留给你补全。

第 1 关：`Catalogue`／`Cart`／`ShoppingService.checkout` 产出一张 `Order`。
第 2 关：`Inventory` 的预留与过期（过期由注入的时钟判定），以及超卖/少卖的取舍。
第 3 关：`OrderState` 显式转移表 + `Saga` 跨"预留—扣款—扣减—发货"的补偿。
第 4 关：同一商品的第二个卖家（多一行 `Listing`）、一条促销规则（多一个 `PricingRule` 函数）。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Protocol


class ShopError(Exception):
    """本设计里所有失败路径的公共基类。"""


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
    """商品目录：按 id 查商品和挂牌，按商品查它的全部挂牌。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def add_product(self, product: Product) -> None:
        raise NotImplementedError

    def add_listing(self, listing: Listing) -> None:
        """新增或更新一条挂牌（改价就是用同一个 id 再写一次）；二级索引要跟着维护，
        同一个 id 不能在索引里留下两份。"""
        raise NotImplementedError

    def product(self, product_id: str) -> Product:
        raise NotImplementedError

    def listing(self, listing_id: str) -> Listing:
        raise NotImplementedError

    def listings_for(self, product_id: str) -> tuple[Listing, ...]:
        """这件商品的全部挂牌，按价格从低到高；只给快照。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class CartLine:
    """购物车里的一行：买哪个挂牌、买几件。"""

    listing_id: str
    quantity: int


class Cart:
    """一个用户的购物车；数量减到 0 时整行删掉，对外只给快照。"""

    def __init__(self, user_id: str) -> None:
        raise NotImplementedError

    @property
    def lines(self) -> tuple[CartLine, ...]:
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        raise NotImplementedError

    def add(self, listing_id: str, quantity: int = 1) -> None:
        raise NotImplementedError

    def remove(self, listing_id: str, quantity: int = 1) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Reservation:
    """一次预留：覆盖一整张订单的若干行，整体成立或整体失败。"""

    id: str
    items: tuple[tuple[str, int], ...]
    expires_at: datetime


class Inventory:
    """库存账：现货数 + 一组带过期时间的预留；可用量 = 现货 - 未过期预留。"""

    def __init__(self, clock: Callable[[], datetime]) -> None:
        raise NotImplementedError

    def receive(self, listing_id: str, quantity: int) -> None:
        raise NotImplementedError

    def on_hand(self, listing_id: str) -> int:
        raise NotImplementedError

    def available(self, listing_id: str) -> int:
        """当前可卖数量：现货减去尚未过期的预留。"""
        raise NotImplementedError

    @property
    def open_reservations(self) -> int:
        """未过期、未结清的预留笔数。"""
        raise NotImplementedError

    def reserve(self, items: Mapping[str, int], ttl: timedelta) -> Reservation:
        """为一张订单整体预留；任何一行不够就整笔失败。"""
        raise NotImplementedError

    def release(self, reservation_id: str) -> None:
        """放弃一次预留；对不存在的预留是无操作（补偿必须幂等）。"""
        raise NotImplementedError

    def commit(self, reservation_id: str) -> None:
        """把预留变成真正的扣减；预留已过期就失败。"""
        raise NotImplementedError

    def restock(self, items: Iterable[tuple[str, int]]) -> None:
        """把已经扣减掉的货补回现货——`commit` 的补偿动作。"""
        raise NotImplementedError


class OrderState(Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


#: 谁能变成谁：这台状态机的定义本身，一眼看完全部合法转移。
ALLOWED_TRANSITIONS: Mapping[OrderState, frozenset[OrderState]] = {
    OrderState.CREATED: frozenset({OrderState.PAID, OrderState.CANCELLED}),
    OrderState.PAID: frozenset({OrderState.SHIPPED, OrderState.CANCELLED}),
    OrderState.SHIPPED: frozenset({OrderState.DELIVERED}),
    OrderState.DELIVERED: frozenset(),
    OrderState.CANCELLED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class OrderLine:
    """订单里的一行；单价在下单那一刻被抄下来。"""

    listing_id: str
    title: str
    unit_price: int
    quantity: int

    @property
    def subtotal(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class StateChange:
    """一次状态变更：从哪来、到哪去、什么时候。"""

    from_state: OrderState
    to_state: OrderState
    at: datetime


class Order:
    """一张订单；唯一的不变式是状态只能沿着 `ALLOWED_TRANSITIONS` 走。"""

    def __init__(self, id: str, user_id: str, lines: Sequence[OrderLine],
                 discount: int, created_at: datetime) -> None:
        raise NotImplementedError

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        raise NotImplementedError

    @property
    def state(self) -> OrderState:
        raise NotImplementedError

    @property
    def history(self) -> tuple[StateChange, ...]:
        raise NotImplementedError

    @property
    def subtotal(self) -> int:
        raise NotImplementedError

    @property
    def total(self) -> int:
        raise NotImplementedError

    def transition_to(self, state: OrderState, at: datetime) -> None:
        """走一次状态转移；不合法就抛 `IllegalTransitionError`。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class SagaStep:
    """一步：一个会失败的动作，加一个把它撤销的补偿动作。补偿必须幂等。"""

    name: str
    action: Callable[[], None]
    compensation: Callable[[], None]


@dataclass(frozen=True, slots=True)
class SagaFailure(ShopError):
    """Saga 失败：失败在哪一步、原始异常、以及回滚过程中自己也失败了的补偿。"""

    step: str
    cause: Exception
    compensation_errors: tuple[tuple[str, Exception], ...] = ()

    def __str__(self) -> str:
        return f"步骤「{self.step}」失败：{self.cause}"


class Saga:
    """按顺序执行若干步；失败时把失败的那一步和它之前已完成的步骤按相反顺序补偿掉。"""

    def run(self, steps: Sequence[SagaStep]) -> None:
        raise NotImplementedError


class PaymentGateway(Protocol):
    """支付网关：按调用方生成的幂等键（idempotency key，这里是订单号）扣款与退款。
    同一个键重复扣款只扣一次；对没有扣过款的键退款是无操作。"""

    def charge(self, idempotency_key: str, amount: int) -> str: ...

    def refund(self, idempotency_key: str) -> None: ...


class Fulfilment(Protocol):
    """履约：创建一次发货，或取消它。"""

    def create_shipment(self, order_id: str) -> str: ...

    def cancel_shipment(self, shipment_id: str) -> None: ...


#: 定价规则：给订单行算一笔折扣（整数最小货币单位，非负）。普通函数，不是抽象基类。
PricingRule = Callable[[Sequence[OrderLine]], int]


def percentage_off(percent: int, minimum_subtotal: int = 0) -> PricingRule:
    """满 `minimum_subtotal` 减 `percent`% 的一条促销规则；向下取整。"""
    raise NotImplementedError


class ShoppingService:
    """浏览、加购、结账的唯一入口；不是 Singleton。"""

    def __init__(self, catalogue: Catalogue, inventory: Inventory,
                 payments: PaymentGateway, fulfilment: Fulfilment,
                 clock: Callable[[], datetime],
                 reservation_ttl: timedelta = timedelta(minutes=15),
                 pricing_rules: Sequence[PricingRule] = ()) -> None:
        raise NotImplementedError

    def cart_for(self, user_id: str) -> Cart:
        raise NotImplementedError

    def add_to_cart(self, user_id: str, listing_id: str, quantity: int = 1) -> None:
        """加购不预留库存；取舍见题解。"""
        raise NotImplementedError

    def order(self, order_id: str) -> Order:
        raise NotImplementedError

    def checkout(self, user_id: str) -> Order:
        """结账：购物车变订单，然后跑"预留—扣款—扣减—发货"的 Saga。"""
        raise NotImplementedError
