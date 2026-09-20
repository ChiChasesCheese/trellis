"""酒店预订（Hotel Booking）——按房型与日期区间的可订量、预订生命周期与取消的参考实现。

核心思路：库存的单位是**一个房型的一晚**，不是一间房。一次入住是半开区间
`[check_in, check_out)`，占用的是其中每一晚，所以退房当天不算占用，上午退房的人和下午入住的人
不冲突。`Inventory` 用一张 `(房型, 日期) → 已订数` 的计数表表达可订量，多晚预订的"查 + 订"在同
一把锁里做成全有或全无——只订到五晚里的三晚是这道题的经典 bug。物理房间在**入住时**才由
`FrontDesk` 分配，订的时候只认房型，这样库存不会被碎片化。订单生命周期是一张显式的转移表
（RESERVED → CHECKED_IN → CHECKED_OUT，或 RESERVED → CANCELLED）。超卖政策和按夜动态定价都是
注入的普通函数，加它们不碰库存结构一行。
"""

from __future__ import annotations

import itertools
import threading
from collections import Counter
from collections.abc import Callable, Iterable, Iterator, Mapping
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum


# --------------------------------------------------------------------------
# 失败路径。

class HotelError(Exception):
    """本设计里所有失败路径的公共基类。"""


class InvalidStayError(HotelError):
    """日期区间不合法：退房日期不晚于入住日期。"""


class NoAvailabilityError(HotelError):
    """这段日期里至少有一晚订不到这个房型——整笔预订都不成立。"""


class HotelNotFoundError(HotelError):
    """目录里没有这家酒店。"""


class BookingNotFoundError(HotelError):
    """订单号不存在。"""


class InvalidTransitionError(HotelError):
    """订单当前状态不允许这次状态转移。"""


class NoRoomToAssignError(HotelError):
    """前台没有这个房型的空房可分配——超卖兑现失败，要升级房型或安排外调。"""


# --------------------------------------------------------------------------
# 房型、房间、入住区间。

class RoomType(Enum):
    """房型。库存、定价、超卖全部按房型统计——客人订的是房型，不是某一间房。"""

    SINGLE = "single"
    DOUBLE = "double"
    DELUXE = "deluxe"
    SUITE = "suite"


@dataclass(frozen=True, slots=True)
class Room:
    """一间物理客房：门牌号、房型、楼层。不带"这几天被谁订了"的状态。

    原因和电影票里的座位一样：日期区间上的占用属于库存，不属于这间房本身。区别在于
    这道题更进一步——客人订的时候根本不指定房间号，所以连"这间房这几晚归谁"都不需要提前决定。
    """

    number: str
    type: RoomType
    floor: int = 1


@dataclass(frozen=True, slots=True)
class Stay:
    """一次入住的日期区间，**半开**：`[check_in, check_out)`，占用其中每一晚。

    半开区间是这道题最省事的建模选择：退房当天不算占用，所以 3 号退房的人和 3 号入住的人
    可以共用同一间房，判重叠也只剩一条 `a.check_in < b.check_out and b.check_in < a.check_out`。
    """

    check_in: date
    check_out: date

    def __post_init__(self) -> None:
        if self.check_out <= self.check_in:
            raise InvalidStayError(f"check_out {self.check_out} must be after check_in {self.check_in}")

    @property
    def nights(self) -> int:
        """住几晚——注意是天数差，不是含头含尾的天数。"""
        return (self.check_out - self.check_in).days

    def each_night(self) -> Iterator[date]:
        """逐晚迭代：第一晚是入住日，最后一晚是退房日的前一天。"""
        night = self.check_in
        while night < self.check_out:
            yield night
            night += timedelta(days=1)

    def overlaps(self, other: "Stay") -> bool:
        """两段入住是否共用至少一晚。"""
        return self.check_in < other.check_out and other.check_in < self.check_out


# --------------------------------------------------------------------------
# 可换的政策：超卖与按夜定价。两者都是无状态的纯函数，注入即可，不需要抽象基类。

