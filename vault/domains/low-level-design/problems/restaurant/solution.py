"""餐厅管理（Restaurant Management）——入座与候位、点单到后厨的状态机、结账拆单的参考实现。

核心思路：这道题有三条互相独立的流水线，但很多答案把它们绞在一起。**入座**（`FloorManager`）
只回答"这一刻哪张桌子是空的、该给谁"；**点单**（`OrderLine`/`Order`）只回答"这道菜现在在哪一步、
账单该算多少"；**后厨**（`Kitchen`）只回答"下一道该做哪道菜"。三者由 `RestaurantService` 这个
门面编排，谁都不知道另外两个的实现细节。账单只认**已经上桌**的菜——`Order.served_total` 是对
`OrderLine.state` 的一次查询，不是另存的一个数字，所以"先付一部分、再加菜"不需要任何特殊状态：
加的菜一旦上桌，余额自然重新变大。拆账（平摊/按菜/按份额）是三个纯函数，不是三个类的
策略模式——它们没有状态，也不会在运行时被换来换去。菜品缺货用整数最小货币单位（分）计价，
一律不用浮点数；拆账里的取整余数用最大余数法（largest remainder）逐分整数分配，不用浮点。
"""

from __future__ import annotations

import itertools
import threading
from collections import deque
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable

Clock = Callable[[], datetime]


# --------------------------------------------------------------------------
# 失败路径：把"没有这个对象""状态机走不通""结不了账"分开，方便调用方分别处理。


class RestaurantError(Exception):
    """本设计里所有失败路径的公共基类。"""

class UnknownTableError(RestaurantError):
    """桌号不存在。"""

class UnknownOrderError(RestaurantError):
    """点单号，或点单里的某一行菜号，不存在。"""

class UnknownReservationError(RestaurantError):
    """预订号不存在，或已经被使用过。"""

class TableOccupiedError(RestaurantError):
    """这张桌子已经坐着人，不能重复入座。"""

class NoTableAvailableError(RestaurantError):
    """没有任何一张桌子能在这个时段坐下这么多人。"""

class ItemUnavailableError(RestaurantError):
    """点的菜里有一道（或多道）此刻做不了。"""

class IllegalLineTransitionError(RestaurantError):
    """这道菜的状态机里根本没有这条边。"""

class SplitMismatchError(RestaurantError):
    """拆账的参数和账单对不上：份额非法，或者按菜分账没有覆盖每一件已上桌的菜。"""

class SettlementError(RestaurantError):
    """这张单还没结清，或者还有菜在路上，不能关单清台。"""


# --------------------------------------------------------------------------
# 菜单与桌位：不可变的规则数据，和会变的运行状态分开。


class Course(Enum):
    """菜的课程序号；数字越小越先做——用大小关系表达"谁必须等谁"，不必逐一列出课程对。"""

    STARTER = 1
    MAIN = 2
    DESSERT = 3


@dataclass(frozen=True, slots=True)
class MenuItem:
    """菜单上的一道菜：单价（分）与课程。不带"还有没有货"——那是后厨此刻的库存状态。"""

    id: str
    name: str
    price: int
    course: Course


class TableStatus(Enum):
    """一张桌子只有两个状态：空着，或坐着人。"""

    FREE = "free"
    OCCUPIED = "occupied"


class Table:
    """一张桌子：容量固定不变，占用状态可以转移。重复占用或释放空桌都是设计错误，必须报错。"""

    def __init__(self, table_id: str, capacity: int) -> None:
        self.id = table_id
        self.capacity = capacity
        self._status = TableStatus.FREE

    @property
    def status(self) -> TableStatus:
        """当前状态；只读，改法只有 `occupy`/`free` 这两条受检的边。"""
        return self._status

    def occupy(self) -> None:
        if self._status is not TableStatus.FREE:
            raise TableOccupiedError(f"table {self.id} is already occupied")
        self._status = TableStatus.OCCUPIED

    def free(self) -> None:
        if self._status is not TableStatus.OCCUPIED:
            raise TableOccupiedError(f"table {self.id} is already free")
        self._status = TableStatus.FREE


@dataclass(frozen=True, slots=True)
class Reservation:
    """一次预订：绑定在下单那一刻就选好的桌子和时段上。"""

    id: str
    table_id: str
    party_size: int
    start: datetime
    duration: timedelta

    @property
    def end(self) -> datetime:
        return self.start + self.duration


