"""库存管理——起始模板。公开的类名、方法签名和异常与 solution.py 一致，把标了 NotImplementedError 的方法体补全。"""
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

class InventoryError(Exception):
    """库存所有失败路径的公共基类。"""

class InvalidQuantity(InventoryError, ValueError):
    """数量不是正整数。"""

class OutOfStock(InventoryError):
    """可售数量不够。带着属性 `sku`、`requested`（要的数量）和 `available`（当时的可售数量），方便调用方给用户一个具体的说法。"""

    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(f'{sku}: 需要 {requested}，可售 {available}')
        self.sku, self.requested, self.available = (sku, requested, available)

class UnknownReservation(InventoryError, LookupError):
    """没有这个预留。"""

class ReservationExpired(InventoryError):
    """预留已经过期，库存已经放回可售。"""

class InvalidState(InventoryError):
    """预留的当前状态不允许这个操作（比如取消已经发货的预留）。"""

class Status(Enum):
    ACTIVE = 'active'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

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
    allocations: tuple[Allocation, ...]
    expires_at: float | None
    status: Status

class Inventory:

    def __init__(self, clock: Callable[[], float]=time.monotonic) -> None:
        raise NotImplementedError

    def add_stock(self, warehouse: str, sku: str, quantity: int) -> None:
        """往仓库里入库 `quantity` 件。仓库和商品第一次出现时自动建立。数量不是正整数抛 InvalidQuantity。"""
        raise NotImplementedError

    def on_hand(self, sku: str, warehouse: str | None=None) -> int:
        """实际在架的数量（含被预留占着的）；`warehouse` 为空时是所有仓库之和。没见过的商品是 0。"""
        raise NotImplementedError

    def available(self, sku: str, warehouse: str | None=None) -> int:
        """可售数量 = 在架 - 有效预留占用；已过期的预留不再占用。"""
        raise NotImplementedError

    def reserve(self, sku: str, quantity: int, ttl: float | None=None) -> Reservation:
        """为 `sku` 预留 `quantity` 件，返回预留快照。

可售不够抛 OutOfStock，什么也不占（全有或全无，绝不先占一部分）。数量不是正整数抛 InvalidQuantity。
分配规则固定且确定：先从可售最多的仓库拿，同样多取仓库名小的，拿完为止，所以一个预留可能跨仓库。
`ttl`（第 2 关）：不为空时，预留在 `clock() + ttl` 到点即过期；`ttl <= 0` 抛 ValueError。"""
        raise NotImplementedError

    def confirm(self, reservation_id: str) -> None:
        """确认发货：在架数量按分配扣减，预留不再占用。

重复确认是无操作；已过期抛 ReservationExpired；已取消抛 InvalidState；不存在抛 UnknownReservation。"""
        raise NotImplementedError

    def cancel(self, reservation_id: str) -> None:
        """取消预留，库存放回可售。重复取消、取消已过期的预留都是无操作；已发货抛 InvalidState；不存在抛 UnknownReservation。"""
        raise NotImplementedError

    def get(self, reservation_id: str) -> Reservation:
        """预留的当前快照（已经结清过期）。不存在抛 UnknownReservation。"""
        raise NotImplementedError

    def extend(self, reservation_id: str, ttl: float) -> Reservation:
        """把有效预留的过期时间改成"现在 + ttl"（从现在起算，不是在原来的基础上加），返回新快照。

已过期抛 ReservationExpired；已确认或已取消抛 InvalidState；`ttl <= 0` 抛 ValueError。"""
        raise NotImplementedError

    def reserve_many(self, lines: Mapping[str, int], ttl: float | None=None) -> tuple[Reservation, ...]:
        """一次预留多件商品（`{sku: 数量}`），全有或全无，返回按 sku 排序的预留快照。

任何一件不够就抛 OutOfStock（报告按 sku 排序的第一件不够的），所有商品都不占；
`lines` 为空抛 ValueError；数量不是正整数抛 InvalidQuantity。多线程下不会出现只占了一半的状态。"""
        raise NotImplementedError

    def transfer(self, sku: str, source: str, target: str, quantity: int) -> None:
        """把 `quantity` 件没被预留的库存从 `source` 仓调到 `target` 仓，立即生效。

只能调可售的部分：被预留占着的不动，已有预留的分配不变；`source` 的可售不够抛 OutOfStock；
两个仓库相同抛 ValueError；数量不是正整数抛 InvalidQuantity。"""
        raise NotImplementedError

    def snapshot(self) -> tuple[StockRow, ...]:
        """所有仓库格子的一致快照，按 (商品, 仓库) 排序。取快照期间不会有别的操作插进来。"""
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class StockRow:
    warehouse: str
    sku: str
    on_hand: int
    reserved: int
