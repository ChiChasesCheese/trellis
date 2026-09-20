"""限流器（Rate Limiter）练习骨架：公开 API 与 `solution.py` 完全一致，方法体全部待补全。
把每个 `raise NotImplementedError` 换成你自己的实现，然后用
`IMPL=starter uv run --with pytest python -m pytest <本目录> -q` 验收。
内部表示随你换，但测试只会通过公开方法和只读属性断言，所以公开面不要改。
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Callable, Hashable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

Clock = Callable[[], float]
AlgorithmFactory = Callable[[], "RateLimitAlgorithm"]


class RateLimiterError(Exception):
    """本模块所有异常的根。"""


class InvalidConfiguration(RateLimiterError, ValueError):
    """参数本身就不成立：非正的限额、非正的窗口、重复的限流器、非正的开销。"""


@dataclass(frozen=True, slots=True)
class Decision:
    """一次判定的结果：准不准、还剩多少额度、多久后重试、由哪条规则决定。

    `remaining` 的口径和 `X-RateLimit-Remaining` 一致：服务完这次请求之后还剩多少。
    """

    allowed: bool
    remaining: int
    retry_after: float
    rule: str = ""

    def __bool__(self) -> bool:
        raise NotImplementedError


class RateLimitAlgorithm(ABC):
    """一个 key 的限流状态。子类实现 `_used` / `_retry_after` / `commit` 三件事。"""

    def __init__(self, limit: int, window: float, capacity: float | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def _used(self, now: float) -> float:
        """此刻已占用的额度。"""

    @abstractmethod
    def _retry_after(self, now: float, cost: int) -> float:
        """额度不够时，距离够用还要等多少秒。"""

    @abstractmethod
    def commit(self, now: float, cost: int) -> None:
        """扣掉 cost 份额度。"""

    def check(self, now: float, cost: int = 1) -> Decision:
        """只判定、不扣额度。"""
        raise NotImplementedError

    def try_acquire(self, now: float, cost: int = 1) -> Decision:
        """check + commit 的合体；被拒时一份额度都不扣。"""
        raise NotImplementedError

    def is_idle(self, now: float) -> bool:
        """这份状态是否已经和刚新建的状态等价。"""
        raise NotImplementedError


class FixedWindowCounter(RateLimitAlgorithm):
    """固定窗口计数。"""

    def __init__(self, limit: int, window: float) -> None:
        raise NotImplementedError

    def _used(self, now: float) -> float:
        raise NotImplementedError

    def _retry_after(self, now: float, cost: int) -> float:
        raise NotImplementedError

    def commit(self, now: float, cost: int) -> None:
        raise NotImplementedError


class TokenBucket(RateLimitAlgorithm):
    """令牌桶：惰性补充，`burst` 把瞬时容量和持续速率解耦。"""

    def __init__(self, limit: int, window: float, burst: float | None = None) -> None:
        raise NotImplementedError

    @property
    def refill_rate(self) -> float:
        """每秒补充的令牌数。"""
        raise NotImplementedError

    def _used(self, now: float) -> float:
        raise NotImplementedError

    def _retry_after(self, now: float, cost: int) -> float:
        raise NotImplementedError

    def commit(self, now: float, cost: int) -> None:
        raise NotImplementedError


class SlidingWindowLog(RateLimitAlgorithm):
    """滑动窗口日志：精确，内存与 limit 成正比。"""

    def __init__(self, limit: int, window: float) -> None:
        raise NotImplementedError

    @property
    def logged(self) -> int:
        """日志里还留着多少条时间戳。"""
        raise NotImplementedError

    def _used(self, now: float) -> float:
        raise NotImplementedError

    def _retry_after(self, now: float, cost: int) -> float:
        raise NotImplementedError

    def commit(self, now: float, cost: int) -> None:
        raise NotImplementedError


class SlidingWindowCounter(RateLimitAlgorithm):
    """滑动窗口计数：当前格 + 上一格按重叠比例加权。"""

    def __init__(self, limit: int, window: float) -> None:
        raise NotImplementedError

    def _used(self, now: float) -> float:
        raise NotImplementedError

    def _retry_after(self, now: float, cost: int) -> float:
        raise NotImplementedError

    def commit(self, now: float, cost: int) -> None:
        raise NotImplementedError


class RateLimiter:
    """按 key 隔离的限流器：隔离、分片加锁、闲置状态回收。"""

    def __init__(self, factory: AlgorithmFactory, *, clock: Clock = time.monotonic,
                 name: str = "", shards: int = 16) -> None:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def tracked_keys(self) -> int:
        """当前占着内存的 key 数。"""
        raise NotImplementedError

    @contextmanager
    def reserve(self, key: Hashable, now: float) -> Iterator[RateLimitAlgorithm]:
        """持锁取出某个 key 的状态，供两阶段判定使用。"""
        raise NotImplementedError
        yield  # pragma: no cover - 让它仍然是一个生成器函数

    def allow(self, key: Hashable, cost: int = 1) -> Decision:
        """判定并（在通过时）扣额度。"""
        raise NotImplementedError

    def peek(self, key: Hashable, cost: int = 1) -> Decision:
        """只看不扣。"""
        raise NotImplementedError

    def reset(self, key: Hashable) -> None:
        """清掉一个 key 的全部状态。"""
        raise NotImplementedError

    def sweep(self) -> int:
        """显式扫一遍全部分片，返回回收掉的 key 数。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Rule(Generic[T]):
    """一条限流规则：给这个限流器喂哪个 key。"""

    name: str
    limiter: RateLimiter
    key_of: Callable[[T], Hashable]


class CompositeLimiter(Generic[T]):
    """多条规则同时生效，任一条拒绝即整体拒绝；先全查、全过才全扣。"""

    def __init__(self, rules: Sequence[Rule[T]], *, clock: Clock = time.monotonic) -> None:
        raise NotImplementedError

    @property
    def rule_names(self) -> tuple[str, ...]:
        raise NotImplementedError

    def allow(self, subject: T, cost: int = 1) -> Decision:
        """所有规则都放行才放行。"""
        raise NotImplementedError
