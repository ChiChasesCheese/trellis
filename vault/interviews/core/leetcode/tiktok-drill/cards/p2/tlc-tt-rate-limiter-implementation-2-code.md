---
id: tlc-tt-rate-limiter-implementation-2-code
node: p2.tt-rate-limiter-implementation
type: qa
step: 2
---
## Q
**手写限流器**｜写出 Python 实现

写两个类，都有 `allow(key, now) -> bool`：`SlidingWindowLimiter(rate, window)` 在窗口 `(now - window, now]` 内最多放行 `rate` 次；`TokenBucketLimiter(rate, burst)` 桶容量 `burst`、每秒补 `rate` 个令牌、一次请求扣 1 个，新 key 从满桶开始。`now` 是秒数（浮点数），`1 <= rate <= 10^4`，`1 <= burst <= 10^6`，key 数量可达 `10^6`，时钟可能回拨。

## A
**思路。** 滑动窗口用 `deque` 存窗口内被放行的时间戳，先弹出过期的再判断数量；令牌桶每个 key 只存剩余令牌数和上次补充的时刻，请求到来时一次性补齐、封顶、判断、扣减。

```python
from collections import defaultdict, deque


class SlidingWindowLimiter:
    """滑动窗口日志：每个 key 最多保留窗口内被放行的时间戳。"""

    def __init__(self, rate: int, window: float = 1.0) -> None:
        self.rate, self.window = rate, window
        self.logs: defaultdict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str, now: float) -> bool:
        log = self.logs[key]
        while log and log[0] <= now - self.window:   # 窗口是 (now - window, now]
            log.popleft()
        if len(log) >= self.rate:
            return False
        log.append(now)                               # 只记录被放行的请求
        return True


class TokenBucketLimiter:
    """令牌桶：桶容量 burst，每秒补 rate 个令牌，一次请求消耗 1 个。"""

    def __init__(self, rate: float, burst: int) -> None:
        self.rate, self.burst = rate, burst
        self.state: dict[str, tuple[float, float]] = {}      # key -> (剩余令牌, 上次补充时刻)

    def allow(self, key: str, now: float) -> bool:
        tokens, last = self.state.get(key, (float(self.burst), now))   # 新 key 从满桶开始
        tokens = min(self.burst, tokens + max(0.0, now - last) * self.rate)   # max(0, …) 防时钟回拨
        ok = tokens >= 1.0
        self.state[key] = (tokens - 1.0 if ok else tokens, max(now, last))
        return ok
```

运行：滑动窗口 `rate = 2`，`t = 0.0, 0.5, 0.9, 1.0, 1.4, 1.5, 2.0` → `[True, True, False, True, False, True, True]`；令牌桶 `rate = 1`、`burst = 3`，`t = 0, 0, 0, 0, 0.5, 1.0, 1.0, 2.5` → `[True, True, True, False, False, True, False, True]`；另一个 key 在 `t = 0` 第一次请求 → `True`；`TokenBucketLimiter(1, 1)` 对同一个 key 在 `t = 10, 9, 10.5, 11` → `[True, False, False, True]`。

**复杂度。** 滑动窗口：`allow` 均摊 `O(1)`（每个时间戳入队、出队各一次），每个 key 内存 `O(rate)`；令牌桶：`O(1)` 时间、每个 key 内存 `O(1)`。

**写法要点。**
- `defaultdict(deque)` 让首次出现的 key 自动得到空队列，省掉 `if key not in` 判断。
- `dict.get(key, 默认元组)` 在新 key 时直接给出「满桶、上次时刻就是现在」的初始状态，同一行完成初始化。
- `min(burst, …)` 封顶，`max(0.0, now - last)` 防回拨，`max(now, last)` 让「上次时刻」不倒退：三处各防一类错误。
- 不开线程、不用定时器：令牌是惰性补充的，没有请求的 key 不花任何 CPU。
