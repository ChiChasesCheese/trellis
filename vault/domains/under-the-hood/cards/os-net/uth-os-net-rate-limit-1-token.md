---
id: uth-os-net-rate-limit-1-token
node: os-net.rate-limit
type: qa
step: 1
---
## Q
**令牌桶：不用定时器补令牌**｜Guava · RateLimiter · 33.7

Guava 的 `RateLimiter` 没有后台线程往桶里加令牌，它怎么知道桶里还剩多少？

## A
**结构。** `SmoothBursty` 只存两个值：`storedPermits`（桶里的令牌）和 `nextFreeTicketMicros`（下一张票最早能发放的时间）。

**细节。**

- 每次请求先 `resync`：若现在晚于 `nextFreeTicketMicros`，按空闲了多久一次算出新令牌，上限 `maxPermits`，默认是 1 秒的量
- 令牌够就直接扣；不够的部分，按 `1/速率` 把 `nextFreeTicketMicros` 往后推
- 先放行后付账：大请求立刻通过，是下一个请求为它等待

**为什么。** 令牌数是时间的函数，用到时再算（惰性补充），不需要定时器，状态只有两个数字。

**对应 LeetCode：** LC 359 日志速率限制器 · LC 933 最近的请求次数
