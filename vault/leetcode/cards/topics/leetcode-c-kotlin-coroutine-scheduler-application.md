---
id: leetcode-c-kotlin-coroutine-scheduler-application
node: topics.uncategorised
type: qa
anki: 1787365292229
tags: [algorithm::cas, algorithm::spmc-queue, algorithm::token-accounting, algorithm::work-stealing, application, case, case::kotlin-coroutine-scheduler, category::runtimes-os, chapter::08, chapter::10, chapter::17, leetcode, system::kotlin, system::kotlinx-coroutines]
---
## Q
Kotlin CoroutineScheduler 为什么同时需要 local queue、work stealing 和 CPU permits？

## A
local queue 降低全局争用并保留 producer affinity；空 worker 随机从其他队列 steal，避免负载倾斜；CPU permits 将执行 CPU tasks 的 worker 限制在 core size。worker 遇到 blocking task 时归还 permit，让补偿 worker 继续跑 CPU work。

**Evidence**

kotlinx.coroutines 官方源码记录了 local/global queues、stale-aware work stealing、SPMC WorkQueue 与 CPU-permit invariant。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FKotlin%20CoroutineScheduler%EF%BC%9A%E6%9C%AC%E5%9C%B0%E9%98%9F%E5%88%97%E3%80%81Work%20Stealing%20%E4%B8%8E%20CPU%20Permit)
