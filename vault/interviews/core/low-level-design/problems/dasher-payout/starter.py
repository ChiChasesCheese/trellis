"""配送员薪资（Dasher Payout）——起始模板。公开的类名、签名、枚举和异常与 `solution.py` 一致。"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, time
from decimal import Decimal
from enum import Enum


class State(Enum):
    TO_RESTAURANT = "to_restaurant"   # 接单 -> 到店
    WAITING = "waiting"               # 到店 -> 取餐
    DELIVERING = "delivering"         # 取餐 -> 送达


class EventType(Enum):
    ACCEPT = 1
    ARRIVE = 2
    PICKUP = 3
    DROPOFF = 4


class PayrollError(Exception):
    """所有失败路径的公共基类。"""


class DriverMismatchError(PayrollError):
    """这一单已经属于另一位配送员。"""


class ConflictingEventError(PayrollError):
    """同一类事件已经记录过，且时间不同。"""


class InconsistentTimelineError(PayrollError):
    """事件时间与这一单已有的事件顺序矛盾（比如取餐早于到店）。"""


class UnknownDeliveryError(PayrollError):
    """没有这一单。"""


class MissingEventError(PayrollError):
    """要更正的事件还没有记录过。"""


@dataclass(frozen=True)
class PeakWindow:
    """第 2 关：每天重复的高峰时段 [start, end)；`end == time(0)` 表示到当天午夜。"""

    start: time
    end: time
    multiplier: Decimal


@dataclass(frozen=True)
class PayPlan:
    """rates 必须给出每个 State 的每分钟单价（非负），否则抛 ValueError。

    第 2 关：peaks 是互不重叠的高峰窗口（窗口为空、倍率不为正、或互相重叠，抛 ValueError）。
    第 3 关：min_delivery_pay 非负，否则抛 ValueError。
    """

    rates: Mapping[State, Decimal]
    peaks: tuple[PeakWindow, ...] = ()
    min_delivery_pay: Decimal = Decimal("0")


@dataclass(frozen=True)
class PaySegment:
    state: State
    start: datetime
    end: datetime
    multiplier: Decimal
    amount: Decimal


class Payroll:
    def __init__(self, plan: PayPlan) -> None:
        raise NotImplementedError

    def record(self, driver_id: str, delivery_id: str, event: EventType, at: datetime) -> None:
        """记一个事件。事件可以乱序到达；同一类事件用同样的时间重复上报被忽略。

        - 订单属于第一次上报它的配送员；别人再报抛 DriverMismatchError。
        - 同一类事件已记录过且时间不同，抛 ConflictingEventError。
        - 时间必须落在生命周期（ACCEPT < ARRIVE < PICKUP < DROPOFF，允许相等）前后相邻已知事件之间，
          否则抛 InconsistentTimelineError。失败的调用不改变任何状态。
        """
        raise NotImplementedError

    def delivery_pay(self, delivery_id: str) -> Decimal:
        """这一单目前应付的钱，四舍五入（0.5 进位）到分，只在整单的最后舍入一次。

        三段各自计费：ACCEPT->ARRIVE 按 TO_RESTAURANT，ARRIVE->PICKUP 按 WAITING，PICKUP->DROPOFF 按 DELIVERING；
        一段的钱 = 每分钟单价 x 秒数 / 60，只有两端事件都已知的段才计费。
        第 2 关：段跨过高峰窗口时在边界处切开，各小段乘上自己的倍率（不在任何窗口内的倍率为 1）。
        第 3 关：四个事件都齐了的订单，至少付 min_delivery_pay。
        没有这一单抛 UnknownDeliveryError。
        """
        raise NotImplementedError

    def driver_payout(self, driver_id: str) -> Decimal:
        """这位配送员所有订单的 delivery_pay 之和；没有订单返回 Decimal("0.00")。"""
        raise NotImplementedError

    def payout(self, driver_id: str, start: datetime, end: datetime) -> Decimal:
        """第 3 关：结算周期 [start, end)。只统计已送达且 DROPOFF 时间落在周期内的订单，整单的钱记入该周期。"""
        raise NotImplementedError

    def correct_event(self, delivery_id: str, event: EventType, new_at: datetime) -> None:
        """第 4 关：更正一个已记录事件的时间。没有这一单抛 UnknownDeliveryError；该事件没记录过抛 MissingEventError；
        新时间与时间线矛盾抛 InconsistentTimelineError，且保持原样。"""
        raise NotImplementedError

    def delivery_breakdown(self, delivery_id: str) -> list[PaySegment]:
        """第 4 关：按时间顺序列出每个计费小段（已按高峰边界切开），amount 精确到 4 位小数。"""
        raise NotImplementedError
