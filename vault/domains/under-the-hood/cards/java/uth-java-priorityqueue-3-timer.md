---
id: uth-java-priorityqueue-3-timer
node: java.priorityqueue
type: qa
step: 3
---
## Q
**Timer 为什么不如定时线程池**｜Java · OpenJDK 25

`java.util.Timer` 内部用什么保存任务？一个任务抛异常会发生什么？

## A
**背景。** `Timer` 是最早的定时器：一个线程专门按时间顺序执行任务，任务按触发时间放在一个堆里。简单，但所有任务共用这一个线程。

**结构。** `TaskQueue`：一个以 `nextExecutionTime` 排序的平衡二叉堆，从下标 1 开始存，初始数组 128 个槽。

**细节。**

- 加入、取出最小是 O(log n)，看堆顶是 O(1)。
- 一个 `Timer` 只有一个执行线程。任务抛出未捕获异常，线程就终止，之后再调度抛 `IllegalStateException`（实测）。
- 慢任务会「霸占」线程，推迟后面所有任务。

**为什么。** 单线程加堆足够简单，但一个任务出错就拖垮整个 `Timer`；线程池版本每个任务的异常只影响自己的 `Future`。

**坑。** 新代码直接用 `ScheduledThreadPoolExecutor`。

**对应 LeetCode：** 无直接对应的题
