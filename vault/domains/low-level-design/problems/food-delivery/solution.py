"""外卖配送（Food Delivery）——三方订单状态机、派单时机与批次合并的参考实现。

核心思路：这道题和网约车的差别只有一句话——**参与方是三个，不是两个**。所以状态机的每一条边
都必须说清楚"谁有权走"：`TRANSITIONS` 是一张 `{当前态: {目标态: 允许的角色}}` 的嵌套表，
非法的目标抛 `IllegalTransitionError`，合法但越权抛 `NotPermittedError`——两个错误分开，才
说得清"这单为什么没送出去"。餐厅**接单之前谁都不派骑手**：接单那一刻才算出预计出餐时间
`ready_at`，派单是一个由时钟驱动的拉取动作，掐着"骑手到店时最多空等 `max_courier_wait`"
发出去，把菜凉的风险压到零、把成本压在骑手的空等上。批次合并只有一条规则：把第二单拼进来，
给**第一单**增加的送达时延不超过上限——这一条同时管住了"两家店要近"和"两单要差不多时候出餐"。
菜品可售状态随时会变，所以校验与抄价在餐厅自己的锁里一次做完：下单那一刻的价格就是最终价格。

坐标与直线距离和网约车同构，此处不再展开；骑手侧只保留最小的独占（IDLE→ASSIGNED 的一次
比较并交换），完整的"要约—拒单—超时顺延"机制见网约车那一题。
"""

from __future__ import annotations

import itertools
import math
import threading
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from enum import Enum


# --------------------------------------------------------------------------
# 失败路径：把"做不到"和"没资格"分开，是这道题最值钱的一条纪律。


class DeliveryError(Exception):
    """本设计里所有失败路径的公共基类。"""

class UnknownRestaurantError(DeliveryError):
    """餐厅 id 不存在。"""

class UnknownOrderError(DeliveryError):
    """订单号不存在。"""

class RestaurantClosedError(DeliveryError):
    """餐厅此刻不接单。"""

class ItemUnavailableError(DeliveryError):
    """菜单上没有这道菜，或它此刻已售罄。"""

class IllegalTransitionError(DeliveryError):
    """订单状态机里根本没有这条边——无论谁来做都不行。"""

class NotPermittedError(DeliveryError):
    """这条边存在，但发起者没有资格走它（比如顾客想把订单标成"已送达"）。"""


# --------------------------------------------------------------------------
# 地理与菜单。


@dataclass(frozen=True, slots=True)
class Location:
    """平面上的一个点，单位当作公里；距离是直线距离。真实系统这里是路网与空间索引。"""

    x: float
    y: float

    def distance_to(self, other: "Location") -> float:
        """到另一点的直线距离。"""
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass(frozen=True, slots=True)
class MenuItem:
    """菜单上的一道菜：单价（分）与单独制作所需的分钟数。不可变——"这道菜现在还有没有"
    是餐厅的库存状态，不是菜本身的属性，所以它不在这里。
    """

    id: str
    name: str
    price: int
    prep_minutes: int = 10


@dataclass(frozen=True, slots=True)
class OrderLine:
    """订单上的一行：**抄下下单那一刻的单价**，此后餐厅改价不追溯已下的单。"""

    item_id: str
    name: str
    quantity: int
    unit_price: int

    @property
    def amount(self) -> int:
        """这一行的小计，单位是分。"""
        return self.quantity * self.unit_price


