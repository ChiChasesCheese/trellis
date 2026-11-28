---
id: hi-c-sd-networking-essentials-b03-py-backoff-breaker
node: sd.core-concepts.networking-essentials.beyond
type: qa
step: 3
---
## Q
**网络基础 · Python：带抖动的退避与熔断器**｜拓展 · 加分

退避和熔断在代码里有多小？时间相关的逻辑怎么才能不用 `sleep` 就测？

## A
**模式。** 注入时钟（injected clock）加转换表状态机：时间由参数传入，熔断器的三个状态靠一张转换规则表达。

```python
import random
import time
from typing import Callable


def backoff(attempt: int, base: float = 0.1, cap: float = 10.0) -> float:
    # 全抖动（full jitter）：在 [0, 上限] 里均匀取值。上限指数增长但有封顶，
    # 随机让一批同时失败的客户端不再同步重试
    return random.uniform(0, min(cap, base * 2**attempt))


class CircuitBreaker:
    def __init__(self, threshold: int = 3, reset_after: float = 30.0,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._threshold, self._reset_after, self._clock = threshold, reset_after, clock
        self._fails = 0
        self._opened_at: float | None = None      # None 表示关闭

    def call(self, fn: Callable[[], str]) -> str:
        if self._opened_at is not None:
            if self._clock() - self._opened_at < self._reset_after:
                raise RuntimeError("open: fail fast")   # 打开：不碰下游，立即失败
            # 超过冷却：半开，放这一次作为探测请求
        try:
            result = fn()
        except Exception:
            self._fails += 1
            if self._opened_at is not None or self._fails >= self._threshold:
                self._opened_at = self._clock()          # 探测失败或达到阈值：（重新）打开
            raise
        self._fails, self._opened_at = 0, None           # 成功：关闭并清零
        return result
```
- **注入时钟：** 测试里传入一个可拨动的 `clock`，不用 `sleep` 就能验证"冷却 30 秒后变半开"，又快又确定。
- **状态靠两个变量表达：** `_opened_at` 为空是关闭；有值且在冷却内是打开；有值且过了冷却就是半开。少一个 `state` 枚举，就少一类状态不一致。
- **半开的缺口：** 这个最小版本在半开时每个调用者都会放行，并发下探测请求不止一个；生产实现要加锁，只放一个探测请求。
- **全抖动与固定退避：** 固定乘以倍数的退避仍让同批客户端同步，全抖动的重试时刻均匀分布，对恢复中的服务最友好。