OverbookingPolicy = Callable[[RoomType, date, int], int]
NightlyRate = Callable[[RoomType, date, int], int]
Clock = Callable[[], datetime]


def no_overbooking(room_type: RoomType, night: date, capacity: int) -> int:
    """不超卖：可订量就是实际房量。"""
    return 0


def percent_overbooking(percent: int) -> OverbookingPolicy:
    """按房量的百分比超卖，对冲爽约（no-show）——酒店业的常规做法，不是 bug。"""

    def allowance(room_type: RoomType, night: date, capacity: int) -> int:
        return capacity * percent // 100

    return allowance


def weekday_overbooking(percent: int) -> OverbookingPolicy:
    """只在周一到周四超卖：商务客爽约率高，周末的休闲客几乎都会来。"""

    def allowance(room_type: RoomType, night: date, capacity: int) -> int:
        return capacity * percent // 100 if night.weekday() < 4 else 0

    return allowance


def flat_nightly(prices: Mapping[RoomType, int]) -> NightlyRate:
    """按房型给一张每晚房价表，单位是分。"""

    def rate(room_type: RoomType, night: date, remaining: int) -> int:
        return prices[room_type]

    return rate


def weekend_uplift(base: NightlyRate, numerator: int, denominator: int) -> NightlyRate:
    """周五、周六两晚按整数分数加价——"叠一层规则"在这里就是包一个函数。"""

    def rate(room_type: RoomType, night: date, remaining: int) -> int:
        price = base(room_type, night, remaining)
        return price * numerator // denominator if night.weekday() in (4, 5) else price

    return rate


def scarcity_uplift(base: NightlyRate, threshold: int, numerator: int, denominator: int) -> NightlyRate:
    """剩余可订量低于阈值时加价——最朴素的动态定价。

    注意签名：那一晚"还剩几间"是**传进来**的，定价函数不需要、也拿不到 `Inventory` 的引用。
    策略只依赖被喂给它的事实，就不会绕过库存的锁去读内部状态。
    """

    def rate(room_type: RoomType, night: date, remaining: int) -> int:
        price = base(room_type, night, remaining)
        return price * numerator // denominator if remaining <= threshold else price

    return rate


# --------------------------------------------------------------------------
# Inventory：这道题的核心——一家酒店按 (房型, 一晚) 计的可订量。