class Restaurant:
    """一家餐厅：菜单、逐菜的可售状态、开关店，以及出餐时长的估计。

    不变量：`quote` 把"营业中吗 → 每道菜都还有吗 → 抄下价格"在自己的锁里**一次做完**。
    菜品可售状态随时可能被后厨改掉，拆成两步就会出现"校验通过、下单时已售罄"的缝。
    """

    def __init__(self, restaurant_id: str, name: str, location: Location,
                 base_prep: timedelta = timedelta(minutes=5)) -> None:
        self.id = restaurant_id
        self.name = name
        self.location = location
        self.base_prep = base_prep
        self._items: dict[str, MenuItem] = {}
        self._sold_out: set[str] = set()
        self._open = True
        self._lock = threading.Lock()

    @property
    def is_open(self) -> bool:
        """此刻是否接单。"""
        with self._lock:
            return self._open

    def add_item(self, item: MenuItem) -> None:
        """上架一道菜。"""
        with self._lock:
            self._items[item.id] = item

    def set_sold_out(self, item_id: str, sold_out: bool = True) -> None:
        """后厨把某道菜标成售罄／恢复。它可以发生在任何时刻，包括顾客正在下单时。"""
        with self._lock:
            self._sold_out.add(item_id) if sold_out else self._sold_out.discard(item_id)

    def set_open(self, is_open: bool) -> None:
        """开店／关店。关店只影响**还没被接的**单，已接的单必须做完。"""
        with self._lock:
            self._open = is_open

    def available_items(self) -> tuple[MenuItem, ...]:
        """此刻可下单的菜的不可变快照——绝不把内部的菜单字典交出去。"""
        with self._lock:
            return tuple(item for item_id, item in self._items.items() if item_id not in self._sold_out)

    def quote(self, wanted: Mapping[str, int]) -> tuple[OrderLine, ...]:
        """把"要哪些菜、各几份"变成订单行，全成立或全失败。

        **不做部分履约**：三道菜缺一道就整单失败。少送一道菜的配送成本一分不少，顾客的
        满意度却断崖式下跌；真要支持，那是一个需要顾客确认的新流程，不是这里的一个 `if`。
        """
        with self._lock:
            if not self._open:
                raise RestaurantClosedError(f"restaurant {self.id} is closed")
            missing = [i for i in wanted if i not in self._items or i in self._sold_out]
            if missing:
                raise ItemUnavailableError(f"restaurant {self.id} cannot serve {missing}")
            return tuple(OrderLine(item_id=i, name=self._items[i].name, quantity=n,
                                   unit_price=self._items[i].price)
                         for i, n in wanted.items() if n > 0)

    def prep_estimate(self, lines: Sequence[OrderLine]) -> timedelta:
        """预计出餐时长：基础准备时间 + **最慢的那道菜**，不是所有菜相加——后厨是并行的。"""
        with self._lock:
            slowest = max((self._items[l.item_id].prep_minutes for l in lines), default=0)
        return self.base_prep + timedelta(minutes=slowest)


# --------------------------------------------------------------------------
# 订单状态机：一张"边 → 有权走它的角色"的嵌套表。这是本题的设计核心。


class OrderState(Enum):
    """订单的八个状态。SCHEDULED 是第 4 关加进来的，只多一条出边。"""

    SCHEDULED = "scheduled"
    PLACED = "placed"
    ACCEPTED = "accepted"
    READY = "ready"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class Actor(Enum):
    """三个真实参与方，加上平台自己。每一条边都必须指明它属于谁。"""

    CUSTOMER = "customer"
    RESTAURANT = "restaurant"
    COURIER = "courier"
    PLATFORM = "platform"


TRANSITIONS: Mapping[OrderState, Mapping[OrderState, frozenset[Actor]]] = {
    OrderState.SCHEDULED: {
        OrderState.PLACED: frozenset({Actor.PLATFORM}),
        OrderState.REJECTED: frozenset({Actor.RESTAURANT, Actor.PLATFORM}),
        OrderState.CANCELLED: frozenset({Actor.CUSTOMER, Actor.PLATFORM}),
    },
    OrderState.PLACED: {
        OrderState.ACCEPTED: frozenset({Actor.RESTAURANT}),
        OrderState.REJECTED: frozenset({Actor.RESTAURANT, Actor.PLATFORM}),
        OrderState.CANCELLED: frozenset({Actor.CUSTOMER, Actor.PLATFORM}),
    },
    OrderState.ACCEPTED: {
        OrderState.READY: frozenset({Actor.RESTAURANT}),
        OrderState.CANCELLED: frozenset({Actor.PLATFORM}),
    },
    OrderState.READY: {OrderState.PICKED_UP: frozenset({Actor.COURIER})},
    OrderState.PICKED_UP: {OrderState.DELIVERED: frozenset({Actor.COURIER})},
    OrderState.DELIVERED: {},
    OrderState.REJECTED: {},
    OrderState.CANCELLED: {},
}


