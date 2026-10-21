"""披萨订单（Pizza Order）：菜单是数据 → Builder 校验组合 → 折扣规则 → 订单总价。

设计五行：
1. 菜单 `Menu` 是数据（尺寸、饼底、配料及其价格、互斥关系、配料上限），新增配料只加一行，不加类。
2. `PizzaBuilder` 分步收集选择，`build()` 一次性校验并产出不可变的 `Pizza`；非法组合在这里就抛 `InvalidChoiceError`。
3. `Pizza` 在构建时把单价定格（分），之后菜单改价不影响已在订单里的披萨。
4. 折扣沿用购物车折扣引擎的两层：`LineRule` 只看一行，`OrderRule` 看整单；`PriceEngine` 只遍历、钳位、记账。
5. 钱一律是整数分，舍入只发生在百分比折扣自己的 `apply` 里；`Order` 的合并数量加锁，对外只给快照。
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from threading import Lock

class PizzaError(Exception):
    """本模块所有可预期失败的基类。"""

class InvalidChoiceError(PizzaError):
    """顾客的选择不合法：未知选项、互斥配料、尺寸不支持该饼底、配料超限。"""

class InvalidRuleError(PizzaError):
    """折扣配置不合法，或某条折扣算出了负数（会凭空造钱）。"""

class InvalidOrderError(PizzaError):
    """订单操作不合法：数量非正、删除不存在的披萨。"""

def to_cents(text: str) -> int:
    """把 "12.50" 这样的十进制字符串精确转成分；绝不经过 float。"""
    return int((Decimal(text) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))

def format_cents(cents: int) -> str:
    sign = '-' if cents < 0 else ''
    return f'{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}'

@dataclass(frozen=True)
class CrustSpec:
    extra_cents: int = 0
    sizes: frozenset[str] | None = None

@dataclass(frozen=True)
class ToppingSpec:
    prices: dict[str, int]
    excludes: frozenset[str] = frozenset()

@dataclass(frozen=True)
class Menu:
    base: dict[str, int]
    crusts: dict[str, CrustSpec]
    toppings: dict[str, ToppingSpec]
    max_toppings: int = 5

    def price(self, size: str, crust: str, toppings: Sequence[str]) -> int:
        """调用前选择必须已通过校验；价格 = 基础价 + 饼底加价 + 每种配料在该尺寸的价。"""
        raise NotImplementedError

def default_menu() -> Menu:
    return Menu(base={'S': 800, 'M': 1000, 'L': 1200}, crusts={'thin': CrustSpec(), 'thick': CrustSpec(100), 'stuffed': CrustSpec(250, frozenset({'M', 'L'}))}, toppings={'cheese': ToppingSpec({'S': 100, 'M': 150, 'L': 200}, frozenset({'vegan_cheese'})), 'vegan_cheese': ToppingSpec({'S': 150, 'M': 200, 'L': 250}, frozenset({'cheese'})), 'pepperoni': ToppingSpec({'S': 150, 'M': 200, 'L': 250}), 'mushroom': ToppingSpec({'S': 100, 'M': 125, 'L': 150}), 'olive': ToppingSpec({'S': 100, 'M': 125, 'L': 150}), 'pineapple': ToppingSpec({'S': 100, 'M': 150, 'L': 200})})

@dataclass(frozen=True, slots=True)
class Pizza:
    """一份配好的披萨，不可变。toppings 已排序去重，所以“同样的披萨”相等、可哈希。"""
    size: str
    crust: str
    toppings: tuple[str, ...]
    unit_cents: int

    @property
    def sku(self) -> str:
        raise NotImplementedError

class PizzaBuilder:
    """分步收集，`build()` 时一次性校验。链式调用，可复用：每次 `build()` 产出新的 Pizza。"""

    def __init__(self, menu: Menu) -> None:
        raise NotImplementedError

    def size(self, size: str) -> PizzaBuilder:
        raise NotImplementedError

    def crust(self, crust: str) -> PizzaBuilder:
        raise NotImplementedError

    def topping(self, name: str) -> PizzaBuilder:
        raise NotImplementedError

    def build(self) -> Pizza:
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class OrderLine:
    pizza: Pizza
    qty: int

    @property
    def original_cents(self) -> int:
        raise NotImplementedError

class Order:
    """可变的订单：同样的披萨合并成一行；对外只给快照。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def add(self, pizza: Pizza, qty: int=1) -> None:
        raise NotImplementedError

    def remove(self, pizza: Pizza) -> None:
        raise NotImplementedError

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        raise NotImplementedError

