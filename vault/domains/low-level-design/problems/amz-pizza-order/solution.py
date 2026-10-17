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
    sign = "-" if cents < 0 else ""
    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"


# ───────────────────────────── 菜单（数据） ─────────────────────────────

@dataclass(frozen=True)
class CrustSpec:
    extra_cents: int = 0
    sizes: frozenset[str] | None = None           # None = 所有尺寸都能做


@dataclass(frozen=True)
class ToppingSpec:
    prices: dict[str, int]                        # 尺寸 → 价格（分）；大号配料更贵
    excludes: frozenset[str] = frozenset()        # 与哪些配料互斥


@dataclass(frozen=True)
class Menu:
    base: dict[str, int]                          # 尺寸 → 基础价（分）
    crusts: dict[str, CrustSpec]
    toppings: dict[str, ToppingSpec]
    max_toppings: int = 5

    def price(self, size: str, crust: str, toppings: Sequence[str]) -> int:
        """调用前选择必须已通过校验；价格 = 基础价 + 饼底加价 + 每种配料在该尺寸的价。"""
        return (self.base[size] + self.crusts[crust].extra_cents
                + sum(self.toppings[t].prices[size] for t in toppings))


def default_menu() -> Menu:
    return Menu(
        base={"S": 800, "M": 1000, "L": 1200},
        crusts={"thin": CrustSpec(), "thick": CrustSpec(100),
                "stuffed": CrustSpec(250, frozenset({"M", "L"}))},
        toppings={
            "cheese": ToppingSpec({"S": 100, "M": 150, "L": 200}, frozenset({"vegan_cheese"})),
            "vegan_cheese": ToppingSpec({"S": 150, "M": 200, "L": 250}, frozenset({"cheese"})),
            "pepperoni": ToppingSpec({"S": 150, "M": 200, "L": 250}),
            "mushroom": ToppingSpec({"S": 100, "M": 125, "L": 150}),
            "olive": ToppingSpec({"S": 100, "M": 125, "L": 150}),
            "pineapple": ToppingSpec({"S": 100, "M": 150, "L": 200}),
        },
    )


# ───────────────────────────── 披萨与 Builder ─────────────────────────────

@dataclass(frozen=True, slots=True)
class Pizza:
    """一份配好的披萨，不可变。toppings 已排序去重，所以“同样的披萨”相等、可哈希。"""
    size: str
    crust: str
    toppings: tuple[str, ...]
    unit_cents: int                               # 构建时定格的单价

    @property
    def sku(self) -> str:
        return f"{self.size}/{self.crust}/{'+'.join(self.toppings) or 'plain'}"


class PizzaBuilder:
    """分步收集，`build()` 时一次性校验。链式调用，可复用：每次 `build()` 产出新的 Pizza。"""

    def __init__(self, menu: Menu) -> None:
        self._menu = menu
        self._size: str | None = None
        self._crust = "thin"
        self._toppings: list[str] = []

    def size(self, size: str) -> PizzaBuilder:
        self._size = size
        return self

    def crust(self, crust: str) -> PizzaBuilder:
        self._crust = crust
        return self

    def topping(self, name: str) -> PizzaBuilder:
        self._toppings.append(name)
        return self

    def build(self) -> Pizza:
        menu, size = self._menu, self._size
        if size not in menu.base:
            raise InvalidChoiceError(f"未知尺寸: {size!r}")
        spec = menu.crusts.get(self._crust)
        if spec is None:
            raise InvalidChoiceError(f"未知饼底: {self._crust!r}")
        if spec.sizes is not None and size not in spec.sizes:
            raise InvalidChoiceError(f"{size} 号做不了 {self._crust} 饼底")
        toppings = tuple(sorted(self._toppings))
        if len(set(toppings)) != len(toppings):
            raise InvalidChoiceError("同一种配料不能重复选")
        if len(toppings) > menu.max_toppings:
            raise InvalidChoiceError(f"配料最多 {menu.max_toppings} 种")
        for name in toppings:
            if name not in menu.toppings:
                raise InvalidChoiceError(f"未知配料: {name!r}")
            clash = menu.toppings[name].excludes.intersection(toppings)
            if clash:
                raise InvalidChoiceError(f"{name} 与 {sorted(clash)[0]} 不能同时选")
        return Pizza(size, self._crust, toppings, menu.price(size, self._crust, toppings))


