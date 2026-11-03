"""熔断器——起始模板。公开的类名、方法签名和异常与 solution.py 一致，把标了 NotImplementedError 的方法体补全。"""
from __future__ import annotations
import logging
import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import TypeVar
T = TypeVar('T')

class State(Enum):
    CLOSED = 'closed'
    OPEN = 'open'
    HALF_OPEN = 'half_open'

class CircuitOpenError(Exception):
    """熔断器拒绝了这次调用（打开，或者半开期的探测名额已满），且没有提供降级函数。"""

@dataclass(frozen=True, slots=True)
class Metrics:
    """某一时刻的计数快照。不可变：调用方拿到后再怎么读，都不会看到半截更新的数字。"""
    success: int
    failure: int
    rejected: int

class CircuitBreaker:

    def __init__(self, failure_threshold: int=5, open_timeout: float=30.0, half_open_max_calls: int=1, success_threshold: int=1, clock: Callable[[], float]=time.monotonic, *, is_failure: Callable[[Exception], bool]=lambda exc: True, window_size: int | None=None, min_calls: int=10, failure_rate: float=0.5, slow_call_threshold: float | None=None, backoff_factor: float=1.0, max_open_timeout: float=300.0, on_state_change: Callable[[State, State], None] | None=None) -> None:
        """配置。数值不合法抛 ValueError。

第 1 关：`failure_threshold` 连续失败几次后熔断；`open_timeout` 熔断后冷却多少秒；`clock` 注入时间。
第 2 关：`half_open_max_calls` 半开期同时放行几个探测；`success_threshold` 探测成功几次才回到关闭。
第 3 关：`is_failure` 判断哪些异常算下游失败；`window_size` 不为空时改用滑动窗口失败率
（最近 `window_size` 次里至少 `min_calls` 次，失败比例达到 `failure_rate` 才熔断，此时不再看连续失败数）；
`slow_call_threshold`：耗时达到这么多秒的调用，即使返回了结果也算失败。
第 4 关：每次探测失败后冷却时间乘 `backoff_factor`，不超过 `max_open_timeout`，回到关闭后复位；
`on_state_change(旧状态, 新状态)` 在状态转换后、锁之外被调用。"""
        raise NotImplementedError

    def call(self, fn: Callable[[], T], fallback: Callable[[], T] | None=None) -> T:
        """包装一次下游调用。放行就执行 `fn()` 并回报结果，拒绝就不碰下游。

被拒绝：有 `fallback` 就返回它的结果，否则抛 CircuitOpenError。
`fn` 抛出算失败的异常（见 `is_failure`）：记一次失败，有 `fallback` 就返回它的结果，否则原样抛出。
`fn` 抛出不算失败的异常：记一次成功，原样抛出（降级不会掩盖这类答复）。
只捕获 Exception，KeyboardInterrupt 之类直接穿过，不记入统计。"""
        raise NotImplementedError

    @property
    def state(self) -> State:
        """当前状态。不会随时间自己变化：OPEN 过了冷却时间，要等下一次调用才转入 HALF_OPEN。"""
        raise NotImplementedError

    @property
    def metrics(self) -> Metrics:
        """成功、失败、被拒绝次数的快照；迟到的旧请求结果也计入，只是不改变状态。"""
        raise NotImplementedError
