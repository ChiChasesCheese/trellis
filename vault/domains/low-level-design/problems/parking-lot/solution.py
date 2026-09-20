"""停车场（Parking Lot）——多楼层、多车型车位分配与释放的参考实现。

核心思路：车辆和车位共用同一把可比较的"尺寸"标尺（`IntEnum`），谁能停谁只看数值大小，
不用一串 `if vehicle_type == ...` 的判断。车位分配和计费都是"会变的算法"，分配策略没有
状态、每次调用只需要当前的空闲表，因此就是普通函数（`AllocationStrategy`）；计费策略里
按时长收费的两种也是闭包函数，唯独阶梯计价要在"算一次"之外再暴露"这次落在哪一档"，才
值得写成一个类（`TieredRate`）。`ParkingLot` 本身不做分配和计费的决定，只负责在一把锁下
原子地"选一个空闲车位、开一张真实存在的 Ticket"——这一步就是多个入口并发时唯一需要互斥
的地方。`ParkingLot` 从不把内部的车位列表交给外面：外部只能拿到一份空闲数快照，或者收到
"哪个车位变空/变占用了"这一件事本身，`DisplayBoard` 就是靠订阅后者维护自己的计数，不用
持有停车场的引用、也不用回头重新扫描车位。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Callable, Iterable, Mapping
from dataclasses import InitVar, dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum, IntEnum
from types import MappingProxyType


# --------------------------------------------------------------------------
# 尺寸：车辆和车位共用同一把尺子，用整数等级比较"装得下"。


class VehicleSize(IntEnum):
    """车辆／车位的尺寸等级，数值越大占地越大：一个大车位可以停小车，反过来不行。

    新增一种车型（比如 XL_TRUCK）只需要在这里加一个成员——分配和计费用到的都是
    数值比较，不需要改 `ParkingSpot.fits`、任何一个分配策略或任何一个计价策略。
    """

    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3


SpotSize = VehicleSize  # 车位用同一把尺子标注它能停的最大车型


class ParkingLotError(Exception):
    """本设计里所有失败路径的公共基类，方便调用方一次性捕获。"""


class NoAvailableSpotError(ParkingLotError):
    """给定尺寸的车辆当前没有能停的空位。"""


class InvalidTicketError(ParkingLotError):
    """取车时给出的 Ticket 不存在，或已经被用掉过一次。"""


@dataclass(frozen=True, slots=True)
class Vehicle:
    """一次入场的车辆：车牌是它的身份，尺寸决定能停进哪些车位。"""

    plate: str
    size: VehicleSize


@dataclass(slots=True)
class ParkingSpot:
    """一个车位：知道自己在哪一层、能停多大的车、当前停了谁。

    这是本设计里唯一持有"占用状态"的地方——`ParkingLot` 不额外维护一份"谁占了哪个位"
    的账本，靠遍历车位本身的 `vehicle` 字段就知道空闲表，天然不会和车位状态本身对不上。
    """

    id: str
    floor: int
    size: SpotSize
    vehicle: Vehicle | None = None

    @property
    def is_free(self) -> bool:
        return self.vehicle is None

    def fits(self, vehicle: Vehicle) -> bool:
        """车位能停下这辆车，当且仅当车位尺寸不小于车辆尺寸。"""
        return vehicle.size <= self.size


@dataclass(frozen=True, slots=True)
class Ticket:
    """一张停车凭证：入场时生成一次，出场时凭它结算并作废，不可重复使用。"""

    id: str
    vehicle: Vehicle
    spot: ParkingSpot
    entry_time: datetime


Clock = Callable[[], datetime]
FreeByFloor = dict[int, list[ParkingSpot]]


# --------------------------------------------------------------------------
# 车位分配策略：给定车辆和按楼层分组的空闲车位，选哪一个。
#
# 两种分配规则都是"输入什么就纯计算一次输出"，调用之间不需要记住任何东西，
# 因此没有写成一个 `AllocationStrategy` 抽象基类再各配一个实现类——那只是给一次性的
# 计算多包一层从不会被复用的壳。函数签名本身就是接口。


AllocationStrategy = Callable[[Vehicle, FreeByFloor], "ParkingSpot | None"]


def nearest_first(vehicle: Vehicle, free_by_floor: FreeByFloor) -> ParkingSpot | None:
    """离入口最近优先：楼层号从小到大找，同一层里按车位 id 的先后顺序找。"""
    for floor in sorted(free_by_floor):
        for spot in free_by_floor[floor]:
            if spot.fits(vehicle):
                return spot
    return None


def spread_across_floors(vehicle: Vehicle, free_by_floor: FreeByFloor) -> ParkingSpot | None:
    """把车分摊到空闲车位最多的楼层，避免某一层被挤爆、别的楼层却空着没人上去找。"""
    candidates = [(floor, spots) for floor, spots in free_by_floor.items()
                  if any(spot.fits(vehicle) for spot in spots)]
    if not candidates:
        return None
    _, spots = max(candidates, key=lambda item: len(item[1]))
    return next(spot for spot in spots if spot.fits(vehicle))


# --------------------------------------------------------------------------
# 计费策略：按车辆尺寸和停留时长算钱。金额用 Decimal，避免浮点误差。


PricingStrategy = Callable[[VehicleSize, timedelta], Decimal]


def _ceil_hours(duration: timedelta) -> int:
    """不足一小时按一小时收——向上取整，且至少收一小时。"""
    seconds = max(int(duration.total_seconds()), 0)
    return max(-(-seconds // 3600), 1)


def hourly_rate(rates: dict[VehicleSize, Decimal]) -> PricingStrategy:
    """按车型给一张每小时单价表，最常见的计费方式。"""

    def price(size: VehicleSize, duration: timedelta) -> Decimal:
        return rates[size] * _ceil_hours(duration)

    return price


def flat_rate(fee: Decimal) -> PricingStrategy:
    """不论停多久、什么车型，进来就是这个价——商场、景区常见的一口价。"""

    def price(size: VehicleSize, duration: timedelta) -> Decimal:
        return fee

    return price


@dataclass(frozen=True, slots=True)
class TieredRate:
    """阶梯计价：前几个小时一个单价，超过之后换更高（或更低）的单价。

    这里没有用闭包，是因为阶梯计价除了"算一次"，收银台还想知道"这次落在哪一档、
    每一档各算了多少钱"（用于小票、客诉核对）——多暴露一个 `breakdown` 方法，闭包
    做不到，普通函数也做不到，这才值得把 `tiers` 包成一个类。
    """

    tiers: tuple[tuple[int, Decimal], ...]  # (这一档封顶到第几小时, 该档每小时单价)，按小时升序

    def __call__(self, size: VehicleSize, duration: timedelta) -> Decimal:
        return sum((billed * rate for _, billed, rate in self.breakdown(duration)), Decimal("0"))

    def breakdown(self, duration: timedelta) -> list[tuple[int, int, Decimal]]:
        """返回每一档 (封顶小时数, 这次在该档计费的小时数, 单价) 的明细，最后一档之后按最后一档单价续费。"""
        hours = _ceil_hours(duration)
        out: list[tuple[int, int, Decimal]] = []
        prev = 0
        for upto, rate in self.tiers:
            billed = min(hours, upto) - prev
            if billed > 0:
                out.append((upto, billed, rate))
            prev = upto
            if hours <= upto:
                return out
        last_rate = self.tiers[-1][1]
        out.append((hours, hours - prev, last_rate))
        return out


# --------------------------------------------------------------------------
# 车位事件：车位状态变化时，`ParkingLot` 通知订阅者的不是"车位对象"或"内部字典"，
# 而是一份不可变的、自己说清楚发生了什么的小记录——订阅者不需要、也不能反过来
# 触达停车场的存储结构。


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
    """按楼层展示当前空闲车位数，供入口处的电子屏读取。

    构造时向 `ParkingLot` 要一份"当前空闲数"的快照来初始化，之后只靠订阅的事件
    做加减法维护自己的计数——不保留对 `ParkingLot` 的引用，收到通知后也不会回头
    重新扫描车位；`lot` 只在构造这一刻用一次，因此写成 `InitVar` 而不是字段。
    """

    lot: InitVar["ParkingLot"]
    free_by_floor: dict[int, int] = field(default_factory=dict, init=False)

    def __post_init__(self, lot: "ParkingLot") -> None:
        self.free_by_floor.update(lot.free_counts_by_floor())
        lot.subscribe(self._on_event)

    def _on_event(self, event: SpotEvent) -> None:
        delta = -1 if event.kind is SpotEventKind.OCCUPIED else 1
        self.free_by_floor[event.floor] = self.free_by_floor.get(event.floor, 0) + delta


# --------------------------------------------------------------------------
# ParkingLot：整座停车场。不做成 Singleton——它就是一个普通对象，测试要能造互不
# 干扰的多个实例，多租户场景也可能真的要管理好几座车库。真需要"进程里只有一份"
# 时，由调用方在组合根（composition root）里只 new 一次、往下传，而不是把构造过程
# 锁死在类里：Singleton 把"这是唯一实例"这件事藏进 `__new__`，调用方从签名上完全
# 看不出来，测试之间还会共享一份没法换、没法重置的隐藏状态。


class ParkingLot:
    """一整座停车场：持有全部车位，按策略分配和计费，发牌、结算。

    并发由一把锁保护"挑一个空位并标记占用"这一步的原子性——这一步是"读空闲表、选
    一个、写回占用状态"好几条 Python 字节码，GIL 只保证单条字节码不被切走，不保证
    这一串操作不被打断，中间随时可能切到另一个线程；没有这把锁，两个并发的调用方
    可能同时把同一个空位判断为空闲，都把车停进去。对外只暴露 `free_counts_by_floor`
    这一份只读快照和基于事件的 `subscribe`，从不把内部的车位列表或字典交出去——拿到
    快照或事件的调用方，改不了停车场的真实状态。
    """

    def __init__(self, spots: Iterable[ParkingSpot], allocate: AllocationStrategy,
                 price: PricingStrategy, clock: Clock) -> None:
        self._spots_by_floor: FreeByFloor = {}
        for spot in spots:
            self._spots_by_floor.setdefault(spot.floor, []).append(spot)
        self._allocate = allocate
        self._price = price
        self._clock = clock
        self._lock = threading.Lock()
        self._tickets: dict[str, Ticket] = {}
        self._observers: list[SpotObserver] = []
        self._ticket_ids = (f"T{n}" for n in itertools.count(1))

    def free_counts_by_floor(self) -> Mapping[int, int]:
        """按楼层给出当前空闲车位数的一份只读快照；不暴露车位列表本身。"""
        with self._lock:
            counts = {floor: sum(1 for spot in spots if spot.is_free)
                      for floor, spots in self._spots_by_floor.items()}
        return MappingProxyType(counts)

    def subscribe(self, observer: SpotObserver) -> None:
        """挂一个"车位状态变化"的订阅者；`DisplayBoard` 就是这么接进来的。"""
        self._observers.append(observer)

    def _notify(self, event: SpotEvent) -> None:
        for observer in self._observers:
            observer(event)

    def park(self, vehicle: Vehicle) -> Ticket:
        """给车辆分配一个车位并开一张 Ticket；没有空位时抛 `NoAvailableSpotError`。"""
        with self._lock:
            free_by_floor = {floor: [spot for spot in spots if spot.is_free]
                              for floor, spots in self._spots_by_floor.items()}
            spot = self._allocate(vehicle, free_by_floor)
            if spot is None:
                raise NoAvailableSpotError(f"no free spot fits {vehicle.size.name}")
            spot.vehicle = vehicle
            ticket = Ticket(id=next(self._ticket_ids), vehicle=vehicle, spot=spot,
                             entry_time=self._clock())
            self._tickets[ticket.id] = ticket
        self._notify(SpotEvent(spot_id=spot.id, floor=spot.floor, kind=SpotEventKind.OCCUPIED))
        return ticket

    def unpark(self, ticket_id: str) -> Decimal:
        """凭 Ticket 取车，释放车位并返回应付金额；无效或用过的 Ticket 抛 `InvalidTicketError`。"""
        with self._lock:
            ticket = self._tickets.pop(ticket_id, None)
            if ticket is None:
                raise InvalidTicketError(f"unknown or already-used ticket {ticket_id!r}")
            ticket.spot.vehicle = None
            duration = self._clock() - ticket.entry_time
            fee = self._price(ticket.vehicle.size, duration)
        self._notify(SpotEvent(spot_id=ticket.spot.id, floor=ticket.spot.floor, kind=SpotEventKind.FREED))
        return fee


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)
    spots = [ParkingSpot(id=f"1-{i}", floor=1, size=VehicleSize.COMPACT) for i in range(3)]
    lot = ParkingLot(spots, allocate=nearest_first,
                      price=hourly_rate({VehicleSize.MOTORCYCLE: Decimal("2"),
                                          VehicleSize.COMPACT: Decimal("5"),
                                          VehicleSize.LARGE: Decimal("8")}),
                      clock=lambda: now)
    board = DisplayBoard(lot)
    # 没有 EntryGate/ExitGate 类：一个"闸机"在这里就是调用 park/unpark 的调用方本身，
    # 见题解「核心对象与职责」——多个闸机并发，就是多个线程各自直接调用这两个方法。
    ticket = lot.park(Vehicle(plate="京A12345", size=VehicleSize.COMPACT))
    print(f"parked at {ticket.spot.id}, free on floor 1: {board.free_by_floor[1]}")
    now = now + timedelta(hours=3)
    print(f"fee: {lot.unpark(ticket.id)}")