@dataclass(frozen=True, slots=True)
class WaitlistEntry:
    """候位名单上的一条记录：谁、几个人、什么时候排的队。"""

    id: str
    party_size: int
    joined_at: datetime


@dataclass(frozen=True, slots=True)
class SeatingResult:
    """一次入座尝试的结果：坐下了给桌号，没坐下给候位号，两者恰好一个非空。"""

    table_id: str | None
    waitlist_id: str | None


# --------------------------------------------------------------------------
# FloorManager：桌位、预订与候位名单。只管"这一刻该给谁哪张桌子"，不知道点单和后厨。


class FloorManager:
    """前厅：桌位分配、按时段预订、候位名单。三样共用一把锁，因为它们会互相影响空桌判断。

    预订过了宽限期还没人来认领，就当是不来了：`_sweep` 在每一次读写之前把这类"鸽子"预订
    清掉，没有定时器、没有后台线程——没人查询的时候，过期与否无人关心；任何一次查询或操作
    都会先把世界推到当前时刻的正确状态（和图书馆那道题的 `_sweep` 是同一个模式）。
    """

    def __init__(self, clock: Clock, grace: timedelta = timedelta(minutes=30)) -> None:
        self._clock = clock
        self._grace = grace
        self._tables: dict[str, Table] = {}
        self._reservations: dict[str, Reservation] = {}
        self._waitlist: deque[WaitlistEntry] = deque()
        self._lock = threading.Lock()
        self._ids = itertools.count(1)

    def add_table(self, table: Table) -> None:
        with self._lock:
            self._tables[table.id] = table

    def table(self, table_id: str) -> Table:
        with self._lock:
            self._sweep(self._clock())
            found = self._tables.get(table_id)
        if found is None:
            raise UnknownTableError(f"unknown table {table_id!r}")
        return found

    @property
    def waitlist_length(self) -> int:
        """候位名单长度——只给计数，不把队列交出去。"""
        with self._lock:
            self._sweep(self._clock())
            return len(self._waitlist)

    @property
    def reservation_count(self) -> int:
        """还没被认领、也没过宽限期的预订数——验证过期的预订真的会让这张表缩小。"""
        with self._lock:
            self._sweep(self._clock())
            return len(self._reservations)

    def _smallest_free_fit(self, party_size: int, now: datetime) -> Table | None:
        free = [t for t in self._tables.values()
                if t.status is TableStatus.FREE and t.capacity >= party_size
                and not self._held(t.id, now)]
        return min(free, key=lambda t: (t.capacity, t.id), default=None)

    def _held(self, table_id: str, now: datetime) -> bool:
        """这张桌子此刻是不是正被一个还在宽限期内、没被认领的预订占着。"""
        return any(r.table_id == table_id and r.start <= now < r.start + self._grace
                   for r in self._reservations.values())

    def seat_walk_in(self, party_size: int, now: datetime) -> SeatingResult:
        """散客到店：挑坐得下这拨人的最小空桌；坐不下就按到达顺序进候位名单。"""
        with self._lock:
            self._sweep(now)
            table = self._smallest_free_fit(party_size, now)
            if table is not None:
                table.occupy()
                return SeatingResult(table.id, None)
            entry = WaitlistEntry(f"W{next(self._ids)}", party_size, now)
            self._waitlist.append(entry)
            return SeatingResult(None, entry.id)

    def reserve(self, party_size: int, start: datetime, duration: timedelta) -> Reservation:
        """按时段预订：在能坐下这拨人的桌子里，挑那一段时间还没被占用的最小一张。"""
        with self._lock:
            self._sweep(self._clock())
            candidates = sorted((t for t in self._tables.values() if t.capacity >= party_size),
                                key=lambda t: (t.capacity, t.id))
            for table in candidates:
                if not self._overlaps(table.id, start, duration):
                    reservation = Reservation(f"R{next(self._ids)}", table.id, party_size,
                                              start, duration)
                    self._reservations[reservation.id] = reservation
                    return reservation
            raise NoTableAvailableError(f"no table fits a party of {party_size} for that slot")

    def _overlaps(self, table_id: str, start: datetime, duration: timedelta) -> bool:
        end = start + duration
        return any(r.table_id == table_id and start < r.end and r.start < end
                   for r in self._reservations.values())

    def seat_reservation(self, reservation_id: str) -> SeatingResult:
        """预订到场：占用当初绑定的那张桌。桌子若仍被占用（前一批还没清台）直接报错，不代为等待。

        过了宽限期才来的客人，预订已经被 `_sweep` 清掉、桌子可能已经转给了别人——这里会像
        预订号真的不存在一样报 `UnknownReservationError`，这正是宽限期这条规则的字面意思。
        """
        with self._lock:
            self._sweep(self._clock())
            reservation = self._reservations.get(reservation_id)
            if reservation is None:
                raise UnknownReservationError(f"unknown reservation {reservation_id!r}")
            table = self._tables[reservation.table_id]
            table.occupy()
            del self._reservations[reservation_id]
            return SeatingResult(table.id, None)

    def clear_table(self, table_id: str) -> None:
        """清台：桌子回到空闲。谁来坐它是下一步 `seat_from_waitlist` 的事，这里不自动接手。"""
        with self._lock:
            self._sweep(self._clock())
            table = self._tables.get(table_id)
            if table is None:
                raise UnknownTableError(f"unknown table {table_id!r}")
            table.free()

    def seat_from_waitlist(self, table_id: str, now: datetime) -> SeatingResult | None:
        """刚清出来的桌子，看候位名单里最早一个坐得下的人——不是队首，是队首往后第一个坐得下的。"""
        with self._lock:
            self._sweep(now)
            table = self._tables.get(table_id)
            if table is None or table.status is not TableStatus.FREE or self._held(table_id, now):
                return None
            return self._seat_from_waitlist_locked(table, now)

    def _seat_from_waitlist_locked(self, table: Table, now: datetime) -> SeatingResult | None:
        """必须已经在锁内、且调用方已经确认桌子确实空闲可用。"""
        for entry in self._waitlist:
            if entry.party_size <= table.capacity:
                self._waitlist.remove(entry)
                table.occupy()
                return SeatingResult(table.id, entry.id)
        return None

    def _sweep(self, now: datetime) -> None:
        """懒惰过期：把过了宽限期还没被认领的预订清掉，桌子回到候位名单的候选池里。

        不清掉的话，这条预订会永远占着 `_overlaps` 的一个位置——这张桌子这个时段以后谁都
        订不到；清掉之后立刻看一眼候位名单里有没有人能顶上，这就是"桌子回到池子里、候位
        名单有机会顶上"这句承诺的全部实现。
        """
        expired = [r for r in self._reservations.values() if now >= r.start + self._grace]
        for r in expired:
            del self._reservations[r.id]
            table = self._tables.get(r.table_id)
            if table is not None and table.status is TableStatus.FREE:
                self._seat_from_waitlist_locked(table, now)


