"""运费计算服务：分段费率整批登记，按订单逐段累计报价。

设计（五行）：
1. `parse_rule` 把一行文本变成 `(国家, 商品, Tier)`；所有行的语法都先检查完，再去看分段是否连续，所以语法错（400）总先于分段错（422）。
2. `Tier` 是冻结的值对象，自己知道"买到 q 件时这一段收多少钱"；`Schedule` 在构造时校验分段从 1 起、无缝、不重叠、末段无上界。
3. 登记在一份局部副本上改，全部校验通过之后整体换掉 `self._schedules`；失败时旧状态一个字节都没变。
4. 报价先按商品合并数量，再逐段累计；金额全用 Python 的精确整数，最后才和 32 位上界比较。
5. 返回值每次新建字典和列表，内部只存不可变的 `Schedule`，调用方碰不到内部状态。
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

MAX_TOKEN = 1_000_000  # 每个十进制数字最多这么大
MAX_CENTS = 2_147_483_647  # 单个商品的费用、整单总额的上界（分）

_COUNTRY = re.compile(r"[A-Z]{2,5}")  # 一律 fullmatch：`$` 会放过末尾的换行
_PRODUCT = re.compile(r"[A-Za-z0-9_-]{1,32}")
_DIGITS = re.compile(r"[0-9]+")  # 不用 \d：它会匹配 Unicode 数字


class ServiceError(Exception):
    """对外的错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def _invalid() -> ServiceError:
    return ServiceError(400, "invalid_input")


def parse_number(token: str) -> int:
    """纯 ASCII 数字，允许前导零，值不超过 MAX_TOKEN。"""
    if _DIGITS.fullmatch(token) is None:
        raise _invalid()
    trimmed = token.lstrip("0")
    if len(trimmed) > len(str(MAX_TOKEN)):  # 先看长度：一长串零或大数交给 int() 会触发位数上限
        raise _invalid()
    value = int(trimmed or "0")
    if value > MAX_TOKEN:
        raise _invalid()
    return value


def is_country(value: object) -> bool:
    return isinstance(value, str) and _COUNTRY.fullmatch(value) is not None


class TierKind(Enum):
    INCREMENTAL = "incremental"  # 进入本段的每一件都收 cost
    FIXED = "fixed"  # 只要进入本段就一次性收 cost


@dataclass(frozen=True, slots=True)
class Tier:
    """一段闭区间 [low, high] 的费率；high 为 None 表示没有上界。"""

    kind: TierKind
    low: int
    high: int | None
    cost: int

    def charge(self, quantity: int) -> int:
        """买 quantity 件时这一段收多少分：没走到这一段是 0。"""
        if quantity < self.low:
            return 0
        if self.kind is TierKind.FIXED:
            return self.cost
        top = quantity if self.high is None else min(quantity, self.high)
        return (top - self.low + 1) * self.cost

    def as_row(self, country: str, product: str) -> dict:
        return {"country": country, "product": product, "type": self.kind.value,
                "min_quantity": self.low, "max_quantity": self.high, "cost_cents": self.cost}


@dataclass(frozen=True, slots=True)
class Schedule:
    """一个（国家，商品）的完整分段表。不变量：从 1 起、首尾相接、末段无上界；构造之后不再改变。"""

    tiers: tuple[Tier, ...]

    @classmethod
    def build(cls, tiers: Iterable[Tier]) -> Schedule:
        ordered = sorted(tiers, key=lambda tier: tier.low)
        expected: int | None = 1  # 下一段必须从这里开始；None 表示已经无界，后面不许再有段
        for tier in ordered:
            if tier.low != expected or (tier.high is not None and tier.high < tier.low):
                raise ServiceError(422, "invalid_rules")
            expected = None if tier.high is None else tier.high + 1
        if expected is not None:  # 最后一段是有限的
            raise ServiceError(422, "invalid_rules")
        return cls(tuple(ordered))

    def fee(self, quantity: int) -> int:
        return sum(tier.charge(quantity) for tier in self.tiers)


