"""AWS 账单服务：一个账户，一个计费周期，按服务用量和费率出账单。

设计五行：
1. 钱用整数分（`Money`），费率和用量用 `Decimal`；只在账单行的最后舍入一次。
2. 费率是策略对象（`RatePlan`）：一口价、阶梯价、免费额度后再计费，互相可以嵌套。
3. 用量记录进 `UsageLedger`：按 `usage_id` 去重，重复投递不会多收钱。
4. `PriceBook` 按生效时间保存每个 (服务, 指标) 的价格版本，月中调价只是多一个版本。
5. `BillingService` 先聚合再分档，每行舍入一次，总额等于各行之和。
"""

from __future__ import annotations

import threading
from bisect import bisect_right
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Protocol


class BillingError(Exception):
    """账单领域错误的基类。"""


class InvalidUsage(BillingError):
    """用量为负数，或同一个 usage_id 带着不同内容再次出现。"""


class UnknownServiceError(BillingError, LookupError):
    """没有为该 (服务, 指标) 在该时刻登记价格。"""


@dataclass(frozen=True, order=True)
class Money:
    """整数分的值对象。币种不同的运算直接报错，不会悄悄相加。"""

    cents: int
    currency: str = "USD"

    @staticmethod
    def from_decimal(amount: Decimal, currency: str = "USD") -> Money:
        """把以「元」为单位的 Decimal 舍入到分，四舍五入（half-up）。"""
        return Money(int((amount * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)), currency)

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise BillingError(f"币种不同：{self.currency} 与 {other.currency}")
        return Money(self.cents + other.cents, self.currency)

    def __str__(self) -> str:
        sign = "-" if self.cents < 0 else ""
        return f"{sign}{abs(self.cents) // 100}.{abs(self.cents) % 100:02d} {self.currency}"


class RatePlan(Protocol):
    """一种计费方式：输入一个周期内的总用量，返回未舍入的金额（元）。"""

    def charge(self, quantity: Decimal) -> Decimal: ...


@dataclass(frozen=True)
class FlatRate:
    """一口价：每单位 `rate`。"""

    rate: Decimal

    def charge(self, quantity: Decimal) -> Decimal:
        return quantity * self.rate


@dataclass(frozen=True)
class Tier:
    up_to: Decimal | None  # 本档的累计上限；None 表示没有上限
    rate: Decimal


@dataclass(frozen=True)
class TieredRate:
    """阶梯价：每一档只对落在本档内的那部分用量收本档的价（边际，不是整体）。"""

    tiers: tuple[Tier, ...]

    def charge(self, quantity: Decimal) -> Decimal:
        total, lower = Decimal(0), Decimal(0)
        for tier in self.tiers:
            upper = quantity if tier.up_to is None else min(quantity, tier.up_to)
            if upper > lower:
                total += (upper - lower) * tier.rate
                lower = upper
            if tier.up_to is None or quantity <= tier.up_to:
                break
        return total


@dataclass(frozen=True)
class FreeTierThen:
    """每个周期先免费 `free_units` 个单位，超出的部分交给 `inner` 计费。"""

    free_units: Decimal
    inner: RatePlan

    def charge(self, quantity: Decimal) -> Decimal:
        return self.inner.charge(max(Decimal(0), quantity - self.free_units))


@dataclass(frozen=True)
class UsageRecord:
    usage_id: str  # 幂等键：同一次用量无论上报几遍，只算一次
    service: str
    metric: str
    quantity: Decimal
    at: datetime


@dataclass(frozen=True)
class PriceVersion:
    effective_from: datetime
    plan: RatePlan
    currency: str


class PriceBook:
    """每个 (服务, 指标) 一串按生效时间排序的价格版本；用量按发生时刻取当时生效的版本。"""

    def __init__(self) -> None:
        self._versions: dict[tuple[str, str], list[PriceVersion]] = {}

    def set_price(self, service: str, metric: str, plan: RatePlan,
                  effective_from: datetime, currency: str = "USD") -> None:
        versions = self._versions.setdefault((service, metric), [])
        versions.append(PriceVersion(effective_from, plan, currency))
        versions.sort(key=lambda v: v.effective_from)

    def version_at(self, service: str, metric: str, at: datetime) -> PriceVersion:
        versions = self._versions.get((service, metric), [])
        i = bisect_right([v.effective_from for v in versions], at) - 1
        if i < 0:
            raise UnknownServiceError(f"{service}/{metric} 在 {at} 没有价格")
        return versions[i]


