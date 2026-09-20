"""租车系统（Car Rental）——练习骨架。公开 API 与 `solution.py` 完全一致，方法体留空。

做法：把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录跑
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/car-rental -q`。
内部表示随你换，但公开的类名、方法名、签名和只读属性（`leg_count`、`scheduled_leg_count`、
`base_branch`）要保留——测试只看这些。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class RentalError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownEntityError(RentalError):
    """预约号、车牌或门店不存在。"""


class InvalidPeriodError(RentalError):
    """租期不合法：结束时刻不晚于开始时刻。"""


class NoVehicleAvailableError(RentalError):
    """这个门店、这个时段、这个车型，没有一辆车排得下。"""


class InvalidTransitionError(RentalError):
    """预约当前状态不允许这次状态转移。"""


@dataclass(frozen=True, slots=True)
class RentalPeriod:
    """一段租期，**半开**：`[start, end)`。粒度是小时。"""

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        """不合法的区间要在这里就抛 `InvalidPeriodError`。"""
        raise NotImplementedError

    @property
    def hours(self) -> int:
        """计费小时数：不足一小时按一小时算。"""
        raise NotImplementedError


class VehicleCategory(Enum):
    """车型档次。"""

    ECONOMY = "economy"
    COMPACT = "compact"
    SUV = "suv"
    LUXURY = "luxury"


@dataclass(frozen=True, slots=True)
class Vehicle:
    """一辆实体车：车牌、车型、基地门店。"""

    plate: str
    category: VehicleCategory
    home_branch: str
    model: str = ""


@dataclass(frozen=True, slots=True)
class ScheduleLeg:
    """车辆时间轴上的一段：`rental=True` 是租约，`rental=False` 是维修封锁。"""

    ref: str
    period: RentalPeriod
    origin: str
    destination: str
    rental: bool = True


class VehicleSchedule:
    """一辆车按开始时间排好的行程链，以及它唯一的一条不变量。"""

    def __init__(self, vehicle: Vehicle, turnaround: timedelta = timedelta(hours=1)) -> None:
        raise NotImplementedError

    @property
    def base_branch(self) -> str:
        """时间轴起点上车停在哪。"""
        raise NotImplementedError

    @property
    def leg_count(self) -> int:
        """时间轴上当前有几段。"""
        raise NotImplementedError

    def legs(self) -> tuple[ScheduleLeg, ...]:
        """时间轴的一份不可变快照。"""
        raise NotImplementedError

    def location_at(self, moment: datetime) -> str:
        """某一时刻车停在哪个门店。"""
        raise NotImplementedError

    def accepts(self, leg: ScheduleLeg) -> bool:
        """把这一段插进来之后整条链是否仍然自洽。"""
        raise NotImplementedError

    def add(self, leg: ScheduleLeg) -> None:
        """排进一段行程；排不下就抛 `NoVehicleAvailableError`。"""
        raise NotImplementedError

    def remove(self, ref: str) -> bool:
        """取消一段行程，返回是否真的删掉了。"""
        raise NotImplementedError

    def force(self, forced: ScheduleLeg) -> tuple[str, ...]:
        """强行写入一段并修复时间轴，返回被挤掉的预约号。"""
        raise NotImplementedError

    def purge_before(self, cutoff: datetime) -> int:
        """丢掉已经结束的历史行程，返回丢掉的段数。"""
        raise NotImplementedError


class Fleet:
    """全部车辆与它们的时间轴；"找车 + 占车"必须原子。"""

    def __init__(self, vehicles: Iterable[Vehicle], turnaround: timedelta = timedelta(hours=1)) -> None:
        raise NotImplementedError

    @property
    def scheduled_leg_count(self) -> int:
        """全车队时间轴上的总段数。"""
        raise NotImplementedError

    def vehicle(self, plate: str) -> Vehicle:
        """按车牌取车辆。"""
        raise NotImplementedError

    def location_of(self, plate: str, moment: datetime) -> str:
        """某一时刻这辆车停在哪个门店。"""
        raise NotImplementedError

    def available_plates(self, category: VehicleCategory, branch: str,
                         period: RentalPeriod, destination: str) -> tuple[str, ...]:
        """能接这单的全部车牌，按车牌排序。"""
        raise NotImplementedError

    def claim(self, category: VehicleCategory, branch: str, period: RentalPeriod,
              destination: str, ref: str, exclude: str = "") -> Vehicle:
        """原子地挑一辆能接这单的车并占上。"""
        raise NotImplementedError

    def release(self, plate: str, ref: str) -> bool:
        """放掉一段行程。"""
        raise NotImplementedError

    def settle(self, plate: str, ref: str, end: datetime, destination: str) -> tuple[str, ...]:
        """把一段租约改写成实际发生的样子，返回被挤掉的预约号。"""
        raise NotImplementedError

    def block(self, plate: str, period: RentalPeriod, branch: str, ref: str) -> tuple[str, ...]:
        """事故或保养封车，返回被挤掉的预约号。"""
        raise NotImplementedError

    def purge_before(self, cutoff: datetime) -> int:
        """清掉全车队的历史行程，返回清掉的段数。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Charge:
    """账单上的一行：科目 + 金额（分，可以为负）。"""

    code: str
    amount: int


