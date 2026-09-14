---
id: leetcode-c-flink-sliding-windows-application
node: topics.uncategorised
type: qa
anki: 1787361363273
tags: [algorithm::incremental-aggregation, algorithm::sliding-window, algorithm::watermark, application, case, case::flink-sliding-windows, category::distributed-streaming, chapter::01, leetcode, system::apache-flink]
---
## Q
Flink 的 sliding window 为什么会让一个事件属于多个窗口？如何避免每次扫描全部事件？

## A
size 大于 slide 时，事件会落入多个重叠区间。用增量 Reduce/Aggregate 维护小状态，而不是每次重扫窗口；watermark 决定 event-time 窗口的触发和清理。

**Evidence**

Flink 官方窗口文档定义 sliding window 的 size/slide、重叠归属、incremental aggregation 与 watermark 行为。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FFlink%20%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%EF%BC%9A%E9%87%8D%E5%8F%A0%E5%88%86%E6%A1%B6%E4%B8%8E%E5%A2%9E%E9%87%8F%E8%81%9A%E5%90%88)
