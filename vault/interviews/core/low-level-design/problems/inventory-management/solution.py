"""库存管理：多仓库存、带过期时间的预留、并发预留不超卖。

库存的账只有两个数，记在"仓库 x 商品"的格子里：`on_hand`（实际在架）和 `reserved`（被有效预留占着）。
可售数量 = `on_hand - reserved`，只有这个差值才能被新的预留拿走。预留生命周期里每一步都只是在这两个数上
做加减，并且保持 `0 <= reserved <= on_hand`：
    预留 reserve：reserved += n          确认发货 confirm：on_hand -= n 且 reserved -= n
    取消 cancel / 过期：reserved -= n

过期不靠后台线程：每个公开操作开头先"结清"所有已到点的预留（`_expire_due`），所以任何读到的数字都已经
把过期算进去了。到点的预留放在一个按过期时间排序的小根堆里；延期、确认、取消不去堆里找人删，
只让对应的堆条目作废，弹出时发现作废就丢掉（惰性删除）。

所有状态都在一把 `RLock` 之内改，临界区只有字典和堆的操作，够用；多件商品的预留（第 3 关）先在锁内算好
全部分配计划，再整体提交，所以要么全成功要么什么都没占。
"""

from __future__ import annotations

import heapq
import itertools
import threading
import time
from collections import defaultdict
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from enum import Enum
from functools import wraps
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])


class InventoryError(Exception):
    """库存所有失败路径的公共基类。"""


class InvalidQuantity(InventoryError, ValueError):
    """数量不是正整数。"""


class OutOfStock(InventoryError):
    """可售数量不够。带着属性 `sku`、`requested`（要的数量）和 `available`（当时的可售数量），方便调用方给用户一个具体的说法。"""

    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(f"{sku}: 需要 {requested}，可售 {available}")
        self.sku, self.requested, self.available = sku, requested, available


class UnknownReservation(InventoryError, LookupError):
    """没有这个预留。"""


class ReservationExpired(InventoryError):
    """预留已经过期，库存已经放回可售。"""


class InvalidState(InventoryError):
    """预留的当前状态不允许这个操作（比如取消已经发货的预留）。"""


class Status(Enum):
    ACTIVE = "active"          # 占着库存，未过期
    CONFIRMED = "confirmed"    # 已发货，库存已扣
    CANCELLED = "cancelled"    # 已取消，库存已放回
    EXPIRED = "expired"        # 到点未确认，库存已放回


@dataclass(frozen=True, slots=True)
class Allocation:
    warehouse: str
    quantity: int


@dataclass(frozen=True, slots=True)
class Reservation:
    """一个预留。冻结的：状态变化时换一个新对象（`dataclasses.replace`），已经交出去的旧快照永远不会变。"""

    id: str
    sku: str
    quantity: int
    allocations: tuple[Allocation, ...]   # 从哪些仓库各拿了多少，数量之和等于 quantity
    expires_at: float | None              # None 表示不会过期
    status: Status


@dataclass(slots=True)
class _Slot:
    on_hand: int = 0
    reserved: int = 0

    @property
    def free(self) -> int:
        return self.on_hand - self.reserved


