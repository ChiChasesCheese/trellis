"""价格 / 账单 / 费用计算（Amazon LLD 高频题族）：披萨、购物车折扣、AWS 用量账单、地铁票价封顶、交易手续费。

运行：`python3 -I pricing_billing.py`（全部 assert 通过打印 OK）。讲解见上一级 `pricing_billing.md`。

这一族题看起来是五道不同的题，骨架是同一个：
    输入（行项目 / 用量 / 行程） + 一串有顺序的规则  →  可解释的账单（每一分钱为什么是这个数）

三条贯穿全文的设计决定：
1. **钱不是浮点数**。`Money` 用整数"分"存储，比例（折扣率、税率、费率）用 `Decimal`，舍入发生在**明确规定的位置**一次，
   而不是每一步都舍。
2. **规则是策略对象，引擎只负责按顺序执行并记账**。新增一种折扣 = 新增一个 `PriceRule` 子类，`PricingEngine` 不动。
3. **结果带解释**。`Receipt` 里每个调整项都有标签和金额，subtotal + 全部调整 = total，可以审计、可以给客户看（Customer Obsession）。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal


# ───────────────────────────── 钱 ─────────────────────────────

@dataclass(frozen=True, order=True)
class Money:
    """不可变值对象，整数分。币种不同的运算直接报错，而不是悄悄相加。"""
    cents: int
    currency: str = "USD"

    @staticmethod
    def of(text: str, currency: str = "USD") -> "Money":
        cents = (Decimal(text) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
        return Money(int(cents), currency)

    @staticmethod
    def zero(currency: str = "USD") -> "Money":
        return Money(0, currency)

    def _check(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"币种不同: {self.currency} vs {other.currency}")

    def __add__(self, other: "Money") -> "Money":
        self._check(other)
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check(other)
        return Money(self.cents - other.cents, self.currency)

    def __neg__(self) -> "Money":
        return Money(-self.cents, self.currency)

    def times(self, n: int) -> "Money":
        return Money(self.cents * n, self.currency)

    def scale(self, rate: Decimal | str, rounding: str = ROUND_HALF_UP) -> "Money":
        """乘以比例并舍入到分。负数也按"远离零"的半入规则对称舍入（ROUND_HALF_UP 在 Decimal 里对负数是远离零）。"""
        value = (Decimal(self.cents) * Decimal(rate)).quantize(Decimal(1), rounding=rounding)
        return Money(int(value), self.currency)

    def is_negative(self) -> bool:
        return self.cents < 0

    def __str__(self) -> str:
        sign = "-" if self.cents < 0 else ""
        c = abs(self.cents)
        return f"{sign}{c // 100}.{c % 100:02d} {self.currency}"


def allocate(total: Money, weights: Sequence[int]) -> list[Money]:
    """最大余数法分摊：份额之和**恰好**等于 total（不多一分不少一分）。

    用途：整单折扣要摊到每个行项目（退货时按行退款）；账单总额拆给多个部门。
    先按比例向下取整，剩下的零头分给"小数部分最大"的那几份，并列时靠前的先得。
    """
    if not weights or any(w < 0 for w in weights) or sum(weights) == 0:
        raise ValueError("权重必须非负且和大于 0")
    sign = -1 if total.cents < 0 else 1
    cents = abs(total.cents)
    wsum = sum(weights)
    base = [cents * w // wsum for w in weights]
    remainders = [(cents * w % wsum, -i) for i, w in enumerate(weights)]
    leftover = cents - sum(base)
    for _, neg_i in sorted(remainders, reverse=True)[:leftover]:
        base[-neg_i] += 1
    return [Money(sign * b, total.currency) for b in base]


# ───────────────────────────── 购物车 / 规则引擎 ─────────────────────────────

@dataclass(frozen=True)
class Line:
    sku: str
    name: str
    category: str
    unit_price: Money
    qty: int

    @property
    def gross(self) -> Money:
        return self.unit_price.times(self.qty)


@dataclass(frozen=True)
class Adjustment:
    """一个调整项：负数 = 折扣，正数 = 税/费。`rule` 记录是哪条规则产生的，方便审计和测试。"""
    label: str
    amount: Money
    rule: str


@dataclass
class CartContext:
    """规则看到的世界：原始行项目、已经产生的调整。规则**只返回**调整，不直接改 ctx（由引擎记账）。"""
    lines: Sequence[Line]
    adjustments: list[Adjustment] = field(default_factory=list)

    @property
    def subtotal(self) -> Money:
        total = Money.zero(self.lines[0].unit_price.currency if self.lines else "USD")
        for ln in self.lines:
            total = total + ln.gross
        return total

    @property
    def running_total(self) -> Money:
        """subtotal + 目前已记账的调整。税、整单百分比这类"在前面规则之后"的规则以它为基数。"""
        total = self.subtotal
        for a in self.adjustments:
            total = total + a.amount
        return total


class PriceRule(ABC):
    """一条定价规则（策略模式）。`apply` 是纯函数：同样的 ctx 得到同样的调整，不记账、不改状态。"""

    name: str = "rule"

    @abstractmethod
    def apply(self, ctx: CartContext) -> list[Adjustment]: ...


@dataclass(frozen=True)
class PercentOff(PriceRule):
    """对满足条件的行项目按**原价**打折（不叠在别的折扣上）。每个行项目一条调整，账单上看得清。"""
    pct: Decimal
    where: Callable[[Line], bool] = lambda ln: True
    label: str = "percent off"
    name: str = "percent_off"

    def apply(self, ctx: CartContext) -> list[Adjustment]:
        out = []
        for ln in ctx.lines:
            if self.where(ln):
                off = ln.gross.scale(self.pct / 100)
                if off.cents:
                    out.append(Adjustment(f"{self.label}: {ln.name}", -off, self.name))
        return out


@dataclass(frozen=True)
class BuyXGetYFree(PriceRule):
    """买 buy 送 free（同一 SKU）：每满 buy+free 件，其中 free 件免费。7 件、买 3 送 1 → 只有 1 组，免 1 件。"""
    sku: str
    buy: int
    free: int
    name: str = "buy_x_get_y_free"

    def apply(self, ctx: CartContext) -> list[Adjustment]:
        out = []
        for ln in ctx.lines:
            if ln.sku == self.sku:
                groups = ln.qty // (self.buy + self.free)
                free_units = groups * self.free
                if free_units:
                    out.append(Adjustment(f"buy {self.buy} get {self.free}: {ln.name}",
                                          -ln.unit_price.times(free_units), self.name))
        return out


@dataclass(frozen=True)
class ThresholdBoost(PriceRule):
    """装饰器：整单原价 ≥ threshold 时，把内部规则产生的调整放大 factor 倍（"满 100 折扣翻倍"）。"""
    inner: PriceRule
    threshold: Money
    factor: int = 2
    name: str = "threshold_boost"

    def apply(self, ctx: CartContext) -> list[Adjustment]:
        adjs = self.inner.apply(ctx)
        if ctx.subtotal >= self.threshold:
            return [Adjustment(f"{a.label} (x{self.factor})", a.amount.times(self.factor), self.name) for a in adjs]
        return adjs


@dataclass(frozen=True)
class BestOf(PriceRule):
    """互斥组：几条规则里只取"优惠最大"的那一条（不可叠加的优惠券）。并列取靠前的，结果确定。"""
    rules: tuple[PriceRule, ...]
    name: str = "best_of"

    def apply(self, ctx: CartContext) -> list[Adjustment]:
        best: list[Adjustment] = []
        best_total = 0
        for r in self.rules:
            adjs = r.apply(ctx)
            total = sum(a.amount.cents for a in adjs)
            if total < best_total:
                best, best_total = adjs, total
        return best


@dataclass(frozen=True)
class TaxRule(PriceRule):
    """税：以**折后**金额为基数（running_total），对满足条件的类别征税。整单只舍入一次。"""
    rate: Decimal
    exempt_categories: frozenset[str] = frozenset()
    name: str = "tax"

    def apply(self, ctx: CartContext) -> list[Adjustment]:
        exempt = sum((ln.gross.cents for ln in ctx.lines if ln.category in self.exempt_categories), 0)
        # 简化：豁免类别按原价从税基里扣除；若豁免品也有折扣，真实系统要按行分摊折扣（见 allocate）
        base = ctx.running_total - Money(exempt, ctx.running_total.currency)
        if base.cents <= 0:
            return []
        return [Adjustment(f"tax {self.rate}%", base.scale(self.rate / 100), self.name)]


@dataclass(frozen=True)
class PercentFee(PriceRule):
    """手续费（证券/债券等）：按类别的费率，可有最低收费和封顶。`rates` 以类别为键，新增类别只改数据。"""
    rates: dict[str, Decimal]
    min_fee: Money = Money(0)
    cap: Money | None = None
    name: str = "fee"

    def apply(self, ctx: CartContext) -> list[Adjustment]:
        out = []
        for ln in ctx.lines:
            rate = self.rates.get(ln.category)
            if rate is None:
                continue
            fee = ln.gross.scale(rate / 100)
            if fee < self.min_fee:
                fee = self.min_fee
            if self.cap is not None and fee > self.cap:
                fee = self.cap
            out.append(Adjustment(f"{ln.category} fee: {ln.name}", fee, self.name))
        return out


@dataclass(frozen=True)
class Receipt:
    lines: tuple[Line, ...]
    adjustments: tuple[Adjustment, ...]
    subtotal: Money
    total: Money
    floored: bool                      # 调整把总价压到 0 以下时被夹到 0

    def explain(self) -> str:
        rows = [f"{ln.qty} x {ln.name} @ {ln.unit_price} = {ln.gross}" for ln in self.lines]
        rows += [f"  {a.label}: {a.amount}" for a in self.adjustments]
        rows.append(f"TOTAL {self.total}" + (" (floored at 0)" if self.floored else ""))
        return "\n".join(rows)


class PricingEngine:
    """按声明顺序执行规则并记账。**顺序就是语义**：先折扣后税与先税后折扣金额不同，所以顺序由调用方显式给出。"""

    def __init__(self, rules: Iterable[PriceRule]) -> None:
        self._rules = list(rules)

    def price(self, lines: Sequence[Line]) -> Receipt:
        if not lines:
            raise ValueError("空购物车")
        if len({ln.unit_price.currency for ln in lines}) != 1:
            raise ValueError("购物车里币种不一致")
        for ln in lines:
            if ln.qty <= 0:
                raise ValueError(f"数量必须为正: {ln.sku}")
        ctx = CartContext(lines)
        for rule in self._rules:
            ctx.adjustments.extend(rule.apply(ctx))
        total = ctx.running_total
        floored = total.is_negative()
        if floored:
            total = Money.zero(total.currency)
        return Receipt(tuple(lines), tuple(ctx.adjustments), ctx.subtotal, total, floored)


# ───────────────────────────── 披萨（定制：底、尺寸、配料）─────────────────────────────

class PizzaMenu:
    """菜单是数据，不是类层级：新增配料 = 加一行数据。尺寸相关的价格也是数据（大号配料更贵）。"""

    def __init__(self) -> None:
        self.base_price = {"S": Money.of("8.00"), "M": Money.of("10.00"), "L": Money.of("12.00")}
        self.crusts = {"thin": Money.of("0"), "thick": Money.of("1.00")}
        self.topping_price = {
            "cheese": {"S": Money.of("1.00"), "M": Money.of("1.50"), "L": Money.of("2.00")},
            "pepperoni": {"S": Money.of("1.50"), "M": Money.of("2.00"), "L": Money.of("2.50")},
            "mushroom": {"S": Money.of("1.00"), "M": Money.of("1.25"), "L": Money.of("1.50")},
        }


class PizzaBuilder:
    """Builder：分步收集选择，`build()` 时一次性校验并生成行项目（非法组合在这里就报错，而不是算出怪价格）。"""

    def __init__(self, menu: PizzaMenu) -> None:
        self._menu = menu
        self._size: str | None = None
        self._crust = "thin"
        self._toppings: list[str] = []

    def size(self, size: str) -> "PizzaBuilder":
        self._size = size
        return self

    def crust(self, crust: str) -> "PizzaBuilder":
        self._crust = crust
        return self

    def topping(self, name: str) -> "PizzaBuilder":
        self._toppings.append(name)
        return self

    def build(self) -> list[Line]:
        m = self._menu
        if self._size not in m.base_price:
            raise ValueError(f"未知尺寸: {self._size}")
        if self._crust not in m.crusts:
            raise ValueError(f"未知饼底: {self._crust}")
        lines = [Line(f"pizza-{self._size}", f"pizza {self._size}", "food", m.base_price[self._size], 1)]
        if m.crusts[self._crust].cents:
            lines.append(Line(f"crust-{self._crust}", f"{self._crust} crust", "food", m.crusts[self._crust], 1))
        for t in self._toppings:
            if t not in m.topping_price:
                raise ValueError(f"未知配料: {t}")
            lines.append(Line(f"top-{t}", f"{t} topping", "food", m.topping_price[t][self._size], 1))
        return lines


# ───────────────────────────── AWS 风格的用量账单 ─────────────────────────────

@dataclass(frozen=True)
class Tier:
    up_to: Decimal | None        # 本档上限（累计量，None = 无上限）
    rate: Decimal                # 每单位费率，可以是亚分（0.023 美元/GB）


class RatePlan(ABC):
    @abstractmethod
    def charge(self, quantity: Decimal) -> Decimal:
        """返回**未舍入**的美元金额（Decimal）。舍入只在账单行末尾做一次，避免亚分误差累积。"""


@dataclass(frozen=True)
class FlatRate(RatePlan):
    rate: Decimal

    def charge(self, quantity: Decimal) -> Decimal:
        return quantity * self.rate


@dataclass(frozen=True)
class TieredRate(RatePlan):
    """阶梯计价：每一档只对落在这一档内的那部分用量按这一档费率收费（边际税率式），而不是整体按最高档。"""
    tiers: tuple[Tier, ...]

    def charge(self, quantity: Decimal) -> Decimal:
        total, lower = Decimal(0), Decimal(0)
        for tier in self.tiers:
            upper = tier.up_to if tier.up_to is not None else quantity
            in_tier = max(Decimal(0), min(quantity, upper) - lower)
            total += in_tier * tier.rate
            lower = upper
            if quantity <= upper:
                break
        return total


@dataclass(frozen=True)
class FreeTierThen(RatePlan):
    """每月免费额度，超出部分按 inner 计费。注意：免费额度扣在**聚合后的月度用量**上。"""
    free_units: Decimal
    inner: RatePlan

    def charge(self, quantity: Decimal) -> Decimal:
        return self.inner.charge(max(Decimal(0), quantity - self.free_units))


@dataclass(frozen=True)
class UsageRecord:
    usage_id: str                # 幂等键：用量上报是至少一次投递，重复的记录不能多收钱
    service: str
    metric: str
    quantity: Decimal


@dataclass(frozen=True)
class InvoiceLine:
    service: str
    metric: str
    quantity: Decimal
    amount: Money


@dataclass(frozen=True)
class Invoice:
    lines: tuple[InvoiceLine, ...]
    total: Money
    duplicates_ignored: int


class BillingService:
    """单个账户一个计费周期的账单。流程：去重 → 按 (service, metric) 聚合 → 套费率计划 → 每行舍入一次 → 求和。

    关键决定（面试要说出口）：
    * 先**聚合再分档**。分档对月度总量生效，逐条记录各自分档会把每条都当成"第一档"，少收钱。
    * **每行舍入一次**，总额 = 各行舍入后之和，保证"账单上每一行加起来恰好等于总额"，客户拿计算器核对不出错。
    """

    def __init__(self, plans: dict[tuple[str, str], RatePlan]) -> None:
        self._plans = plans

    def invoice(self, usages: Iterable[UsageRecord]) -> Invoice:
        seen: set[str] = set()
        totals: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
        dups = 0
        for u in usages:
            if u.usage_id in seen:
                dups += 1
                continue
            seen.add(u.usage_id)
            if u.quantity < 0:
                raise ValueError(f"用量不能为负: {u.usage_id}")
            totals[(u.service, u.metric)] += u.quantity
        lines = []
        for key in sorted(totals):
            plan = self._plans.get(key)
            if plan is None:
                raise KeyError(f"没有费率计划: {key}")
            amount = plan.charge(totals[key])
            cents = int((amount * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))
            lines.append(InvoiceLine(key[0], key[1], totals[key], Money(cents)))
        total = Money.zero()
        for ln in lines:
            total = total + ln.amount
        return Invoice(tuple(lines), total, dups)


# ───────────────────────────── 地铁票价：按站数计费 + 每日封顶 ─────────────────────────────

class FareCalculator:
    """`calculate_fare(rider, start, stop, when)`：按经过的站数计费，同一乘客同一天累计封顶（周末封顶更低）。

    状态 = (乘客, 日期) → 当日已付。时间由调用方传入（`when`），代码里没有 `datetime.now()`，可确定性测试。
    封顶的语义写进文档：本次实付 = min(本次原价, 封顶 − 当日已付)，不会为负。
    """

    def __init__(self, stations: Sequence[str], per_stop: Money, weekday_cap: Money, weekend_cap: Money) -> None:
        self._index = {s: i for i, s in enumerate(stations)}
        if len(self._index) != len(stations):
            raise ValueError("站名重复")
        self._per_stop = per_stop
        self._caps = (weekday_cap, weekend_cap)
        self._paid: dict[tuple[str, date], Money] = {}

    def calculate_fare(self, rider: str, start: str, stop: str, when: datetime) -> Money:
        for s in (start, stop):
            if s not in self._index:
                raise KeyError(f"未知车站: {s}")
        base = self._per_stop.times(abs(self._index[start] - self._index[stop]))
        day = when.date()
        cap = self._caps[1] if day.weekday() >= 5 else self._caps[0]
        paid = self._paid.get((rider, day), Money.zero(base.currency))
        room = cap - paid
        charge = base if base <= room else (room if room.cents > 0 else Money.zero(base.currency))
        self._paid[(rider, day)] = paid + charge
        return charge


# ───────────────────────────── 测试 ─────────────────────────────

def _d(x: str) -> Decimal:
    return Decimal(x)


def _cart() -> list[Line]:
    return [
        Line("book", "Book", "books", Money.of("20.00"), 2),     # 40.00
        Line("pen", "Pen", "stationery", Money.of("5.00"), 4),   # 20.00
        Line("laptop", "Laptop", "electronics", Money.of("1000.00"), 1),
    ]


def _run_tests() -> None:
    # ── Money：整数分，无浮点误差；币种不同报错；零头分摊 ──
    assert Money.of("0.10").times(3) == Money.of("0.30")             # 浮点里 0.1*3 != 0.3
    assert Money.of("19.99") + Money.of("0.01") == Money.of("20")
    assert str(Money.of("-3.5")) == "-3.50 USD"
    try:
        Money.of("1") + Money.of("1", "EUR")
    except ValueError:
        pass
    else:
        raise AssertionError("币种不同应报错")
    assert Money.of("10.00").scale("0.075") == Money(75)             # 0.75 -> 75 分
    assert Money(5).scale("0.5") == Money(3) and Money(-5).scale("0.5") == Money(-3)   # 半入对称（远离零）
    parts = allocate(Money.of("10.00"), [1, 1, 1])
    assert [p.cents for p in parts] == [334, 333, 333] and sum(p.cents for p in parts) == 1000
    parts = allocate(Money.of("-0.05"), [3, 1])
    assert sum(p.cents for p in parts) == -5

    # ── 购物车：无规则 / 全场 10% / 分类 / 买三送一 ──
    base = PricingEngine([]).price(_cart())
    assert base.subtotal == Money.of("1060.00") and base.total == base.subtotal and not base.adjustments

    ten = PricingEngine([PercentOff(_d("10"), label="all 10%")]).price(_cart())
    assert ten.total == Money.of("954.00") and len(ten.adjustments) == 3
    assert ten.subtotal + sum((a.amount for a in ten.adjustments), Money.zero()) == ten.total   # 可审计：原价 + 全部调整 = 总价

    books = PricingEngine([PercentOff(_d("20"), where=lambda ln: ln.category == "books")]).price(_cart())
    assert books.total == Money.of("1052.00") and [a.amount for a in books.adjustments] == [Money.of("-8.00")]

    pens = _cart()
    pens[1] = Line("pen", "Pen", "stationery", Money.of("5.00"), 7)
    r7 = PricingEngine([BuyXGetYFree("pen", 3, 1)]).price(pens)
    assert r7.adjustments[0].amount == Money.of("-5.00")             # 7 件只有 1 组（4 件一组）
    pens[1] = Line("pen", "Pen", "stationery", Money.of("5.00"), 8)
    assert PricingEngine([BuyXGetYFree("pen", 3, 1)]).price(pens).adjustments[0].amount == Money.of("-10.00")
    pens[1] = Line("pen", "Pen", "stationery", Money.of("5.00"), 3)
    assert PricingEngine([BuyXGetYFree("pen", 3, 1)]).price(pens).adjustments == ()   # 不满一组不免

    # ── 满额翻倍（装饰器）：低于阈值不翻倍 ──
    boosted = ThresholdBoost(PercentOff(_d("10")), threshold=Money.of("100.00"), factor=2)
    big = PricingEngine([boosted]).price(_cart())
    assert big.total == Money.of("1060.00") - Money.of("212.00")     # 10% 翻倍 = 20%
    small_cart = [Line("pen", "Pen", "stationery", Money.of("5.00"), 4)]
    assert PricingEngine([boosted]).price(small_cart).total == Money.of("18.00")        # 20.00 < 100，保持 10%

    # ── 互斥组：只取最大的一条 ──
    best = BestOf((PercentOff(_d("5")), PercentOff(_d("10")), PercentOff(_d("10"), where=lambda ln: ln.category == "books")))
    assert PricingEngine([best]).price(_cart()).total == Money.of("954.00")

    # ── 顺序即语义：先折扣后税 ≠ 先税后折扣 ──
    tax = TaxRule(_d("8"))
    disc_then_tax = PricingEngine([PercentOff(_d("10")), tax]).price(_cart())
    tax_then_disc = PricingEngine([tax, PercentOff(_d("10"))]).price(_cart())
    assert disc_then_tax.total == Money.of("954.00") + Money.of("76.32")      # 税基 954.00 的 8%
    assert tax_then_disc.total == Money.of("1060.00") + Money.of("84.80") - Money.of("106.00")  # 税基是原价；折扣只按原价
    assert disc_then_tax.total != tax_then_disc.total
    exempt = PricingEngine([TaxRule(_d("8"), exempt_categories=frozenset({"books"}))]).price(_cart())
    assert exempt.total == Money.of("1060.00") + Money.of("81.60")      # 税基 = 1060 - 40（书豁免）= 1020，税 8% = 81.60

    # ── 价格下限：折扣叠加不会把总价压成负数 ──
    floored = PricingEngine([PercentOff(_d("100")), PercentOff(_d("50"))]).price(small_cart)
    assert floored.total == Money.zero() and floored.floored
    assert "floored" in floored.explain()

    # ── 校验 ──
    for bad in ([], [Line("x", "x", "c", Money.of("1"), 0)],
                [Line("x", "x", "c", Money.of("1"), 1), Line("y", "y", "c", Money.of("1", "EUR"), 1)]):
        try:
            PricingEngine([]).price(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("非法购物车应报错")

    # ── 披萨：尺寸相关配料价、饼底加价、税 ──
    menu = PizzaMenu()
    lines = PizzaBuilder(menu).size("L").crust("thick").topping("pepperoni").topping("mushroom").build()
    assert [ln.unit_price for ln in lines] == [Money.of("12.00"), Money.of("1.00"), Money.of("2.50"), Money.of("1.50")]
    order = PricingEngine([TaxRule(_d("10"))]).price(lines)
    assert order.subtotal == Money.of("17.00") and order.total == Money.of("18.70")
    small = PizzaBuilder(menu).size("S").topping("cheese").build()
    assert PricingEngine([]).price(small).total == Money.of("9.00")
    for bad_build in (lambda: PizzaBuilder(menu).build(), lambda: PizzaBuilder(menu).size("M").topping("anchovy").build(),
                      lambda: PizzaBuilder(menu).size("M").crust("stuffed").build()):
        try:
            bad_build()
        except ValueError:
            pass
        else:
            raise AssertionError("非法披萨应报错")
    # 团餐：5 份以上（行数无关，数量）整单 10% —— 用 ThresholdBoost 的思路也能写；这里直接用 PercentOff 演示数据驱动
    team = [ln for _ in range(5) for ln in PizzaBuilder(menu).size("M").topping("cheese").build()]
    team_receipt = PricingEngine([PercentOff(_d("10"), label="team lunch")]).price(team)
    assert team_receipt.subtotal == Money.of("57.50") and team_receipt.total == Money.of("51.75")

    # ── 证券手续费：按类别费率、最低收费、封顶；新增类别只改数据 ──
    trades = [Line("AAPL", "AAPL", "stock", Money.of("200.00"), 10),     # 2000.00
              Line("UST", "T-Bond", "bond", Money.of("1000.00"), 1),       # 1000.00
              Line("DOGE", "Doge", "crypto", Money.of("1.00"), 5)]         # 无费率的类别：不收费
    fees = PricingEngine([PercentFee({"stock": _d("0.5"), "bond": _d("0.1")}, min_fee=Money.of("2.00"), cap=Money.of("8.00"))]).price(trades)
    assert [a.amount for a in fees.adjustments] == [Money.of("8.00"), Money.of("2.00")]   # 股票 10.00 → 封顶 8.00；债券 1.00 → 最低 2.00
    assert fees.total == Money.of("3005.00") + Money.of("10.00")

    # ── AWS 用量账单：阶梯 / 免费额度 / 先聚合再分档 / 幂等去重 / 每行舍入一次 ──
    s3 = TieredRate((Tier(_d("51200"), _d("0.023")), Tier(_d("512000"), _d("0.022")), Tier(None, _d("0.021"))))   # 示例费率，非 AWS 现价
    assert s3.charge(_d("0")) == 0
    assert s3.charge(_d("51200")) == _d("1177.600")                       # 恰好用满第一档
    assert s3.charge(_d("102400")) == _d("2304.000")                      # 51200*0.023 + 51200*0.022
    assert s3.charge(_d("512001")) == _d("1177.6") + _d("10137.6") + _d("0.021")   # 51200*0.023 + 460800*0.022 + 1*0.021
    lam = FreeTierThen(_d("1000000"), FlatRate(_d("0.0000002")))           # 每月 100 万次免费，之后每次 0.0000002 美元
    assert lam.charge(_d("900000")) == 0 and lam.charge(_d("2500000")) == _d("0.30000000")
    svc = BillingService({("s3", "gb-month"): s3, ("lambda", "requests"): lam, ("ec2", "hours"): FlatRate(_d("0.0416"))})
    inv = svc.invoice([
        UsageRecord("u1", "s3", "gb-month", _d("30000")),
        UsageRecord("u2", "s3", "gb-month", _d("30000")),                  # 聚合后 60000，跨过第一档
        UsageRecord("u2", "s3", "gb-month", _d("30000")),                  # 重复投递：忽略
        UsageRecord("u3", "lambda", "requests", _d("2500000")),
        UsageRecord("u4", "ec2", "hours", _d("730")),
    ])
    assert inv.duplicates_ignored == 1
    by = {(ln.service, ln.metric): ln for ln in inv.lines}
    assert by[("s3", "gb-month")].quantity == _d("60000")
    assert by[("s3", "gb-month")].amount == Money.of("1177.60") + Money.of("193.60")      # 51200*0.023 + 8800*0.022 = 1177.6 + 193.6
    assert by[("lambda", "requests")].amount == Money.of("0.30")
    assert by[("ec2", "hours")].amount == Money.of("30.37")                # 730*0.0416 = 30.368 → 30.37（每行舍入一次）
    assert inv.total == sum((ln.amount for ln in inv.lines), Money.zero())  # 账单各行相加恰好等于总额
    # 为什么必须先聚合再分档：两条 30000 若各自分档，各自都落在最贵的第一档 → 1380.00；
    # 聚合后第二个 30000 里有 8800 落在更便宜的第二档 → 1371.20。费率随用量递减时，逐条分档会向客户多收钱。
    per_record = s3.charge(_d("30000")) * 2
    assert per_record == _d("1380.000") and s3.charge(_d("60000")) == _d("1371.200")
    try:
        svc.invoice([UsageRecord("x", "s3", "gb-month", _d("-1"))])
    except ValueError:
        pass
    else:
        raise AssertionError("负用量应报错")
    try:
        svc.invoice([UsageRecord("y", "sqs", "requests", _d("1"))])
    except KeyError:
        pass
    else:
        raise AssertionError("没有费率计划应报错")

    # ── 地铁票价：G→U→H→K→I 每站 2 美元，工作日封顶 15，周末封顶 10 ──
    fare = FareCalculator(["G", "U", "H", "K", "I"], Money.of("2.00"), Money.of("15.00"), Money.of("10.00"))
    sat = datetime(2026, 10, 17, 9, 0)                                      # 2026-10-17 是周六
    assert fare.calculate_fare("ann", "G", "I", sat) == Money.of("8.00")
    assert fare.calculate_fare("ann", "I", "G", sat) == Money.of("2.00")   # 周末封顶 10：8 + 2
    assert fare.calculate_fare("ann", "G", "U", sat) == Money.zero()       # 已封顶，本次免费
    assert fare.calculate_fare("bob", "G", "I", sat) == Money.of("8.00")   # 不同乘客各算各的
    assert fare.calculate_fare("ann", "G", "I", datetime(2026, 10, 19, 9, 0)) == Money.of("8.00")   # 周一，新的一天
    assert fare.calculate_fare("ann", "H", "H", sat) == Money.zero()        # 同站：0
    try:
        fare.calculate_fare("ann", "G", "Z", sat)
    except KeyError:
        pass
    else:
        raise AssertionError("未知车站应报错")


if __name__ == "__main__":
    _run_tests()
    print("OK pricing_billing")
