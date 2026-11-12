---
slug: tt-rate-limiter-implementation
---
## Q
**手写限流器**｜Medium

实现 `allow(key, now) -> bool`：每个 `key` 每秒最多放行 `r` 次，突发上限 `b`。先用滑动窗口实现，再用令牌桶重写。例：`r = 2` 的滑动窗口对 `t = 0.0, 0.5, 0.9, 1.0` 返回 `True, True, False, True`。

## A
**一句话。** 滑动窗口给每个 key 一个 `deque` 存窗口内放行的时间戳；令牌桶只存 `(令牌, 上次时刻)`，先按流逝时间补令牌并封顶，够 1 个就扣 1 放行。

```python
class SlidingWindowLimiter:
    def __init__(self, rate, window=1.0):
        self.rate, self.window = rate, window
        self.logs = defaultdict(deque)

    def allow(self, key, now):
        log = self.logs[key]
        while log and log[0] <= now - self.window:  # 左开右闭
            log.popleft()
        if len(log) >= self.rate:
            return False
        log.append(now)         # 只记被放行的
        return True

class TokenBucketLimiter:
    def __init__(self, rate, burst):
        self.rate, self.burst = rate, burst
        self.state = {}         # key -> (令牌, 上次补充时刻)

    def allow(self, key, now):
        tokens, last = self.state.get(
            key, (float(self.burst), now))   # 新 key 满桶
        gap = max(0.0, now - last)           # 防时钟回拨
        tokens = min(self.burst, tokens + gap * self.rate)
        ok = tokens >= 1.0
        self.state[key] = (tokens - ok, max(now, last))
        return ok
```

**复杂度。** 时间 `allow` 均摊 `O(1)`，空间每个 key 滑动窗口 `O(r)`、令牌桶 `O(1)`。

**易错点。**
- 弹出条件写成 `<`：`r = 2` 的 `t = 0.0, 0.5, 1.0` 第三个请求得 `False`，应为 `True`。
- 被拒的请求也入队：持续高频请求永远被拒，`r = 1` 的 `t = 0, 0.5, 1.0, 1.5` 应为 `[T, F, T, F]`。
- 令牌补充后不封顶 `b`：空闲很久后一口气放行远超 `b` 个。

**追问。**
- 多实例怎么办？：把 `(tokens, last)` 放 Redis，用 Lua 脚本一次完成读、补、判、扣、写保证原子。
- 固定窗口计数有什么问题？：窗口边界两侧各放 `r` 个，短时间通过 `2r`；滑动窗口没有。

**同模式。** LC 359 日志速率限制器、LC 362 敲击计数器、LC 933 最近的请求次数