# --------------------------------------------------------------------------
# 点单：每一行菜自己的状态机，账单从状态里现算，不另存一份。


class OrderKind(Enum):
    """一张点单属于三种流水线之一；后厨和拆账逻辑对三者一视同仁。"""

    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"


class LineState(Enum):
    """一道菜从下单到上桌的四步，外加"做不了了"这一条终态。"""

    ORDERED = "ordered"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    UNAVAILABLE = "unavailable"


LINE_TRANSITIONS: Mapping[LineState, frozenset[LineState]] = {
    LineState.ORDERED: frozenset({LineState.PREPARING, LineState.UNAVAILABLE}),
    LineState.PREPARING: frozenset({LineState.READY}),
    LineState.READY: frozenset({LineState.SERVED}),
    LineState.SERVED: frozenset(),
    LineState.UNAVAILABLE: frozenset(),
}


class OrderLine:
    """点单里的一行：数量、下单那一刻的价格快照、以及它在后厨的状态机。"""

    def __init__(self, line_id: str, order_id: str, menu_item: MenuItem, quantity: int) -> None:
        self.id = line_id
        self.order_id = order_id
        self.menu_item_id = menu_item.id
        self.name = menu_item.name
        self.course = menu_item.course
        self.unit_price = menu_item.price
        self.quantity = quantity
        self._state = LineState.ORDERED

    @property
    def state(self) -> LineState:
        return self._state

    @property
    def amount(self) -> int:
        """这一行的小计，单位是分。"""
        return self.unit_price * self.quantity

    def transition_to(self, target: LineState) -> None:
        if target not in LINE_TRANSITIONS[self._state]:
            raise IllegalLineTransitionError(
                f"line {self.id}: {self._state.value} -> {target.value} is not a transition")
        self._state = target


