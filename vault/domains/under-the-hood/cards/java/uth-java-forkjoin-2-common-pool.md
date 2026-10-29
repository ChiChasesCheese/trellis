---
id: uth-java-forkjoin-2-common-pool
node: java.forkjoin
type: qa
step: 2
---
## Q
**parallelStream 的线程从哪来**｜Java · OpenJDK 25

`parallelStream()`、`CompletableFuture.supplyAsync` 不传线程池时，任务在哪个线程池里跑？有几个线程？

## A
**结构。** 全进程共享的公共池 `ForkJoinPool.commonPool()`，`CompletableFuture` 的默认池也是它（`asyncCommonPool`）。

**细节。**

- 默认并行度是 `availableProcessors() - 1`；本机 12 核实测为 11，调用方线程也会参与干活。
- 线程名是 `ForkJoinPool.commonPool-worker-N`，用不到时会被慢慢回收。
- 可用系统属性 `java.util.concurrent.ForkJoinPool.common.parallelism` 调整。

**为什么。** 所有并行流共用一个池，避免每个调用各建线程池，线程数受控。

**坑。** 共享意味着一个人堵住大家都慢，所以 CPU 密集任务才适合放进去。

**对应 LeetCode：** LC 912 排序数组 · LC 4 寻找两个正序数组的中位数