def _op(method: _F) -> _F:
    """每个公开操作：先拿锁，再结清已到点的预留，然后才做自己的事。读到的数字永远已经算过期。"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            self._expire_due()
            return method(self, *args, **kwargs)

    return wrapper  # type: ignore[return-value]


def _check_quantity(quantity: int) -> None:
    if type(quantity) is not int or quantity <= 0:
        raise InvalidQuantity(f"数量必须是正整数，得到 {quantity!r}")


class Inventory:
    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._slots: dict[str, dict[str, _Slot]] = defaultdict(dict)    # 商品 -> 仓库 -> 格子
        self._entries: dict[str, Reservation] = {}
        self._expiry: list[tuple[float, str]] = []                      # 小根堆：(过期时间, 预留 ID)
        self._ids = itertools.count(1)
        self._lock = threading.RLock()

    # ---- 第 1 关：多仓库存、预留、确认、取消 -----------------------------------

    @_op
    def add_stock(self, warehouse: str, sku: str, quantity: int) -> None:
        """往仓库里入库 `quantity` 件。仓库和商品第一次出现时自动建立。数量不是正整数抛 InvalidQuantity。"""
        _check_quantity(quantity)
        self._slots[sku].setdefault(warehouse, _Slot()).on_hand += quantity

    @_op
    def on_hand(self, sku: str, warehouse: str | None = None) -> int:
        """实际在架的数量（含被预留占着的）；`warehouse` 为空时是所有仓库之和。没见过的商品是 0。"""
        return sum(s.on_hand for w, s in self._slots.get(sku, {}).items() if warehouse in (None, w))

    @_op
    def available(self, sku: str, warehouse: str | None = None) -> int:
        """可售数量 = 在架 - 有效预留占用；已过期的预留不再占用。"""
        return sum(s.free for w, s in self._slots.get(sku, {}).items() if warehouse in (None, w))

    @_op
    def reserve(self, sku: str, quantity: int, ttl: float | None = None) -> Reservation:
        """为 `sku` 预留 `quantity` 件，返回预留快照。

        可售不够抛 OutOfStock，什么也不占（全有或全无，绝不先占一部分）。数量不是正整数抛 InvalidQuantity。
        分配规则固定且确定：先从可售最多的仓库拿，同样多取仓库名小的，拿完为止，所以一个预留可能跨仓库。
        `ttl`（第 2 关）：不为空时，预留在 `clock() + ttl` 到点即过期；`ttl <= 0` 抛 ValueError。
        """
        _check_quantity(quantity)
        _check_ttl(ttl)
        return self._commit(sku, quantity, self._plan(sku, quantity), ttl)

    @_op
    def confirm(self, reservation_id: str) -> None:
        """确认发货：在架数量按分配扣减，预留不再占用。

        重复确认是无操作；已过期抛 ReservationExpired；已取消抛 InvalidState；不存在抛 UnknownReservation。
        """
        entry = self._entry(reservation_id)
        match entry.status:
            case Status.ACTIVE:
                for a in entry.allocations:
                    slot = self._slots[entry.sku][a.warehouse]
                    slot.on_hand -= a.quantity
                    slot.reserved -= a.quantity
                self._entries[reservation_id] = replace(entry, status=Status.CONFIRMED)
            case Status.CONFIRMED:
                return
            case Status.EXPIRED:
                raise ReservationExpired(reservation_id)
            case Status.CANCELLED:
                raise InvalidState(f"{reservation_id} 已取消")

    @_op
    def cancel(self, reservation_id: str) -> None:
        """取消预留，库存放回可售。重复取消、取消已过期的预留都是无操作；已发货抛 InvalidState；不存在抛 UnknownReservation。"""
        entry = self._entry(reservation_id)
        match entry.status:
            case Status.ACTIVE:
                self._release(entry)
                self._entries[reservation_id] = replace(entry, status=Status.CANCELLED)
            case Status.CONFIRMED:
                raise InvalidState(f"{reservation_id} 已发货，不能取消")
            case Status.CANCELLED | Status.EXPIRED:
                return

    @_op
    def get(self, reservation_id: str) -> Reservation:
        """预留的当前快照（已经结清过期）。不存在抛 UnknownReservation。"""
        return self._entry(reservation_id)

    def _entry(self, reservation_id: str) -> Reservation:
        try:
            return self._entries[reservation_id]
        except KeyError:
            raise UnknownReservation(reservation_id) from None

    def _plan(self, sku: str, quantity: int) -> tuple[Allocation, ...]:
        """只读：算出从哪些仓库各拿多少；不够就抛 OutOfStock。"""
        slots = sorted(self._slots.get(sku, {}).items(), key=lambda item: (-item[1].free, item[0]))
        plan, remaining = [], quantity
        for warehouse, slot in slots:
            take = min(slot.free, remaining)
            if take > 0:
                plan.append(Allocation(warehouse, take))
                remaining -= take
        if remaining > 0:
            raise OutOfStock(sku, quantity, quantity - remaining)
        return tuple(plan)

    def _commit(self, sku: str, quantity: int, plan: tuple[Allocation, ...], ttl: float | None) -> Reservation:
        """提交一个已经验证过的计划：只做加法，不会失败。"""
        expires_at = None if ttl is None else self._clock() + ttl
        entry = Reservation(f"r{next(self._ids)}", sku, quantity, plan, expires_at, Status.ACTIVE)
        self._entries[entry.id] = entry
        for a in plan:
            self._slots[sku][a.warehouse].reserved += a.quantity
        if expires_at is not None:
            heapq.heappush(self._expiry, (expires_at, entry.id))
        return entry

    def _release(self, entry: Reservation) -> None:
        for a in entry.allocations:
            self._slots[entry.sku][a.warehouse].reserved -= a.quantity

    # ---- 第 2 关：过期、延期 -------------------------------------------------

    @_op
    def extend(self, reservation_id: str, ttl: float) -> Reservation:
        """把有效预留的过期时间改成"现在 + ttl"（从现在起算，不是在原来的基础上加），返回新快照。

        已过期抛 ReservationExpired；已确认或已取消抛 InvalidState；`ttl <= 0` 抛 ValueError。
        """
        _check_ttl(ttl)
        entry = self._entry(reservation_id)
        if entry.status is Status.EXPIRED:
            raise ReservationExpired(reservation_id)
        if entry.status is not Status.ACTIVE:
            raise InvalidState(f"{reservation_id} 已{'发货' if entry.status is Status.CONFIRMED else '取消'}")
        entry = self._entries[reservation_id] = replace(entry, expires_at=self._clock() + ttl)
        heapq.heappush(self._expiry, (entry.expires_at, entry.id))   # 旧的堆条目不删，弹出时发现对不上就丢掉
        return entry

    def _expire_due(self) -> None:
        """结清所有 `expires_at <= 现在` 的有效预留：恰好到点也算过期（有效期是左闭右开）。"""
        now = self._clock()
        while self._expiry and self._expiry[0][0] <= now:
            at, rid = heapq.heappop(self._expiry)
            entry = self._entries[rid]
            if entry.status is Status.ACTIVE and entry.expires_at == at:   # 否则是被延期、确认或取消作废的旧条目
                self._release(entry)
                self._entries[rid] = replace(entry, status=Status.EXPIRED)

    # ---- 第 3 关：多件商品的原子预留 ------------------------------------------

    @_op
    def reserve_many(self, lines: Mapping[str, int], ttl: float | None = None) -> tuple[Reservation, ...]:
        """一次预留多件商品（`{sku: 数量}`），全有或全无，返回按 sku 排序的预留快照。

        任何一件不够就抛 OutOfStock（报告按 sku 排序的第一件不够的），所有商品都不占；
        `lines` 为空抛 ValueError；数量不是正整数抛 InvalidQuantity。多线程下不会出现只占了一半的状态。
        """
        if not lines:
            raise ValueError("至少要有一件商品")
        for quantity in lines.values():
            _check_quantity(quantity)
        _check_ttl(ttl)
        plans = {sku: self._plan(sku, lines[sku]) for sku in sorted(lines)}    # 先全部算好；任何一件失败就整体放弃
        return tuple(self._commit(sku, lines[sku], plan, ttl) for sku, plan in plans.items())

    # ---- 第 4 关（选做）：仓间调拨、库存快照 -----------------------------------

    @_op
    def transfer(self, sku: str, source: str, target: str, quantity: int) -> None:
        """把 `quantity` 件没被预留的库存从 `source` 仓调到 `target` 仓，立即生效。

        只能调可售的部分：被预留占着的不动，已有预留的分配不变；`source` 的可售不够抛 OutOfStock；
        两个仓库相同抛 ValueError；数量不是正整数抛 InvalidQuantity。
        """
        _check_quantity(quantity)
        if source == target:
            raise ValueError("调出和调入不能是同一个仓库")
        src = self._slots.get(sku, {}).get(source)
        free = src.free if src else 0
        if src is None or free < quantity:
            raise OutOfStock(sku, quantity, free)
        src.on_hand -= quantity
        self._slots[sku].setdefault(target, _Slot()).on_hand += quantity

    @_op
    def snapshot(self) -> tuple[StockRow, ...]:
        """所有仓库格子的一致快照，按 (商品, 仓库) 排序。取快照期间不会有别的操作插进来。"""
        return tuple(StockRow(w, sku, s.on_hand, s.reserved)
                     for sku, by_wh in sorted(self._slots.items()) for w, s in sorted(by_wh.items()))


@dataclass(frozen=True, slots=True)
class StockRow:
    warehouse: str
    sku: str
    on_hand: int
    reserved: int


def _check_ttl(ttl: float | None) -> None:
    if ttl is not None and ttl <= 0:
        raise ValueError("ttl 必须大于 0")
