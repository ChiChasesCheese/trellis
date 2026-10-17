"""【练习骨架】购物车折扣引擎：公开 API 与参考解答完全一致，把每个 raise NotImplementedError 换成你的实现。

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
    raise NotImplementedError


def format_cents(cents: int) -> str:
    raise NotImplementedError


def _div_half_up(numerator: int, denominator: int) -> int:
    """非负整数的四舍五入除法，纯整数运算。"""
    raise NotImplementedError


# ───────────────────────────── 购物车 ─────────────────────────────

@dataclass(frozen=True, slots=True)
class LineItem:
    """一行商品：同一个 SKU 一行，数量合并。不可变，所以可以放心交给折扣去读。"""
    sku: str
    unit_cents: int
    qty: int
    category: str = ""

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def original_cents(self) -> int:
        raise NotImplementedError


class Cart:
    """购物车：可变，但对外只给快照。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def add(self, sku: str, unit_cents: int, qty: int = 1, category: str = "") -> None:
        raise NotImplementedError

    def remove(self, sku: str) -> None:
        raise NotImplementedError

    @property
    def lines(self) -> tuple[LineItem, ...]:
        raise NotImplementedError


# ───────────────────────────── 折扣 ─────────────────────────────

@dataclass(frozen=True, slots=True)
class Scope:
    """折扣适用哪些行：None 表示不限；两个条件同时给出则都要满足。全场折扣就是默认的 Scope()。"""
    skus: frozenset[str] | None = None
    categories: frozenset[str] | None = None

    def covers(self, line: LineItem) -> bool:
        raise NotImplementedError


class LineDiscount(ABC):
    """行级折扣：先问 `is_eligible`，再问 `apply` 减多少。`remaining_cents` 是前面折扣减完后这一行还剩的价格。"""

    def __init__(self, label: str, scope: Scope = Scope()) -> None:
        raise NotImplementedError

    def is_eligible(self, line: LineItem) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, line: LineItem, remaining_cents: int) -> int:
        """返回减免的分；不得为负，超过剩余价格的部分由引擎钳掉。"""


class PercentOff(LineDiscount):
    def __init__(self, label: str, percent: str, scope: Scope = Scope()) -> None:
        raise NotImplementedError

    def apply(self, line: LineItem, remaining_cents: int) -> int:
        raise NotImplementedError


class BuyXGetY(LineDiscount):
    """买 buy 送 free：每凑满 buy+free 件，其中 free 件免费。它不直接减钱，而是算出送了几件，再折成这一行的价。"""

    def __init__(self, label: str, buy: int, free: int, scope: Scope = Scope()) -> None:
        raise NotImplementedError

    def is_eligible(self, line: LineItem) -> bool:
        raise NotImplementedError

    def apply(self, line: LineItem, remaining_cents: int) -> int:
        raise NotImplementedError


class CartDiscount(ABC):
    """购物车级折扣：只看行级折扣之后的总额。"""

    def __init__(self, label: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_eligible(self, subtotal_cents: int) -> bool: ...

    @abstractmethod
    def apply(self, subtotal_cents: int) -> int: ...


class ThresholdOff(CartDiscount):
    """满 threshold 减 off：门槛按折后小计判断：先打折、再看够不够满额，和常见优惠券「满 X」的口径一致。"""

    def __init__(self, label: str, threshold_cents: int, off_cents: int) -> None:
        raise NotImplementedError

    def is_eligible(self, subtotal_cents: int) -> bool:
        raise NotImplementedError

    def apply(self, subtotal_cents: int) -> int:
        raise NotImplementedError


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
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Receipt:
    lines: tuple[LineResult, ...]
    cart_adjustments: tuple[Adjustment, ...]

    @property
    def subtotal_cents(self) -> int:
        raise NotImplementedError

    @property
    def discount_cents(self) -> int:
        raise NotImplementedError

    @property
    def total_cents(self) -> int:
        raise NotImplementedError


class Stacking(Enum):
    STACK = "stack"                               # 所有适用折扣按顺序叠加
    BEST_ONLY = "best_only"                       # 每行（和购物车级）只取减免最大的一条


class PriceEngine:
    """不可变的规则集 + 纯函数 `compute`：同一个购物车算多少次都得到同一张账单，可以被多线程共享。"""

    def __init__(self, line_discounts: Sequence[LineDiscount] = (),
                 cart_discounts: Sequence[CartDiscount] = (),
                 stacking: Stacking = Stacking.STACK) -> None:
        raise NotImplementedError

    @staticmethod
    def _bounded(amount: int, remaining: int, label: str) -> int:
        raise NotImplementedError

    def _price_line(self, line: LineItem) -> LineResult:
        raise NotImplementedError

    def compute(self, cart: Cart) -> Receipt:
        raise NotImplementedError