@dataclass(frozen=True, slots=True)
class StateChange:
    """一次转移的留痕：什么时候、从哪到哪、**谁**干的、为什么。三方系统里"谁"是必填项。"""

    at: datetime
    previous: OrderState
    current: OrderState
    by: Actor
    reason: str | None = None


class Order:
    """一张订单。它只拥有一条不变量：状态只能沿 `TRANSITIONS` 走，且必须由有权的角色来走。

    `ready_at` 是餐厅接单那一刻算出的**预计出餐时间**——派单时机完全由它决定，所以它是
    订单上除状态之外最重要的一个字段。它不带锁：订单永远在 `DeliveryService` 的锁里被改。
    """

    def __init__(self, order_id: str, customer_id: str, restaurant_id: str,
                 lines: Sequence[OrderLine], dropoff: Location, placed_at: datetime,
                 delivery_fee: int, state: OrderState = OrderState.PLACED,
                 deliver_by: datetime | None = None) -> None:
        self.id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.lines = tuple(lines)
        self.dropoff = dropoff
        self.placed_at = placed_at
        self.delivery_fee = delivery_fee
        self.deliver_by = deliver_by
        self.ready_at: datetime | None = None
        self.batch_id: str | None = None
        self._state = state
        self._history: list[StateChange] = []

    @property
    def state(self) -> OrderState:
        """当前状态。只读——唯一的改法是一次受检、受权的转移。"""
        return self._state

    @property
    def history(self) -> tuple[StateChange, ...]:
        """状态轨迹的不可变快照。"""
        return tuple(self._history)

    @property
    def subtotal(self) -> int:
        """菜品小计，单位是分。"""
        return sum(line.amount for line in self.lines)

    @property
    def total(self) -> int:
        """顾客实付：小计加配送费。"""
        return self.subtotal + self.delivery_fee

    def transition_to(self, target: OrderState, now: datetime, by: Actor,
                      reason: str | None = None) -> None:
        """走一步。两种失败**必须分开**：这条边不存在（`IllegalTransitionError`），
        和这条边存在但你没资格走（`NotPermittedError`）。前者是流程错，后者是权限错，
        给调用方的提示、给客服的解释、给监控的告警都不一样。
        """
        allowed = TRANSITIONS[self._state].get(target)
        if allowed is None:
            raise IllegalTransitionError(
                f"order {self.id}: {self._state.value} -> {target.value} is not a transition")
        if by not in allowed:
            raise NotPermittedError(
                f"{by.value} may not move order {self.id} to {target.value}")
        self._history.append(StateChange(now, self._state, target, by, reason))
        self._state = target


# --------------------------------------------------------------------------
# 骑手与批次。


class CourierStatus(Enum):
    """骑手只有派单关心的两个状态。上下线、接单意愿、要约超时这些和网约车完全同构，
    本题不重复——多一个用不上的 OFFLINE 成员，就是一处永远不会被测到的死代码。
    """

    IDLE = "idle"
    ASSIGNED = "assigned"


@dataclass(frozen=True, slots=True)
class Courier:
    """一位骑手此刻的全部状态。不可变，改状态靠整条替换。"""

    id: str
    location: Location | None = None
    status: CourierStatus = CourierStatus.IDLE
    batch_id: str | None = None


@dataclass(frozen=True, slots=True)
class Batch:
    """一位骑手一次带走的若干单，**第一个 id 是锚单**：它先被送到。

    批次自己没有状态——它的状态就是其中每一单的状态之和，另起一套只会多一份要对齐的真相。
    """

    id: str
    courier_id: str
    order_ids: tuple[str, ...]
    created_at: datetime


