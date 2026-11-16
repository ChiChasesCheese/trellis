"""汇率换算服务：批量报价整批登记，三种路线查询。

设计（五行）：
1. `parse_quotes` 把整段文本先解析成 `Quote` 列表；任何一条不合法就抛 400，此时服务的状态还没被碰过。
2. `RateBook` 是不可变的汇率簿：`extend` 返回一本新簿子，登记 = 解析成功、合并成功之后一次赋值。
3. 返回值每次都新建字典和列表（浮点数本身不可变），调用方改返回值碰不到内部状态。
4. 路线用递归深度优先枚举所有简单路径（货币至多 8 种，最多 1957 条），只在 `best_path` 里选一条。
5. 错误优先级固定：先格式（400），再货币是否出现过（404 currency_not_found），最后有没有路（404 route_not_found）。
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass

MAX_CURRENCIES = 8
RATE_MIN, RATE_MAX = 1e-12, 1e12
TOLERANCE = 1e-5  # 最优路线的绝对容差：以全局最大乘积为基准

_CODE = re.compile(r"[A-Z]{3,5}")  # fullmatch：`$` 会放过末尾的换行，fullmatch 不会
_RATE = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


class ServiceError(Exception):
    """对外的错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def _invalid() -> ServiceError:
    return ServiceError(400, "invalid_input")


@dataclass(frozen=True, slots=True)
class Quote:
    """一条有向报价：1 单位 source 换 rate 单位 target。"""

    source: str
    target: str
    rate: float


def is_code(value: object) -> bool:
    return isinstance(value, str) and _CODE.fullmatch(value) is not None


def parse_quote(record: str) -> Quote:
    """一条记录恰好三段；货币 3–5 位大写；汇率按语法匹配后再看解析出的 binary64 值。"""
    parts = record.split(":")
    if len(parts) != 3:
        raise _invalid()
    source, target, token = parts
    if not (is_code(source) and is_code(target)) or source == target:
        raise _invalid()
    if _RATE.fullmatch(token) is None:
        raise _invalid()
    rate = float(token)  # 最近的 binary64；语法已保证不会抛错
    if not (math.isfinite(rate) and RATE_MIN <= rate <= RATE_MAX):
        raise _invalid()
    return Quote(source, target, rate)


def parse_quotes(stream: object) -> list[Quote]:
    """整段先解析完：空串、空记录、非字符串都是 400。这一步不碰任何服务状态。"""
    if not isinstance(stream, str) or stream == "":
        raise _invalid()
    return [parse_quote(record) for record in stream.split(",")]


class RateBook:
    """不可变的汇率簿。不变量：边的端点至多 MAX_CURRENCIES 种；构造之后不再改变。"""

    def __init__(self, rates: Mapping[tuple[str, str], float] | None = None) -> None:
        self._rates = dict(rates or {})
        self._out: dict[str, dict[str, float]] = {}
        for (source, target), rate in self._rates.items():
            self._out.setdefault(source, {})[target] = rate
        if len(self.currencies) > MAX_CURRENCIES:
            raise _invalid()

    @property
    def currencies(self) -> frozenset[str]:
        """出现过的货币：边的起点和终点都算（只作终点的也算）。"""
        return frozenset(c for pair in self._rates for c in pair)

    def extend(self, quotes: list[Quote]) -> RateBook:
        """合并一批报价，返回新簿子；后面的同向报价覆盖前面的。原簿子不变，所以失败时无需回滚。"""
        merged = dict(self._rates)
        for quote in quotes:
            merged[(quote.source, quote.target)] = quote.rate
        return RateBook(merged)

    def rate(self, source: str, target: str) -> float | None:
        return self._rates.get((source, target))

    def pairs(self, source: str | None = None) -> list[tuple[str, str, float]]:
        """按起点、再按终点排序的所有报价。"""
        return sorted((s, t, r) for (s, t), r in self._rates.items() if source in (None, s))

    def single_hop(self, source: str, target: str) -> list[float]:
        """直达报价，加上每个中转货币 M（M 不是 source 也不是 target）的两段乘积；升序，重复值保留。"""
        rates = []
        direct = self.rate(source, target)
        if direct is not None:
            rates.append(direct)
        for middle, first in self._out.get(source, {}).items():
            second = self.rate(middle, target)
            if second is not None:  # 自报价在登记时就被拒绝，所以 middle 不可能等于 source 或 target
                rates.append(first * second)
        return sorted(rates)

    def routes(self, source: str, target: str) -> Iterator[tuple[list[str], float]]:
        """递归枚举 source 到 target 的所有简单有向路径及其乘积；走到 target 就停，不穿过它。"""

        def walk(path: list[str], product: float) -> Iterator[tuple[list[str], float]]:
            here = path[-1]
            if here == target:
                yield list(path), product
                return
            for nxt, rate in self._out.get(here, {}).items():
                if nxt not in path:  # 简单路径：每种货币至多出现一次，环就走不起来
                    path.append(nxt)
                    yield from walk(path, product * rate)  # 从 1 开始，从左到右连乘
                    path.pop()

        yield from walk([source], 1.0)