@dataclass(frozen=True, slots=True)
class Quote:
    """一次报价：逐行明细 + 合计。"""

    lines: tuple[Charge, ...]

    @property
    def total(self) -> int:
        """合计（分）。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class RentalRequest:
    """报价与排期需要的全部事实。"""

    category: VehicleCategory
    period: RentalPeriod
    pickup_branch: str
    return_branch: str
    tier: str = "none"
    extras: tuple[str, ...] = ()

    @property
    def one_way(self) -> bool:
        """是不是异地还车。"""
        raise NotImplementedError


PriceComponent = Callable[["RentalRequest", int], "Charge | None"]
Clock = Callable[[], datetime]


def category_rate(rates: Mapping[VehicleCategory, int], daily_cap_hours: int = 20) -> PriceComponent:
    """按小时计价，每满 24 小时最多收 `daily_cap_hours` 小时。"""
    raise NotImplementedError


def one_way_fee(amount: int) -> PriceComponent:
    """异地还车附加费。"""
    raise NotImplementedError


def extras_fee(per_hour: Mapping[str, int]) -> PriceComponent:
    """加购项按小时计。"""
    raise NotImplementedError


def loyalty_discount(percent: Mapping[str, int]) -> PriceComponent:
    """按此前小计打折的会员折扣，排在最后。"""
    raise NotImplementedError


def price(components: Sequence[PriceComponent], request: RentalRequest) -> Quote:
    """按顺序跑组件，把非零的行拼成报价。"""
    raise NotImplementedError


class RentalStatus(Enum):
    """预约生命周期的五个状态。"""

    RESERVED = "reserved"
    PICKED_UP = "picked_up"
    RETURNED = "returned"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


ALLOWED_TRANSITIONS: Mapping[RentalStatus, frozenset[RentalStatus]] = {
    RentalStatus.RESERVED: frozenset({RentalStatus.PICKED_UP, RentalStatus.CANCELLED,
                                      RentalStatus.NO_SHOW}),
    RentalStatus.PICKED_UP: frozenset({RentalStatus.RETURNED}),
    RentalStatus.RETURNED: frozenset(),
    RentalStatus.CANCELLED: frozenset(),
    RentalStatus.NO_SHOW: frozenset(),
}
"""合法转移写成一张数据表。"""


@dataclass(slots=True)
class Reservation:
    """一笔预约及其生命周期。`plate` 为 `None` 表示被挤掉后暂时没车。"""

    id: str
    customer: str
    request: RentalRequest
    quote: Quote
    plate: str | None = None
    status: RentalStatus = RentalStatus.RESERVED
    picked_up_at: datetime | None = None
    returned_at: datetime | None = None
    returned_branch: str | None = None
    extra_charges: tuple[Charge, ...] = ()

    @property
    def total(self) -> int:
        """含还车后追加科目的最终金额（分）。"""
        raise NotImplementedError

    def transition_to(self, new_status: RentalStatus) -> None:
        """按转移表改状态；不合法就抛 `InvalidTransitionError`。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ReturnOutcome:
    """一次还车发生了什么。"""

    reservation_id: str
    late_hours: int
    charges: tuple[Charge, ...]
    reassigned: tuple[str, ...]
    unassigned: tuple[str, ...]


class RentalService:
    """租车服务门面。"""

    def __init__(self, fleet: Fleet, clock: Clock, components: Sequence[PriceComponent], *,
                 late_fee_per_hour: int = 8000, wrong_branch_fee: int = 30000,
                 no_show_fee: int = 12000, grace: timedelta = timedelta(hours=2),
                 repair: timedelta = timedelta(hours=48)) -> None:
        raise NotImplementedError

    def quote(self, request: RentalRequest) -> Quote:
        """报价。"""
        raise NotImplementedError

    def search(self, branches: Iterable[str], category: VehicleCategory, period: RentalPeriod,
               return_branch: str | None = None) -> tuple[str, ...]:
        """这些门店里哪些能提供这个车型、这个时段的车。"""
        raise NotImplementedError

    def reserve(self, customer: str, request: RentalRequest) -> Reservation:
        """下单。"""
        raise NotImplementedError

    def reservation(self, reservation_id: str) -> Reservation:
        """按预约号取预约。"""
        raise NotImplementedError

    def cancel(self, reservation_id: str) -> Reservation:
        """取消。"""
        raise NotImplementedError

    def mark_no_show(self, reservation_id: str) -> Reservation:
        """爽约。"""
        raise NotImplementedError

    def pick_up(self, reservation_id: str) -> Vehicle:
        """取车。"""
        raise NotImplementedError

    def return_vehicle(self, reservation_id: str, *, branch: str | None = None,
                       damaged: bool = False) -> ReturnOutcome:
        """还车。"""
        raise NotImplementedError
