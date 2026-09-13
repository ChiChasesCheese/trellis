---
id: cache-stampede-singleflight
node: caching.stampede
type: qa
---
## Q
A hot key expires and 10,000 requests arrive. What does singleflight guarantee, and what does it not guarantee across a fleet?

## A
Within one coordination scope, one caller performs the refresh and waiters share its result. Process-local singleflight still permits one origin fetch **per process or POP**, so a large fleet can stampede. Coordinate at the shield/distributed tier or combine local coalescing with stale serving, jitter, and an origin concurrency cap.

## Q zh
hot key 过期，同时到达 10,000 个请求。singleflight 保证什么？在 fleet 范围内不保证什么？

## A zh
在一个 coordination scope 内，只有一个 caller 执行 refresh，waiter 共享结果。但 process-local singleflight 仍允许 **每个 process 或 POP** 各回源一次，大 fleet 仍可能 stampede。应在 shield/distributed tier 协调，或把 local coalescing 与 stale serving、jitter、origin concurrency cap 组合使用。
