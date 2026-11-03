---
id: hi-pt-rate-limiter-system-2-decision
node: qb.lld.rate-limiter-system.points
type: qa
step: 2
---
## Q
**限流器（单机类设计） · 返回 Decision 而不是布尔**｜必会 · 出自：限流器（单机类设计） › 需求

`allow(key)` 为什么不只返回布尔值？

## A
**要点。** 还要返回剩余额度 `remaining` 和被拒后应多久再试 `retry_after`，用于 `Retry-After` 响应头。
**例。** 令牌桶被拒时 `(1 - 令牌数) / 速率` 是下一个令牌到来的等待时间；滑动窗口日志是最早那条过期的时刻。
