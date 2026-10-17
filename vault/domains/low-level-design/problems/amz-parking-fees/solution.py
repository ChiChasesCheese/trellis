"""停车场计费（Parking Lot Fees）参考解：车位分配见题库的停车场，这里只做「出场时该收多少钱」。

设计五句话：
1. Tariff 是一张纯数据的价目表：按车型的小时单价（高峰／非高峰）、每日封顶、免费宽限时长；它还会回答
   「从此刻起价格下一次可能变化是什么时候」——午夜、高峰开始、高峰结束。
2. FeeEngine 把一次停留沿这些时刻切成若干段，每段单价固定；一天内的段先用整数「分钟×单价」累加，
   每个日历日只向上取整到分一次，再套当天的封顶。
3. Adjustment 是出场后的调整接缝（会员折扣、丢票罚款），按列表顺序依次应用，每一步都留一行明细。
4. FeeDesk 管票：入场发票、出场凭票结算；开着的票只存在一张表里，结算时在锁内一次性取走，所以同一张票
   不可能被两个出口各付一次。
5. 时间只从注入的时钟进来；金额只用整数「分」，没有浮点。
"""

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
        return Money(self.cents + other.cents)

    def __sub__(self, other: Money) -> Money:
        return Money(self.cents - other.cents)

    def __str__(self) -> str:
        sign = "-" if self.cents < 0 else ""
        return f"{sign}{abs(self.cents) // 100}.{abs(self.cents) % 100:02d}"


ZERO = Money(0)


class VehicleType(Enum):
    """车型；与题库停车场的车辆尺寸是同一个概念，这里只关心价目表按它分行。"""

    MOTORCYCLE = "motorcycle"
    CAR = "car"
    LARGE = "large"


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
        rate = self.rates[vehicle]
        is_peak = at.weekday() < 5 and self.peak_start <= at.time() < self.peak_end
        return rate.peak if is_peak else rate.off_peak

    def next_change(self, at: datetime) -> datetime:
        """严格晚于 at 的、单价或日历日可能变化的最近时刻：今天的高峰边界或下一个午夜。"""
        candidates = [datetime.combine(at.date() + timedelta(days=1), time.min)]
        for edge in (self.peak_start, self.peak_end):
            moment = datetime.combine(at.date(), edge)
            if moment > at:
                candidates.append(moment)
        return min(candidates)


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

    def apply(self, amount: Money, stay: Stay) -> Money: ...


