---
id: problems-rate-limiter-token-bucket-lazy-refill
node: problems.components.rate-limiter
type: qa
step: 4
tags: [grown]
---
## Q
限流器（Rate Limiter）里的令牌桶（token bucket）为什么绝不能用后台线程定时补充令牌？正确写法是什么，还要额外防一件什么事？

## A
因为限流是**按 key 隔离**的：一百万个用户就是一百万个桶，用定时器补充等于一百万个定时任务，CPU 全烧在闲置 key 上。

正确写法是**惰性补充**——令牌数在每次判定时用「距上次记账过了多久」现算，闲置 key 一分钱不花：

```python
def _tokens_at(self, now: float) -> float:
    if self._stamp is None:
        return self.capacity
    elapsed = max(0.0, now - self._stamp)
    return min(self.capacity, self._tokens + elapsed * self._rate)
```

要额外防的是**时钟倒退**：`now - stamp` 为负会凭空造出令牌，把 `elapsed` 夹到 0 以上是唯一安全的处理。时钟本身也要选 `time.monotonic` 而不是 `time.time`，后者会被 NTP 往回拨。

顺带一提，令牌桶把瞬时容量 `capacity` 和持续速率 `limit/window` 分开，于是能表达「每分钟 60 次，但一口气最多 5 次」——这是其他三种算法做不到的。
