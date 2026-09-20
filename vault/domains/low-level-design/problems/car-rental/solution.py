"""租车系统（Car Rental）——按门店与时段的车辆可用性、异地还车、取还车状态机与计费的参考实现。

核心思路：库存的单位不是"门店里停着的一辆车"，而是**一辆具体的车在时间轴上的一段行程**。
异地还车（one-way）把"这个门店有没有车"变成一个与时间有关的问题：车此刻在 A，不代表下周还在 A。
所以每辆车挂一条 `VehicleSchedule`，全题只有一条不变量——行程按开始时间排好后，每一段的取车门店
必须等于上一段的还车门店，且租约之间留够周转时间。可用性查询、异地还车、迟还挤占、事故封车，
都是这条不变量的不同用法。计费是一串注入的纯函数，加保险或会员折扣不碰可用性一行。
"""

from __future__ import annotations

import itertools
import math
import threading
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from enum import Enum

# --------------------------------------------------------------------------
# 失败路径。

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


# --------------------------------------------------------------------------
# 租期：小时粒度的半开区间。

@dataclass(frozen=True, slots=True)
class RentalPeriod:
    """一段租期，**半开**：`[start, end)`。粒度是小时，跨度可以是几小时到几个月。"""

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise InvalidPeriodError(f"end {self.end} must be after start {self.start}")

    @property
    def hours(self) -> int:
        """计费小时数：不足一小时按一小时算。租车行业按"开始计费的那一小时"收钱。"""
        return max(1, math.ceil((self.end - self.start).total_seconds() / 3600))


# --------------------------------------------------------------------------
# 门店、车型、车辆。

class VehicleCategory(Enum):
    """车型档次。客人订的是车型，不是某一辆车——和酒店订房型是同一条业务事实。"""

    ECONOMY = "economy"
    COMPACT = "compact"
    SUV = "suv"
    LUXURY = "luxury"


@dataclass(frozen=True, slots=True)
class Vehicle:
    """一辆实体车：车牌、车型、基地门店。不带"现在被谁租着"的状态。"""

    plate: str
    category: VehicleCategory
    home_branch: str
    model: str = ""


@dataclass(frozen=True, slots=True)
class ScheduleLeg:
    """车辆时间轴上的一段：`rental=True` 是一次租约，`rental=False` 是一次维修封锁。

    它同时记了 `origin` 和 `destination`：异地还车之下，一段行程不只占用时间，还**搬动了车**。
    """

    ref: str
    period: RentalPeriod
    origin: str
    destination: str
    rental: bool = True


# --------------------------------------------------------------------------
# VehicleSchedule：这道题的核心——一辆车的时间轴与它唯一的一条不变量。