def parse_rule(line: object) -> tuple[str, str, Tier]:
    """一行恰好六段；只看语法，不看分段之间的关系。"""
    if not isinstance(line, str):
        raise _invalid()
    fields = line.split(",")
    if len(fields) != 6:
        raise _invalid()
    country, product, kind, low, high, cost = fields
    if not is_country(country) or _PRODUCT.fullmatch(product) is None:
        raise _invalid()
    try:
        tier_kind = TierKind(kind)
    except ValueError:
        raise _invalid() from None
    amount = parse_number(cost)
    if amount == 0:
        raise _invalid()
    upper = None if high == "*" else parse_number(high)
    return country, product, Tier(tier_kind, parse_number(low), upper, amount)


def parse_item(item: object) -> tuple[str, int]:
    """订单行 `商品,数量`：数量是 1 到 MAX_TOKEN 的整数。"""
    if not isinstance(item, str):
        raise _invalid()
    fields = item.split(",")
    if len(fields) != 2 or _PRODUCT.fullmatch(fields[0]) is None:
        raise _invalid()
    quantity = parse_number(fields[1])
    if quantity == 0:
        raise _invalid()
    return fields[0], quantity


class ShippingService:
    def __init__(self) -> None:
        self._schedules: dict[str, dict[str, Schedule]] = {}  # 国家 -> 商品 -> 分段表

    def register_rules(self, rules: list[str]) -> tuple[int, dict]:
        if not isinstance(rules, (list, tuple)) or not rules:
            raise _invalid()
        parsed = [parse_rule(line) for line in rules]  # 全部语法先过一遍
        grouped: dict[tuple[str, str], list[Tier]] = {}
        for country, product, tier in parsed:
            grouped.setdefault((country, product), []).append(tier)
        staged = {country: dict(products) for country, products in self._schedules.items()}
        for (country, product), tiers in grouped.items():  # 再逐对校验分段，改的是副本
            staged.setdefault(country, {})[product] = Schedule.build(tiers)
        self._schedules = staged  # 唯一的一次写入
        return 201, {"registered_count": len(parsed)}

    def calculate_shipping(self, country: str, items: list[str]) -> tuple[int, dict]:
        if not is_country(country) or not isinstance(items, (list, tuple)):
            raise _invalid()
        book = self._schedules.get(country)
        if book is None:
            raise ServiceError(404, "country_not_found")
        quantities: dict[str, int] = {}
        for item in items:  # 先合并重复商品：固定费率按总量算，分开算会多收
            product, quantity = parse_item(item)
            quantities[product] = quantities.get(product, 0) + quantity
            if quantities[product] > MAX_TOKEN:
                raise _invalid()
        if any(product not in book for product in quantities):
            raise ServiceError(404, "product_not_found")
        breakdown, total = [], 0
        for product in sorted(quantities):
            fee = book[product].fee(quantities[product])  # Python 整数是精确的，不会溢出
            if fee > MAX_CENTS:
                raise _invalid()
            breakdown.append({"product": product, "quantity": quantities[product], "cost": fee})
            total += fee
        if total > MAX_CENTS:
            raise _invalid()
        return 200, {"total_cost": total, "country": country, "breakdown": breakdown}

    def list_rules(self, country: str | None = None) -> tuple[int, list[dict]]:
        rows = [tier.as_row(name, product)
                for name in sorted(self._schedules) if country in (None, name)
                for product in sorted(self._schedules[name])
                for tier in self._schedules[name][product].tiers]
        return 200, rows


if __name__ == "__main__":
    service = ShippingService()
    service.register_rules(["NL,kettle,incremental,1,4,300", "NL,kettle,fixed,5,9,900", "NL,kettle,incremental,10,*,150"])
    print(service.calculate_shipping("NL", ["kettle,6", "kettle,5"]))  # 4*300 + 900 + 2*150 = 2400
