"""幂等转账服务——起始模板。公开的类名、方法签名和异常与 solution.py 一致，把标了 NotImplementedError 的方法体补全。"""
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
    status: Literal['succeeded', 'rejected']
    reason: str | None = None
    seq: int | None = None

@dataclass(frozen=True, slots=True)
class TransferRecord:
    seq: int
    client: str
    key: str
    src: str
    dst: str
    amount: int
    currency: str

class TransferService:

    def __init__(self, balances: Mapping[tuple[str, str], int] | None=None, *, wait: float=5.0, ttl: float | None=None, lease: float | None=None, clock: Callable[[], float]=time.monotonic, on_execute: Callable[[str, str], None] | None=None) -> None:
        """`balances` 是 (账户, 币种) -> 初始余额。

`wait`：重复请求最多等第一个请求多少秒（第 2 关）；`on_execute(client, key)`：占键之后、
动钱之前调用一次的外部步骤，比如风控，它可能很慢，也可能抛异常（第 2、3 关）；
`ttl`：结果保留多少秒，之后同一个键视为新请求（第 3 关）；`lease`：执行中的记录超过多少秒
没出结果就视为拥有者已经失联，允许别的请求接手（第 4 关）；`clock` 注入时间。"""
        raise NotImplementedError

    def transfer(self, client: str, key: str, src: str, dst: str, amount: int, currency: str) -> TransferResult:
        """把 `amount` 从 src 转到 dst；同 (client, key) 只会真正转一次，重试拿到第一次的结果。

请求不合法抛 InvalidRequest（不占键）；同键不同请求抛 KeyReuse；余额不足不抛异常，
返回 status="rejected" 的结果，且这个结果同样被记住。
第一个请求超过 `wait` 秒没结束，重复请求抛 StillRunning（第 2 关）。
`on_execute` 抛出的异常原样传给调用方，键被释放，钱没动，之后可以用同一个键重试（第 3 关）。"""
        raise NotImplementedError

    def balance(self, account: str, currency: str) -> int:
        """账户余额；没出现过的账户是 0。"""
        raise NotImplementedError

    def transfers(self) -> tuple[TransferRecord, ...]:
        """已成功的转账记录，按序号排列（只读快照）。"""
        raise NotImplementedError

    def purge(self) -> int:
        """清掉保留期已过的结果，返回清掉几条。没设 `ttl` 时什么也不清。"""
        raise NotImplementedError
