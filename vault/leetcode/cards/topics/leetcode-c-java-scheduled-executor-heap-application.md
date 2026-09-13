---
id: leetcode-c-java-scheduled-executor-heap-application
node: topics.uncategorised
type: qa
anki: 1787361364348
tags: [algorithm::delay-queue, algorithm::min-heap, algorithm::sequence-number, application, case, case::java-scheduled-executor-heap, category::runtimes-os, chapter::08, chapter::17, leetcode, system::openjdk-scheduledthreadpoolexecutor]
---
## Q
ScheduledThreadPoolExecutor 为什么需要 deadline heap 和 sequence number？周期任务如何避免无限预生成？

## A
heap 让最早 deadline 位于队首；相同 deadline 用递增 sequence number 保持提交 FIFO。周期任务完成一次后计算下一 deadline，把同一逻辑任务重新入队。

**Evidence**

Java 官方 API 与 OpenJDK source 定义 DelayedWorkQueue heap、time、sequenceNumber 和 periodic re-enqueue。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FJava%20ScheduledThreadPoolExecutor%EF%BC%9ADelay%20Heap%20%E4%B8%8E%20Worker%20Queue)