class CourierPool:
    """骑手名册与独占。`assign` 是锁内的一次比较并交换，所以一位骑手不会拿到两个批次。

    完整的"发要约—可拒绝—超时顺延"机制在网约车那一题里，本类只保留它的最小形态：
    外卖的难点不在骑手要不要接，而在什么时候派、以及能不能拼单。
    """

    def __init__(self) -> None:
        self._couriers: dict[str, Courier] = {}
        self._lock = threading.Lock()

    def go_online(self, courier_id: str, location: Location) -> None:
        """骑手上线并报位置。"""
        with self._lock:
            self._couriers[courier_id] = Courier(courier_id, location, CourierStatus.IDLE)

    def idle(self) -> tuple[Courier, ...]:
        """此刻空闲的骑手快照。"""
        with self._lock:
            return tuple(c for c in self._couriers.values() if c.status is CourierStatus.IDLE)

    @property
    def idle_count(self) -> int:
        """空闲骑手数——只给计数，不把名册交出去。"""
        with self._lock:
            return sum(1 for c in self._couriers.values() if c.status is CourierStatus.IDLE)

    def assign(self, courier_id: str, batch_id: str) -> bool:
        """IDLE → ASSIGNED，成功返回 `True`；抢不到是正常路径，不是异常。"""
        with self._lock:
            courier = self._couriers.get(courier_id)
            if courier is None or courier.status is not CourierStatus.IDLE:
                return False
            self._couriers[courier_id] = replace(courier, status=CourierStatus.ASSIGNED,
                                                 batch_id=batch_id)
            return True

    def finish(self, courier_id: str, location: Location) -> None:
        """整个批次送完：骑手回到 IDLE，位置更新为最后一个送达点。"""
        with self._lock:
            courier = self._couriers.get(courier_id)
            if courier is not None:
                self._couriers[courier_id] = replace(courier, status=CourierStatus.IDLE,
                                                     location=location, batch_id=None)


# --------------------------------------------------------------------------
# DeliveryService：门面。目录、下单、三方推进、派单时机、批次合并。


Clock = Callable[[], datetime]