@dataclass(frozen=True, slots=True)
class MemberDiscount:
    """会员按百分比打折；折扣额向下取整到分，所以顾客不会多得。"""

    percent: int
    label: str = "会员折扣"

    def apply(self, amount: Money, stay: Stay) -> Money:
        return amount - Money(amount.cents * self.percent // 100) if stay.member else amount


@dataclass(frozen=True, slots=True)
class LostTicketPenalty:
    """丢票加收固定罚款，放在折扣之后，所以不会被打折。"""

    penalty: Money
    label: str = "丢票罚款"

    def apply(self, amount: Money, stay: Stay) -> Money:
        return amount + self.penalty if stay.lost else amount


class FeeEngine:
    """纯计算：一次停留 → 收据。不持有票，不读时钟，所以可以随便并发调用。"""

    def __init__(self, tariff: Tariff, adjustments: Sequence[Adjustment] = ()) -> None:
        self._tariff = tariff
        self._adjustments = tuple(adjustments)

    def day_charges(self, vehicle: VehicleType, entered: datetime, exited: datetime) -> tuple[DayCharge, ...]:
        """沿价格变化时刻切段，同一日历日内累加「单价×秒」，每日只取整一次，再套当日封顶。"""
        if exited < entered:
            raise InvalidStayError(f"exit {exited} is before entry {entered}")
        if exited - entered <= self._tariff.grace:
            return ()
        units: dict[date, int] = {}  # 单位：分/小时 × 秒，除以 3600 才是分
        seconds: dict[date, int] = {}
        at = entered
        while at < exited:
            end = min(self._tariff.next_change(at), exited)
            span = int((end - at).total_seconds())
            rate = self._tariff.rate_at(vehicle, at).cents
            units[at.date()] = units.get(at.date(), 0) + rate * span
            seconds[at.date()] = seconds.get(at.date(), 0) + span
            at = end
        cap = self._tariff.daily_cap[vehicle]
        result = []
        for day in sorted(units):
            raw = Money(-(-units[day] // 3600))  # 向上取整到分，每日一次
            result.append(DayCharge(day, seconds[day], raw, min(raw, cap)))
        return tuple(result)

    def price(self, ticket: Ticket, exited_at: datetime, *, member: bool = False, lost: bool = False) -> Receipt:
        days = self.day_charges(ticket.vehicle, ticket.entered_at, exited_at)
        total = sum((d.charged for d in days), ZERO)
        stay = Stay(ticket, exited_at, member, lost)
        lines = []
        for adjustment in self._adjustments:
            after = adjustment.apply(total, stay)
            if after != total:
                lines.append(Line(adjustment.label, after - total))
            total = after
        return Receipt(ticket.id, ticket.plate, ticket.entered_at, exited_at, days, tuple(lines), total)


class FeeDesk:
    """入口发票、出口结算。开着的票只存一份，结算时在锁内取走。"""

    def __init__(self, engine: FeeEngine, clock: Callable[[], datetime] = datetime.now) -> None:
        self._engine = engine
        self._clock = clock
        self._lock = threading.Lock()
        self._open: dict[str, Ticket] = {}
        self._by_plate: dict[str, str] = {}
        self._ids = (f"T{n}" for n in itertools.count(1))

    @property
    def open_count(self) -> int:
        with self._lock:
            return len(self._open)

    def enter(self, plate: str, vehicle: VehicleType) -> Ticket:
        with self._lock:
            if plate in self._by_plate:
                raise DuplicatePlateError(plate)
            ticket = Ticket(next(self._ids), plate, vehicle, self._clock())
            self._open[ticket.id] = ticket
            self._by_plate[plate] = ticket.id
            return ticket

    def quote(self, ticket_id: str, *, member: bool = False) -> Receipt:
        """现在出场要付多少；不结算，票仍然有效。"""
        with self._lock:
            ticket = self._open.get(ticket_id)
        if ticket is None:
            raise UnknownTicketError(ticket_id)
        return self._engine.price(ticket, self._clock(), member=member)

    def exit(self, ticket_id: str, *, member: bool = False) -> Receipt:
        """凭票出场：先在锁内取走票（同一张票只有一个出口取得到），再在锁外计价。"""
        with self._lock:
            ticket = self._take(ticket_id)
        return self._settle(ticket, member=member, lost=False)

    def exit_lost(self, plate: str, *, member: bool = False) -> Receipt:
        """丢票出场：用车牌找到入场记录，照常计价再加罚款。"""
        with self._lock:
            ticket_id = self._by_plate.get(plate)
            if ticket_id is None:
                raise UnknownTicketError(plate)
            ticket = self._take(ticket_id)
        return self._settle(ticket, member=member, lost=True)

    def _take(self, ticket_id: str) -> Ticket:
        ticket = self._open.pop(ticket_id, None)
        if ticket is None:
            raise UnknownTicketError(ticket_id)
        del self._by_plate[ticket.plate]
        return ticket

    def _settle(self, ticket: Ticket, *, member: bool, lost: bool) -> Receipt:
        exited_at = self._clock()
        try:
            return self._engine.price(ticket, exited_at, member=member, lost=lost)
        except InvalidStayError:
            with self._lock:  # 时钟倒退：把票放回去，别让车主白白丢票
                self._open[ticket.id] = ticket
                self._by_plate[ticket.plate] = ticket.id
            raise


def default_tariff() -> Tariff:
    """示例价目表（演示用的数字，面试时应先问清费率）。"""
    return Tariff(
        rates={
            VehicleType.MOTORCYCLE: HourlyRate(Money(200), Money(100)),
            VehicleType.CAR: HourlyRate(Money(400), Money(200)),
            VehicleType.LARGE: HourlyRate(Money(600), Money(300)),
        },
        daily_cap={
            VehicleType.MOTORCYCLE: Money(1000),
            VehicleType.CAR: Money(2000),
            VehicleType.LARGE: Money(3000),
        },
    )


if __name__ == "__main__":
    now = [datetime(2026, 10, 16, 19, 30)]
    desk = FeeDesk(FeeEngine(default_tariff(), [MemberDiscount(10), LostTicketPenalty(Money(1500))]), lambda: now[0])
    t = desk.enter("京A12345", VehicleType.CAR)
    now[0] = datetime(2026, 10, 17, 8, 30)
    r = desk.exit(t.id)
    print(r.total, [(str(d.day), str(d.charged)) for d in r.days])
