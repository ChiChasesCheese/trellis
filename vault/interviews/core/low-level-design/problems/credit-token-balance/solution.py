"""额度账本（Credit Token Balance）：带过期的额度包、先到期的先扣、幂等扣费、乱序到达的事件。

核心思路：账本只保存"事件"（额度包 Grant 和扣费 Charge），余额和每笔扣费用了哪些包，都是把事件按
时间戳排好序后"重放"一遍得到的结果（`_replay`，一个纯函数）。这样事件以什么顺序到达都无所谓：迟到的
事件插进去，重放一遍，该变的分配自然就变了。接受一个新事件之前，先在副本上重放，所有扣费仍然能全额
扣下才提交，已经接受的扣费不会被迟到的事件"饿死"。重放里时间是单调向前的，所以用一个按到期时间排的
最小堆：过期的包会一直浮在堆顶，扣费时顺手弹掉（惰性删除），用完的包也从堆顶弹出。
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, replace
from datetime import datetime
from typing import NamedTuple


class LedgerError(Exception):
    """所有失败路径的公共基类。"""


class InsufficientCreditsError(LedgerError):
    """额度不够：这笔扣费，或者因它而扣不下的某笔已有扣费。"""


class ConflictError(LedgerError):
    """同一个 id 已经用不同的参数提交过。"""


class UnknownGrantError(LedgerError):
    pass


class UnknownChargeError(LedgerError):
    pass


class Allocation(NamedTuple):
    grant_id: str
    amount: int


@dataclass(frozen=True, slots=True)
class Grant:
    id: str
    amount: int
    at: datetime                       # 从这一刻起可用（含）
    expires_at: datetime | None = None  # 到这一刻失效（不含）；None 永不过期


@dataclass(frozen=True, slots=True)
class Charge:
    id: str
    amount: int
    at: datetime


def _expiry_key(g: Grant) -> tuple:
    """先到期的先扣；永不过期的排最后；同一时刻到期的，先发放的先扣，再按 id。"""
    return (g.expires_at is None, g.expires_at, g.at, g.id)


def _replay(grants: dict[str, Grant], charges: dict[str, Charge],
            until: datetime | None = None) -> tuple[dict[str, tuple[Allocation, ...]], dict[str, int]]:
    """按 (时间, 先额度包后扣费, id) 的顺序重放事件。返回每笔扣费的分配，和每个包的剩余额度。

    某笔扣费凑不够额度就抛 InsufficientCreditsError。`until` 之后的事件不参与。
    """
    events = sorted([*grants.values(), *charges.values()], key=lambda e: (e.at, isinstance(e, Charge), e.id))
    heap: list[tuple] = []
    remaining: dict[str, int] = {}
    allocations: dict[str, tuple[Allocation, ...]] = {}
    for event in events:
        if until is not None and event.at > until:
            break
        match event:
            case Grant():
                remaining[event.id] = event.amount
                heapq.heappush(heap, (_expiry_key(event), event.id))
            case Charge():
                need, taken = event.amount, []
                while need and heap:
                    _, gid = heap[0]
                    expires = grants[gid].expires_at
                    if expires is not None and expires <= event.at:
                        heapq.heappop(heap)          # 惰性删除：时间只往前走，过期的包不会再有效
                        continue
                    use = min(need, remaining[gid])
                    remaining[gid] -= use
                    need -= use
                    taken.append(Allocation(gid, use))
                    if remaining[gid] == 0:
                        heapq.heappop(heap)
                if need:
                    raise InsufficientCreditsError(f"charge {event.id} is short by {need}")
                allocations[event.id] = tuple(taken)
    return allocations, remaining


class CreditLedger:
    def __init__(self) -> None:
        self._grants: dict[str, Grant] = {}
        self._charges: dict[str, Charge] = {}

    # ---------------------------------------------------------------- 第 1 关：额度包与扣费

    def grant(self, grant_id: str, amount: int, at: datetime, expires_at: datetime | None = None) -> None:
        if amount <= 0 or (expires_at is not None and expires_at <= at):
            raise ValueError("amount must be positive and expiry must be after the grant time")
        new = Grant(grant_id, amount, at, expires_at)
        old = self._grants.get(grant_id)
        if old is not None:                      # 第 2 关：同参数重复提交是幂等的
            if old != new:
                raise ConflictError(f"grant {grant_id} already exists with different terms")
            return
        self._commit(grants={**self._grants, grant_id: new})

    def charge(self, charge_id: str, amount: int, at: datetime) -> tuple[Allocation, ...]:
        if amount <= 0:
            raise ValueError("amount must be positive")
        new = Charge(charge_id, amount, at)
        old = self._charges.get(charge_id)
        if old is not None:
            if old != new:
                raise ConflictError(f"charge {charge_id} already exists with different terms")
            return self.allocations(charge_id)   # 幂等：不再扣第二次
        self._commit(charges={**self._charges, charge_id: new})
        return self.allocations(charge_id)

    def balance(self, at: datetime) -> int:
        """`at` 这一刻可用的额度总和：只算 at 之前（含）发生的事件，已过期的包不算。"""
        _, remaining = _replay(self._grants, self._charges, until=at)
        return sum(left for gid, left in remaining.items()
                   if (exp := self._grants[gid].expires_at) is None or exp > at)

    def _commit(self, *, grants: dict[str, Grant] | None = None, charges: dict[str, Charge] | None = None) -> None:
        """先在副本上重放：所有扣费都仍能全额扣下才替换真实状态，失败时账本原封不动。"""
        grants = self._grants if grants is None else grants
        charges = self._charges if charges is None else charges
        _replay(grants, charges)
        self._grants, self._charges = grants, charges

    # ---------------------------------------------------------------- 第 3 关：乱序

    def allocations(self, charge_id: str) -> tuple[Allocation, ...]:
        """这笔扣费按"所有事件按时间排好"的结果用了哪些包。迟到的事件可能改变分配，但总额不变。"""
        if charge_id not in self._charges:
            raise UnknownChargeError(charge_id)
        allocations, _ = _replay(self._grants, self._charges)
        return allocations[charge_id]

    # ---------------------------------------------------------------- 第 4 关：作废额度包

    def revoke(self, grant_id: str, at: datetime) -> None:
        """从 `at` 起这个包剩余的额度作废（等于把到期时间提前到 at）。已经扣掉的不追回；
        如果会让某笔已有扣费凑不够，就拒绝。"""
        grant = self._grants.get(grant_id)
        if grant is None:
            raise UnknownGrantError(grant_id)
        if at <= grant.at:
            raise ValueError("cannot revoke at or before the grant time")
        if grant.expires_at is not None and grant.expires_at <= at:
            return                                 # 已经更早失效，什么都不用做
        self._commit(grants={**self._grants, grant_id: replace(grant, expires_at=at)})
