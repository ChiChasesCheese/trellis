---
id: async-queue-backpressure
node: async.queues
type: qa
---
## Q
A queue's depth is growing without bound. Why is "the queue absorbs it" not an answer, and what are your options?

## A
An unbounded queue converts an overload failure into a *latency* failure: messages still get processed, but hours late, and the backlog hides that consumers can't keep up.

Options, in order of preference:
- **Scale consumers** until you hit the downstream bottleneck (often the DB, not the workers).
- **Bound the queue and push back**: reject/slow producers (backpressure) so callers fail fast instead of queuing stale work.
- **Shed load**: drop or downgrade low-value messages; route poison/expired work to a DLQ.
- Alert on **queue depth and consumer lag age**, not just error rate.

## Q zh
队列深度无限增长。为什么"队列吸收它"不是答案，你的选项是什么？

## A zh
无限制的队列将过载故障转换为*延迟*故障：消息仍被处理，但晚几小时，积压隐藏了 consumer 无法跟上的事实。

选项，按优先级顺序：
- **扩展 consumer**，直到你遇到下游瓶颈（通常是 DB，不是 worker）。
- **限制队列并推回**：拒绝/减速生产者（backpressure），使调用者快速失败而不是排队陈旧工作。
- **甩掉负载**：丢弃或降级低价值消息；将有毒/过期工作路由到 DLQ。
- 对**队列深度和 consumer lag age** 告警，不仅仅是错误率。
