---
id: hi-c-lld-scarcity-b03-py-token-bucket
node: lld.concurrency.scarcity.beyond
type: qa
step: 3
---
## Q
**并发稀缺资源 · Python：并发上限与速率上限是两回事**｜拓展 · 加分

信号量限制"同时多少个"，为什么限制"每秒多少个"要用令牌桶？令牌桶怎么写、怎么测？

## A
**模式。** 令牌桶（token bucket）加注入时钟。

```python
import threading
import time
from typing import Callable


class TokenBucket:
    def __init__(self, rate: float, burst: float, clock: Callable[[], float] = time.monotonic) -> None:
        self._rate, self._burst, self._clock = rate, burst, clock
        self._tokens, self._last = burst, clock()
        self._lock = threading.Lock()

    def allow(self, cost: float = 1.0) -> bool:
        with self._lock:                                   # 补充与扣减必须是一个整体
            now = self._clock()
            self._tokens = min(self._burst, self._tokens + (now - self._last) * self._rate)
            self._last = now
            if self._tokens >= cost:
                self._tokens -= cost
                return True
            return False


t = [0.0]
tb = TokenBucket(rate=10, burst=5, clock=lambda: t[0])
assert [tb.allow() for _ in range(6)] == [True] * 5 + [False]     # 突发 5 个，第 6 个被拒
t[0] = 0.25                                                       # 过了 0.25 秒，补回 2.5 个令牌
assert [tb.allow() for _ in range(3)] == [True, True, False]
```
- **区别：** 信号量的许可在操作结束时归还；令牌随时间补充，与操作是否结束无关
- **惰性补充：** 不开后台线程，每次 `allow` 时按流逝的时间计算应补多少，省线程
- **`burst`：** 桶容量决定允许的突发大小，`rate` 决定长期速率
- **并发：** 补充与扣减是读改写，要在锁内一起完成
- **何时不用：** 要限制的是同时在途数量时，用信号量
