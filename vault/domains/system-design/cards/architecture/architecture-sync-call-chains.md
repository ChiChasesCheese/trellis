---
id: architecture-sync-call-chains
node: architecture.services
type: qa
---
## Q
A request fans through a synchronous chain of 5 services. What does the chain do to availability and latency, and what are the three escapes?

## A
Every synchronous hop is a **serial hard dependency**: availabilities multiply (five 99.9% hops ≈ 99.5% — from 43 min to 3.6 h of monthly downtime, [[reliability-serial-parallel-composition]]), latencies add, tail latencies compound (the chain is as slow as its worst hop per request), and each hop needs its own timeout/retry budget.

Escapes:

- **Collapse boundaries**: if two services always call each other synchronously, they're probably one service.
- **Go async** where the caller doesn't need the answer now (queue/event instead of RPC).
- **Cache / replicate the needed data locally** so the hop disappears from the request path.

Chain depth is an architecture review metric, not an accident.

## Q zh
一个请求扇过 5 个服务的同步链。链对可用性和延迟做什么，三个逃生是什么？

## A zh
每个同步跳是一个**序列硬依赖**：可用性乘以（五个 99.9% hop ≈ 99.5% ——从 43 分钟到每月 3.6 小时停机，[[reliability-serial-parallel-composition]]），延迟相加，尾延迟复合（链和每个请求最坏 hop 一样慢），每个 hop 需要自己的 timeout/retry 预算。

逃生：

- **崩溃边界**：如果两个服务总是同步彼此调用，它们可能是一个服务。
- **异步走**调用者不需要现在答案的地方（queue/event 而不是 RPC）。
- **缓存 / 本地复制所需的数据**所以 hop 从请求路径消失。

链深度是架构审查指标，不是事故。
