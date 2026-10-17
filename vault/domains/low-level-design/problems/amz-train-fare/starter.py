"""火车票价练习骨架：公开 API 与 `solution.py` 完全一致，方法体全部待补全。
把每个 `raise NotImplementedError` 换成你自己的实现，然后用
`IMPL=starter uv run --with pytest python -m pytest <本目录> -q` 验收。
内部表示随你换，测试只通过公开方法断言。"""
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
        raise NotImplementedError

    def __sub__(self, other: Money) -> Money:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
ZERO = Money(0)

class Route:
    """一条线性线路：站名按顺序排列，hops[i] 是第 i 站到第 i+1 站的价格。

    prefix[i] = 从首站坐到第 i 站的累计价格，所以 fare(a, b) = |prefix[a] - prefix[b]|。
    """

    def __init__(self, stations: Iterable[str]=(), hop_price: Money=Money(100)) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, name: object) -> bool:
        raise NotImplementedError

    @property
    def stations(self) -> tuple[str, ...]:
        raise NotImplementedError

    def append(self, name: str, price: Money | None=None) -> None:
        """在线路末端加一站；price 是上一站到这一站的价格，缺省用默认价。O(1)。"""
        raise NotImplementedError

    def _append_locked(self, name: str, price: Money | None) -> None:
        raise NotImplementedError

    def insert_after(self, anchor: str, name: str) -> None:
        """在 anchor 之后插入一站：原来的一个区间被切成两个默认价区间。O(n)，因为后面的位置与前缀和都要重排。"""
        raise NotImplementedError

    def _index(self, name: str) -> int:
        raise NotImplementedError

    def price_between(self, start: str, stop: str) -> Money:
        """两站之间的原价，与方向无关；同一站为零。"""
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class Trip:
    """一次行程；规则只看这个，不看系统时钟。"""
    start: str
    stop: str
    when: datetime

class FareRule(Protocol):
    """一条定价规则：拿到当前价格，返回调整后的价格。无状态，按列表顺序依次应用。"""

    def apply(self, fare: Money, trip: Trip) -> Money:
        ...

@dataclass(frozen=True, slots=True)
class WeekendCap:
    """周末（周六、周日）单程票价封顶。"""
    cap: Money

    def apply(self, fare: Money, trip: Trip) -> Money:
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class PeakSurcharge:
    """工作日 [start_hour, end_hour) 加价 percent%，向下取整到分。"""
    start_hour: int
    end_hour: int
    percent: int

    def apply(self, fare: Money, trip: Trip) -> Money:
        raise NotImplementedError

class FareCalculator:
    """两站之间的票价：线路给原价，规则依次调整。"""

    def __init__(self, route: Route, rules: Sequence[FareRule]=(), clock: Callable[[], datetime]=datetime.now) -> None:
        raise NotImplementedError

    def quote(self, start: str, stop: str, when: datetime) -> Money:
        """在指定时刻乘这一程要付多少（不记账）。"""
        raise NotImplementedError

    def calculate_fare(self, start: str, stop: str) -> Money:
        raise NotImplementedError

    @property
    def clock(self) -> Callable[[], datetime]:
        raise NotImplementedError

class DailyCapLedger:
    """同一乘客同一天的累计封顶：本次实付 = min(本次票价, 封顶 - 当日已付)，不会为负。"""

    def __init__(self, calculator: FareCalculator, daily_cap: Money) -> None:
        raise NotImplementedError

    @property
    def tracked_days(self) -> int:
        raise NotImplementedError

    def paid_today(self, rider: str, day: date) -> Money:
        raise NotImplementedError

    def charge(self, rider: str, start: str, stop: str, when: datetime | None=None) -> Money:
        raise NotImplementedError