# ───────────────────────────── 订单 ─────────────────────────────

@dataclass(frozen=True, slots=True)
class OrderLine:
    pizza: Pizza
    qty: int

    @property
    def original_cents(self) -> int:
        return self.pizza.unit_cents * self.qty


class Order:
    """可变的订单：同样的披萨合并成一行；对外只给快照。"""

    def __init__(self) -> None:
        self._lines: dict[Pizza, int] = {}
        self._lock = Lock()

    def add(self, pizza: Pizza, qty: int = 1) -> None:
        if qty <= 0:
            raise InvalidOrderError("数量必须为正")
        with self._lock:                          # 读-改-写必须在锁内
            self._lines[pizza] = self._lines.get(pizza, 0) + qty

    def remove(self, pizza: Pizza) -> None:
        with self._lock:
            if self._lines.pop(pizza, None) is None:
                raise InvalidOrderError(f"{pizza.sku}: 不在订单里")

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        with self._lock:
            return tuple(OrderLine(p, q) for p, q in self._lines.items())


# ───────────────────────────── 折扣规则（两层） ─────────────────────────────

class LineRule(ABC):
    """行级折扣：`is_eligible` 问这行能不能用，`apply` 问在剩余价格上减多少。"""

    def __init__(self, label: str) -> None:
        self.label = label

    def is_eligible(self, line: OrderLine) -> bool:
        return True

    @abstractmethod
    def apply(self, line: OrderLine, remaining_cents: int) -> int: ...


class PercentOff(LineRule):
    def __init__(self, label: str, percent: str, sizes: frozenset[str] | None = None) -> None:
        super().__init__(label)
        value = Decimal(percent)
        if not 0 < value <= 100:
            raise InvalidRuleError(f"{label}: 百分比必须在 (0, 100]")
        self._bps, self._sizes = int(value * 100), sizes   # 基点：万分之一

    def is_eligible(self, line: OrderLine) -> bool:
        return self._sizes is None or line.pizza.size in self._sizes

    def apply(self, line: OrderLine, remaining_cents: int) -> int:
        return (2 * remaining_cents * self._bps + 10_000) // 20_000   # 整数半进位


class BuyXGetY(LineRule):
    """同一款披萨买 buy 送 free：先算送几份，再按剩余价格的份额折成钱。"""

    def __init__(self, label: str, buy: int, free: int) -> None:
        super().__init__(label)
        if buy <= 0 or free <= 0:
            raise InvalidRuleError(f"{label}: buy 和 free 都必须为正")
        self.buy, self.free = buy, free

    def is_eligible(self, line: OrderLine) -> bool:
        return line.qty >= self.buy + self.free

    def apply(self, line: OrderLine, remaining_cents: int) -> int:
        free_units = line.qty // (self.buy + self.free) * self.free
        return remaining_cents * free_units // line.qty


class OrderRule(ABC):
    """整单折扣：看行级折扣之后的各行结果和剩余总额，回答适用吗、减多少。"""

    def __init__(self, label: str) -> None:
        self.label = label

    @abstractmethod
    def is_eligible(self, results: Sequence[LineResult], remaining_cents: int) -> bool: ...

    @abstractmethod
    def apply(self, results: Sequence[LineResult], remaining_cents: int) -> int: ...


class ThresholdOff(OrderRule):
    """满 threshold 减 off，门槛按折后总额判断。"""

    def __init__(self, label: str, threshold_cents: int, off_cents: int) -> None:
        super().__init__(label)
        if threshold_cents <= 0 or off_cents <= 0:
            raise InvalidRuleError(f"{label}: 门槛和减免都必须为正")
        self.threshold_cents, self.off_cents = threshold_cents, off_cents

    def is_eligible(self, results: Sequence[LineResult], remaining_cents: int) -> bool:
        return remaining_cents >= self.threshold_cents

    def apply(self, results: Sequence[LineResult], remaining_cents: int) -> int:
        return self.off_cents