def best_path(routes: Iterator[tuple[list[str], float]]) -> tuple[list[str], float] | None:
    """先找全局最大乘积 M；乘积与 M 的差不超过容差的都算合格；合格里选边数最少，再选字典序最小。"""
    found = list(routes)
    if not found:
        return None
    top = max(product for _, product in found)
    eligible = [(path, product) for path, product in found if top - product <= TOLERANCE]
    return min(eligible, key=lambda item: (len(item[0]), item[0]))


class CurrencyExchangeService:
    def __init__(self) -> None:
        self._book = RateBook()

    def register_rates(self, rates_stream: str) -> tuple[int, dict]:
        quotes = parse_quotes(rates_stream)
        self._book = self._book.extend(quotes)  # 解析与合并都成功之后，唯一的一次写入
        return 201, {"registered_count": len(quotes)}

    def _known_pair(self, source: object, target: object) -> None:
        """错误优先级的前两层：两个码的格式都先查，再查有没有出现过。"""
        if not (is_code(source) and is_code(target)):
            raise _invalid()
        known = self._book.currencies
        if source not in known or target not in known:
            raise ServiceError(404, "currency_not_found")

    def get_direct_rate(self, from_currency: str, to_currency: str) -> tuple[int, dict]:
        self._known_pair(from_currency, to_currency)
        rate = 1.0 if from_currency == to_currency else self._book.rate(from_currency, to_currency)
        if rate is None:
            raise ServiceError(404, "route_not_found")
        return 200, {"from": from_currency, "to": to_currency, "rate": rate}

    def get_single_hop_rates(self, from_currency: str, to_currency: str) -> tuple[int, dict]:
        self._known_pair(from_currency, to_currency)
        if from_currency == to_currency:
            rates = [1.0]
        else:
            rates = self._book.single_hop(from_currency, to_currency)
        if not rates:
            raise ServiceError(404, "route_not_found")
        return 200, {"from": from_currency, "to": to_currency, "rates": rates}

    def get_best_rate(self, from_currency: str, to_currency: str) -> tuple[int, dict]:
        self._known_pair(from_currency, to_currency)
        if from_currency == to_currency:
            path, rate = [from_currency], 1.0
        else:
            best = best_path(self._book.routes(from_currency, to_currency))
            if best is None:
                raise ServiceError(404, "route_not_found")
            path, rate = best
        return 200, {"from": from_currency, "to": to_currency, "best_rate": rate, "path": path}

    def list_pairs(self, from_currency: str | None = None) -> tuple[int, list[dict]]:
        if from_currency is not None:
            if not is_code(from_currency):
                raise _invalid()
            if from_currency not in self._book.currencies:
                raise ServiceError(404, "currency_not_found")
        rows = self._book.pairs(from_currency)
        return 200, [{"from_currency": s, "to_currency": t, "rate": r} for s, t, r in rows]


if __name__ == "__main__":
    service = CurrencyExchangeService()
    service.register_rates("USD:EUR:0.9,EUR:CAD:1.5,USD:CAD:1.2")
    print(service.get_single_hop_rates("USD", "CAD"))
    print(service.get_best_rate("USD", "CAD"))