class VehicleSchedule:
    """一辆车按开始时间排好的行程链。

    不变量（全题唯一的那条）：每一段的取车门店等于上一段的还车门店（第一段等于基地门店），
    且租约段与上一段之间留够周转时间（清洁、加油）。维修段紧接还车那一刻开始，不需要周转。

    可用性因此不是"这辆车这段时间空不空"，而是"把这一段插进去之后整条链还自洽不自洽"——
    一辆 7 号从 A 开到 B 的车，10 号在 A 明明没有任何重叠，却根本不在 A。
    """

    def __init__(self, vehicle: Vehicle, turnaround: timedelta = timedelta(hours=1)) -> None:
        self.vehicle = vehicle
        self._base = vehicle.home_branch
        self._turnaround = turnaround
        self._legs: list[ScheduleLeg] = []

    @property
    def base_branch(self) -> str:
        """时间轴起点上车停在哪。它会随着历史行程被清理而前移。"""
        return self._base

    @property
    def leg_count(self) -> int:
        """时间轴上当前有几段——用来验证"取消即删、过期即清"真的生效。"""
        return len(self._legs)

    def legs(self) -> tuple[ScheduleLeg, ...]:
        """时间轴的一份不可变快照，绝不交出内部列表。"""
        return tuple(self._legs)

    @staticmethod
    def _ordered(legs: Iterable[ScheduleLeg]) -> list[ScheduleLeg]:
        return sorted(legs, key=lambda leg: (leg.period.start, leg.period.end))

    def _consistent(self, legs: Sequence[ScheduleLeg]) -> bool:
        """一条按时间排好的行程链是否自洽——重叠、周转缓冲、门店接续三件事写在一个循环里。"""
        where: str = self._base
        previous_end: datetime | None = None
        for leg in legs:
            if leg.origin != where:
                return False
            if previous_end is not None:
                gap = self._turnaround if leg.rental else timedelta(0)
                if leg.period.start < previous_end + gap:
                    return False
            where, previous_end = leg.destination, leg.period.end
        return True

    def location_at(self, moment: datetime) -> str:
        """某一时刻车停在哪：最后一段在此之前结束的行程的还车门店，没有就是基地门店。

        位置是**算出来的**，不是存下来的。存一个 `current_branch` 字段就等于给同一件事留了
        两个真相，而未来的预约根本无法在"当前位置"上表达。
        """
        where = self._base
        for leg in self._legs:
            if leg.period.end <= moment:
                where = leg.destination
            else:
                break
        return where

    def accepts(self, leg: ScheduleLeg) -> bool:
        """把这一段插进来之后整条链是否仍然自洽。"""
        return self._consistent(self._ordered([*self._legs, leg]))

    def add(self, leg: ScheduleLeg) -> None:
        """排进一段行程；排不下就抛 `NoVehicleAvailableError`。"""
        if not self.accepts(leg):
            raise NoVehicleAvailableError(f"{self.vehicle.plate} cannot serve {leg.ref}")
        self._legs = self._ordered([*self._legs, leg])

    def remove(self, ref: str) -> bool:
        """取消一段行程，返回是否真的删掉了。删的是整段，不留空壳。"""
        kept = [leg for leg in self._legs if leg.ref != ref]
        changed = len(kept) != len(self._legs)
        self._legs = kept
        return changed

    def force(self, forced: ScheduleLeg) -> tuple[str, ...]:
        """强行写入一段（迟还的延长、乱还的改点、事故封车），再把时间轴修回自洽。

        固定不动的是：已经开始的行程、维修段、以及这一段本身——既成事实不能被"排不下"推翻。
        可以被挤掉的只有尚未开始的租约。异地还车之下挤占会**连锁**：丢掉中间一段，后面一段的
        取车门店就对不上，于是也留不住。返回被挤掉的预约号，由上层去改派。
        """
        rest = [leg for leg in self._legs if leg.ref != forced.ref]
        pinned = {leg.ref for leg in rest
                  if not leg.rental or leg.period.start < forced.period.start}
        self._legs = self._ordered([leg for leg in rest if leg.ref in pinned] + [forced])
        displaced: list[str] = []
        for leg in self._ordered(leg for leg in rest if leg.ref not in pinned):
            if self.accepts(leg):
                self._legs = self._ordered([*self._legs, leg])
            else:
                displaced.append(leg.ref)
        return tuple(displaced)

    def purge_before(self, cutoff: datetime) -> int:
        """丢掉 `cutoff` 之前已经结束的行程，返回丢掉的段数。

        关键在第一行：丢之前先把"车最后停在哪"吸收进 `_base`。位置是沿着链算出来的，删掉
        最后一段历史却不前移起点，这辆车就会凭空瞬移回基地——**容器可以缩，但不能连它承载的
        状态一起丢**。
        """
        stale = self._ordered(leg for leg in self._legs if leg.period.end <= cutoff)
        if not stale:
            return 0
        self._base = stale[-1].destination
        self._legs = [leg for leg in self._legs if leg.period.end > cutoff]
        return len(stale)


# --------------------------------------------------------------------------
# Fleet：车队。"挑一辆能接这单的车 + 占上"这一步必须是一次原子操作。