class Inventory:
    """一家酒店的按夜库存：房量固定，已订数按 (房型, 日期) 逐晚记。

    不变量：任一晚的已订数不超过"房量 + 超卖额度"；计数归零的格子立刻从表里删掉，
    不留空壳；整段预订要么每一晚都订上，要么一晚都不动。

    只用一张普通字典而不是线段树：见题解「关键设计决策」——365 天的排期表上，一次
    住 1–5 晚的预订只要动 1–5 个键，而线段树的区间查询加区间更新要走约 2×log2(365)≈18
    个结点，代码量还多出一个数量级。
    """

    def __init__(self, capacity: Mapping[RoomType, int],
                 overbooking: OverbookingPolicy = no_overbooking) -> None:
        self._capacity = dict(capacity)
        self._overbooking = overbooking
        self._booked: dict[tuple[RoomType, date], int] = {}
        self._lock = threading.Lock()

    @property
    def tracked_nights(self) -> int:
        """计数表里当前有多少个非零格子——用来验证"归零即删"和"过期即清"真的生效。"""
        with self._lock:
            return len(self._booked)

    def capacity_of(self, room_type: RoomType) -> int:
        """这个房型一共有几间实体房。"""
        return self._capacity.get(room_type, 0)

    def _available_locked(self, room_type: RoomType, night: date) -> int:
        """某一晚还能订几间；调用方必须已经持有 `self._lock`。"""
        capacity = self._capacity.get(room_type, 0)
        allowance = self._overbooking(room_type, night, capacity)
        return capacity + allowance - self._booked.get((room_type, night), 0)

    def available_on(self, room_type: RoomType, night: date) -> int:
        """某一晚这个房型还能订几间（已计入超卖额度）。"""
        with self._lock:
            return self._available_locked(room_type, night)

    def min_available(self, room_type: RoomType, stay: Stay) -> int:
        """整段入住期间最紧的那一晚还剩几间——这才是"这段日期能订几间"的答案。

        取最小值而不是平均或首晚：一段五晚的预订，只要有一晚满了，整段就订不了。
        """
        with self._lock:
            return min(self._available_locked(room_type, night) for night in stay.each_night())

    def reserve(self, room_type: RoomType, stay: Stay) -> None:
        """为整段入住各占一间，全有或全无；任一晚不足就抛 `NoAvailabilityError`。

        先把每一晚检查完再开始写，两件事在同一把锁里。分成"边检查边写"的循环是这道题的
        经典 bug：五晚里前三晚写成功、第四晚发现满了，客人被扣掉三晚库存却没有订单，而
        回滚代码往往根本没写。
        """
        with self._lock:
            short = [night for night in stay.each_night()
                     if self._available_locked(room_type, night) <= 0]
            if short:
                raise NoAvailabilityError(
                    f"{room_type.value} is sold out on {short[0]} ({len(short)} night(s) short)")
            for night in stay.each_night():
                key = (room_type, night)
                self._booked[key] = self._booked.get(key, 0) + 1

    def release(self, room_type: RoomType, stay: Stay) -> None:
        """退掉整段入住占的库存。计数减到 0 的格子直接删键，不留空壳。

        留空壳是最容易被忽略的泄漏：一家开了十年的酒店，退掉的日期如果只把计数写成 0，
        这张表就会按"房型 × 曾经被订过的每一天"无限长大。
        """
        with self._lock:
            for night in stay.each_night():
                key = (room_type, night)
                left = self._booked.get(key, 0) - 1
                if left > 0:
                    self._booked[key] = left
                else:
                    self._booked.pop(key, None)

    def purge_nights_before(self, cutoff: date) -> int:
        """清掉 `cutoff` 之前的历史晚次，返回清掉的格子数。

        这是计数表随时间收缩的唯一途径：已经过去的日子再也不会被查询或预订，留着只占内存。
        """
        with self._lock:
            stale = [key for key in self._booked if key[1] < cutoff]
            for key in stale:
                del self._booked[key]
        return len(stale)


# --------------------------------------------------------------------------
# FrontDesk：前台。物理房间只在这里出现——入住时分配，退房时收回。

class FrontDesk:
    """一家酒店的前台：把实体房间在入住时分配给订单，退房时收回。

    不变量：一间房同一时刻最多分配给一个订单；`_assigned` 只在退房时缩小。
    它和 `Inventory` 的分工是这道题的第二条主线：库存管的是"未来每一晚还能卖几间"，
    前台管的是"此刻哪间房里住着谁"，两者的锁互不嵌套。
    """

    def __init__(self, rooms: Iterable[Room]) -> None:
        self._rooms = tuple(rooms)
        self._assigned: dict[str, str] = {}  # 房号 → 订单号
        self._lock = threading.Lock()

    @property
    def occupied_count(self) -> int:
        """当前有人住的房间数——只读计数，不交出内部的分配表。"""
        with self._lock:
            return len(self._assigned)

    def occupancy(self) -> Mapping[str, str]:
        """当前"房号 → 订单号"的一份快照副本。"""
        with self._lock:
            return dict(self._assigned)

    def assign(self, room_type: RoomType, booking_id: str) -> Room:
        """给订单挑一间该房型的空房；没有空房时抛 `NoRoomToAssignError`。

        超卖政策允许库存卖超，兑现失败就发生在这里——这正是超卖的真实代价，要么升级房型
        （walk-up），要么替客人安排到别家。让它成为一个显式的异常，比在库存层假装不会发生好。
        """
        with self._lock:
            for room in self._rooms:
                if room.type is room_type and room.number not in self._assigned:
                    self._assigned[room.number] = booking_id
                    return room
        raise NoRoomToAssignError(f"no free {room_type.value} room to assign to {booking_id}")

    def release_room(self, room_number: str) -> None:
        """退房：把房间收回。按房号而不是按订单号收回，回滚路径才能只还刚分出去的那一间。"""
        with self._lock:
            self._assigned.pop(room_number, None)


