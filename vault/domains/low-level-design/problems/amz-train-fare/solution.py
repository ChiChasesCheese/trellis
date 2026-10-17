"""火车线路票价（Train Fare Calculator）参考解。

设计五句话：
1. Route 拥有「有序站点 + 相邻两站的价格 + 前缀和」，任意两站的票价是两个前缀和的差，查询 O(1)。
2. Money 是整数「分」的值对象，所有金额运算都不碰浮点。
3. FareRule 是一条小接缝：拿「原价 + 行程」返回新价格，周末封顶、高峰加价各是一个无状态规则。
4. FareCalculator 把 Route 与规则串起来；时钟从构造函数注入，签名仍是报告里的 calculate_fare(start, stop)。
5. DailyCapLedger 是唯一有状态的部分：同一乘客同一天的累计封顶，一把锁保证不超额，并清理过期的日期。
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Protocol


class FareError(Exception):
    """本模块所有异常的根。"""


class UnknownStationError(FareError, LookupError):
    """车站不在线路上。"""


class DuplicateStationError(FareError, ValueError):
    """线路上已经有同名车站。"""


@dataclass(frozen=True, slots=True, order=True)
class Money:
    """金额，单位是「分」（最小货币单位）。frozen 加 order，所以可以直接 min() 与比较。"""

    cents: int

    def __add__(self, other: Money) -> Money:
        return Money(self.cents + other.cents)

    def __sub__(self, other: Money) -> Money:
        return Money(self.cents - other.cents)

    def __str__(self) -> str:
        return f"{self.cents // 100}.{self.cents % 100:02d}"


ZERO = Money(0)


class Route:
    """一条线性线路：站名按顺序排列，hops[i] 是第 i 站到第 i+1 站的价格。

    prefix[i] = 从首站坐到第 i 站的累计价格，所以 fare(a, b) = |prefix[a] - prefix[b]|。
    """

    def __init__(self, stations: Iterable[str] = (), hop_price: Money = Money(100)) -> None:
        self._default = hop_price
        self._names: list[str] = []
        self._hops: list[Money] = []
        self._pos: dict[str, int] = {}
        self._prefix: list[int] = []
        self._lock = threading.Lock()  # 加站与查价可能并发，查价要同时读位置与前缀和
        for name in stations:
            self.append(name)

    def __len__(self) -> int:
        with self._lock:
            return len(self._names)

    def __contains__(self, name: object) -> bool:
        with self._lock:
            return name in self._pos

    @property
    def stations(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._names)

    def append(self, name: str, price: Money | None = None) -> None:
        """在线路末端加一站；price 是上一站到这一站的价格，缺省用默认价。O(1)。"""
        with self._lock:
            self._append_locked(name, price)

    def _append_locked(self, name: str, price: Money | None) -> None:
        if name in self._pos:
            raise DuplicateStationError(name)
        if self._names:
            hop = self._default if price is None else price
            self._hops.append(hop)
            self._prefix.append(self._prefix[-1] + hop.cents)
        else:
            if price is not None:
                raise FareError("首站之前没有区间，不能指定价格")
            self._prefix.append(0)
        self._pos[name] = len(self._names)
        self._names.append(name)

    def insert_after(self, anchor: str, name: str) -> None:
        """在 anchor 之后插入一站：原来的一个区间被切成两个默认价区间。O(n)，因为后面的位置与前缀和都要重排。"""
        with self._lock:
            j = self._index(anchor)
            if j == len(self._names) - 1:
                self._append_locked(name, None)
                return
            if name in self._pos:
                raise DuplicateStationError(name)
            self._names.insert(j + 1, name)
            self._hops[j : j + 1] = [self._default, self._default]
            self._pos = {n: i for i, n in enumerate(self._names)}
            self._prefix = [0]
            for hop in self._hops:
                self._prefix.append(self._prefix[-1] + hop.cents)

    def _index(self, name: str) -> int:
        try:
            return self._pos[name]
        except KeyError:
            raise UnknownStationError(name) from None

    def price_between(self, start: str, stop: str) -> Money:
        """两站之间的原价，与方向无关；同一站为零。"""
        with self._lock:
            return Money(abs(self._prefix[self._index(start)] - self._prefix[self._index(stop)]))


@dataclass(frozen=True, slots=True)
class Trip:
    """一次行程；规则只看这个，不看系统时钟。"""

    start: str
    stop: str
    when: datetime


class FareRule(Protocol):
    """一条定价规则：拿到当前价格，返回调整后的价格。无状态，按列表顺序依次应用。"""

    def apply(self, fare: Money, trip: Trip) -> Money: ...


@dataclass(frozen=True, slots=True)
class WeekendCap:
    """周末（周六、周日）单程票价封顶。"""

    cap: Money

    def apply(self, fare: Money, trip: Trip) -> Money:
        return min(fare, self.cap) if trip.when.weekday() >= 5 else fare


@dataclass(frozen=True, slots=True)
class PeakSurcharge:
    """工作日 [start_hour, end_hour) 加价 percent%，向下取整到分。"""

    start_hour: int
    end_hour: int
    percent: int

    def apply(self, fare: Money, trip: Trip) -> Money:
        peak = trip.when.weekday() < 5 and self.start_hour <= trip.when.hour < self.end_hour
        return fare + Money(fare.cents * self.percent // 100) if peak else fare


class FareCalculator:
    """报告里的 calculateFare(start, stop)：线路给原价，规则依次调整。"""

    def __init__(
        self,
        route: Route,
        rules: Sequence[FareRule] = (),
        clock: Callable[[], datetime] = datetime.now,
    ) -> None:
        self._route = route
        self._rules = tuple(rules)
        self._clock = clock

    def quote(self, start: str, stop: str, when: datetime) -> Money:
        """在指定时刻乘这一程要付多少（不记账）。"""
        fare = self._route.price_between(start, stop)
        trip = Trip(start, stop, when)
        for rule in self._rules:
            fare = rule.apply(fare, trip)
        return fare

    def calculate_fare(self, start: str, stop: str) -> Money:
        return self.quote(start, stop, self._clock())

    @property
    def clock(self) -> Callable[[], datetime]:
        return self._clock


class DailyCapLedger:
    """同一乘客同一天的累计封顶：本次实付 = min(本次票价, 封顶 - 当日已付)，不会为负。"""

    def __init__(self, calculator: FareCalculator, daily_cap: Money) -> None:
        self._calc = calculator
        self._cap = daily_cap
        self._paid: dict[date, dict[str, Money]] = {}
        self._lock = threading.Lock()  # 「读已付、算、写回」必须是一步，否则两次并发乘车会一起突破封顶

    @property
    def tracked_days(self) -> int:
        with self._lock:
            return len(self._paid)

    def paid_today(self, rider: str, day: date) -> Money:
        with self._lock:
            return self._paid.get(day, {}).get(rider, ZERO)

    def charge(self, rider: str, start: str, stop: str, when: datetime | None = None) -> Money:
        when = when if when is not None else self._calc.clock()
        fare = self._calc.quote(start, stop, when)
        day = when.date()
        with self._lock:
            paid = self._paid.setdefault(day, {}).get(rider, ZERO)
            charged = min(fare, max(self._cap - paid, ZERO))
            self._paid[day][rider] = paid + charged
            for old in [d for d in self._paid if d < day - timedelta(days=1)]:
                del self._paid[old]  # 只保留今天和昨天（跨午夜的迟到记录），避免按天无限增长
            return charged


if __name__ == "__main__":
    route = Route("GUHKI")
    calc = FareCalculator(route, [WeekendCap(Money(300))], clock=lambda: datetime(2026, 10, 17, 9, 0))
    print(calc.calculate_fare("G", "I"), route.stations)