class Fleet:
    """全部车辆与它们的时间轴。锁守的是"找车 + 占车"不可分割这一条。

    不变量：任一时刻每辆车的时间轴自洽；释放一段就整段删掉，不留空壳。
    """

    def __init__(self, vehicles: Iterable[Vehicle], turnaround: timedelta = timedelta(hours=1)) -> None:
        self._schedules = {v.plate: VehicleSchedule(v, turnaround) for v in vehicles}
        self._lock = threading.Lock()

    @property
    def scheduled_leg_count(self) -> int:
        """全车队时间轴上的总段数——只读计数，不把内部结构交出去。"""
        with self._lock:
            return sum(schedule.leg_count for schedule in self._schedules.values())

    def _schedule(self, plate: str) -> VehicleSchedule:
        schedule = self._schedules.get(plate)
        if schedule is None:
            raise UnknownEntityError(f"unknown plate {plate!r}")
        return schedule

    def vehicle(self, plate: str) -> Vehicle:
        """按车牌取车辆。"""
        return self._schedule(plate).vehicle

    def location_of(self, plate: str, moment: datetime) -> str:
        """某一时刻这辆车停在哪个门店。"""
        with self._lock:
            return self._schedule(plate).location_at(moment)

    def available_plates(self, category: VehicleCategory, branch: str,
                         period: RentalPeriod, destination: str) -> tuple[str, ...]:
        """这个车型、这个门店、这个时段能接单的全部车牌，按车牌排序。"""
        with self._lock:
            return tuple(sorted(
                plate for plate, schedule in self._schedules.items()
                if schedule.vehicle.category is category
                and schedule.accepts(ScheduleLeg("?", period, branch, destination))))

    def claim(self, category: VehicleCategory, branch: str, period: RentalPeriod,
              destination: str, ref: str, exclude: str = "") -> Vehicle:
        """原子地挑一辆能接这单的车并占上。查与占分成两次调用就是这道题的经典超卖 bug。"""
        leg = ScheduleLeg(ref, period, branch, destination)
        with self._lock:
            for plate in sorted(self._schedules):
                schedule = self._schedules[plate]
                if plate == exclude or schedule.vehicle.category is not category:
                    continue
                if schedule.accepts(leg):
                    schedule.add(leg)
                    return schedule.vehicle
        raise NoVehicleAvailableError(
            f"no {category.value} at {branch} for {period.start}–{period.end}")

    def release(self, plate: str, ref: str) -> bool:
        """放掉一段行程（取消、爽约、改派走）。"""
        with self._lock:
            return self._schedule(plate).remove(ref)

    def settle(self, plate: str, ref: str, end: datetime, destination: str) -> tuple[str, ...]:
        """把一段租约改写成**实际发生**的样子，再修复时间轴，返回被挤掉的预约号。

        迟还和"还到了别的门店"其实是同一件事：计划被现实推翻，时间轴按现实重排。准点还车时
        这次调用什么也挤不掉，所以还车路径只有这一条，不需要为"正常还车"单写一个分支。
        """
        with self._lock:
            schedule = self._schedule(plate)
            leg = next((l for l in schedule.legs() if l.ref == ref), None)
            if leg is None:
                raise UnknownEntityError(f"{plate} has no leg {ref!r}")
            floor = leg.period.start + timedelta(hours=1)
            actual = replace(leg, period=RentalPeriod(leg.period.start, max(end, floor)),
                             destination=destination)
            return schedule.force(actual)

    def block(self, plate: str, period: RentalPeriod, branch: str, ref: str) -> tuple[str, ...]:
        """事故或保养：把车从时间轴上整段封掉，返回被挤掉的预约号。

        维修复用同一条时间轴而不是一个 `under_repair` 布尔值，于是"修到几号"天然可查，
        维修期之后的预约也天然还在——布尔值只能表达"现在坏了"，表达不了"到 15 号才能用"。
        """
        with self._lock:
            return self._schedule(plate).force(
                ScheduleLeg(ref, period, branch, branch, rental=False))

    def purge_before(self, cutoff: datetime) -> int:
        """清掉全车队的历史行程，返回清掉的段数。"""
        with self._lock:
            return sum(s.purge_before(cutoff) for s in self._schedules.values())


# --------------------------------------------------------------------------
# 计费：一串注入的纯函数。加一项等于加一个函数，不碰时间轴一行。

@dataclass(frozen=True, slots=True)
class Charge:
    """账单上的一行：科目 + 金额（分，可以为负表示折扣）。"""

    code: str
    amount: int


@dataclass(frozen=True, slots=True)
class Quote:
    """一次报价：逐行明细 + 合计。给客人看明细，而不是一个说不清的总数。"""

    lines: tuple[Charge, ...]

    @property
    def total(self) -> int:
        """合计（分）。"""
        return sum(line.amount for line in self.lines)


@dataclass(frozen=True, slots=True)
class RentalRequest:
    """报价与排期需要的全部事实。定价函数只看它，拿不到车队，也就绕不过车队的锁。"""

    category: VehicleCategory
    period: RentalPeriod
    pickup_branch: str
    return_branch: str
    tier: str = "none"
    extras: tuple[str, ...] = ()

    @property
    def one_way(self) -> bool:
        """是不是异地还车。"""
        return self.pickup_branch != self.return_branch