# --------------------------------------------------------------------------
# Hotel：聚合根。把物理房间、按夜库存、前台绑在一起，自己不转发它们的方法。

class Hotel:
    """一家酒店：所在城市、实体房间，以及属于它自己的 `Inventory` 和 `FrontDesk`。

    它**不**提供 `hotel.reserve(...)` 这样的转发方法——调用方直接用 `hotel.inventory`
    和 `hotel.front_desk`。多包一层只转发一次调用的方法，除了让调用栈变长没有任何作用。
    """

    def __init__(self, hotel_id: str, name: str, city: str, rooms: Iterable[Room],
                 overbooking: OverbookingPolicy = no_overbooking) -> None:
        self.id = hotel_id
        self.name = name
        self.city = city
        self.rooms = tuple(rooms)
        self.inventory = Inventory(Counter(room.type for room in self.rooms), overbooking)
        self.front_desk = FrontDesk(self.rooms)

    def room_types(self) -> tuple[RoomType, ...]:
        """这家店有哪些房型，按枚举顺序给出。"""
        present = {room.type for room in self.rooms}
        return tuple(t for t in RoomType if t in present)


# --------------------------------------------------------------------------
# 订单与它的生命周期：一张显式的状态转移表。

class BookingStatus(Enum):
    """订单生命周期的四个状态。"""

    RESERVED = "reserved"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"


ALLOWED_TRANSITIONS: Mapping[BookingStatus, frozenset[BookingStatus]] = {
    BookingStatus.RESERVED: frozenset({BookingStatus.CHECKED_IN, BookingStatus.CANCELLED}),
    BookingStatus.CHECKED_IN: frozenset({BookingStatus.CHECKED_OUT}),
    BookingStatus.CHECKED_OUT: frozenset(),
    BookingStatus.CANCELLED: frozenset(),
}
"""合法转移写成一张数据表，而不是散落在各个方法里的 `if`：新增一个状态（比如 NO_SHOW）
只要在表里加一行，不用去翻每一处状态判断。"""


@dataclass(slots=True)
class Booking:
    """一笔预订：哪家店、谁、什么房型、住哪几晚、多少钱、现在处在生命周期的哪一步。

    它只认 `room_type`，不认房号——房号是入住后才填上的 `room_number`。
    """

    id: str
    hotel_id: str
    guest: str
    room_type: RoomType
    stay: Stay
    amount: int
    status: BookingStatus = BookingStatus.RESERVED
    room_number: str | None = None

    def transition_to(self, new_status: BookingStatus) -> None:
        """按转移表改状态；不合法的转移抛 `InvalidTransitionError`。"""
        if new_status not in ALLOWED_TRANSITIONS[self.status]:
            raise InvalidTransitionError(
                f"booking {self.id}: cannot go from {self.status.value} to {new_status.value}")
        self.status = new_status


# --------------------------------------------------------------------------
# HotelService：面向调用方的门面。管目录、报价、下单、取消、入住、退房。

