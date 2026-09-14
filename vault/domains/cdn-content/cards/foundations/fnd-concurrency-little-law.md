---
id: fnd-concurrency-little-law
node: foundations.concurrency
type: qa
---
## Q
A service sustains 2,000 requests/s with 150 ms average time in system. Roughly how many requests are in flight, and why is that estimate operationally useful?

## A
By **Little's Law**, `L = λW = 2000 × 0.15 ≈ 300` in-flight requests in steady state. If observed concurrency is far higher, requests are queueing or the latency assumption is wrong. Use the estimate to size connection pools, semaphore limits, memory, and queue alarms—but validate with percentiles because bursts and heavy tails violate the simple steady-state picture.

## Q zh
一个服务稳定处理 2,000 requests/s，平均 system time 为 150 ms。大约有多少 in-flight request？这个估算为什么有运维价值？

## A zh
根据 **Little's Law**，`L = λW = 2000 × 0.15 ≈ 300` 个 in-flight request。如果观测到的 concurrency 高得多，说明请求在 queueing，或 latency 假设错误。这个估算可用于设置 connection pool、semaphore limit、memory 与 queue alarm；但 burst 和 heavy tail 会破坏简单稳态模型，所以仍要用 percentile 验证。