class CheapestFreePerN(OrderRule):
    """组合优惠：每 n 份披萨（跨款式），其中最便宜的一份免费。
    价格取行级折扣之后的每份均价（整除向下），从高到低排，每 n 份切一组，每个满组最后（最便宜）的一份免费；不满一组的不算。"""

    def __init__(self, label: str, n: int) -> None:
        super().__init__(label)
        if n < 2:
            raise InvalidRuleError(f"{label}: n 至少为 2")
        self.n = n

    def _prices(self, results: Sequence[LineResult]) -> list[int]:
        return sorted((r.final_cents // r.line.qty for r in results for _ in range(r.line.qty)), reverse=True)

    def is_eligible(self, results: Sequence[LineResult], remaining_cents: int) -> bool:
        return sum(r.line.qty for r in results) >= self.n

    def apply(self, results: Sequence[LineResult], remaining_cents: int) -> int:
        return sum(self._prices(results)[self.n - 1::self.n])


# ───────────────────────────── 账单与引擎 ─────────────────────────────

@dataclass(frozen=True, slots=True)
class Adjustment:
    label: str
    cents: int                                    # 正数 = 减免的金额


@dataclass(frozen=True, slots=True)
class LineResult:
    line: OrderLine
    adjustments: tuple[Adjustment, ...]

    @property
    def final_cents(self) -> int:
        return self.line.original_cents - sum(a.cents for a in self.adjustments)


@dataclass(frozen=True, slots=True)
class Receipt:
    lines: tuple[LineResult, ...]
    order_adjustments: tuple[Adjustment, ...] = field(default=())

    @property
    def subtotal_cents(self) -> int:
        return sum(r.line.original_cents for r in self.lines)

    @property
    def discount_cents(self) -> int:
        return (sum(a.cents for r in self.lines for a in r.adjustments)
                + sum(a.cents for a in self.order_adjustments))

    @property
    def total_cents(self) -> int:
        return self.subtotal_cents - self.discount_cents


class PriceEngine:
    """规则集不可变，`price` 是纯函数：同一份订单快照算多少次结果都一样，引擎可被多线程共享。"""

    def __init__(self, line_rules: Sequence[LineRule] = (), order_rules: Sequence[OrderRule] = ()) -> None:
        self._line_rules = tuple(line_rules)
        self._order_rules = tuple(order_rules)

    @staticmethod
    def _bounded(amount: int, remaining: int, label: str) -> int:
        if amount < 0:
            raise InvalidRuleError(f"{label}: 折扣算出了负数 {amount}，会让总价变高")
        return min(amount, remaining)             # 折扣永远不会把价格减到负数

    def _price_line(self, line: OrderLine) -> LineResult:
        remaining, adjustments = line.original_cents, []
        for rule in self._line_rules:             # 后一条看到的是前一条减完后的剩余价格
            if rule.is_eligible(line):
                amount = self._bounded(rule.apply(line, remaining), remaining, rule.label)
                if amount > 0:
                    adjustments.append(Adjustment(rule.label, amount))
                    remaining -= amount
        return LineResult(line, tuple(adjustments))

    def price(self, lines: Sequence[OrderLine]) -> Receipt:
        results = tuple(self._price_line(line) for line in lines)
        remaining, order_adjustments = sum(r.final_cents for r in results), []
        for rule in self._order_rules:            # 每减一次都重新问一遍是否适用
            if rule.is_eligible(results, remaining):
                amount = self._bounded(rule.apply(results, remaining), remaining, rule.label)
                if amount > 0:
                    order_adjustments.append(Adjustment(rule.label, amount))
                    remaining -= amount
        return Receipt(results, tuple(order_adjustments))


if __name__ == "__main__":
    menu = default_menu()
    order = Order()
    order.add(PizzaBuilder(menu).size("L").crust("thick").topping("pepperoni").topping("mushroom").build(), 2)
    order.add(PizzaBuilder(menu).size("S").topping("cheese").build())
    engine = PriceEngine([PercentOff("小号九折", "10", frozenset({"S"}))],
                         [CheapestFreePerN("买二送一", 3), ThresholdOff("满30减3", to_cents("30"), to_cents("3"))])
    receipt = engine.price(order.lines)
    print(format_cents(receipt.subtotal_cents), "->", format_cents(receipt.total_cents))
