---
id: hl-sdrun-quiz-kafka-where
node: system-design.how-to-run
type: qa
step: 36
---
## Q
口头自测：为什么 Kafka 不该出现在 tick-to-trade 路径上？它应该出现在哪？100 MB/s 的堆分配率意味着什么？

## A
- Kafka 每一跳是 ms 级，p99 就比整个微秒级预算大几个数量级；它应出现在**侧链路**：研究、监控、对账、落盘等离线或准实时场景。
- 100 MB/s 分配率意味着年轻代 1 GB 每 10 s 一次 minor GC，停顿几 ms 到几十 ms，超出 10 µs 预算三个数量级。「换更好的 GC」不是完整答案：ZGC 停顿亚毫秒，但仍有读屏障和并发线程抢缓存，对 µs 级仍不够；根治是稳态分配率约为 0。
