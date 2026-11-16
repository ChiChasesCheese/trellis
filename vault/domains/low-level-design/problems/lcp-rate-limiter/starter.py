"""LLM 网关限流器练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `rate_limiter.py`。

产品规则（逐条都有测试）：
 1. `check(client_id, endpoint, limit, window_ms, capacity, refill_rate)` 返回三元组
    `(allowed, remaining, reset_after_ms)`，第三项是 `int`；时间取自 `check` 被调用的那一刻，不由调用方传入。
 2. 状态按 `(client_id, endpoint)` 隔离：换客户端、换接口，都是一份全新的额度。
 3. `remaining` 在本次判定之后计算，只算此刻就能放行的次数；被拒绝时恒为 0。
 4. 被拒绝的请求不消耗额度，也不进入"已放行请求"的历史；它不改变任何 key 的状态。
 5. 策略 A（滑动窗口）：最近 `window_ms` 毫秒内最多放行 `limit` 次；放行时间恰好满一个窗口的旧请求不再计数；
    先清掉过期的再判定；放行后新请求进入窗口；`remaining = limit - 窗口内计数`；
    `reset_after_ms` 是窗口内最老的那条请求退出窗口的时间，放行时也可以大于 0。
 6. 策略 B（令牌桶）：新桶是满的（`capacity` 个令牌），每次放行花 1 个，按 `refill_rate`（个/秒）连续补充，
    不超过 `capacity`；令牌数可以是小数，判定前不取整；放行时 `remaining` 是剩余令牌的整数部分、
    `reset_after_ms` 为 0；被拒且 `refill_rate > 0` 时，`reset_after_ms` 是凑够 1 个整令牌的时间；
    `refill_rate == 0` 时返回任意非负整数。
 7. 毫秒数一律向 0 截断（7.5 ms 记 7），不四舍五入；所有计时值都是非负整数。
 8. 当前策略用不到的参数可以是任意值；当前策略要用的参数不合法（`limit < 1`、`window_ms < 1`、
    `capacity < 1`、`refill_rate < 0`）抛 `ValueError`，且不留任何痕迹。
 9. `stats()` 返回新字典 `{strategy, total_allowed, total_rejected, active_keys}`；计数从 0 开始，
    `active_keys` 是被跟踪的 key 数；一次决策与它的计数更新不可分割，多线程下 `check` 与 `stats` 互相一致。
10. 并发：同一个 key 上 N 个线程同时抢 M 个额度，放行数恰好是 M，不多不少。
11. 长期不用的 key 不能让内存无界增长：回收只能删掉"与新建状态等价"的 key。
12. 时钟可以注入（返回整数纳秒），默认 `time.monotonic_ns`，测试里没有 `sleep`。
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from typing import NamedTuple, TypedDict

Key = tuple[str, str]
Clock = Callable[[], int]

NS_PER_MS = 1_000_000
STRATEGIES = ("policy_a", "policy_b")


class Decision(NamedTuple):
    """一次判定：(是否放行, 判定之后还能立刻放行几次, 多少毫秒后有额度恢复)。"""

    allowed: bool
    remaining: int
    reset_after_ms: int


class StatsDict(TypedDict):
    strategy: str
    total_allowed: int
    total_rejected: int
    active_keys: int


class SlidingWindow:
    """策略 A 的单个 key 的状态。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def decide(self, now: int, limit: int, window_ms: int) -> Decision:
        raise NotImplementedError

    def idle(self, now: int) -> bool:
        raise NotImplementedError


class TokenBucket:
    """策略 B 的单个 key 的状态。"""

    def __init__(self, capacity: int, now: int) -> None:
        raise NotImplementedError

    def decide(self, now: int, capacity: int, rate: float) -> Decision:
        raise NotImplementedError

    def idle(self, now: int) -> bool:
        raise NotImplementedError


class RateLimiter:
    def __init__(self, strategy: str = "policy_a", clock: Clock = time.monotonic_ns) -> None:
        raise NotImplementedError

    def check(self, client_id: str, endpoint: str, limit: int, window_ms: int,
              capacity: int, refill_rate: float) -> Decision:
        raise NotImplementedError

    def policy_a_limit(self, client_id: str, endpoint: str, limit: int, window_ms: int) -> Decision:
        raise NotImplementedError

    def policy_b_limit(self, client_id: str, endpoint: str, capacity: int, refill_rate: float) -> Decision:
        raise NotImplementedError

    def stats(self) -> StatsDict:
        raise NotImplementedError
