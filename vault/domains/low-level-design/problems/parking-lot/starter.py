"""停车场（Parking Lot）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/parking-lot -q
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import InitVar, dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum, IntEnum


class VehicleSize(IntEnum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3


SpotSize = VehicleSize


class ParkingLotError(Exception):
    """本设计里所有失败路径的公共基类。"""


class NoAvailableSpotError(ParkingLotError):
    """给定尺寸的车辆当前没有能停的空位。"""


class InvalidTicketError(ParkingLotError):
    """取车时给出的 Ticket 不存在，或已经被用掉过一次。"""


@dataclass(frozen=True, slots=True)
class Vehicle:
    plate: str
    size: VehicleSize


@dataclass(slots=True)
class ParkingSpot:
    id: str
    floor: int
    size: SpotSize
    vehicle: Vehicle | None = None

    @property
    def is_free(self) -> bool:
        raise NotImplementedError

    def fits(self, vehicle: Vehicle) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Ticket:
    id: str
    vehicle: Vehicle
    spot: ParkingSpot
    entry_time: datetime


Clock = Callable[[], datetime]
FreeByFloor = dict[int, list[ParkingSpot]]
AllocationStrategy = Callable[[Vehicle, FreeByFloor], "ParkingSpot | None"]


def nearest_first(vehicle: Vehicle, free_by_floor: FreeByFloor) -> ParkingSpot | None:
    """离入口最近优先：楼层号从小到大找，同一层里按车位 id 的先后顺序找。"""
    raise NotImplementedError


def spread_across_floors(vehicle: Vehicle, free_by_floor: FreeByFloor) -> ParkingSpot | None:
    """把车分摊到空闲车位最多的楼层。"""
    raise NotImplementedError


PricingStrategy = Callable[[VehicleSize, timedelta], Decimal]


def _ceil_hours(duration: timedelta) -> int:
    """不足一小时按一小时收——向上取整，且至少收一小时。"""
    raise NotImplementedError


def hourly_rate(rates: dict[VehicleSize, Decimal]) -> PricingStrategy:
    """按车型给一张每小时单价表。"""
    raise NotImplementedError


def flat_rate(fee: Decimal) -> PricingStrategy:
    """不论停多久、什么车型，进来就是这个价。"""
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class TieredRate:
    tiers: tuple[tuple[int, Decimal], ...]

    def __call__(self, size: VehicleSize, duration: timedelta) -> Decimal:
        raise NotImplementedError

    def breakdown(self, duration: timedelta) -> list[tuple[int, int, Decimal]]:
        """返回每一档 (封顶小时数, 这次在该档计费的小时数, 单价) 的明细。"""
        raise NotImplementedError


class SpotEventKind(Enum):
    OCCUPIED = "occupied"
    FREED = "freed"


@dataclass(frozen=True, slots=True)
class SpotEvent:
    """一次车位状态变化：哪个车位、在哪一层、变成了占用还是空闲。"""

    spot_id: str
    floor: int
    kind: SpotEventKind


SpotObserver = Callable[[SpotEvent], None]


@dataclass
class DisplayBoard:
    """按楼层展示当前空闲车位数；`lot` 只在构造时用一次，不作为字段保留。"""

    lot: InitVar["ParkingLot"]
    free_by_floor: dict[int, int] = field(default_factory=dict, init=False)

    def __post_init__(self, lot: "ParkingLot") -> None:
        raise NotImplementedError

    def _on_event(self, event: SpotEvent) -> None:
        raise NotImplementedError


class ParkingLot:
    """一整座停车场：持有全部车位，按策略分配和计费，发牌、结算。"""

    def __init__(self, spots: Iterable[ParkingSpot], allocate: AllocationStrategy,
                 price: PricingStrategy, clock: Clock) -> None:
        raise NotImplementedError

    def free_counts_by_floor(self) -> Mapping[int, int]:
        """按楼层给出当前空闲车位数的一份只读快照；不暴露车位列表本身。"""
        raise NotImplementedError

    def subscribe(self, observer: SpotObserver) -> None:
        """挂一个"车位状态变化"的订阅者。"""
        raise NotImplementedError

    def _notify(self, event: SpotEvent) -> None:
        raise NotImplementedError

    def park(self, vehicle: Vehicle) -> Ticket:
        """给车辆分配一个车位并开一张 Ticket；没有空位时抛 `NoAvailableSpotError`。"""
        raise NotImplementedError

    def unpark(self, ticket_id: str) -> Decimal:
        """凭 Ticket 取车，释放车位并返回应付金额；无效或用过的 Ticket 抛 `InvalidTicketError`。"""
        raise NotImplementedError