class HotelService:
    """酒店预订服务：跨店搜索、下单、取消、入住、退房，以及清理历史晚次。

    锁纪律：它自己的锁只保护酒店目录和订单表，**绝不**在持有它时去拿某家店的
    `Inventory` 或 `FrontDesk` 的锁。三把锁永远"先放后拿"，不存在嵌套。
    """

    def __init__(self, clock: Clock, rate: NightlyRate) -> None:
        self._clock = clock
        self._rate = rate
        self._hotels: dict[str, Hotel] = {}
        self._bookings: dict[str, Booking] = {}
        self._lock = threading.Lock()
        self._ids = (f"R{n}" for n in itertools.count(1))

    # ---- 目录与报价 ------------------------------------------------------

    def register(self, hotel: Hotel) -> None:
        """把一家酒店加进目录。"""
        with self._lock:
            self._hotels[hotel.id] = hotel

    def hotel(self, hotel_id: str) -> Hotel:
        """按 id 取酒店；不存在就抛 `HotelNotFoundError`。"""
        with self._lock:
            hotel = self._hotels.get(hotel_id)
        if hotel is None:
            raise HotelNotFoundError(f"unknown hotel {hotel_id!r}")
        return hotel

    def search(self, city: str, room_type: RoomType, stay: Stay) -> tuple[Hotel, ...]:
        """某城市里，整段日期每一晚都还有这个房型的酒店，按 id 排序。"""
        with self._lock:
            hotels = list(self._hotels.values())
        found = [h for h in hotels
                 if h.city == city and h.inventory.min_available(room_type, stay) > 0]
        return tuple(sorted(found, key=lambda h: h.id))

    def quote(self, hotel_id: str, room_type: RoomType, stay: Stay) -> int:
        """整段入住的总价（分）：逐晚算，把那一晚的剩余可订量喂给定价函数。"""
        inventory = self.hotel(hotel_id).inventory
        return sum(self._rate(room_type, night, inventory.available_on(room_type, night))
                   for night in stay.each_night())

    def purge_nights_before(self, cutoff: date) -> int:
        """跨所有酒店清掉历史晚次，返回清掉的格子数。"""
        with self._lock:
            hotels = list(self._hotels.values())
        return sum(hotel.inventory.purge_nights_before(cutoff) for hotel in hotels)

    # ---- 下单与取消 ------------------------------------------------------

    def book(self, hotel_id: str, room_type: RoomType, stay: Stay, guest: str) -> Booking:
        """下单：先报价，再原子地占掉整段库存，最后落订单。

        报价用的是占库存**之前**的剩余量——先报价后扣减，客人看到的价格和付的价格一致；
        反过来先扣再算，自己的这一间会把自己推进"剩余紧张"的档位，凭空涨价。
        """
        hotel = self.hotel(hotel_id)
        amount = self.quote(hotel_id, room_type, stay)
        hotel.inventory.reserve(room_type, stay)
        try:
            with self._lock:
                booking = Booking(id=next(self._ids), hotel_id=hotel_id, guest=guest,
                                  room_type=room_type, stay=stay, amount=amount)
                self._bookings[booking.id] = booking
        except Exception:
            hotel.inventory.release(room_type, stay)  # 落单失败也不能把库存吞掉
            raise
        return booking

    def booking(self, booking_id: str) -> Booking:
        """按订单号取订单。"""
        with self._lock:
            booking = self._bookings.get(booking_id)
        if booking is None:
            raise BookingNotFoundError(f"unknown booking {booking_id!r}")
        return booking

    def cancel(self, booking_id: str) -> Booking:
        """取消预订：把整段库存还回去。已入住或已取消的订单不能再取消。

        状态位在锁内先翻，这一步就是"认领"这张订单：两个线程同时点取消，只有一个能把
        RESERVED 翻成 CANCELLED，另一个拿到 `InvalidTransitionError`，库存只会被还一次。
        """
        with self._lock:
            booking = self._bookings.get(booking_id)
            if booking is None:
                raise BookingNotFoundError(f"unknown booking {booking_id!r}")
            hotel = self._hotels.get(booking.hotel_id)
            if hotel is None:
                raise HotelNotFoundError(f"hotel {booking.hotel_id!r} is no longer registered")
            booking.transition_to(BookingStatus.CANCELLED)
        hotel.inventory.release(booking.room_type, booking.stay)
        return booking

    # ---- 入住与退房 ------------------------------------------------------

    def check_in(self, booking_id: str) -> Room:
        """办理入住：分配一间实体房，并把订单推进 CHECKED_IN，返回分到的房间。

        先做两道预检——转移是否合法、今天是否落在这段入住区间里（不合法就直接失败，不白占
        房间；"提前三天来办入住"必须被挡住，否则房间会被占着却不计入任何一晚的库存）——再去前台拿房，
        最后回到锁内正式认领状态。两个线程同时办同一张订单的入住时，晚到的那个会在第二步
        失败，并把自己刚分到的房间立刻还回去——所以按**房号**还房，而不是按订单号。
        """
        booking = self.booking(booking_id)
        hotel = self.hotel(booking.hotel_id)
        if BookingStatus.CHECKED_IN not in ALLOWED_TRANSITIONS[booking.status]:
            raise InvalidTransitionError(
                f"booking {booking_id}: cannot check in from {booking.status.value}")
        today = self._clock().date()
        if not booking.stay.check_in <= today < booking.stay.check_out:
            raise InvalidTransitionError(
                f"booking {booking_id}: today {today} is outside the stay {booking.stay.check_in}"
                f"–{booking.stay.check_out}")
        room = hotel.front_desk.assign(booking.room_type, booking.id)
        with self._lock:
            try:
                booking.transition_to(BookingStatus.CHECKED_IN)
            except InvalidTransitionError:
                hotel.front_desk.release_room(room.number)
                raise
            booking.room_number = room.number
        return room

    def check_out(self, booking_id: str) -> Booking:
        """办理退房：收回房间，订单推进 CHECKED_OUT。

        注意**不**归还库存：那几晚是实实在在被住掉的，历史晚次由 `purge_nights_before`
        按日期清理，而不是在退房时"还回去"。
        """
        with self._lock:
            booking = self._bookings.get(booking_id)
            if booking is None:
                raise BookingNotFoundError(f"unknown booking {booking_id!r}")
            hotel = self._hotels.get(booking.hotel_id)
            if hotel is None:
                raise HotelNotFoundError(f"hotel {booking.hotel_id!r} is no longer registered")
            booking.transition_to(BookingStatus.CHECKED_OUT)
            room_number = booking.room_number
        if room_number is not None:
            hotel.front_desk.release_room(room_number)
        return booking