class Order:
    """一张点单：堂食挂在一张桌上，外带/外送则不挂桌。账单只认已经上桌的菜。"""

    def __init__(self, order_id: str, kind: OrderKind, table_id: str | None) -> None:
        self.id = order_id
        self.kind = kind
        self.table_id = table_id
        self._lines: dict[str, OrderLine] = {}
        self._paid = 0

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        """点单里所有行的不可变快照。"""
        return tuple(self._lines.values())

    def add_line(self, line: OrderLine) -> None:
        self._lines[line.id] = line

    def discard_line(self, line_id: str) -> None:
        """撤掉还没提交成功的一行——后厨拒收时用来整批回滚，不留半张单。"""
        self._lines.pop(line_id, None)

    def line(self, line_id: str) -> OrderLine:
        found = self._lines.get(line_id)
        if found is None:
            raise UnknownOrderError(f"unknown line {line_id!r} on order {self.id}")
        return found

    @property
    def served_total(self) -> int:
        """账单金额：只认已经上桌的菜——没上的菜顾客还没拿到，不该先收钱。"""
        return sum(l.amount for l in self._lines.values() if l.state is LineState.SERVED)

    @property
    def paid_total(self) -> int:
        return self._paid

    @property
    def balance_due(self) -> int:
        """还差多少钱。加菜、再上桌都会让它重新变大——不需要任何"追加账单"的特殊状态。"""
        return self.served_total - self._paid

    def record_payment(self, amount: int) -> None:
        if amount <= 0:
            raise SplitMismatchError("付款金额必须为正")
        self._paid += amount

    def pending_lines(self) -> tuple[OrderLine, ...]:
        """还没有走到终态（上桌或缺货）的行——前厅想知道"这一桌还在等什么"就问这个。"""
        return tuple(l for l in self._lines.values()
                     if l.state not in (LineState.SERVED, LineState.UNAVAILABLE))

    def is_settled(self) -> bool:
        return self.balance_due <= 0 and not self.pending_lines()


# --------------------------------------------------------------------------
# 后厨：一条队列，课程顺序与库存。不知道桌位，也不知道钱。


class Kitchen:
    """后厨：点单进来的菜排成一条队列，课程序号更小的必须先就绪，缺货整批拒收。"""

    def __init__(self) -> None:
        self._unavailable: set[str] = set()
        self._orders: dict[str, Order] = {}
        self._queue: deque[OrderLine] = deque()
        self._lock = threading.Lock()

    def submit(self, order: Order, lines: Sequence[OrderLine]) -> None:
        """把一批菜下厨：校验有没有货和真正入队在同一次加锁里完成，不留缝。"""
        with self._lock:
            missing = sorted({l.menu_item_id for l in lines} & self._unavailable)
            if missing:
                raise ItemUnavailableError(f"items no longer available: {missing}")
            self._orders[order.id] = order
            self._queue.extend(lines)

    def _eligible(self, line: OrderLine) -> bool:
        """某道菜能开始做的条件：同一单里课程序号更小的菜，都已经就绪或到了终态。"""
        order = self._orders[line.order_id]
        return all(sib.state in (LineState.READY, LineState.SERVED, LineState.UNAVAILABLE)
                  for sib in order.lines if sib.course.value < line.course.value)

    def start_next(self) -> OrderLine | None:
        """从队首找第一道"该做"的菜：还在排队、且前置课程已经就绪。跳过的菜留在原位置等下一轮。"""
        with self._lock:
            for line in self._queue:
                if line.state is LineState.ORDERED and self._eligible(line):
                    self._queue.remove(line)
                    line.transition_to(LineState.PREPARING)
                    return line
            return None

    def mark_ready(self, line: OrderLine) -> None:
        line.transition_to(LineState.READY)

    def mark_unavailable(self, menu_item_id: str) -> tuple[OrderLine, ...]:
        """后厨中途宣布这道菜没了：还没开始做的同款菜全部转缺货，已经在做/做好的不受影响。"""
        with self._lock:
            self._unavailable.add(menu_item_id)
            affected = [l for l in self._queue
                       if l.menu_item_id == menu_item_id and l.state is LineState.ORDERED]
            for line in affected:
                line.transition_to(LineState.UNAVAILABLE)
                self._queue.remove(line)
            return tuple(affected)

    def restock(self, menu_item_id: str) -> None:
        with self._lock:
            self._unavailable.discard(menu_item_id)

    def forget_order(self, order_id: str) -> None:
        """点单结清关闭后，后厨不再需要为它做课程门禁查询——删掉这条索引，防止无限增长。"""
        with self._lock:
            self._orders.pop(order_id, None)

    @property
    def queue_length(self) -> int:
        """还排着队的菜数——只给计数，验证它确实会随 `start_next` 缩小。"""
        with self._lock:
            return len(self._queue)

    @property
    def known_order_count(self) -> int:
        """后厨此刻还记着多少张点单——验证 `forget_order` 真的会让这张表缩小。"""
        with self._lock:
            return len(self._orders)


