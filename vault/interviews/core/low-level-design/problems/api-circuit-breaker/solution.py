"""熔断器（Circuit Breaker）：保护外部依赖调用的小状态机。

三个状态、四条转换，其余都是"并发下怎么保证这四条转换不出错"：
    CLOSED --连续失败达到阈值--> OPEN --冷却时间到--> HALF_OPEN --探测成功达到要求--> CLOSED
                                                      HALF_OPEN --任一次探测失败--> OPEN

难点在三处，全部落在 `call` 的拆分上：
1. 拿许可（持锁，判断放行还是拒绝）-> 调用下游（不持锁）-> 回报结果（持锁）。慢调用不能把所有线程锁住；
2. 半开期只放有限个探测，其余继续被拒绝，避免冷却一结束所有线程同时冲向刚恢复的下游；
3. 每次状态转换让"代号" `_gen` 加一，许可带着领取时的代号，回报时代号不一致就只计入指标，不改变状态——
   迟到的旧请求不能把很久以前的失败当成"这一轮探测失败"。

时间一律经注入的 `clock` 读取，状态也不会自己随时间变化：OPEN 过了冷却时间，要等下一次调用才转入 HALF_OPEN。
"""

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

T = TypeVar("T")
_log = logging.getLogger(__name__)


class State(Enum):
    CLOSED = "closed"        # 正常放行，统计失败
    OPEN = "open"            # 熔断：直接拒绝，不碰下游
    HALF_OPEN = "half_open"  # 试探：只放少量请求，看下游是否恢复


class CircuitOpenError(Exception):
    """熔断器拒绝了这次调用（打开，或者半开期的探测名额已满），且没有提供降级函数。"""


@dataclass(frozen=True, slots=True)
class Metrics:
    """某一时刻的计数快照。不可变：调用方拿到后再怎么读，都不会看到半截更新的数字。"""

    success: int
    failure: int
    rejected: int