class DeliveryService:
    """外卖平台：接单、派单、送达，以及定时单与关店这两个第 4 关的追加需求。

    锁纪律：服务锁保护订单表与批次表；它可以在持有自己的锁时去调 `Restaurant` 和
    `CourierPool`（服务锁 → 资源锁，方向唯一），反向调用不存在，所以没有锁序死锁。

    派单策略优化的是**食物温度**：骑手到店时最多空等 `max_courier_wait`，绝不让做好的菜
    在出餐口等骑手。代价落在骑手的有效工时上——这是平台每天都在调的那个旋钮，不是一个
    有唯一正确答案的算法。
    """

    def __init__(self, clock: Clock, couriers: CourierPool,
                 speed_km_per_minute: float = 0.4,
                 max_courier_wait: timedelta = timedelta(minutes=2),
                 max_added_delay: timedelta = timedelta(minutes=5),
                 max_batch_size: int = 3,
                 delivery_fee: int = 500) -> None:
        self._clock, self._couriers = clock, couriers
        self._speed, self._max_wait = speed_km_per_minute, max_courier_wait
        self._max_added_delay, self._max_batch = max_added_delay, max_batch_size
        self._delivery_fee = delivery_fee
        self._restaurants: dict[str, Restaurant] = {}
        self._orders: dict[str, Order] = {}
        self._batches: dict[str, Batch] = {}
        self._lock = threading.RLock()
        self._ids = itertools.count(1)

    # ---- 目录与读 ---------------------------------------------------------

    def register(self, restaurant: Restaurant) -> None:
        """把一家餐厅挂上平台。"""
        with self._lock:
            self._restaurants[restaurant.id] = restaurant

    def restaurant(self, restaurant_id: str) -> Restaurant:
        """按 id 取餐厅。"""
        with self._lock:
            found = self._restaurants.get(restaurant_id)
        if found is None:
            raise UnknownRestaurantError(f"unknown restaurant {restaurant_id!r}")
        return found

    def order(self, order_id: str) -> Order:
        """按订单号取订单。"""
        with self._lock:
            found = self._orders.get(order_id)
        if found is None:
            raise UnknownOrderError(f"unknown order {order_id!r}")
        return found

    def batch(self, batch_id: str) -> Batch:
        """按批次号取批次。"""
        with self._lock:
            return self._batches[batch_id]

    @property
    def open_batch_count(self) -> int:
        """尚未送完的批次数——用计数暴露内部表的大小，测试据此断言它确实会缩小。"""
        with self._lock:
            return len(self._batches)

    # ---- 第 1 关：下单与三方推进 -------------------------------------------

    def place_order(self, customer_id: str, restaurant_id: str, wanted: Mapping[str, int],
                    dropoff: Location, deliver_by: datetime | None = None) -> Order:
        """顾客下单：在餐厅的锁里一次性校验营业与可售、并抄下价格，然后落一张订单。

        `deliver_by` 非空就是定时单，落在 SCHEDULED，由 `release_scheduled` 到点放出来。
        """
        now = self._clock()
        restaurant = self.restaurant(restaurant_id)
        lines = restaurant.quote(wanted)
        state = OrderState.SCHEDULED if deliver_by else OrderState.PLACED
        with self._lock:
            order = Order(f"F{next(self._ids)}", customer_id, restaurant_id, lines, dropoff,
                          now, self._delivery_fee, state=state, deliver_by=deliver_by)
            self._orders[order.id] = order
            return order

    def accept(self, order_id: str) -> Order:
        """餐厅接单：PLACED → ACCEPTED，并在**这一刻**算出预计出餐时间。

        `ready_at` 必须此时才算：下单时餐厅还没看单，不知道后厨排了多少单；而派单的全部
        时机判断都挂在它上面。接单之前**一个骑手都不派**——派了之后餐厅拒单，骑手白跑。
        """
        now = self._clock()
        with self._lock:
            order = self.order(order_id)
            order.transition_to(OrderState.ACCEPTED, now, Actor.RESTAURANT)
            order.ready_at = now + self.restaurant(order.restaurant_id).prep_estimate(order.lines)
            return order

    def reject(self, order_id: str, reason: str, by: Actor = Actor.RESTAURANT) -> Order:
        """餐厅（或平台代为）拒单：PLACED → REJECTED，终态。"""
        return self._move(order_id, OrderState.REJECTED, by, reason)

    def mark_ready(self, order_id: str) -> Order:
        """餐厅出餐：ACCEPTED → READY。只有餐厅能做这一步。"""
        return self._move(order_id, OrderState.READY, Actor.RESTAURANT)

    def pick_up(self, order_id: str) -> Order:
        """骑手取餐：READY → PICKED_UP。菜没出好就取不走，这条边天然挡住了抢跑。"""
        return self._move(order_id, OrderState.PICKED_UP, Actor.COURIER)

    def deliver(self, order_id: str) -> Order:
        """骑手送达：PICKED_UP → DELIVERED；批次里最后一单送完，骑手才回到空闲。"""
        now = self._clock()
        with self._lock:
            order = self._move(order_id, OrderState.DELIVERED, Actor.COURIER)
            batch = self._batches.get(order.batch_id or "")
            if batch is not None and all(self._orders[i].state is OrderState.DELIVERED
                                         for i in batch.order_ids):
                self._couriers.finish(batch.courier_id, order.dropoff)
                del self._batches[batch.id]
            return order

    def cancel(self, order_id: str, by: Actor, reason: str | None = None) -> Order:
        """取消。餐厅一旦接单，顾客就不能再取消——菜已经在做了，成本已经发生。"""
        return self._move(order_id, OrderState.CANCELLED, by, reason)

    # ---- 第 2、3 关：派单时机与批次合并 ------------------------------------

    def dispatch_due(self) -> tuple[Batch, ...]:
        """把此刻"该派了"的订单派出去，返回新建的批次。由时钟驱动，测试里显式调用。

        对每一张已接单、还没进批次的订单：找到到店最快的空闲骑手，算出他**现在出发**会
        几点到店；只要到店时刻还早于"出餐时间减去可接受的空等"，就再等一轮。这样骑手最多
        空等 `max_courier_wait`，而做好的菜一秒都不用等——这就是本策略优化的目标。
        """
        now = self._clock()
        created: list[Batch] = []
        with self._lock:
            pending = sorted((o for o in self._orders.values()
                              if o.state is OrderState.ACCEPTED and o.batch_id is None),
                             key=lambda o: (o.ready_at or now, o.id))
            for anchor in pending:
                if anchor.batch_id is not None:
                    continue
                courier = self._closest_idle(anchor)
                if courier is None:
                    continue
                arrival = now + self._travel(courier.location, self._pickup(anchor))
                if arrival < (anchor.ready_at or now) - self._max_wait:
                    continue
                members = (anchor, *self._batch_mates(anchor, pending))
                batch_id = f"B{next(self._ids)}"
                if not self._couriers.assign(courier.id, batch_id):
                    continue
                batch = Batch(batch_id, courier.id, tuple(o.id for o in members), now)
                for member in members:
                    member.batch_id = batch_id
                self._batches[batch_id] = batch
                created.append(batch)
        return tuple(created)

    def _batch_mates(self, anchor: Order, pending: Sequence[Order]) -> tuple[Order, ...]:
        """给锚单挑拼车伙伴：**唯一的规则**是"拼进来给锚单增加的送达时延不超过上限"。

        这一条同时管住了两件事——两家店必须近（`travel(R锚, R拼)` 进了公式），两单必须
        差不多时候出餐（`ready_at` 之差也进了公式）。不需要再单独配一个"距离上限"参数：
        多一个旋钮就多一处要解释的取舍。
        """
        mates: list[Order] = []
        for other in pending:
            if len(mates) >= self._max_batch - 1:
                break
            if other is anchor or other.batch_id is not None:
                continue
            if self._added_delay(anchor, other) <= self._max_added_delay:
                mates.append(other)
        return tuple(mates)

    def _added_delay(self, anchor: Order, other: Order) -> timedelta:
        """把 `other` 拼进来之后，锚单的送达晚了多久。

        路线固定为"锚店 → 第二家店 → 锚单地址 → 第二单地址"。骑手在锚单出餐时刻拿到第一份，
        骑到第二家店要 `travel(a, b)`，若第二单还没出餐还得等，所以这一段的耗时是
        `max(travel(a, b), 第二单出餐 - 锚单出餐)`；再加上从第二家店去锚单地址比直接去多
        走的那一段。两个上限（店要近、出餐要同时）就这样被压进了同一条不等式。
        """
        a, b, drop = self._pickup(anchor), self._pickup(other), anchor.dropoff
        gap = (other.ready_at or other.placed_at) - (anchor.ready_at or anchor.placed_at)
        return max(self._travel(a, b), gap) + self._travel(b, drop) - self._travel(a, drop)

    def _closest_idle(self, order: Order) -> Courier | None:
        """离取餐点最近的空闲骑手；并列按 id 打破，否则测试会飘。"""
        pickup = self._pickup(order)
        idle = [c for c in self._couriers.idle() if c.location is not None]
        return min(idle, key=lambda c: (c.location.distance_to(pickup), c.id), default=None)

    # ---- 第 4 关：定时单与关店 ---------------------------------------------

    def release_scheduled(self) -> tuple[Order, ...]:
        """把到点的定时单放成普通的 PLACED 单，交给餐厅去接。

        放行时刻 = 期望送达 -（预计出餐 + 从餐厅到顾客的路程）。**派单一行没改**：它只认
        `ready_at`，而 `ready_at` 依旧在餐厅接单那一刻产生。SCHEDULED 只多了一条出边。
        """
        now = self._clock()
        released: list[Order] = []
        with self._lock:
            for order in list(self._orders.values()):
                if order.state is not OrderState.SCHEDULED or order.deliver_by is None:
                    continue
                restaurant = self.restaurant(order.restaurant_id)
                lead = restaurant.prep_estimate(order.lines) + self._travel(
                    restaurant.location, order.dropoff)
                if now >= order.deliver_by - lead:
                    order.transition_to(OrderState.PLACED, now, Actor.PLATFORM, "scheduled order due")
                    released.append(order)
        return tuple(released)

    def close_restaurant(self, restaurant_id: str) -> tuple[str, ...]:
        """餐厅打烊：不再接新单，**还没被接的单由平台代为拒绝**，已接的单必须做完。

        关店不是撤单——餐厅接单那一刻就已经承诺了，菜也已经在做。这条规则让"关店"这个
        第 4 关需求完全不碰派单：已接的单照常走 `ready_at`，派单逻辑毫不知情。

        并发上有一条**刻意留着**的缝：另一个线程可能刚通过 `quote` 的校验、正要落单，于是
        关店之后仍然多出一张 PLACED。兜底是现成的——PLACED → REJECTED 这条边一直可用，
        餐厅（或下一次关店调用）随时能拒掉它。为这条缝去跨两把锁做一次全局互斥，代价远大于
        收益，这正是"乐观校验 + 权威兜底"那个结构的意义。
        """
        now = self._clock()
        self.restaurant(restaurant_id).set_open(False)
        with self._lock:
            doomed = [o for o in self._orders.values() if o.restaurant_id == restaurant_id
                      and o.state in (OrderState.PLACED, OrderState.SCHEDULED)]
            for order in doomed:
                order.transition_to(OrderState.REJECTED, now, Actor.PLATFORM, "restaurant closed")
            return tuple(o.id for o in doomed)

    # ---- 内部 -------------------------------------------------------------

    def _move(self, order_id: str, target: OrderState, by: Actor,
              reason: str | None = None) -> Order:
        """一次受检、受权的状态推进。"""
        now = self._clock()
        with self._lock:
            order = self.order(order_id)
            order.transition_to(target, now, by, reason)
            return order

    def _pickup(self, order: Order) -> Location:
        """这张订单的取餐点。"""
        return self.restaurant(order.restaurant_id).location

    def _travel(self, a: Location | None, b: Location) -> timedelta:
        """按固定骑行速度把距离折算成时间。"""
        km = 0.0 if a is None else a.distance_to(b)
        return timedelta(minutes=km / self._speed)


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 9, 20, 11, 30, tzinfo=UTC)
    kitchen = Restaurant("R1", "川办", Location(0, 0), base_prep=timedelta(minutes=5))
    kitchen.add_item(MenuItem("m1", "回锅肉", 3800, prep_minutes=12))
    kitchen.add_item(MenuItem("m2", "米饭", 300, prep_minutes=2))

    couriers = CourierPool()
    couriers.go_online("c1", Location(2.0, 0.0))
    service = DeliveryService(clock=lambda: now, couriers=couriers)
    service.register(kitchen)

    order = service.place_order("u1", "R1", {"m1": 1, "m2": 2}, Location(4.0, 0.0))
    print(f"{order.id}: {order.total} fen, state {order.state.value}")
    service.accept(order.id)
    print(f"accepted, ready at {order.ready_at:%H:%M}; dispatch now? {bool(service.dispatch_due())}")
    now = now + timedelta(minutes=10)
    print(f"ten minutes later, dispatched: {[b.id for b in service.dispatch_due()]}")
    service.mark_ready(order.id)
    service.pick_up(order.id)
    service.deliver(order.id)
    print(f"{order.id} {order.state.value}; courier idle again: {couriers.idle_count == 1}")