# --------------------------------------------------------------------------
# 拆账：三个纯函数，不是三个类。金额单位一律是分，取整用最大余数法。


def split_even(amount: int, payer_count: int) -> tuple[int, ...]:
    """平摊：整除的余数（分）按顺序发给前几位付款人，谁付多一分是确定的，不是谁抢到算谁的。"""
    if payer_count <= 0:
        raise SplitMismatchError("拆分人数必须大于 0")
    if amount < 0:
        raise SplitMismatchError("金额不能为负")
    base, remainder = divmod(amount, payer_count)
    return tuple(base + (1 if i < remainder else 0) for i in range(payer_count))


def split_by_share(amount: int, shares: Sequence[int]) -> tuple[int, ...]:
    """按份额拆：先按比例整数除，再把因取整丢掉的分，按"丢得最多的人优先"补回去（最大余数法）。"""
    if not shares or any(s <= 0 for s in shares):
        raise SplitMismatchError("份额必须是正整数")
    total_shares = sum(shares)
    scaled = [amount * s for s in shares]
    floors = [v // total_shares for v in scaled]
    remainders = [v % total_shares for v in scaled]
    leftover = amount - sum(floors)
    order = sorted(range(len(shares)), key=lambda i: (-remainders[i], i))
    for i in order[:leftover]:
        floors[i] += 1
    return tuple(floors)


def split_by_item(lines: Sequence[OrderLine], assignment: Mapping[str, tuple[str, ...]]
                   ) -> Mapping[str, int]:
    """按菜拆：每位付款人认领若干行菜号，必须恰好覆盖每一件已上桌的菜——不多不少。"""
    servable = {l.id: l for l in lines if l.state is LineState.SERVED}
    assigned_ids = [line_id for ids in assignment.values() for line_id in ids]
    if sorted(assigned_ids) != sorted(servable):
        raise SplitMismatchError("按菜分账必须覆盖且只覆盖每一件已上桌的菜，不能重复或遗漏")
    return {payer: sum(servable[line_id].amount for line_id in ids)
           for payer, ids in assignment.items()}


# --------------------------------------------------------------------------
# RestaurantService：门面。入座、点单、上菜、结账拆单、外带外送。


class RestaurantService:
    """餐厅：入座与候位、点单进后厨、上菜、结账；外带外送走同一条点单流水线，不碰桌位。"""

    def __init__(self, clock: Clock, floor: FloorManager, kitchen: Kitchen) -> None:
        self._clock, self._floor, self._kitchen = clock, floor, kitchen
        self._menu: dict[str, MenuItem] = {}
        self._orders: dict[str, Order] = {}
        self._lock = threading.RLock()
        self._ids = itertools.count(1)

    def add_menu_item(self, item: MenuItem) -> None:
        with self._lock:
            self._menu[item.id] = item

    def order(self, order_id: str) -> Order:
        with self._lock:
            found = self._orders.get(order_id)
        if found is None:
            raise UnknownOrderError(f"unknown order {order_id!r}")
        return found

    # ---- 第 1 关：入座与候位 ------------------------------------------------

    def seat_walk_in(self, party_size: int) -> tuple[Order | None, str | None]:
        """散客到店。坐下了返回新开的点单；坐不下返回候位号，此时点单是 `None`。"""
        result = self._floor.seat_walk_in(party_size, self._clock())
        if result.table_id is None:
            return None, result.waitlist_id
        return self._open_order(OrderKind.DINE_IN, result.table_id), None

    def reserve(self, party_size: int, start: datetime, duration: timedelta) -> Reservation:
        return self._floor.reserve(party_size, start, duration)

    def seat_reservation(self, reservation_id: str) -> Order:
        """预订到场：占桌，并立刻开一张挂在这张桌上的点单。"""
        result = self._floor.seat_reservation(reservation_id)
        assert result.table_id is not None
        return self._open_order(OrderKind.DINE_IN, result.table_id)

    def reseat_waitlist(self, table_id: str) -> Order | None:
        """桌子清出来之后，看候位名单里有没有坐得下的人；有就直接开新单。"""
        result = self._floor.seat_from_waitlist(table_id, self._clock())
        if result is None:
            return None
        assert result.table_id is not None
        return self._open_order(OrderKind.DINE_IN, result.table_id)

    def open_takeaway_order(self) -> Order:
        """外带单：不占任何桌。第 4 关——这个方法之外，桌位相关的代码一行没动。"""
        return self._open_order(OrderKind.TAKEAWAY, None)

    def open_delivery_order(self) -> Order:
        """外送单：同样不占桌，走的是和外带一模一样的后厨流水线。"""
        return self._open_order(OrderKind.DELIVERY, None)

    def _open_order(self, kind: OrderKind, table_id: str | None) -> Order:
        with self._lock:
            order = Order(f"O{next(self._ids)}", kind, table_id)
            self._orders[order.id] = order
            return order

    # ---- 第 2 关：点单、上菜、结账拆单 --------------------------------------

    def submit_items(self, order_id: str, requests: Sequence[tuple[str, int]]
                     ) -> tuple[OrderLine, ...]:
        """点单：一次性提交若干道菜，任何一道缺货就整批失败，不留下半提交的行。"""
        with self._lock:
            order = self.order(order_id)
            items = [self._menu_item(menu_item_id) for menu_item_id, _ in requests]
            lines = tuple(OrderLine(f"L{next(self._ids)}", order.id, item, qty)
                          for item, (_, qty) in zip(items, requests))
            for line in lines:
                order.add_line(line)
            try:
                self._kitchen.submit(order, lines)
            except ItemUnavailableError:
                for line in lines:
                    order.discard_line(line.id)
                raise
            return lines

    def _menu_item(self, menu_item_id: str) -> MenuItem:
        item = self._menu.get(menu_item_id)
        if item is None:
            raise ItemUnavailableError(f"unknown menu item {menu_item_id!r}")
        return item

    def start_next_in_kitchen(self) -> OrderLine | None:
        return self._kitchen.start_next()

    def mark_ready(self, order_id: str, line_id: str) -> OrderLine:
        line = self.order(order_id).line(line_id)
        self._kitchen.mark_ready(line)
        return line

    def serve(self, order_id: str, line_id: str) -> OrderLine:
        """服务员把做好的菜端上桌：READY -> SERVED。这一步之后这道菜才计入账单。"""
        line = self.order(order_id).line(line_id)
        line.transition_to(LineState.SERVED)
        return line

    def mark_unavailable(self, menu_item_id: str) -> tuple[OrderLine, ...]:
        return self._kitchen.mark_unavailable(menu_item_id)

    def record_payment(self, order_id: str, amount: int) -> None:
        self.order(order_id).record_payment(amount)

    def close_order(self, order_id: str) -> Order:
        """结账关闭点单：必须已经付清、且没有还在流转的菜。堂食单会顺带清出桌子。"""
        with self._lock:
            order = self.order(order_id)
            if not order.is_settled():
                raise SettlementError(f"order {order_id} is not settled or still has pending items")
            if order.kind is OrderKind.DINE_IN and order.table_id is not None:
                self._floor.clear_table(order.table_id)
            self._kitchen.forget_order(order.id)
            return order

    def floor_status(self) -> Mapping[str, tuple[OrderLine, ...]]:
        """哪些桌子还在等哪些菜——从各自的点单里现算，不另存一份会走样的副本。"""
        with self._lock:
            return {o.table_id: o.pending_lines() for o in self._orders.values()
                   if o.kind is OrderKind.DINE_IN and o.table_id is not None and o.pending_lines()}


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 9, 20, 18, 0, tzinfo=UTC)
    floor, kitchen = FloorManager(clock=lambda: now), Kitchen()
    for table_id, capacity in (("T1", 2), ("T2", 4)):
        floor.add_table(Table(table_id, capacity))
    service = RestaurantService(clock=lambda: now, floor=floor, kitchen=kitchen)
    service.add_menu_item(MenuItem("m1", "沙拉", 1800, Course.STARTER))
    service.add_menu_item(MenuItem("m2", "牛排", 6800, Course.MAIN))

    order, waitlist_id = service.seat_walk_in(2)
    print(f"seated on {order.table_id if order else None}, waitlist {waitlist_id}")
    lines = service.submit_items(order.id, [("m1", 1), ("m2", 1)])
    started = service.start_next_in_kitchen()
    print(f"kitchen starts: {started.name} ({started.course.name})")