# 合法的状态转换表：`_move` 用它守住"只有这四条转换"，写错转换会立刻抛 AssertionError，而不是悄悄进入非法状态。
_TRANSITIONS = MappingProxyType({
    State.CLOSED: frozenset({State.OPEN}),
    State.OPEN: frozenset({State.HALF_OPEN}),
    State.HALF_OPEN: frozenset({State.CLOSED, State.OPEN}),
})


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, open_timeout: float = 30.0,
                 half_open_max_calls: int = 1, success_threshold: int = 1,
                 clock: Callable[[], float] = time.monotonic, *,
                 is_failure: Callable[[Exception], bool] = lambda exc: True,
                 window_size: int | None = None, min_calls: int = 10, failure_rate: float = 0.5,
                 slow_call_threshold: float | None = None,
                 backoff_factor: float = 1.0, max_open_timeout: float = 300.0,
                 on_state_change: Callable[[State, State], None] | None = None) -> None:
        """配置。数值不合法抛 ValueError。

        第 1 关：`failure_threshold` 连续失败几次后熔断；`open_timeout` 熔断后冷却多少秒；`clock` 注入时间。
        第 2 关：`half_open_max_calls` 半开期同时放行几个探测；`success_threshold` 探测成功几次才回到关闭。
        第 3 关：`is_failure` 判断哪些异常算下游失败；`window_size` 不为空时改用滑动窗口失败率
        （最近 `window_size` 次里至少 `min_calls` 次，失败比例达到 `failure_rate` 才熔断，此时不再看连续失败数）；
        `slow_call_threshold`：耗时达到这么多秒的调用，即使返回了结果也算失败。
        第 4 关：每次探测失败后冷却时间乘 `backoff_factor`，不超过 `max_open_timeout`，回到关闭后复位；
        `on_state_change(旧状态, 新状态)` 在状态转换后、锁之外被调用。
        """
        if (failure_threshold < 1 or open_timeout < 0 or half_open_max_calls < 1 or success_threshold < 1
                or backoff_factor < 1 or not 0 < failure_rate <= 1
                or (window_size is not None and not 1 <= min_calls <= window_size)):
            raise ValueError("熔断器配置不合法")
        self.failure_threshold, self.half_open_max_calls = failure_threshold, half_open_max_calls
        self.success_threshold, self.min_calls, self.failure_rate = success_threshold, min_calls, failure_rate
        self._base_timeout, self._timeout, self._max_timeout = open_timeout, open_timeout, max_open_timeout
        self._backoff, self._clock, self._is_failure = backoff_factor, clock, is_failure
        self._slow, self._listener = slow_call_threshold, on_state_change
        self._lock = threading.Lock()
        self._state, self._gen = State.CLOSED, 0
        self._failures = self._successes = self._probes = 0     # 连续失败数 / 半开期成功数 / 半开期在途探测数
        self._window: deque[bool] = deque(maxlen=window_size)   # 滑动窗口：True 表示成功
        self._windowed = window_size is not None
        self._opened_at = 0.0
        self._counts = [0, 0, 0]                                # 成功 / 失败 / 被拒绝
        self._events: list[tuple[State, State]] = []            # 锁内记录、锁外派发的状态变化

    # ---- 第 1 关：三状态、阈值、冷却、降级、指标 -------------------------------

    def call(self, fn: Callable[[], T], fallback: Callable[[], T] | None = None) -> T:
        """包装一次下游调用。放行就执行 `fn()` 并回报结果，拒绝就不碰下游。

        被拒绝：有 `fallback` 就返回它的结果，否则抛 CircuitOpenError。
        `fn` 抛出算失败的异常（见 `is_failure`）：记一次失败，有 `fallback` 就返回它的结果，否则原样抛出。
        `fn` 抛出不算失败的异常：记一次成功，原样抛出（降级不会掩盖这类答复）。
        只捕获 Exception，KeyboardInterrupt 之类直接穿过，不记入统计。
        """
        gen = self._acquire()                        # 不持锁调用下游：慢调用不能把所有线程锁住
        if gen is None:
            self._dispatch()
            if fallback is not None:
                return fallback()
            raise CircuitOpenError("circuit open")
        started = self._clock()
        try:
            result = fn()
        except Exception as exc:
            counted = self._is_failure(exc)
            self._record(gen, ok=not counted)
            self._dispatch()
            if counted and fallback is not None:
                return fallback()
            raise
        slow = self._slow is not None and self._clock() - started >= self._slow
        self._record(gen, ok=not slow)               # 慢调用算失败，但调用方照样拿到结果
        self._dispatch()
        return result

    @property
    def state(self) -> State:
        """当前状态。不会随时间自己变化：OPEN 过了冷却时间，要等下一次调用才转入 HALF_OPEN。"""
        with self._lock:
            return self._state

    @property
    def metrics(self) -> Metrics:
        """成功、失败、被拒绝次数的快照；迟到的旧请求结果也计入，只是不改变状态。"""
        with self._lock:
            return Metrics(*self._counts)

    def _acquire(self) -> int | None:
        """取许可：返回领取时的代号，或 None 表示拒绝。"""
        with self._lock:
            if self._state is State.OPEN:
                if self._clock() - self._opened_at < self._timeout:
                    self._counts[2] += 1
                    return None
                self._move(State.HALF_OPEN)          # 冷却结束，进入试探
            if self._state is State.HALF_OPEN:
                if self._probes >= self.half_open_max_calls:   # 第 2 关：试探名额已满
                    self._counts[2] += 1
                    return None
                self._probes += 1
            return self._gen

    def _record(self, gen: int, ok: bool) -> None:
        with self._lock:
            self._counts[0 if ok else 1] += 1
            if gen != self._gen:                     # 第 2 关：状态已变，迟到的旧结果只计数，不影响新状态
                return
            match self._state:
                case State.HALF_OPEN:
                    self._probes -= 1
                    if not ok:                       # 试探失败：立刻重新熔断，重新计时
                        self._timeout = min(self._timeout * self._backoff, self._max_timeout)
                        self._trip()
                    else:
                        self._successes += 1
                        if self._successes >= self.success_threshold:
                            self._timeout = self._base_timeout
                            self._move(State.CLOSED)
                case State.CLOSED:
                    if self._windowed:               # 第 3 关：滑动窗口失败率
                        self._window.append(ok)
                        fails = self._window.count(False)
                        if len(self._window) >= self.min_calls and fails / len(self._window) >= self.failure_rate:
                            self._trip()
                    else:
                        self._failures = 0 if ok else self._failures + 1   # 连续失败：一次成功就清零
                        if self._failures >= self.failure_threshold:
                            self._trip()

    def _trip(self) -> None:
        self._move(State.OPEN)
        self._opened_at = self._clock()

    def _move(self, new: State) -> None:
        assert new in _TRANSITIONS[self._state], f"非法转换 {self._state} -> {new}"
        self._events.append((self._state, new))
        self._state, self._gen = new, self._gen + 1  # 代号加一：让所有在途的旧许可作废
        self._failures = self._successes = self._probes = 0
        self._window.clear()

    # ---- 第 4 关（选做）：状态变化通知 ---------------------------------------

    def _dispatch(self) -> None:
        """把锁内记下的状态变化在锁外通知出去：回调里再读 `state` 或调用 `call` 都不会死锁。"""
        with self._lock:
            events, self._events = self._events, []
        for old, new in events:
            if self._listener is not None:
                try:
                    self._listener(old, new)
                except Exception:                    # 通知方的故障不能影响熔断器自己
                    _log.exception("on_state_change 回调抛出异常")
