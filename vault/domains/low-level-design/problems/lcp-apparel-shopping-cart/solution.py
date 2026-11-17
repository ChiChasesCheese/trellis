"""服装购物车（Apparel Shopping Cart）参考解：公开 API 与真实工作区的 `cart.py` 一致，可以原样放进去。

设计一共五行：
1. 目录（`Catalogue`）在构造时把调用方的商品拷成私有的冻结条目（`_Entry`），之后怎么改自己的 `Product` 都与购物车无关。
2. 购物车的行只存「商品 ID → 数量」，只存数量大于 0 的行；字典的插入序就是行序，
   改量不动位置，删除再加回去就落在末尾，正好是合同要的顺序。
3. 总数不另存，每次快照从各行现算：数据只有一份，没有"总数与行对不上"的可能；至多 100 行，现算的代价可以忽略。
4. 全是 `int`：单行至多 10**12，全目录至多 10**14，超出 32 位但 Python 的整数不会溢出，也不经过浮点数。
5. 每次 `snapshot()` 都新建全部对象与列表，所以旧快照、被调用方改坏的快照、另一辆购物车，彼此都碰不到。

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

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

MAX_QUANTITY = 1_000_000


class CartError(Exception):
    """购物车自己抛出的错误的基类。"""


class UnknownProductError(CartError, LookupError):
    """商品 ID 不在目录里。"""

    def __init__(self, product_id: str) -> None:
        super().__init__(f"未知商品：{product_id!r}")
        self.product_id = product_id


class QuantityError(CartError, ValueError):
    """数量不是 0 到 1_000_000 的整数，或加一会越界。"""

    def __init__(self, product_id: str, quantity: object) -> None:
        super().__init__(f"商品 {product_id!r} 的数量 {quantity!r} 不合法（要求 0 到 {MAX_QUANTITY} 的整数）")
        self.product_id = product_id
        self.quantity = quantity


@dataclass
class Product:
    """调用方交进来的商品：构造时被拷贝，之后与购物车无关。"""

    id: str
    name: str
    priceCents: int


@dataclass
class CatalogProduct(Product):
    """快照里的目录条目：商品加上它在购物车里的数量。"""

    cartQuantity: int


@dataclass
class CartItem(Product):
    """快照里的购物车行。"""

    quantity: int
    lineTotalCents: int


@dataclass
class CartSnapshot:
    """某一时刻购物车的独立副本：每次调用 `snapshot()` 都重新构造。"""

    products: list[CatalogProduct]
    items: list[CartItem]
    totalQuantity: int
    totalPriceCents: int
    empty: bool


@dataclass(frozen=True, slots=True)
class _Entry:
    """目录里的一个商品，冻结：快照只从它读值，永远拿不到它本身。"""

    id: str
    name: str
    price_cents: int

    @classmethod
    def copy_of(cls, product: Product) -> _Entry:
        """从调用方的对象拷出一个条目；价格必须是非负整数、名字非空。"""
        if type(product.priceCents) is not int or product.priceCents < 0 or not product.name:
            raise ValueError(f"商品 {product.id} 的名字为空或价格不是非负整数")
        return cls(product.id, product.name, product.priceCents)

    def as_catalog(self, cart_quantity: int) -> CatalogProduct:
        return CatalogProduct(self.id, self.name, self.price_cents, cart_quantity)

    def as_item(self, quantity: int) -> CartItem:
        return CartItem(self.id, self.name, self.price_cents, quantity, self.price_cents * quantity)


class Catalogue:
    """不可变的目录：保持原序、按 ID 查找。不变量：ID 唯一；构造之后不再改变。"""

    def __init__(self, products: Iterable[Product]) -> None:
        self._entries = tuple(_Entry.copy_of(p) for p in products)  # 立刻拷贝，之后不再引用调用方的对象
        self._by_id = {entry.id: entry for entry in self._entries}
        if len(self._by_id) != len(self._entries):
            raise ValueError("目录里有重复的商品 ID")

    def get(self, product_id: str) -> _Entry:
        try:
            return self._by_id[product_id]
        except KeyError:
            raise UnknownProductError(product_id) from None

    def __iter__(self) -> Iterator[_Entry]:
        return iter(self._entries)


class CartLines:
    """有序的购物车行：商品 ID → 数量。不变量：只存 1 到 MAX_QUANTITY 的数量，0 从不入库。"""

    def __init__(self) -> None:
        self._quantity: dict[str, int] = {}

    def quantity_of(self, product_id: str) -> int:
        return self._quantity.get(product_id, 0)

    def add(self, product_id: str) -> None:
        current = self._quantity.get(product_id, 0)
        if current >= MAX_QUANTITY:
            raise QuantityError(product_id, current + 1)
        # 已有的键重新赋值不改变它在字典里的位置；新键追加在末尾
        self._quantity[product_id] = current + 1

    def set(self, product_id: str, quantity: int) -> None:
        if type(quantity) is not int or not 0 <= quantity <= MAX_QUANTITY:
            raise QuantityError(product_id, quantity)
        if quantity == 0:
            self._quantity.pop(product_id, None)  # 不存在时什么都不做
        else:
            self._quantity[product_id] = quantity

    def entries(self) -> tuple[tuple[str, int], ...]:
        """按插入序的 (ID, 数量) 元组，是副本，不是内部字典的视图。"""
        return tuple(self._quantity.items())

    def __len__(self) -> int:
        return len(self._quantity)


class ShoppingCart:
    """目录 + 购物车行 + 快照的组装：自己不存第二份状态。"""

    def __init__(self, products: Iterable[Product]) -> None:
        self._catalogue = Catalogue(products)
        self._lines = CartLines()

    @property
    def line_count(self) -> int:
        """当前有几行（数量大于 0 的商品数）。"""
        return len(self._lines)

    def quantityOf(self, productId: str) -> int:
        """某个商品当前的数量（不在购物车里是 0），O(1)，不必为一个数字构造整份快照。"""
        self._catalogue.get(productId)
        return self._lines.quantity_of(productId)

    def addLine(self, productId: str) -> None:
        self._catalogue.get(productId)  # 先确认商品存在；失败时行还没被碰过
        self._lines.add(productId)

    def updateLine(self, productId: str, quantity: int) -> None:
        self._catalogue.get(productId)
        self._lines.set(productId, quantity)

    def snapshot(self) -> CartSnapshot:
        # 每个对象、每个列表都现建：快照与购物车内部、与别的快照没有共享的可变部分
        items = [self._catalogue.get(pid).as_item(quantity) for pid, quantity in self._lines.entries()]
        products = [entry.as_catalog(self._lines.quantity_of(entry.id)) for entry in self._catalogue]
        return CartSnapshot(
            products=products,
            items=items,
            totalQuantity=sum(item.quantity for item in items),
            totalPriceCents=sum(item.lineTotalCents for item in items),
            empty=not items,
        )


if __name__ == "__main__":
    demo = ShoppingCart([Product("p1", "Linen Shirt", 3175), Product("p2", "Rain Jacket", 5400)])
    demo.addLine("p1")
    demo.addLine("p2")
    demo.updateLine("p1", 0)  # 删除 p1
    demo.addLine("p1")  # 再加回来：落在末尾
    shot = demo.snapshot()
    print([item.id for item in shot.items], shot.totalQuantity, shot.totalPriceCents, shot.empty)
    # 精确总价：3200 分的衬衫放满 1_000_000 件是 3_200_000_000，超过 32 位有符号整数的上限 2_147_483_647
    big = ShoppingCart([Product("shirt", "Trail Shirt", 3200)])
    big.updateLine("shirt", MAX_QUANTITY)
    print(big.snapshot().totalPriceCents, big.snapshot().totalPriceCents > 2**31 - 1)
    # 旧快照不受之后调用的影响
    before = big.snapshot()
    big.updateLine("shirt", 0)
    print(before.totalQuantity, big.snapshot().totalQuantity)
