---
id: hl-hc02-what-asked
node: problems.hc02-merge-k-streams
type: qa
step: 1
---
## Q
合并 K 路有序流（merge k sorted streams）题分哪四个 Part？每个 Part 加了什么要求？

## A
核心工具是**最小堆**（min-heap）：k 个序列各自的「队首」里最小的就是下一个输出。

- **Part 1**：合并 k 个各自升序（允许相等）的序列，相等时**序列编号小的在前**（稳定）。`k` 可为 0，序列可为空；元素 `null` → `NullPointerException`；输入不得被修改；不升序抛 `UnsortedInputException(stream, position)`。例：`[[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`。
- **Part 2**：**惰性 / 流式**。`mergeIterators` 构造时不碰任何 source，输出一个元素后下一个推迟到下一次调用才取；可对两个无限序列取前 10 个。
- **Part 3**：**多线程、非阻塞、有界**。每个 source 一个虚拟线程生产者，放进各自的有界队列；`tryNext()` 返回 `Ready / Pending / Done`。
- **Part 4**：**结构化并发**。`mergeAll` 把所有生产者和合并任务放进 `StructuredTaskScope.ShutdownOnFailure`，一个失败其余被中断。

Part 1 是 LeetCode 23 的变体，门槛是想到堆并说出 O(N log k)；拉开差距的是惰性、稳定、Pending 的含义、背压、永不无限阻塞、失败传播。