class LineRule(ABC):
    """行级折扣：`is_eligible` 问这行能不能用，`apply` 问在剩余价格上减多少。"""

    def __init__(self, label: str) -> None:
        raise NotImplementedError

    def is_eligible(self, line: OrderLine) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, line: OrderLine, remaining_cents: int) -> int:
        ...

class PercentOff(LineRule):

    def __init__(self, label: str, percent: str, sizes: frozenset[str] | None=None) -> None:
        raise NotImplementedError

    def is_eligible(self, line: OrderLine) -> bool:
        raise NotImplementedError

    def apply(self, line: OrderLine, remaining_cents: int) -> int:
        raise NotImplementedError

class BuyXGetY(LineRule):
    """同一款披萨买 buy 送 free：先算送几份，再按剩余价格的份额折成钱。"""

    def __init__(self, label: str, buy: int, free: int) -> None:
        raise NotImplementedError

    def is_eligible(self, line: OrderLine) -> bool:
        raise NotImplementedError

    def apply(self, line: OrderLine, remaining_cents: int) -> int:
        raise NotImplementedError

class OrderRule(ABC):
    """整单折扣：看行级折扣之后的各行结果和剩余总额，回答适用吗、减多少。"""

    def __init__(self, label: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_eligible(self, results: Sequence[LineResult], remaining_cents: int) -> bool:
        ...

    @abstractmethod
    def apply(self, results: Sequence[LineResult], remaining_cents: int) -> int:
        ...

class ThresholdOff(OrderRule):
    """满 threshold 减 off，门槛按折后总额判断。"""

    def __init__(self, label: str, threshold_cents: int, off_cents: int) -> None:
        raise NotImplementedError

    def is_eligible(self, results: Sequence[LineResult], remaining_cents: int) -> bool:
        raise NotImplementedError

    def apply(self, results: Sequence[LineResult], remaining_cents: int) -> int:
        raise NotImplementedError

class CheapestFreePerN(OrderRule):
    """组合优惠：每 n 份披萨（跨款式），其中最便宜的一份免费。
    价格取行级折扣之后的每份均价（整除向下），从高到低排，每 n 份切一组，每个满组最后（最便宜）的一份免费；不满一组的不算。"""

    def __init__(self, label: str, n: int) -> None:
        raise NotImplementedError

    def _prices(self, results: Sequence[LineResult]) -> list[int]:
        raise NotImplementedError

    def is_eligible(self, results: Sequence[LineResult], remaining_cents: int) -> bool:
        raise NotImplementedError

    def apply(self, results: Sequence[LineResult], remaining_cents: int) -> int:
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class Adjustment:
    label: str
    cents: int

@dataclass(frozen=True, slots=True)
class LineResult:
    line: OrderLine
    adjustments: tuple[Adjustment, ...]

    @property
    def final_cents(self) -> int:
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class Receipt:
    lines: tuple[LineResult, ...]
    order_adjustments: tuple[Adjustment, ...] = field(default=())

    @property
    def subtotal_cents(self) -> int:
        raise NotImplementedError

    @property
    def discount_cents(self) -> int:
        raise NotImplementedError

    @property
    def total_cents(self) -> int:
        raise NotImplementedError

class PriceEngine:
    """规则集不可变，`price` 是纯函数：同一份订单快照算多少次结果都一样，引擎可被多线程共享。"""

    def __init__(self, line_rules: Sequence[LineRule]=(), order_rules: Sequence[OrderRule]=()) -> None:
        raise NotImplementedError

    @staticmethod
    def _bounded(amount: int, remaining: int, label: str) -> int:
        raise NotImplementedError

    def _price_line(self, line: OrderLine) -> LineResult:
        raise NotImplementedError

    def price(self, lines: Sequence[OrderLine]) -> Receipt:
        raise NotImplementedError
