---
id: uth-java-priorityqueue-2-scheduled
node: java.priorityqueue
type: qa
step: 2
---
## Q
**定时线程池怎么按时间取任务**｜Java · OpenJDK 25

`ScheduledThreadPoolExecutor` 里一堆延迟任务，工作线程怎么知道下一个该跑哪个、要睡多久？

## A
**结构。** 任务队列 `DelayedWorkQueue` 是数组上的最小堆，按触发时间排序，时间相同按提交序号（`sequenceNumber`）排，先提交的先跑。

**细节。**

- 堆顶任务的延迟最小，线程只对堆顶睡眠。
- 每个任务记着自己的 `heapIndex`，取消时不用线性查找，O(log n) 就能从堆中摘掉；默认 `removeOnCancel` 为 `false`，取消的任务要等到期才清除。
- 只有一个领头线程做限时等待，其余线程无限等待。

**为什么。** 堆让取最近到期的任务是 O(1)，插入 O(log n)。`DelayQueue` 也是包着一个 `PriorityQueue`。

**对应 LeetCode：** LC 253 会议室 II · LC 1834 单线程 CPU
