"""AWS 账单服务（练习骨架）：补全每个方法体，使测试通过。

要点：钱用整数分；阶梯价按边际计；先聚合再分档；每行只舍入一次；用量按 usage_id 去重；
价格按生效时间有多个版本。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Protocol


class BillingError(Exception):
    """账单领域错误的基类。"""


class InvalidUsage(BillingError):
    """用量为负数，或同一个 usage_id 带着不同内容再次出现。"""


class UnknownServiceError(BillingError, LookupError):
    """没有为该 (服务, 指标) 在该时刻登记价格。"""


@dataclass(frozen=True, order=True)
class Money:
    cents: int
    currency: str = "USD"

    @staticmethod
    def from_decimal(amount: Decimal, currency: str = "USD") -> Money:
        """元 → 分，四舍五入（half-up）。"""
        raise NotImplementedError

    def __add__(self, other: Money) -> Money:
        """币种不同抛 BillingError。"""
        raise NotImplementedError

    def __str__(self) -> str:
        """例如 "1371.20 USD"。"""
        raise NotImplementedError


class RatePlan(Protocol):
    def charge(self, quantity: Decimal) -> Decimal: ...


@dataclass(frozen=True)
class FlatRate:
    rate: Decimal

    def charge(self, quantity: Decimal) -> Decimal:
        raise NotImplementedError


@dataclass(frozen=True)
class Tier:
    up_to: Decimal | None
    rate: Decimal


@dataclass(frozen=True)
class TieredRate:
    tiers: tuple[Tier, ...]

    def charge(self, quantity: Decimal) -> Decimal:
        raise NotImplementedError


@dataclass(frozen=True)
class FreeTierThen:
    free_units: Decimal
    inner: RatePlan

    def charge(self, quantity: Decimal) -> Decimal:
        raise NotImplementedError


@dataclass(frozen=True)
class UsageRecord:
    usage_id: str
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
    def __init__(self) -> None:
        raise NotImplementedError

    def set_price(self, service: str, metric: str, plan: RatePlan,
                  effective_from: datetime, currency: str = "USD") -> None:
        raise NotImplementedError

    def version_at(self, service: str, metric: str, at: datetime) -> PriceVersion:
        """at 时刻生效的版本；没有则抛 UnknownServiceError。"""
        raise NotImplementedError


class UsageLedger:
    def __init__(self) -> None:
        raise NotImplementedError

    def add(self, record: UsageRecord) -> bool:
        """新记录 True；内容相同的重复 False；负数量或同 id 不同内容抛 InvalidUsage。"""
        raise NotImplementedError

    @property
    def duplicates_ignored(self) -> int:
        raise NotImplementedError

    def between(self, start: datetime, end: datetime) -> tuple[UsageRecord, ...]:
        """[start, end) 内的记录快照。"""
        raise NotImplementedError


@dataclass(frozen=True)
class InvoiceLine:
    service: str
    metric: str
    quantity: Decimal
    price_from: datetime
    amount: Money


@dataclass(frozen=True)
class Invoice:
    lines: tuple[InvoiceLine, ...]
    duplicates_ignored: int = 0

    @property
    def totals(self) -> dict[str, Money]:
        raise NotImplementedError

    @property
    def total(self) -> Money:
        raise NotImplementedError


@dataclass
class BillingService:
    prices: PriceBook
    ledger: UsageLedger = field(default_factory=lambda: UsageLedger())

    def record(self, usage: UsageRecord) -> bool:
        raise NotImplementedError

    def invoice(self, start: datetime, end: datetime) -> Invoice:
        raise NotImplementedError
