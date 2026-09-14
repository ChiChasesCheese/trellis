---
id: foundations-utilization-latency-knee
node: foundations.tradeoffs
type: qa
---
## Q
A latency-sensitive service runs its servers at 60% CPU, and finance proposes 90% to cut cost. Why does response time — especially the tail — blow up long before utilization reaches 100%?

## A
Because of **queueing delay**: requests arrive randomly and burstily, so even below saturation, momentary bursts form queues, and the closer utilization ρ gets to 1, the slower those queues drain — waiting time grows roughly like **1/(1−ρ)**, i.e. nonlinearly. Going 60% → 90% doesn't add 30% latency; it can multiply queue wait several times over.

- The tail suffers first: p99 is dominated by requests that landed behind a burst.
- The spare capacity isn't waste — it's the **burst absorber** that keeps queues short.
- Rule of thumb: latency-sensitive services buy headroom (often targeting ~50–70%); only throughput-oriented batch work should run hardware near 100%.

This is the core **latency vs utilization (cost)** trade-off: you can have cheap servers or flat tail latency, not both.

## Q zh
一个延迟敏感的服务把服务器 CPU 跑在 60%，财务提议提到 90% 来省钱。为什么响应时间 — 尤其是尾部 — 会在利用率远未到 100% 之前就急剧恶化？

## A zh
因为**排队延迟（queueing delay）**：请求的到达是随机且突发的，所以即使未饱和，瞬时突发也会形成队列；利用率 ρ 越接近 1，队列排空得越慢 — 等待时间大约按 **1/(1−ρ)** 增长，也就是非线性的。从 60% 提到 90% 不是多 30% 的延迟，而可能把排队等待放大好几倍。

- 尾部最先受伤：p99 由那些排在突发后面的请求主导。
- 空闲容量不是浪费 — 它是让队列保持短的**突发吸收器**。
- 经验法则：延迟敏感的服务要买余量（常见目标约 50–70%）；只有面向吞吐的批处理工作才应该把硬件跑到接近 100%。

这就是核心的**延迟 vs 利用率（成本）**权衡：便宜的服务器和平稳的尾延迟，二者不可兼得。
