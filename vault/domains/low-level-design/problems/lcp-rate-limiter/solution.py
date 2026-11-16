"""LLM 网关限流器（Rate Limiter）：进程内、按 (client_id, endpoint) 隔离、两种策略二选一。
设计：策略 A（滑动窗口）和策略 B（令牌桶）各是一个只管"一个 key 的状态"的小类，
`RateLimiter` 负责按 key 找状态、在同一把锁里完成"读时钟 → 判定 → 记账 → 更新统计"；
时间一律用整数纳秒，毫秒数由整数除法截断得到，避免浮点把 6500 算成 6499；
被拒绝的请求不写任何状态，也不新建 key；长时间不用的 key 在字典翻倍时被批量清理。
"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable
from typing import NamedTuple, TypedDict

Key = tuple[str, str]
Clock = Callable[[], int]
"""时钟：返回单调递增的整数纳秒；生产用 `time.monotonic_ns`，测试注入假时钟。"""

NS_PER_MS = 1_000_000
STRATEGIES = ("policy_a", "policy_b")
SWEEP_FLOOR = 4096
"""字典至少长到这个规模才会触发一次整理，小流量下永远不扫。"""


def _require_window(limit: int, window_ms: int) -> None:
    """策略 A 的前置条件；不合法就在碰任何状态之前抛出。"""
    if limit < 1:
        raise ValueError(f"policy_a needs limit >= 1, got {limit!r}")
    if window_ms < 1:
        raise ValueError(f"policy_a needs window_ms >= 1, got {window_ms!r}")


def _require_bucket(capacity: int, refill_rate: float) -> None:
    """策略 B 的前置条件；写成 `not >= 0`，让 NaN 也被拒。"""
    if capacity < 1:
        raise ValueError(f"policy_b needs capacity >= 1, got {capacity!r}")
    if not refill_rate >= 0:
        raise ValueError(f"policy_b needs refill_rate >= 0, got {refill_rate!r}")


class Decision(NamedTuple):
    """一次判定：(是否放行, 判定之后还能立刻放行几次, 多少毫秒后有额度恢复)。是普通元组的子类。"""

    allowed: bool
    remaining: int
    reset_after_ms: int


class StatsDict(TypedDict):
    strategy: str
    total_allowed: int
    total_rejected: int
    active_keys: int


class SlidingWindow:
    """策略 A 的单个 key：窗口内被放行请求的时间戳（升序）。不变量：长度只在放行时增加。
    还记着这个 key 最近一次用的窗口长度：判断它是否闲置只能用它自己的参数。"""

    def __init__(self) -> None:
        self._stamps: deque[int] = deque()
        self._window_ms = 0

    def decide(self, now: int, limit: int, window_ms: int) -> Decision:
        self._window_ms = window_ms
        window = window_ms * NS_PER_MS
        stamps = self._stamps
        while stamps and now - stamps[0] >= window:  # 恰好满一个窗口的请求已不再计数
            stamps.popleft()
        allowed = len(stamps) < limit
        if allowed:
            stamps.append(now)  # 只有放行才留下痕迹
        remaining = limit - len(stamps) if allowed else 0
        reset_ns = stamps[0] + window - now
        return Decision(allowed, remaining, max(0, reset_ns) // NS_PER_MS)

    def idle(self, now: int) -> bool:
        return not self._stamps or now - self._stamps[-1] >= self._window_ms * NS_PER_MS


class TokenBucket:
    """策略 B 的单个 key：可以是小数的令牌数，新建时是满的，用到时才按流逝时间补。
    还记着这个 key 最近一次用的容量和补充速率：判断它是否闲置只能用它自己的参数。"""

    def __init__(self, capacity: int, now: int) -> None:
        self._tokens = float(capacity)
        self._stamp = now
        self._capacity, self._rate = capacity, 0.0

    def _refilled(self, now: int, capacity: int, rate: float) -> float:
        elapsed_s = max(0, now - self._stamp) / 1e9  # 时钟倒退按没有流逝处理
        return min(float(capacity), self._tokens + elapsed_s * rate)

    def decide(self, now: int, capacity: int, rate: float) -> Decision:
        self._capacity, self._rate = capacity, rate
        tokens = self._refilled(now, capacity, rate)
        if tokens >= 1.0:
            self._tokens, self._stamp = tokens - 1.0, now
            return Decision(True, int(self._tokens), 0)
        if rate <= 0:  # 永不恢复：README 允许任意非负整数
            return Decision(False, 0, 0)
        return Decision(False, 0, int((1.0 - tokens) / rate * 1000))

    def idle(self, now: int) -> bool:
        return self._refilled(now, self._capacity, self._rate) >= self._capacity


class RateLimiter:
    """按 (client_id, endpoint) 隔离的限流器。一把锁罩住整个判定与计数，所以决策和统计互相一致。"""

    def __init__(self, strategy: str = "policy_a", clock: Clock = time.monotonic_ns) -> None:
        if strategy not in STRATEGIES:
            raise ValueError(f"Unknown strategy: {strategy}")
        self.strategy = strategy
        self._clock = clock
        self._lock = threading.Lock()
        self._state: dict[Key, SlidingWindow | TokenBucket] = {}
        self._total_allowed = 0
        self._total_rejected = 0
        self._sweep_at = SWEEP_FLOOR

    def check(self, client_id: str, endpoint: str, limit: int, window_ms: int,
              capacity: int, refill_rate: float) -> Decision:
        """按当前策略判定一次请求。时间取自锁内读到的时钟，不由调用方传入。"""
        if self.strategy == "policy_a":
            _require_window(limit, window_ms)
        else:
            _require_bucket(capacity, refill_rate)
        with self._lock:
            now = self._clock()  # 必须在锁内读：先读后拿锁会让时间戳乱序
            if self.strategy == "policy_a":
                result = self._policy_a(now, client_id, endpoint, limit, window_ms)
            else:
                result = self._policy_b(now, client_id, endpoint, capacity, refill_rate)
            if result.allowed:
                self._total_allowed += 1
            else:
                self._total_rejected += 1
            if len(self._state) >= self._sweep_at:
                self._sweep(now)
            return result

    def policy_a_limit(self, client_id: str, endpoint: str, limit: int, window_ms: int) -> Decision:
        """直接跑策略 A（持锁、读时钟，但不计入统计）。"""
        with self._lock:
            return self._policy_a(self._clock(), client_id, endpoint, limit, window_ms)

    def policy_b_limit(self, client_id: str, endpoint: str, capacity: int, refill_rate: float) -> Decision:
        """直接跑策略 B（持锁、读时钟，但不计入统计）。"""
        with self._lock:
            return self._policy_b(self._clock(), client_id, endpoint, capacity, refill_rate)

    def _policy_a(self, now: int, client_id: str, endpoint: str, limit: int, window_ms: int) -> Decision:
        state = self._state.setdefault((client_id, endpoint), SlidingWindow())
        assert isinstance(state, SlidingWindow)
        return state.decide(now, limit, window_ms)

    def _policy_b(self, now: int, client_id: str, endpoint: str, capacity: int, rate: float) -> Decision:
        state = self._state.setdefault((client_id, endpoint), TokenBucket(capacity, now))
        assert isinstance(state, TokenBucket)
        return state.decide(now, capacity, rate)

    def _sweep(self, now: int) -> None:
        """删掉"和新建状态等价"的 key：按它自己的参数，窗口全过期，或令牌桶已满。门槛按整理后的规模翻倍。"""
        for key in [k for k, s in self._state.items() if s.idle(now)]:
            del self._state[key]
        self._sweep_at = max(SWEEP_FLOOR, 2 * len(self._state))

    def stats(self) -> StatsDict:
        """在同一把锁里一次读齐，返回的是新字典，调用方改它不影响限流器。"""
        with self._lock:
            return {"strategy": self.strategy, "total_allowed": self._total_allowed,
                    "total_rejected": self._total_rejected, "active_keys": len(self._state)}


if __name__ == "__main__":
    ms = 0
    limiter = RateLimiter("policy_a", clock=lambda: ms * NS_PER_MS)
    for ms in (0, 3000, 3500):
        print(ms, limiter.check("alice", "/v1/chat", 2, 10000, 0, 0.0))
