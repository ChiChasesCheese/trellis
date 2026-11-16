"""带定时付款的银行账本（Scheduled Banking Ledger）参考实现，可原样放进工作区的 `service.py`。

五行设计：
1. 没有后台线程也没有时钟：每个公开方法都由 `@settles` 包一层，先把"到期时间不晚于本次时间戳"的定时付款结算完，
   再做自己的事——失败的调用、纯查询也不例外；结算只在调用发生时才发生，但每笔余额变化都记在它的到期时刻。
2. 每个账户自己拥有一条只增不减的余额时间线（`BalanceHistory`），历史查询是一次二分查找；合并只是给存活账户
   在合并时刻追加一个新点，被并掉的账户整个丢弃，所以"合并前的历史不被追溯改写"不需要任何特殊代码。
3. 待付款项放在"到期时间、创建序号"的最小堆里，另有按编号索引的字典；取消只删字典，堆里的残留项到期时被跳过，
   残留过多时重建堆，内存不会无限增长。
4. 转账批次先在"暂存余额"上完整演算，全部通过才一次性写入；演算过程不碰任何真实状态，所以回滚不需要撤销日志。
5. 失败一律用返回值（`None` / `False`）表达，不抛异常；曾经用过的账户 ID 永不复用（`_ever_used`）。
"""

from __future__ import annotations

import heapq
import itertools
from bisect import bisect_right
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from functools import wraps
from typing import Any


class BalanceHistory:
    """一个账户的余额时间线：时间严格不倒退，同一时刻只保留最后一个余额。"""

    def __init__(self) -> None:
        self._times: list[int] = []
        self._balances: list[int] = []

    def record(self, time: int, balance: int) -> None:
        if self._times and time < self._times[-1]:
            raise ValueError("余额时间线不能倒退")  # 破坏它就会让历史查询静默出错，所以抛异常而不是 assert
        if self._times and self._times[-1] == time:
            self._balances[-1] = balance
        else:
            self._times.append(time)
            self._balances.append(balance)

    def at(self, time: int) -> int | None:
        """`time` 时刻（含）之前最近的余额；那时账户还不存在则为 None。"""
        index = bisect_right(self._times, time)
        return self._balances[index - 1] if index else None


@dataclass(slots=True)
class Account:
    id: str
    balance: int = 0
    outgoing: int = 0  # 成功转出与成功定时付款的累计
    history: BalanceHistory = field(default_factory=BalanceHistory)


@dataclass(slots=True)
class Payment:
    id: str
    seq: int  # 创建序号：同一到期时间内按它的数值排序，不能按字符串排序
    amount: int
    due: int
    owner: Account  # 合并时改指向存活账户，id、due、seq 都不变


def settles(method: Callable[..., Any]) -> Callable[..., Any]:
    """装饰每个公开方法：先结算到期付款，再执行方法体。"""

    @wraps(method)
    def wrapper(self: Bank, timestamp: int, *args: Any, **kwargs: Any) -> Any:
        self._settle(timestamp)
        return method(self, timestamp, *args, **kwargs)

    return wrapper


