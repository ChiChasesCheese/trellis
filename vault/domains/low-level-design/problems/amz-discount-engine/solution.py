"""购物车折扣引擎（Checkout Price Engine）：购物车 + 一组可插拔折扣 → 一张可审计的账单。

设计五行：
1. 钱一律是整数分（`int`），比例用整数基点（万分之一）；舍入只发生在每条折扣自己的 `apply` 里，一次、半进位。
2. 折扣分两层：`LineDiscount` 只看一行（百分比、买 X 送 Y），`CartDiscount` 只看折后总额（满减）。
3. 引擎 `PriceEngine` 只做三件事：按顺序遍历、把每笔减免钳在剩余价格以内、记账；它不认识任何具体折扣。
4. 结果 `Receipt` 带解释：每笔减免都有标签和金额，原价 - 全部减免 = 应付，永不为负。
5. 叠加策略是引擎的一个枚举参数（全叠加 / 每行只取最大一条），不是第二个引擎类。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from threading import Lock


class PricingError(Exception):
    """本模块所有可预期失败的基类。"""


class InvalidCartError(PricingError):
    """购物车内容不合法：数量非正、同一 SKU 价格冲突。"""


class InvalidRuleError(PricingError):
    """折扣配置不合法，或某条折扣算出了负数（会凭空造钱）。"""


def to_cents(text: str) -> int:
    """把 "19.99" 这样的十进制字符串精确转成分；绝不经过 float。"""
    return int((Decimal(text) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def format_cents(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"


def _div_half_up(numerator: int, denominator: int) -> int:
    """非负整数的四舍五入除法，纯整数运算。"""
    return (2 * numerator + denominator) // (2 * denominator)


# ───────────────────────────── 购物车 ─────────────────────────────

@dataclass(frozen=True, slots=True)
class LineItem:
    """一行商品：同一个 SKU 一行，数量合并。不可变，所以可以放心交给折扣去读。"""
    sku: str
    unit_cents: int
    qty: int
    category: str = ""

    def __post_init__(self) -> None:
        if self.qty <= 0 or self.unit_cents < 0:
            raise InvalidCartError(f"{self.sku}: 数量必须为正、单价不能为负")

    @property
    def original_cents(self) -> int:
        return self.unit_cents * self.qty


class Cart:
    """购物车：可变，但对外只给快照。"""

    def __init__(self) -> None:
        self._lines: dict[str, LineItem] = {}
        self._lock = Lock()

    def add(self, sku: str, unit_cents: int, qty: int = 1, category: str = "") -> None:
        with self._lock:
            old = self._lines.get(sku)
            if old is not None and old.unit_cents != unit_cents:
                raise InvalidCartError(f"{sku}: 同一 SKU 不能有两个单价")
            total = qty + (old.qty if old else 0)
            self._lines[sku] = LineItem(sku, unit_cents, total, category)

    def remove(self, sku: str) -> None:
        with self._lock:
            if self._lines.pop(sku, None) is None:
                raise InvalidCartError(f"{sku}: 不在购物车里")

    @property
    def lines(self) -> tuple[LineItem, ...]:
        with self._lock:
            return tuple(self._lines.values())


# ───────────────────────────── 折扣 ─────────────────────────────

@dataclass(frozen=True, slots=True)
class Scope:
    """折扣适用哪些行：None 表示不限；两个条件同时给出则都要满足。全场折扣就是默认的 Scope()。"""
    skus: frozenset[str] | None = None
    categories: frozenset[str] | None = None

    def covers(self, line: LineItem) -> bool:
        return ((self.skus is None or line.sku in self.skus)
                and (self.categories is None or line.category in self.categories))


class LineDiscount(ABC):
    """行级折扣：先问 `is_eligible`，再问 `apply` 减多少。`remaining_cents` 是前面折扣减完后这一行还剩的价格。"""

    def __init__(self, label: str, scope: Scope = Scope()) -> None:
        self.label = label
        self.scope = scope

    def is_eligible(self, line: LineItem) -> bool:
        return self.scope.covers(line)

    @abstractmethod
    def apply(self, line: LineItem, remaining_cents: int) -> int:
        """返回减免的分；不得为负，超过剩余价格的部分由引擎钳掉。"""


class PercentOff(LineDiscount):
    def __init__(self, label: str, percent: str, scope: Scope = Scope()) -> None:
        super().__init__(label, scope)
        value = Decimal(percent)
        if not 0 < value <= 100:
            raise InvalidRuleError(f"{label}: 百分比必须在 (0, 100]")
        self._bps = int(value * 100)             # 基点：万分之一，8.5% → 850

    def apply(self, line: LineItem, remaining_cents: int) -> int:
        return _div_half_up(remaining_cents * self._bps, 10_000)


class BuyXGetY(LineDiscount):
    """买 buy 送 free：每凑满 buy+free 件，其中 free 件免费。它不直接减钱，而是算出送了几件，再折成这一行的价。"""

    def __init__(self, label: str, buy: int, free: int, scope: Scope = Scope()) -> None:
        super().__init__(label, scope)
        if buy <= 0 or free <= 0:
            raise InvalidRuleError(f"{label}: buy 和 free 都必须为正")
        self.buy, self.free = buy, free

    def is_eligible(self, line: LineItem) -> bool:
        return super().is_eligible(line) and line.qty >= self.buy + self.free

    def apply(self, line: LineItem, remaining_cents: int) -> int:
        free_units = line.qty // (self.buy + self.free) * self.free
        # 按“剩余价格的份额”折算：前面已有折扣时，送出的那几件也是折后价，而不是原价
        return remaining_cents * free_units // line.qty


class CartDiscount(ABC):
    """购物车级折扣：只看行级折扣之后的总额。"""

    def __init__(self, label: str) -> None:
        self.label = label

    @abstractmethod
    def is_eligible(self, subtotal_cents: int) -> bool: ...

    @abstractmethod
    def apply(self, subtotal_cents: int) -> int: ...


class ThresholdOff(CartDiscount):
    """满 threshold 减 off：门槛按折后小计判断（推断：与 Amazon 优惠券“满 X”的常见口径一致）。"""

    def __init__(self, label: str, threshold_cents: int, off_cents: int) -> None:
        super().__init__(label)
        if threshold_cents <= 0 or off_cents <= 0:
            raise InvalidRuleError(f"{label}: 门槛和减免都必须为正")
        self.threshold_cents, self.off_cents = threshold_cents, off_cents

    def is_eligible(self, subtotal_cents: int) -> bool:
        return subtotal_cents >= self.threshold_cents

    def apply(self, subtotal_cents: int) -> int:
        return self.off_cents


# ───────────────────────────── 账单与引擎 ─────────────────────────────

@dataclass(frozen=True, slots=True)
class Adjustment:
    label: str
    cents: int                                    # 正数 = 减免的金额


@dataclass(frozen=True, slots=True)
class LineResult:
    line: LineItem
    adjustments: tuple[Adjustment, ...]

    @property
    def final_cents(self) -> int:
        return self.line.original_cents - sum(a.cents for a in self.adjustments)


@dataclass(frozen=True, slots=True)
class Receipt:
    lines: tuple[LineResult, ...]
    cart_adjustments: tuple[Adjustment, ...]

    @property
    def subtotal_cents(self) -> int:
        return sum(r.line.original_cents for r in self.lines)

    @property
    def discount_cents(self) -> int:
        return (sum(a.cents for r in self.lines for a in r.adjustments)
                + sum(a.cents for a in self.cart_adjustments))

    @property
    def total_cents(self) -> int:
        return self.subtotal_cents - self.discount_cents


class Stacking(Enum):
    STACK = "stack"                               # 所有适用折扣按顺序叠加
    BEST_ONLY = "best_only"                       # 每行（和购物车级）只取减免最大的一条


class PriceEngine:
    """不可变的规则集 + 纯函数 `compute`：同一个购物车算多少次都得到同一张账单，可以被多线程共享。"""

    def __init__(self, line_discounts: Sequence[LineDiscount] = (),
                 cart_discounts: Sequence[CartDiscount] = (),
                 stacking: Stacking = Stacking.STACK) -> None:
        self._line_discounts = tuple(line_discounts)
        self._cart_discounts = tuple(cart_discounts)
        self._stacking = stacking

    @staticmethod
    def _bounded(amount: int, remaining: int, label: str) -> int:
        if amount < 0:
            raise InvalidRuleError(f"{label}: 折扣算出了负数 {amount}，会让总价变高")
        return min(amount, remaining)             # 折扣永远不会把价格减到负数

    def _price_line(self, line: LineItem) -> LineResult:
        original = line.original_cents
        eligible = [d for d in self._line_discounts if d.is_eligible(line)]
        if self._stacking is Stacking.BEST_ONLY and eligible:
            eligible = [max(eligible, key=lambda d: self._bounded(d.apply(line, original), original, d.label))]
        remaining, adjustments = original, []
        for discount in eligible:                 # 叠加时后一条看到的是前一条减完后的剩余价格
            amount = self._bounded(discount.apply(line, remaining), remaining, discount.label)
            if amount > 0:
                adjustments.append(Adjustment(discount.label, amount))
                remaining -= amount
        return LineResult(line, tuple(adjustments))

    def compute(self, cart: Cart) -> Receipt:
        results = tuple(self._price_line(line) for line in cart.lines)
        subtotal = sum(r.final_cents for r in results)
        eligible = [d for d in self._cart_discounts if d.is_eligible(subtotal)]
        if self._stacking is Stacking.BEST_ONLY and eligible:
            eligible = [max(eligible, key=lambda d: self._bounded(d.apply(subtotal), subtotal, d.label))]
        remaining, cart_adjustments = subtotal, []
        for discount in eligible:
            if not discount.is_eligible(remaining):
                continue                          # 前一条把小计压到门槛以下，这一条就不再适用
            amount = self._bounded(discount.apply(remaining), remaining, discount.label)
            if amount > 0:
                cart_adjustments.append(Adjustment(discount.label, amount))
                remaining -= amount
        return Receipt(results, tuple(cart_adjustments))


if __name__ == "__main__":
    cart = Cart()
    cart.add("pen", to_cents("2.50"), 6, "stationery")
    cart.add("book", to_cents("30.00"), 2, "books")
    engine = PriceEngine(
        [BuyXGetY("买2送1", 2, 1, Scope(frozenset({"pen"}))), PercentOff("图书九折", "10", Scope(categories=frozenset({"books"})))],
        [ThresholdOff("满60减5", to_cents("60"), to_cents("5"))],
    )
    receipt = engine.compute(cart)
    print(format_cents(receipt.subtotal_cents), "->", format_cents(receipt.total_cents))
