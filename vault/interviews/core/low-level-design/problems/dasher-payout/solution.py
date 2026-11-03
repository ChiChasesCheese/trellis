"""配送员薪资（Dasher Payout）：配送事件、按状态计价、高峰倍率、按人汇总。

核心思路：只存"事实"（每单的四个时间点），不存"钱"。配送分三段：接单到到店（去餐厅）、到店到取餐
（等餐）、取餐到送达（送餐）。每一段的钱总是从两端的时间点现算：按状态的每分钟单价，乘上高峰
倍率（跨过高峰窗口的段在边界处切开，各算各的），最后每单只做一次四舍五入。因为钱是现算的，事件
乱序到达、重复上报、事后更正都不需要"回滚旧账"：只要事实表对了，钱就对。
金额内部用 `Fraction` 精确计算，避免 `Decimal` 除以 60 的循环小数在四舍五入边界上出错。
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from itertools import pairwise
from types import MappingProxyType


class State(Enum):
    TO_RESTAURANT = "to_restaurant"
    WAITING = "waiting"
    DELIVERING = "delivering"


class EventType(Enum):
    ACCEPT = 1
    ARRIVE = 2
    PICKUP = 3
    DROPOFF = 4


LIFECYCLE = list(EventType)  # 生命周期顺序
STATE_AFTER = {EventType.ACCEPT: State.TO_RESTAURANT, EventType.ARRIVE: State.WAITING,
               EventType.PICKUP: State.DELIVERING}  # 某个事件之后到下一个事件之前，处于什么状态


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


@dataclass(frozen=True, slots=True)
class PeakWindow:
    """每天重复的高峰时段 [start, end)；`end == time(0)` 表示到当天午夜。跨午夜的窗口拆成两个。"""

    start: time
    end: time
    multiplier: Decimal

    @property
    def end_seconds(self) -> int:
        return 86400 if self.end == time(0) else _secs(self.end)

    def covers(self, t: time) -> bool:
        return _secs(self.start) <= _secs(t) < self.end_seconds


def _secs(t: time) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second


@dataclass(frozen=True, slots=True)
class PayPlan:
    rates: Mapping[State, Decimal]       # 每分钟单价
    peaks: tuple[PeakWindow, ...] = ()   # 第 2 关
    min_delivery_pay: Decimal = Decimal("0")  # 第 3 关：每个完成的订单至少付这么多

    def __post_init__(self) -> None:
        object.__setattr__(self, "rates", MappingProxyType(dict(self.rates)))  # 拷贝成只读视图：调用方之后再改原字典也不影响
        if set(self.rates) != set(State) or any(r < 0 for r in self.rates.values()):
            raise ValueError("need a non-negative rate for every state")
        if self.min_delivery_pay < 0:
            raise ValueError("min_delivery_pay must be non-negative")
        ordered = sorted(self.peaks, key=lambda w: _secs(w.start))
        for w in ordered:
            if not (w.end_seconds > _secs(w.start)) or w.multiplier <= 0:
                raise ValueError(f"bad peak window {w}")
        if any(a.end_seconds > _secs(b.start) for a, b in pairwise(ordered)):
            raise ValueError("peak windows overlap")


@dataclass(frozen=True, slots=True)
class PaySegment:
    state: State
    start: datetime
    end: datetime
    multiplier: Decimal
    amount: Decimal  # 精确到 4 位小数


def _cents(x: Fraction) -> Decimal:
    """四舍五入（0.5 进位）到分，只在每单的最后做一次。"""
    return Decimal(int(x * 100 + Fraction(1, 2))).scaleb(-2)


@dataclass(frozen=True, slots=True)
class _Seg:
    state: State
    start: datetime
    end: datetime
    multiplier: Decimal
    amount_exact: Fraction


def _at(day: date, seconds: int, like: datetime) -> datetime:
    """`day` 当天第 `seconds` 秒，时区与 `like` 相同；86400 秒就是第二天零点。"""
    return datetime.combine(day, time(0), tzinfo=like.tzinfo) + timedelta(seconds=seconds)


class Payroll:
    def __init__(self, plan: PayPlan) -> None:
        self._plan = plan
        self._driver: dict[str, str] = {}                         # 订单 -> 配送员
        self._events: dict[str, dict[EventType, datetime]] = {}   # 订单 -> 已知的事件时间

    # ---------------------------------------------------------------- 第 1 关：记录事实

    def record(self, driver_id: str, delivery_id: str, event: EventType, at: datetime) -> None:
        """记一个事件。可以乱序到达；完全相同的重复上报被忽略。校验全部通过才写入。"""
        owner = self._driver.get(delivery_id, driver_id)
        if owner != driver_id:
            raise DriverMismatchError(f"{delivery_id} belongs to {owner}")
        events = self._events.get(delivery_id, {})
        if event in events:
            if events[event] == at:
                return
            raise ConflictingEventError(f"{event.name} of {delivery_id} already at {events[event]}")
        self._check_timeline(events, event, at)
        self._driver[delivery_id] = driver_id
        self._events.setdefault(delivery_id, {})[event] = at

    @staticmethod
    def _check_timeline(events: Mapping[EventType, datetime], event: EventType, at: datetime) -> None:
        """新事件的时间必须落在生命周期里前后相邻已知事件之间。"""
        for other, t in events.items():
            if other is event:
                continue
            if (other.value < event.value and t > at) or (other.value > event.value and t < at):
                raise InconsistentTimelineError(f"{event.name} at {at} conflicts with {other.name} at {t}")

    def delivery_pay(self, delivery_id: str) -> Decimal:
        """这一单目前应付的钱：两端事件都已知的段才计费；四个事件齐了才适用保底。"""
        total = sum((seg.amount_exact for seg in self._segments(delivery_id)), Fraction(0))
        events = self._events[delivery_id]
        if len(events) == len(LIFECYCLE):
            total = max(total, Fraction(self._plan.min_delivery_pay))
        return _cents(total)

    def driver_payout(self, driver_id: str) -> Decimal:
        """这位配送员所有订单（包括还没送完的、已计费的段）应付的总和。"""
        return sum((self.delivery_pay(d) for d, owner in self._driver.items() if owner == driver_id), Decimal("0.00"))

    # ---------------------------------------------------------------- 把一段时间算成钱

    def _segments(self, delivery_id: str) -> list[_Seg]:
        if delivery_id not in self._events:
            raise UnknownDeliveryError(delivery_id)
        events, out = self._events[delivery_id], []
        for first, second in pairwise(LIFECYCLE):
            if first in events and second in events:
                out.extend(self._price_span(STATE_AFTER[first], events[first], events[second]))
        return out

    def _price_span(self, state: State, start: datetime, end: datetime) -> list[_Seg]:
        """第 2 关：在高峰窗口的边界处把 [start, end) 切开，每一小段用自己的倍率。"""
        points = sorted({start, end, *(c for c in self._boundaries(start, end) if start < c < end)})
        out = []
        for a, b in pairwise(points):
            mid = a + (b - a) / 2
            mult = next((w.multiplier for w in self._plan.peaks if w.covers(mid.time())), Decimal(1))
            seconds = Fraction((b - a) // timedelta(microseconds=1), 10**6)
            out.append(_Seg(state, a, b, mult,
                            Fraction(self._plan.rates[state]) * Fraction(mult) * seconds / 60))
        return out

    def _boundaries(self, start: datetime, end: datetime) -> list[datetime]:
        cuts, day = [], start.date()
        while day <= end.date():
            for w in self._plan.peaks:
                cuts.append(_at(day, _secs(w.start), start))
                cuts.append(_at(day, w.end_seconds, start))
            day += timedelta(days=1)
        return cuts

    # ---------------------------------------------------------------- 第 3 关：按结算周期汇总

    def payout(self, driver_id: str, start: datetime, end: datetime) -> Decimal:
        """结算周期 [start, end)：只统计送达时间落在周期内的订单，整单的钱记在送达那一天所在的周期。"""
        total = Decimal("0.00")
        for d, owner in self._driver.items():
            dropoff = self._events[d].get(EventType.DROPOFF)
            if owner == driver_id and dropoff is not None and start <= dropoff < end:
                total += self.delivery_pay(d)
        return total

    # ---------------------------------------------------------------- 第 4 关：更正与明细

    def correct_event(self, delivery_id: str, event: EventType, new_at: datetime) -> None:
        """改一个已记录事件的时间；钱是现算的，所以不用重算任何旧账。时间线矛盾则整体拒绝。"""
        if delivery_id not in self._events:
            raise UnknownDeliveryError(delivery_id)
        events = self._events[delivery_id]
        if event not in events:
            raise MissingEventError(f"{event.name} of {delivery_id} was never recorded")
        self._check_timeline(events, event, new_at)
        events[event] = new_at

    def delivery_breakdown(self, delivery_id: str) -> list[PaySegment]:
        """每一小段的状态、时间、倍率和金额（4 位小数）；整单的 `delivery_pay` 是总和只舍入一次。"""
        return [PaySegment(s.state, s.start, s.end, s.multiplier,
                           Decimal(int(s.amount_exact * 10000 + Fraction(1, 2))).scaleb(-4))
                for s in self._segments(delivery_id)]