class UsageLedger:
    """用量记录的去重仓库。上报是「至少一次」投递，所以同一个 usage_id 可能来很多遍。"""

    def __init__(self) -> None:
        self._records: dict[str, UsageRecord] = {}
        self._duplicates = 0
        self._lock = threading.Lock()

    def add(self, record: UsageRecord) -> bool:
        """记入一条用量。新记录返回 True；内容相同的重复投递返回 False；同 id 不同内容抛错。"""
        if record.quantity < 0:
            raise InvalidUsage(f"用量不能为负：{record.usage_id}")
        with self._lock:
            old = self._records.get(record.usage_id)
            if old is None:
                self._records[record.usage_id] = record
                return True
            if old != record:
                raise InvalidUsage(f"usage_id {record.usage_id} 的内容与之前不同")
            self._duplicates += 1
            return False

    @property
    def duplicates_ignored(self) -> int:
        with self._lock:
            return self._duplicates

    def between(self, start: datetime, end: datetime) -> tuple[UsageRecord, ...]:
        """[start, end) 内的记录快照。"""
        with self._lock:
            return tuple(r for r in self._records.values() if start <= r.at < end)


@dataclass(frozen=True)
class InvoiceLine:
    service: str
    metric: str
    quantity: Decimal
    price_from: datetime  # 本行用的是哪一个价格版本
    amount: Money


@dataclass(frozen=True)
class Invoice:
    lines: tuple[InvoiceLine, ...]
    duplicates_ignored: int = 0

    @property
    def totals(self) -> dict[str, Money]:
        """按币种分别求和；账单永远不跨币种相加。"""
        out: dict[str, Money] = {}
        for line in self.lines:
            cur = line.amount.currency
            out[cur] = out[cur] + line.amount if cur in out else line.amount
        return out

    @property
    def total(self) -> Money:
        """只有一种币种时的总额；多币种时请用 `totals`。"""
        if len(self.totals) != 1:
            raise BillingError("账单有零种或多种币种，请用 totals")
        return next(iter(self.totals.values()))


@dataclass
class BillingService:
    """记录用量、出账单。流程：取周期内记录 → 按价格版本聚合 → 套费率 → 每行舍入一次。"""

    prices: PriceBook
    ledger: UsageLedger = field(default_factory=UsageLedger)

    def record(self, usage: UsageRecord) -> bool:
        return self.ledger.add(usage)

    def invoice(self, start: datetime, end: datetime) -> Invoice:
        totals: dict[tuple[str, str, datetime], Decimal] = defaultdict(Decimal)
        versions: dict[tuple[str, str, datetime], PriceVersion] = {}
        for rec in self.ledger.between(start, end):
            version = self.prices.version_at(rec.service, rec.metric, rec.at)
            key = (rec.service, rec.metric, version.effective_from)
            totals[key] += rec.quantity
            versions[key] = version
        lines = tuple(
            InvoiceLine(service, metric, totals[key], since,
                        Money.from_decimal(versions[key].plan.charge(totals[key]), versions[key].currency))
            for key in sorted(totals)
            for service, metric, since in [key]
        )
        return Invoice(lines, self.ledger.duplicates_ignored)


if __name__ == "__main__":
    d = Decimal
    book = PriceBook()
    start = datetime(2026, 10, 1)
    book.set_price("s3", "gb-month", TieredRate((Tier(d("51200"), d("0.023")), Tier(None, d("0.022")))), start)
    svc = BillingService(book)
    svc.record(UsageRecord("u1", "s3", "gb-month", d("30000"), datetime(2026, 10, 2)))
    svc.record(UsageRecord("u2", "s3", "gb-month", d("30000"), datetime(2026, 10, 9)))
    svc.record(UsageRecord("u2", "s3", "gb-month", d("30000"), datetime(2026, 10, 9)))  # 重复投递
    bill = svc.invoice(start, datetime(2026, 11, 1))
    print(bill.total, bill.duplicates_ignored)
