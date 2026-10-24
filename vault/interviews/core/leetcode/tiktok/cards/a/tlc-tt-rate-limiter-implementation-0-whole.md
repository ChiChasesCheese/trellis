---
id: tlc-tt-rate-limiter-implementation-0-whole
node: a.tt-rate-limiter-implementation
type: qa
---
## Q
**手写限流器**｜Medium · TikTok 高频

实现限流器 `allow(key, now) -> bool`：限制每个 `key` 每秒最多放行 `r` 次请求，突发上限为 `b`。`now` 是请求到达的时刻（秒，浮点数，一般单调不减），返回 `True` 放行、`False` 拒绝。`1 <= r <= 10^4`，`1 <= b <= 10^6`，key 的数量可达 `10^6`。先用滑动窗口实现，再用令牌桶重写（令牌按 `tokens = min(b, tokens + (now - last) * r)` 补充，一次请求消耗 1 个）。例：`r = 2` 的滑动窗口对 `t = 0.0, 0.5, 0.9, 1.0` 依次返回 `True, True, False, True`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 滑动窗口：每个 key 一个 `deque` 存窗口 `(now - 1, now]` 内被放行的时间戳，先从队首弹出过期的，数量 `< r` 才放行并入队；令牌桶：每个 key 只存 `(剩余令牌, 上次补充时刻)`，请求到来时先按流逝时间补令牌并封顶 `b`，够 1 个就放行并扣 1。

**识别。** 「每个 key 每秒最多 r 次」是限流。两条路线：精确计数（滑动窗口）、额度模型（令牌桶、漏桶）。「突发上限 b」是令牌桶的参数：桶满时可以瞬间放行 `b` 个，之后按 `r` 的速率放行。

**推导。** 暴力：保存每个 key 的全部历史时间戳，每次请求数一遍窗口内的个数，`O(历史长度)`。浪费：窗口之外的时间戳永远不会再被数到，而且被放行的请求最多 `r` 个在窗口里。洞察一：用 `deque` 只留窗口内被放行的时间戳，队首过期就弹，每个时间戳进出一次，均摊 `O(1)`，每个 key 内存 `O(r)`。洞察二：窗口里每个时间戳都存下来是多余的，剩余额度只由「剩多少令牌、上次什么时候算的」两个数决定，惰性补充：不开定时器，下一次请求来时一次算清，每个 key 内存 `O(1)`，还自然支持突发。

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

运行：滑动窗口 `r = 2`，`t = 0.0, 0.5, 0.9, 1.0, 1.4, 1.5, 2.0` → `[True, True, False, True, False, True, True]`；令牌桶 `r = 1`、`b = 3`，`t = 0, 0, 0, 0, 0.5, 1.0, 1.0, 2.5` → `[True, True, True, False, False, True, False, True]`；另一个 key 在 `t = 0` 第一次请求 → `True`；时钟回拨：`TokenBucketLimiter(1, 1)` 对同一个 key 在 `t = 10, 9, 10.5, 11` → `[True, False, False, True]`。

**复杂度。** 滑动窗口：`allow` 均摊 `O(1)`，每个 key 内存 `O(r)`；令牌桶：`allow` 为 `O(1)`，每个 key 内存 `O(1)`。

**易错点。**
- 弹出条件是 `<=`（窗口左开右闭）：写成 `<`，`r = 2` 的 `t = 0.0, 0.5, 1.0` 第三个请求得到 `False`，正确是 `True`。
- 只记录被放行的请求：把被拒的也入队，持续高频请求会永远被拒。`r = 1` 时 `t = 0, 0.5, 1.0, 1.5` 错成 `[True, False, False, False]`，正确是 `[True, False, True, False]`。
- 令牌补充后必须封顶 `b`：不封顶，空闲 100 秒后 `r = 1`、`b = 3` 一口气放行 5 个请求，正确只放行前 3 个。
- 浮点误差：`0.7 - 0.6` 是 `0.09999999999999998`，`r = 10`、`b = 1` 时 `t = 0.6, 0.7` 的第二个请求被拒；时间用整数毫秒可以避开。

**追问。**
- 多实例：把 `(tokens, last)` 放进 Redis，用 Lua 脚本在服务端一次完成「读、补充、判断、扣减、写回」保证原子，时间取 Redis 的 `TIME`，key 形如 `rl:{业务}:{用户}`，加 `PEXPIRE`。
- 固定窗口计数的边界突发：窗口 `[0, 1)` 末尾放 `r` 个、`[1, 2)` 开头再放 `r` 个，短时间内通过 `2r`；滑动窗口没有这个问题。
- 内存：令牌桶里令牌已回满的 key 可以直接删除，下次来时按满桶处理，结果相同。

**同模式。** LC 359 日志速率限制器、LC 362 敲击计数器、LC 933 最近的请求次数、LC 346 数据流中的移动平均值。
