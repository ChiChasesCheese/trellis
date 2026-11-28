---
id: hi-c-lld-rate-limiter-b02-gcra
node: lld.problem-breakdowns.rate-limiter.beyond
type: qa
step: 3
---
## Q
**限流器 · 拓展：GCRA，每键只存一个浮点数的令牌桶**｜拓展 · 加分

令牌桶每键要存令牌数和上次结算时间。有没有每键只存一个数的等价写法？

## A
**模式。** 通用信元速率算法（GCRA，Generic Cell Rate Algorithm）：不存"桶里有几个令牌"，而存"理论到达时间 TAT"。

```python
import math


class GCRA:
    """等价于令牌桶，但每个键只存一个浮点数：理论到达时间 tat（毫秒）。"""

    def __init__(self, rate_per_s: float, burst: int, clock) -> None:
        self._t = 1000 / rate_per_s              # 发放间隔：每个令牌占多少毫秒
        self._tau = (burst - 1) * self._t        # 突发容忍：允许 tat 比 now 超前多少
        self._clock = clock
        self._tat: dict[str, float] = {}         # 状态就这一张表（并发时仍要每键加锁）

    def allow(self, key: str) -> tuple[bool, int | None]:
        now = self._clock()
        tat = max(self._tat.get(key, now), now)  # 空闲后 tat 追上当前时间，相当于桶满
        if tat - now > self._tau:                # 超前太多 = 桶空
            return False, math.ceil(tat - now - self._tau)   # 等到超前量回落到容忍线以内
        self._tat[key] = tat + self._t           # 放行：把"下一个令牌的时间"往后推一格
        return True, None


t = [0.0]
g = GCRA(rate_per_s=1, burst=3, clock=lambda: t[0])
assert [g.allow("k")[0] for _ in range(4)] == [True, True, True, False]   # 突发 3 个
assert g.allow("k") == (False, 1000)             # 要再等 1 秒才补回一个
t[0] = 1000
assert g.allow("k") == (True, None)
```
- **思路：** 每放行一个请求，就把"下一个请求按速率应该到达的时间"往后推一格（`tat += 间隔`）。`tat` 超前 `now` 越多，说明近期用得越多；超前量超过突发容忍 `tau` 就拒绝。
- **等价于令牌桶：** 容量 = `burst`，速率相同时，放行与重试时间逐步和令牌桶一致（整数毫秒下可以逐条验证）。
- **好处：** 每键只有一个数，更新是"取、比较、写回"，很适合放进 Redis 的原子脚本；不需要单独的"结算"步骤。Redis 的限流模块 `redis-cell` 用的就是 GCRA。
- **代价：** 不如令牌桶直观，面试里要先讲令牌桶再说"这是它的等价变形"，别直接上 GCRA。
- **何时不用：** 单进程内存版，两个数的令牌桶已经够清楚。
