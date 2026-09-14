---
id: leetcode-c-flink-monotonic-queue-application
node: topics.uncategorised
type: qa
anki: 1787361363375
tags: [algorithm::monotonic-deque, algorithm::sliding-window-maximum, algorithm::stateful-operator, application, case, case::flink-monotonic-queue, category::distributed-streaming, chapter::03, leetcode, system::apache-flink]
---
## Q
在 Flink 自定义滚动最大值 operator 中，单调队列删掉尾部较小元素为什么安全？

## A
新值更晚且不小于这些尾部元素；在它过期前，那些旧小值不可能再成为窗口最大值。队首过期时按时间淘汰，因此每个元素只进出一次，均摊 O(1)。

**Evidence**

Flink 官方 ProcessFunction 文档提供 keyed state/timer；单调队列不变量决定应用只需保存仍可能成为最大值的候选。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FFlink%20%E6%BB%9A%E5%8A%A8%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%9A%E5%8D%95%E8%B0%83%E9%98%9F%E5%88%97%E5%8E%8B%E7%BC%A9%E7%AA%97%E5%8F%A3%E7%8A%B6%E6%80%81)
