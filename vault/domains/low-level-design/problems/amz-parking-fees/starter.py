"""练习骨架：公开 API 与 `solution.py` 完全一致，方法体全部待补全。
把每个 `raise NotImplementedError` 换成你自己的实现，然后用
`IMPL=starter uv run --with pytest python -m pytest <本目录> -q` 验收。内部表示随你换，测试只通过公开方法断言。"""
from __future__ import annotations
import itertools
import threading
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import Protocol

class ParkingFeeError(Exception):
    """本模块所有失败路径的根。"""

class UnknownTicketError(ParkingFeeError, LookupError):
    """票不存在，或已经结算过。"""

class DuplicatePlateError(ParkingFeeError, ValueError):
    """这个车牌已经有一张未结算的票。"""

class InvalidStayError(ParkingFeeError, ValueError):
    """出场时间早于入场时间。"""

@dataclass(frozen=True, slots=True, order=True)
class Money:
    """金额，单位是「分」。frozen 加 order，可以直接比较和 min()。"""
    cents: int

    def __add__(self, other: Money) -> Money:
        raise NotImplementedError

    def __sub__(self, other: Money) -> Money:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
ZERO = Money(0)

class VehicleType(Enum):
    """车型；与题库停车场的车辆尺寸是同一个概念，这里只关心价目表按它分行。"""
    MOTORCYCLE = 'motorcycle'
    CAR = 'car'
    LARGE = 'large'

@dataclass(frozen=True, slots=True)
class HourlyRate:
    """每小时单价：高峰（工作日）与非高峰（夜间和周末）。"""
    peak: Money
    off_peak: Money

@dataclass(frozen=True, slots=True)
class Tariff:
    """价目表：纯数据加两个纯查询，没有任何状态。"""
    rates: Mapping[VehicleType, HourlyRate]
    daily_cap: Mapping[VehicleType, Money]
    peak_start: time = time(8, 0)
    peak_end: time = time(20, 0)
    grace: timedelta = timedelta(minutes=15)

    def rate_at(self, vehicle: VehicleType, at: datetime) -> Money:
        """at 这一刻每小时收多少：工作日 [peak_start, peak_end) 是高峰，其余是非高峰。"""
        raise NotImplementedError

    def next_change(self, at: datetime) -> datetime:
        """严格晚于 at 的、单价或日历日可能变化的最近时刻：今天的高峰边界或下一个午夜。"""
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class DayCharge:
    """一个日历日的计费结果：raw 是封顶前，charged 是封顶后。"""
    day: date
    seconds: int
    raw: Money
    charged: Money

@dataclass(frozen=True, slots=True)
class Line:
    """收据上的一行调整：标签加带符号的金额。"""
    label: str
    amount: Money

@dataclass(frozen=True, slots=True)
class Ticket:
    """入场时发出的票。"""
    id: str
    plate: str
    vehicle: VehicleType
    entered_at: datetime

@dataclass(frozen=True, slots=True)
class Stay:
    """一次要结算的停留：调整规则只看它，不看系统时钟。"""
    ticket: Ticket
    exited_at: datetime
    member: bool = False
    lost: bool = False

@dataclass(frozen=True, slots=True)
class Receipt:
    """出场收据：total 恒等于「各日封顶后金额之和 + 各调整行之和」。"""
    ticket_id: str
    plate: str
    entered_at: datetime
    exited_at: datetime
    days: tuple[DayCharge, ...]
    adjustments: tuple[Line, ...]
    total: Money

class Adjustment(Protocol):
    """出场后的调整：拿到当前金额与这次停留，返回调整后的金额。无状态，按列表顺序应用。"""
    label: str

    def apply(self, amount: Money, stay: Stay) -> Money:
        ...

@dataclass(frozen=True, slots=True)
class MemberDiscount:
    """会员按百分比打折；折扣额向下取整到分，所以顾客不会多得。"""
    percent: int
    label: str = '会员折扣'

    def apply(self, amount: Money, stay: Stay) -> Money:
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class LostTicketPenalty:
    """丢票加收固定罚款，放在折扣之后，所以不会被打折。"""
    penalty: Money
    label: str = '丢票罚款'

    def apply(self, amount: Money, stay: Stay) -> Money:
        raise NotImplementedError

class FeeEngine:
    """纯计算：一次停留 → 收据。不持有票，不读时钟，所以可以随便并发调用。"""

    def __init__(self, tariff: Tariff, adjustments: Sequence[Adjustment]=()) -> None:
        raise NotImplementedError

    def day_charges(self, vehicle: VehicleType, entered: datetime, exited: datetime) -> tuple[DayCharge, ...]:
        """沿价格变化时刻切段，同一日历日内累加「单价×秒」，每日只取整一次，再套当日封顶。"""
        raise NotImplementedError

    def price(self, ticket: Ticket, exited_at: datetime, *, member: bool=False, lost: bool=False) -> Receipt:
        raise NotImplementedError

class FeeDesk:
    """入口发票、出口结算。开着的票只存一份，结算时在锁内取走。"""

    def __init__(self, engine: FeeEngine, clock: Callable[[], datetime]=datetime.now) -> None:
        raise NotImplementedError

    @property
    def open_count(self) -> int:
        raise NotImplementedError

    def enter(self, plate: str, vehicle: VehicleType) -> Ticket:
        raise NotImplementedError

    def quote(self, ticket_id: str, *, member: bool=False) -> Receipt:
        """现在出场要付多少；不结算，票仍然有效。"""
        raise NotImplementedError

    def exit(self, ticket_id: str, *, member: bool=False) -> Receipt:
        """凭票出场：先在锁内取走票（同一张票只有一个出口取得到），再在锁外计价。"""
        raise NotImplementedError

    def exit_lost(self, plate: str, *, member: bool=False) -> Receipt:
        """丢票出场：用车牌找到入场记录，照常计价再加罚款。"""
        raise NotImplementedError

    def _take(self, ticket_id: str) -> Ticket:
        raise NotImplementedError

    def _settle(self, ticket: Ticket, *, member: bool, lost: bool) -> Receipt:
        raise NotImplementedError

def default_tariff() -> Tariff:
    """示例价目表（推断的数字，不是 Amazon 报告里的）。"""
    raise NotImplementedError
