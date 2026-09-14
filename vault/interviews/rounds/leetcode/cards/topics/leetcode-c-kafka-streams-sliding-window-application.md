---
id: leetcode-c-kafka-streams-sliding-window-application
node: topics.uncategorised
type: qa
anki: 1787361363572
tags: [algorithm::event-time, algorithm::sliding-window, algorithm::state-store, application, case, case::kafka-streams-sliding-window, category::distributed-streaming, chapter::01, leetcode, system::kafka-streams]
---
## Q
Kafka Streams SlidingWindows 与普通 tumbling window 的边界有什么不同？

## A
它用两条记录的最大时间差定义窗口，窗口会因记录到达而产生，不依赖固定整点边界。状态按 key 保存在 store 中，grace period 决定迟到记录还能否更新结果。

**Evidence**

Kafka 官方 SlidingWindows Javadoc 明确定义 time difference、before/after windows 与 grace period。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FKafka%20Streams%20%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%EF%BC%9A%E6%97%B6%E9%97%B4%E5%B7%AE%E8%BE%B9%E7%95%8C%E4%B8%8E%E4%B9%B1%E5%BA%8F)
