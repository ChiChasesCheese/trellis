"""幂等转账服务：先占位，再执行，最后保存结果；并发的重复请求合并到第一个请求上。

核心想法：幂等不是"检查一下做没做过"，而是
1. 用 (调用方, 键) 原子地占住一条记录——第一个到的成为拥有者，其余都是重复请求；
2. 重复请求等拥有者出结果，而不是各自再执行一遍（否则两个同时到达的请求都查不到记录，各转一次）；
3. 检查余额、扣款、保存结果放进同一个临界区，且"这条记录已有结果"本身就是临界区里的第一道检查，
   所以即使拥有者被租约夺走（第 4 关），钱也最多动一次。

锁分两把：`_mu` 只保护键表，持有时间极短；`_money` 保护"检查余额 + 扣款 + 存结果"。
外部调用（风控、渠道，`on_execute`）两把锁都不持有——否则一个慢请求会卡住所有转账。
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Literal, Mapping


class TransferError(Exception):
    """本服务所有失败路径的公共基类。"""


class InvalidRequest(TransferError, ValueError):
    """请求本身不合法：金额不是正整数、转出转入是同一个账户、调用方或键为空。不会被记住。"""


class KeyReuse(TransferError):
    """同一个（调用方，键）配了不同的请求内容：调用方的 bug，对应 HTTP 422。"""


class StillRunning(TransferError):
    """第一个请求在 `wait` 秒内没有结束：让调用方稍后用同一个键重试，对应 HTTP 409。"""


class LeaseLost(TransferError):
    """执行到一半时租约已被别的请求夺走并且记录已被释放：这一轮没有动钱，用同一个键重试即可（第 4 关）。"""


@dataclass(frozen=True, slots=True)
class TransferResult:
    status: Literal["succeeded", "rejected"]
    reason: str | None = None  # rejected 时是 "insufficient_funds"
    seq: int | None = None     # succeeded 时是转账序号（从 1 开始）


@dataclass(frozen=True, slots=True)
class TransferRecord:
    seq: int
    client: str
    key: str
    src: str
    dst: str
    amount: int
    currency: str


@dataclass(frozen=True, slots=True)
class _Request:
    """请求内容的指纹：frozen 的数据类自带 `==` 和 `hash`，比较"是不是同一个请求"就是一个 `!=`。"""

    src: str
    dst: str
    amount: int
    currency: str


@dataclass(slots=True)
class _Record:
    """键表里的一条记录：占位（result 为空）或已完成。"""

    fingerprint: _Request
    started: float                                        # 当前这一轮执行的开始时间，租约从这里算
    attempt: int = 1                                      # 第几轮执行；租约被夺走时加一
    finished: float | None = None
    result: TransferResult | None = None
    done: threading.Event = field(default_factory=threading.Event)


class TransferService:
    def __init__(self, balances: Mapping[tuple[str, str], int] | None = None, *, wait: float = 5.0,
                 ttl: float | None = None, lease: float | None = None,
                 clock: Callable[[], float] = time.monotonic,
                 on_execute: Callable[[str, str], None] | None = None) -> None:
        """`balances` 是 (账户, 币种) -> 初始余额。

        `wait`：重复请求最多等第一个请求多少秒（第 2 关）；`on_execute(client, key)`：占键之后、
        动钱之前调用一次的外部步骤，比如风控，它可能很慢，也可能抛异常（第 2、3 关）；
        `ttl`：结果保留多少秒，之后同一个键视为新请求（第 3 关）；`lease`：执行中的记录超过多少秒
        没出结果就视为拥有者已经失联，允许别的请求接手（第 4 关）；`clock` 注入时间。
        """
        self._bal: dict[tuple[str, str], int] = defaultdict(int, balances or {})
        self._keys: dict[tuple[str, str], _Record] = {}       # (调用方, 键) -> 记录；生产里是唯一约束
        self._log: list[TransferRecord] = []
        self._wait, self._ttl, self._lease = wait, ttl, lease
        self._clock, self._on_execute = clock, on_execute
        self._mu = threading.Lock()                           # 只保护键表
        self._money = threading.Lock()                        # 检查余额 + 扣款 + 存结果，代替账户行锁

    # ---- 第 1 关：同键只转一次 ----------------------------------------------

    def transfer(self, client: str, key: str, src: str, dst: str, amount: int, currency: str) -> TransferResult:
        """把 `amount` 从 src 转到 dst；同 (client, key) 只会真正转一次，重试拿到第一次的结果。

        请求不合法抛 InvalidRequest（不占键）；同键不同请求抛 KeyReuse；余额不足不抛异常，
        返回 status="rejected" 的结果，且这个结果同样被记住。
        第一个请求超过 `wait` 秒没结束，重复请求抛 StillRunning（第 2 关）。
        `on_execute` 抛出的异常原样传给调用方，键被释放，钱没动，之后可以用同一个键重试（第 3 关）。
        """
        if not client or not key or src == dst or not isinstance(amount, int) or amount <= 0:
            raise InvalidRequest("非法转账请求")                     # 不合法的请求不占键
        fingerprint = _Request(src, dst, amount, currency)
        k = (client, key)
        while True:
            with self._mu:                                    # 第一步：占键（相当于唯一键插入）
                rec = self._keys.get(k)
                if rec is not None and self._expired(rec):
                    rec = None                                # 保留期已过：当作从没见过
                mine = 0
                if rec is None:
                    rec = self._keys[k] = _Record(fingerprint, self._clock())
                    mine = rec.attempt
                elif rec.fingerprint == fingerprint and self._abandoned(rec):
                    rec.attempt += 1                          # 接手：沿用同一条记录，等待者无需换对象
                    rec.started = self._clock()
                    mine = rec.attempt
            if rec.fingerprint != fingerprint:
                raise KeyReuse("同一个键不能用于不同的请求")
            if mine:
                return self._run(k, rec, mine, src, dst, amount, currency)
            if not rec.done.wait(self._wait):                 # 合并：等第一个请求，而不是再执行一次
                raise StillRunning("第一个请求仍在处理")
            if rec.result is not None:
                return rec.result                             # 原样返回第一次的结果
            # 拥有者失败并释放了键：回到循环重新竞争

    def balance(self, account: str, currency: str) -> int:
        """账户余额；没出现过的账户是 0。"""
        with self._money:
            return self._bal.get((account, currency), 0)

    def transfers(self) -> tuple[TransferRecord, ...]:
        """已成功的转账记录，按序号排列（只读快照）。"""
        with self._money:
            return tuple(self._log)

    def _run(self, k: tuple[str, str], rec: _Record, mine: int, src: str, dst: str,
             amount: int, currency: str) -> TransferResult:
        with self._owning(k, rec, mine):
            if self._on_execute is not None:
                self._on_execute(*k)                          # 外部步骤：不持有任何锁
            with self._money:                                 # 第二步：检查 + 记账 + 存结果
                if rec.result is None:                        # 已有结果说明别的拥有者先提交了：直接用
                    with self._mu:
                        registered = self._keys.get(k) is rec
                    if not registered:                        # 夺走租约的新拥有者失败并释放了键：旧的这一轮不能再动钱
                        raise LeaseLost("租约已被收回")
                    if self._bal[(src, currency)] < amount:
                        rec.result = TransferResult("rejected", "insufficient_funds")   # 业务拒绝也记住
                    else:
                        self._bal[(src, currency)] -= amount
                        self._bal[(dst, currency)] += amount
                        seq = len(self._log) + 1
                        self._log.append(TransferRecord(seq, k[0], k[1], src, dst, amount, currency))
                        rec.result = TransferResult("succeeded", seq=seq)
                    rec.finished = self._clock()
                return rec.result

    @contextmanager
    def _owning(self, k: tuple[str, str], rec: _Record, mine: int) -> Iterator[None]:
        """拥有者的"善后"：无论怎么退出，都要做对的收尾，调用方不用记得手写 try / finally。"""
        try:
            yield
        except BaseException:
            with self._money, self._mu:                       # 与提交互斥：要么提交先发生，要么键先被释放
                if rec.attempt == mine and rec.result is None and self._keys.get(k) is rec:
                    del self._keys[k]                         # 还没动钱就失败：释放键，允许重试
            raise
        finally:
            if rec.attempt == mine:                           # 被夺走租约的旧拥有者不唤醒等待者
                rec.done.set()                                # 先存结果，后唤醒

    # ---- 第 3 关：结果保留期 ------------------------------------------------

    def purge(self) -> int:
        """清掉保留期已过的结果，返回清掉几条。没设 `ttl` 时什么也不清。"""
        with self._mu:
            dead = [k for k, rec in self._keys.items() if self._expired(rec)]
            for k in dead:
                del self._keys[k]
            return len(dead)

    def _expired(self, rec: _Record) -> bool:
        # 只有已完成的记录才会过期；执行中的记录归租约管，不归保留期管
        return (self._ttl is not None and rec.finished is not None
                and self._clock() - rec.finished >= self._ttl)

    # ---- 第 4 关（选做）：租约 -----------------------------------------------

    def _abandoned(self, rec: _Record) -> bool:
        return (self._lease is not None and rec.result is None
                and self._clock() - rec.started >= self._lease)