class Bank:
    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}  # 只放活跃账户
        self._ever_used: set[str] = set()  # 含已并掉的账户 ID
        self._pending: dict[str, Payment] = {}  # 待付款项，按编号索引
        self._due: list[tuple[int, int, str]] = []  # (到期时间, 序号, 编号) 的最小堆
        self._payment_seq = itertools.count(1)

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    @property
    def queue_size(self) -> int:
        """到期堆里存着的条目数，含已取消、尚未清掉的残留项。"""
        return len(self._due)

    # ---- 结算 ----
    def _settle(self, now: int) -> None:
        while self._due and self._due[0][0] <= now:
            due, _, payment_id = heapq.heappop(self._due)
            payment = self._pending.pop(payment_id, None)
            if payment is None:  # 已取消，残留项
                continue
            owner = payment.owner
            if owner.balance >= payment.amount:  # 不够就永久失败，什么也不留
                owner.balance -= payment.amount
                owner.outgoing += payment.amount
                owner.history.record(due, owner.balance)  # 记在到期时刻，而不是触发结算的这次调用的时刻

    def _compact(self) -> None:
        if len(self._due) > 2 * len(self._pending) + 16:
            self._due = [(p.due, p.seq, p.id) for p in self._pending.values()]
            heapq.heapify(self._due)

    # ---- 账户与转账 ----
    @settles
    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self._ever_used:
            return False
        self._ever_used.add(account_id)
        account = Account(account_id)
        account.history.record(timestamp, 0)
        self._accounts[account_id] = account
        return True

    @settles
    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        account = self._accounts.get(account_id)
        if account is None:
            return None
        account.balance += amount
        account.history.record(timestamp, account.balance)
        return account.balance

    @settles
    def transfer(self, timestamp: int, source: str, target: str, amount: int) -> int | None:
        balances = self._apply(timestamp, [(source, target, amount)])
        return None if balances is None else balances[0]

    @settles
    def transfer_batch(
        self, timestamp: int, transfers: Iterable[Sequence[Any]]
    ) -> list[int] | None:
        return self._apply(timestamp, transfers)

    def _apply(self, timestamp: int, transfers: Iterable[Sequence[Any]]) -> list[int] | None:
        """在暂存余额上按顺序演算；任何一笔失败就返回 None，真实状态还没被碰过。"""
        staged: dict[str, int] = {}  # 只含被碰到的账户
        spent: dict[str, int] = {}
        after: list[int] = []
        for source, target, amount in transfers:
            if source == target or source not in self._accounts or target not in self._accounts:
                return None
            available = staged.get(source, self._accounts[source].balance)
            if available < amount:
                return None
            staged[source] = available - amount
            staged[target] = staged.get(target, self._accounts[target].balance) + amount
            spent[source] = spent.get(source, 0) + amount
            after.append(staged[source])
        for account_id, balance in staged.items():  # 提交：只有赋值，不会失败
            account = self._accounts[account_id]
            account.balance = balance
            account.history.record(timestamp, balance)  # 同一时刻只留批次结束后的余额
        for account_id, total in spent.items():
            self._accounts[account_id].outgoing += total
        return after

    @settles
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        ranked = heapq.nsmallest(n, self._accounts.values(), key=lambda a: (-a.outgoing, a.id))
        return [f"{a.id}({a.outgoing})" for a in ranked]

    # ---- 定时付款 ----
    @settles
    def schedule_payment(
        self, timestamp: int, account_id: str, amount: int, delay: int
    ) -> str | None:
        account = self._accounts.get(account_id)
        if account is None:
            return None  # 失败不消耗编号
        seq = next(self._payment_seq)
        payment = Payment(f"payment{seq}", seq, amount, timestamp + delay, account)
        self._pending[payment.id] = payment
        heapq.heappush(self._due, (payment.due, seq, payment.id))
        return payment.id

    @settles
    def cancel_payment(self, timestamp: int, account_id: str, payment_id: str) -> bool:
        payment = self._pending.get(payment_id)
        account = self._accounts.get(account_id)
        if payment is None or account is None or payment.owner is not account:
            return False
        del self._pending[payment_id]
        self._compact()
        return True

    # ---- 合并与历史 ----
    @settles
    def merge_accounts(self, timestamp: int, id1: str, id2: str) -> bool:
        target, source = self._accounts.get(id1), self._accounts.get(id2)
        if target is None or source is None or target is source:
            return False
        target.balance += source.balance
        target.outgoing += source.outgoing
        for payment in self._pending.values():  # 待付款项改归存活账户，其余字段原样
            if payment.owner is source:
                payment.owner = target
        del self._accounts[id2]  # id2 仍留在 _ever_used 里，永不复用
        target.history.record(timestamp, target.balance)
        return True

    @settles
    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        account = self._accounts.get(account_id)
        if account is None or time_at > timestamp:
            return None
        return account.history.at(time_at)