if __name__ == "__main__":
    from datetime import UTC

    today = date(2026, 6, 1)
    now = datetime(2026, 6, 1, 14, 0, tzinfo=UTC)
    rooms = ([Room(number=f"1{i:02d}", type=RoomType.DOUBLE, floor=1) for i in range(1, 3)]
             + [Room(number=f"2{i:02d}", type=RoomType.SUITE, floor=2) for i in range(1, 2)])
    hotel = Hotel("H1", "Seaside", "Sanya", rooms, overbooking=no_overbooking)

    service = HotelService(clock=lambda: now,
                           rate=weekend_uplift(flat_nightly({RoomType.DOUBLE: 48000,
                                                             RoomType.SUITE: 120000}), 13, 10))
    service.register(hotel)

    stay = Stay(check_in=today, check_out=today + timedelta(days=3))
    print(f"available doubles for {stay.nights} nights: "
          f"{hotel.inventory.min_available(RoomType.DOUBLE, stay)}")
    first = service.book("H1", RoomType.DOUBLE, stay, guest="chi")
    second = service.book("H1", RoomType.DOUBLE, stay, guest="lee")
    print(f"{first.id} {first.amount} fen, {second.id} {second.amount} fen, "
          f"left: {hotel.inventory.min_available(RoomType.DOUBLE, stay)}")
    print(f"check-in {first.id} → room {service.check_in(first.id).number}, "
          f"occupied: {hotel.front_desk.occupied_count}")
    service.cancel(second.id)
    print(f"after cancelling {second.id}: left {hotel.inventory.min_available(RoomType.DOUBLE, stay)}, "
          f"tracked nights {hotel.inventory.tracked_nights}")
    service.check_out(first.id)
    print(f"after check-out: occupied {hotel.front_desk.occupied_count}, "
          f"purged {service.purge_nights_before(today + timedelta(days=30))} night(s)")
