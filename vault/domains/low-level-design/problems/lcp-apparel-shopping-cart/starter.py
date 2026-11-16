"""服装购物车练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `cart.py`。

产品规则（逐条都有测试）：
 1. `ShoppingCart(products)`：目录至多 100 个商品，商品靠 `id` 区分（`id` 唯一）；名字或价格相同不算同一个商品；
    每个商品起始数量为 0。目录被拷贝：之后调用方改动或清空自己的列表与对象，都不影响购物车；构造也不修改调用方的对象。
 2. `addLine(id)`：数量加 1。从 0 变成非零的行追加在行序末尾；已有的行保持原来的位置。
 3. `updateLine(id, quantity)`：把数量设成绝对值（0 到 1_000_000）。正数可以新建行（追加在末尾），已有行保持位置；
    0 删除这一行，行不存在时什么都不做；删除后再加回来，行落在末尾。
 4. `snapshot()` 返回 `CartSnapshot`：`products` 按目录原序，每项 `id / name / priceCents / cartQuantity`；
    `items` 按行的插入序，每项 `id / name / priceCents / quantity / lineTotalCents`。
 5. `lineTotalCents = priceCents * quantity`；`totalQuantity` 是各行数量之和；`totalPriceCents` 是各行小计之和；
    `empty` 当且仅当没有任何行；空购物车的两个总数都是 0。
 6. 总价是精确的整数：单价与数量各至多 10**6，一行至多 10**12，整本目录至多 10**14，都远超 2**32。
 7. 快照互相独立：之后的任何调用都不改变已经拿到的快照；改动一个快照不影响下一个快照；两辆购物车不共享可变状态。
 8. 失败不留痕（合同保证入参合法，这是本解多加的防线）：未知商品 ID 抛 `UnknownProductError`；
    数量不是 `int`（`bool` 也不行）或超出 0 到 1_000_000、或 `addLine` 会让数量超过 1_000_000，抛 `QuantityError`；
    两种失败之后购物车都没有任何变化；ID 和数量同时有错时，先报未知商品。
 9. `quantityOf(id)` 是多加的只读口：返回当前数量（不在购物车里是 0），未知 ID 同样抛 `UnknownProductError`。
10. 调用是顺序的，不加锁。结账、支付、库存、持久化、同步都不在范围内；HTTP 层对 JSON 数字的校验由传输层负责。
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

MAX_QUANTITY = 1_000_000


class CartError(Exception):
    """购物车自己抛出的错误的基类。"""


class UnknownProductError(CartError, LookupError):
    """商品 ID 不在目录里；`product_id` 属性记下是哪个。"""

    def __init__(self, product_id: str) -> None:
        super().__init__(f"未知商品：{product_id!r}")
        self.product_id = product_id


class QuantityError(CartError, ValueError):
    """数量不是 0 到 1_000_000 的整数，或加一会越界；`product_id`、`quantity` 记下是哪个。"""

    def __init__(self, product_id: str, quantity: object) -> None:
        super().__init__(f"商品 {product_id!r} 的数量 {quantity!r} 不合法")
        self.product_id = product_id
        self.quantity = quantity


@dataclass
class Product:
    id: str
    name: str
    priceCents: int


@dataclass
class CatalogProduct(Product):
    cartQuantity: int


@dataclass
class CartItem(Product):
    quantity: int
    lineTotalCents: int


@dataclass
class CartSnapshot:
    products: list[CatalogProduct]
    items: list[CartItem]
    totalQuantity: int
    totalPriceCents: int
    empty: bool


class ShoppingCart:
    def __init__(self, products: Iterable[Product]) -> None:
        # TODO：拷贝目录（别保存调用方的列表和对象），准备有序的行。
        raise NotImplementedError

    @property
    def line_count(self) -> int:
        """当前有几行（数量大于 0 的商品数）。"""
        raise NotImplementedError

    def quantityOf(self, productId: str) -> int:
        """某个商品当前的数量（不在购物车里是 0）。"""
        raise NotImplementedError

    def addLine(self, productId: str) -> None:
        raise NotImplementedError

    def updateLine(self, productId: str, quantity: int) -> None:
        raise NotImplementedError

    def snapshot(self) -> CartSnapshot:
        raise NotImplementedError