PriceComponent = Callable[["RentalRequest", int], Charge | None]
Clock = Callable[[], datetime]


def category_rate(rates: Mapping[VehicleCategory, int], daily_cap_hours: int = 20) -> PriceComponent:
    """按小时计价，但每满 24 小时最多收 `daily_cap_hours` 小时——长租不该比短租的整数倍还贵。"""

    def component(request: RentalRequest, subtotal: int) -> Charge | None:
        days, spare = divmod(request.period.hours, 24)
        billed = days * daily_cap_hours + min(spare, daily_cap_hours)
        return Charge("base", rates[request.category] * billed)

    return component


def one_way_fee(amount: int) -> PriceComponent:
    """异地还车附加费：车被留在了别处，回程调度要花钱。"""

    def component(request: RentalRequest, subtotal: int) -> Charge | None:
        return Charge("one_way", amount) if request.one_way else None

    return component


def extras_fee(per_hour: Mapping[str, int]) -> PriceComponent:
    """保险、儿童座椅一类加购项，按小时计。"""

    def component(request: RentalRequest, subtotal: int) -> Charge | None:
        rate = sum(per_hour.get(extra, 0) for extra in request.extras)
        return Charge("extras", rate * request.period.hours) if rate else None

    return component


def loyalty_discount(percent: Mapping[str, int]) -> PriceComponent:
    """会员折扣：按**此前的小计**打折，所以它必须排在组件序列的最后一项。"""

    def component(request: RentalRequest, subtotal: int) -> Charge | None:
        off = percent.get(request.tier, 0)
        return Charge("loyalty", -(subtotal * off // 100)) if off else None

    return component


def price(components: Sequence[PriceComponent], request: RentalRequest) -> Quote:
    """按顺序跑一遍组件，把非零的行拼成报价。组件之间只通过"此前小计"这一个数字耦合。"""
    lines: list[Charge] = []
    for component in components:
        charge = component(request, sum(line.amount for line in lines))
        if charge is not None and charge.amount:
            lines.append(charge)
    return Quote(tuple(lines))


# --------------------------------------------------------------------------
# 预约与它的生命周期。

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
"""合法转移写成一张数据表，而不是散落在各方法里的 `if`：加一个 EXTENDED 只要加一行。"""


@dataclass(slots=True)
class Reservation:
    """一笔预约：谁、什么诉求、报价多少、派了哪辆车、现在走到生命周期的哪一步。

    `plate` 可以是 `None`——被迟还挤掉又改派不到车时就是这个状态。它**不**等于取消：
    单子还在，运营还有时间调车或升舱，取车那一刻才失败。
    """

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
        return self.quote.total + sum(charge.amount for charge in self.extra_charges)

    def transition_to(self, new_status: RentalStatus) -> None:
        """按转移表改状态；不合法就抛 `InvalidTransitionError`。"""
        if new_status not in ALLOWED_TRANSITIONS[self.status]:
            raise InvalidTransitionError(
                f"reservation {self.id}: cannot go from {self.status.value} to {new_status.value}")
        self.status = new_status


@dataclass(frozen=True, slots=True)
class ReturnOutcome:
    """一次还车发生了什么：迟了几小时、追加了哪些钱、连累了谁、谁没救回来。"""

    reservation_id: str
    late_hours: int
    charges: tuple[Charge, ...]
    reassigned: tuple[str, ...]
    unassigned: tuple[str, ...]


# --------------------------------------------------------------------------
# RentalService：门面。报价、搜索、预约、取消、取车、还车、爽约、清理。

class RentalService:
    """租车服务。

    锁纪律：它自己的锁只保护门店表和预约表，**绝不**在持有它时去拿 `Fleet` 的锁。
    两把锁永远"先放后拿"，不存在嵌套，因此也不可能死锁。
    """

    def __init__(self, fleet: Fleet, clock: Clock, components: Sequence[PriceComponent], *,
                 late_fee_per_hour: int = 8000, wrong_branch_fee: int = 30000,
                 no_show_fee: int = 12000, grace: timedelta = timedelta(hours=2),
                 repair: timedelta = timedelta(hours=48)) -> None:
        self._fleet = fleet
        self._clock = clock
        self._components = tuple(components)
        self._late_fee_per_hour = late_fee_per_hour
        self._wrong_branch_fee = wrong_branch_fee
        self._no_show_fee = no_show_fee
        self._grace = grace
        self._repair = repair
        self._reservations: dict[str, Reservation] = {}
        self._lock = threading.Lock()
        self._ids = (f"R{n}" for n in itertools.count(1))

    # ---- 报价与搜索 ------------------------------------------------------

    def quote(self, request: RentalRequest) -> Quote:
        """报价。纯计算，不碰车队，所以可以随便调，也可以单独测。"""
        return price(self._components, request)

    def search(self, branches: Iterable[str], category: VehicleCategory, period: RentalPeriod,
               return_branch: str | None = None) -> tuple[str, ...]:
        """这些门店里，哪些能提供这个车型、这个时段（可指定异地还到哪）的车。"""
        return tuple(branch for branch in branches
                     if self._fleet.available_plates(category, branch, period,
                                                     return_branch or branch))

    # ---- 预约与取消 ------------------------------------------------------

    def reserve(self, customer: str, request: RentalRequest) -> Reservation:
        """下单：先报价，再原子地占一辆车，最后落单。占车失败就整笔失败。"""
        quote = self.quote(request)
        with self._lock:
            reservation = Reservation(id=next(self._ids), customer=customer,
                                      request=request, quote=quote)
        vehicle = self._fleet.claim(request.category, request.pickup_branch, request.period,
                                    request.return_branch, reservation.id)
        reservation.plate = vehicle.plate
        with self._lock:
            self._reservations[reservation.id] = reservation
        return reservation

    def _require(self, reservation_id: str) -> Reservation:
        """取预约；调用方必须已经持有 `self._lock`。"""
        found = self._reservations.get(reservation_id)
        if found is None:
            raise UnknownEntityError(f"unknown reservation {reservation_id!r}")
        return found

    def reservation(self, reservation_id: str) -> Reservation:
        """按预约号取预约。"""
        with self._lock:
            return self._require(reservation_id)

    def cancel(self, reservation_id: str) -> Reservation:
        """取消：状态位先在锁内翻，再放车。并发重复取消只有一个能成功，车只会被放一次。"""
        with self._lock:
            found = self._require(reservation_id)
            found.transition_to(RentalStatus.CANCELLED)
            plate = found.plate
        if plate is not None:
            self._fleet.release(plate, reservation_id)
        return found

    def mark_no_show(self, reservation_id: str) -> Reservation:
        """爽约：过了取车宽限期人还没来，收爽约费并把车放回去给别人。"""
        now = self._clock()
        with self._lock:
            found = self._require(reservation_id)
            if now < found.request.period.start + self._grace:
                raise InvalidTransitionError(f"reservation {reservation_id}: still within grace")
            found.transition_to(RentalStatus.NO_SHOW)
            found.extra_charges = (Charge("no_show", self._no_show_fee),)
            plate = found.plate
        if plate is not None:
            self._fleet.release(plate, reservation_id)
        return found

    # ---- 取车与还车 ------------------------------------------------------

    def pick_up(self, reservation_id: str) -> Vehicle:
        """取车：核对时间窗与车真的在这个门店，再把状态推进 PICKED_UP。

        "车真的在这个门店"这一条必须在取车时复核，而不是信预约时的结论：预约之后可能发生过
        迟还挤占、事故封车、改派。复核用的就是时间轴算出来的位置，不需要任何额外字段。
        """
        now = self._clock()
        found = self.reservation(reservation_id)
        if RentalStatus.PICKED_UP not in ALLOWED_TRANSITIONS[found.status]:
            raise InvalidTransitionError(
                f"reservation {reservation_id}: cannot pick up from {found.status.value}")
        if not found.request.period.start - self._grace <= now < found.request.period.end:
            raise InvalidTransitionError(f"reservation {reservation_id}: {now} is outside the window")
        if found.plate is None:
            raise NoVehicleAvailableError(f"reservation {reservation_id} has no vehicle assigned")
        if self._fleet.location_of(found.plate, now) != found.request.pickup_branch:
            raise NoVehicleAvailableError(
                f"{found.plate} is not at {found.request.pickup_branch}")
        with self._lock:
            found.transition_to(RentalStatus.PICKED_UP)
            found.picked_up_at = now
        return self._fleet.vehicle(found.plate)

    def return_vehicle(self, reservation_id: str, *, branch: str | None = None,
                       damaged: bool = False) -> ReturnOutcome:
        """还车：按实际时刻和实际门店重排时间轴，结算追加费用，再替被挤掉的预约改派。"""
        now = self._clock()
        with self._lock:
            found = self._require(reservation_id)
            found.transition_to(RentalStatus.RETURNED)
            plate = found.plate
        if plate is None:  # PICKED_UP 必有车；裸 assert 会被 -O 去掉，不变量要用真异常
            raise RentalError(f"reservation {reservation_id} was picked up without a vehicle")
        request = found.request
        where = branch or request.return_branch
        charges: list[Charge] = []
        late = max(0, math.ceil((now - request.period.end).total_seconds() / 3600))
        if late:
            charges.append(Charge("late", late * self._late_fee_per_hour))
        if where != request.return_branch:
            charges.append(Charge("wrong_branch", self._wrong_branch_fee))
        displaced = list(self._fleet.settle(plate, reservation_id, now, where))
        if damaged:
            displaced += self._fleet.block(plate, RentalPeriod(now, now + self._repair),
                                           where, f"MAINT-{reservation_id}")
        reassigned, unassigned = self._rehome(displaced)
        with self._lock:
            found.returned_at, found.returned_branch = now, where
            found.extra_charges = tuple(charges)
        return ReturnOutcome(reservation_id, late, tuple(charges), reassigned, unassigned)

    def _rehome(self, displaced: Iterable[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """被挤掉的预约先试着换一辆同型车，换不到就把车牌置空——绝不替客人偷偷取消订单。"""
        reassigned: list[str] = []
        unassigned: list[str] = []
        for reservation_id in dict.fromkeys(displaced):
            with self._lock:
                found = self._reservations.get(reservation_id)
                pending = found is not None and found.status is RentalStatus.RESERVED
            if found is None or not pending:
                continue
            request = found.request
            try:  # 车队的锁只在这一句里拿，此时本服务的锁已经放掉了
                plate = self._fleet.claim(request.category, request.pickup_branch, request.period,
                                          request.return_branch, reservation_id,
                                          exclude=found.plate or "").plate
            except NoVehicleAvailableError:
                plate, target = None, unassigned
            else:
                target = reassigned
            with self._lock:
                found.plate = plate
                target.append(reservation_id)
        return tuple(reassigned), tuple(unassigned)



if __name__ == "__main__":
    from datetime import UTC

    base = datetime(2026, 7, 1, 9, 0, tzinfo=UTC)
    now = base
    fleet = Fleet([Vehicle("京A001", VehicleCategory.SUV, "SH-PVG", "Model Y"),
                   Vehicle("京A002", VehicleCategory.SUV, "SH-PVG", "CR-V")])
    service = RentalService(
        fleet, clock=lambda: now,
        components=[category_rate({VehicleCategory.SUV: 4500}), one_way_fee(30000),
                    extras_fee({"insurance": 800}), loyalty_discount({"gold": 10})])
    shanghai = ("SH-PVG", "SH-HQ")

    first = service.reserve("chi", RentalRequest(
        VehicleCategory.SUV, RentalPeriod(base, base + timedelta(hours=30)),
        "SH-PVG", "SH-HQ", tier="gold", extras=("insurance",)))
    print(f"{first.id} → {first.plate}, {first.quote.total} 分, "
          f"{[(c.code, c.amount) for c in first.quote.lines]}")

    later = RentalPeriod(base + timedelta(hours=40), base + timedelta(hours=44))
    print("40 小时后京A001 停在", fleet.location_of("京A001", later.start),
          "；此时还能出 SUV 的门店：", service.search(shanghai, VehicleCategory.SUV, later))

    second = service.reserve("lee", RentalRequest(VehicleCategory.SUV, later, "SH-PVG", "SH-PVG"))
    service.pick_up(first.id)
    now = base + timedelta(hours=41)
    outcome = service.return_vehicle(first.id, damaged=True)
    print(f"迟还 {outcome.late_hours} 小时 {[(c.code, c.amount) for c in outcome.charges]}，"
          f"改派 {outcome.reassigned}，没救回来 {outcome.unassigned}；"
          f"{second.id} 的车是 {service.reservation(second.id).plate}")
