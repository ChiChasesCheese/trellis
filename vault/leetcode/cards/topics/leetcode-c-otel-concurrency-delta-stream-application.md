---
id: leetcode-c-otel-concurrency-delta-stream-application
node: topics.uncategorised
type: qa
anki: 1787361363697
tags: [algorithm::difference-array, algorithm::event-sourcing, algorithm::prefix-sum, application, case, case::otel-concurrency-delta-stream, category::distributed-streaming, chapter::14, leetcode, system::opentelemetry, system::stream-processor]
---
## Q
为什么在线并发量可以视为 start/end delta 的 prefix sum？最大故障模式是什么？

## A
start 让 active count +1，end 让它 -1，累计值就是当前并发。最大风险是事件丢失、重复或乱序造成永久漂移，因此要用 span/session ID 幂等并定期 reconciliation。

**Evidence**

OpenTelemetry 官方模型定义 spans 与 cumulative/delta metrics；该 case 把生命周期事件建模为可重放差分流。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FOpenTelemetry%20%E5%B9%B6%E5%8F%91%E4%BC%9A%E8%AF%9D%EF%BC%9AStart-End%20%E5%B7%AE%E5%88%86%E6%B5%81)
