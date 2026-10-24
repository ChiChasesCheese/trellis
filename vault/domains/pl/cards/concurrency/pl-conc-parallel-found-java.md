---
id: pl-conc-parallel-found-java
node: concurrency.parallelism
type: qa
step: 2
---
## Q
Java 的 Stream、并行流（`.parallel()`）和 `ForkJoinPool` 是什么？一个 `.parallel()` 做了什么？

## A
**Stream** 是 Java 8 起的“数据流水线”抽象：从一个数据源（集合、数组、数字范围）出发，串联中间操作（`filter`、`map`），最后用终端操作（`sum`、`collect`）产出结果。操作是**惰性**的：直到终端操作才真正执行。

```java
long total = LongStream.range(0, N).mapToDouble(i -> Math.sqrt(i) * Math.sin(i)).sum();
```
**并行流**：在流上调用 `.parallel()`（或集合的 `parallelStream()`），流水线的执行方式从“一个线程顺序处理”变成“拆成多块，多线程同时处理，最后合并”。写法不变：
```java
LongStream.range(0, N).parallel().mapToDouble(...).sum();
```

底层是 **`ForkJoinPool`**：一个工作窃取的线程池。默认使用整个 JVM 共享的**公共池**（`ForkJoinPool.commonPool()`），线程数是核数减 1（本机 12 核时为 11，因为调用线程自己也参与）。`.parallel()` 的流程：
1. 数据源把自己递归地一分为二（`Spliterator`），直到块足够小；
2. 每一块作为一个任务提交到池，空闲线程会从别的线程队列里“偷”任务；
3. 各块算出部分结果，再按结合律合并（求和就是相加）。

实测（1 亿个元素，`sqrt(i) * sin(i)` 求和，一次测量）：顺序 2553 毫秒，并行 343 毫秒，约 7.4 倍。

使用前提：每个元素的处理**无副作用、彼此独立**，合并操作满足**结合律**。如果在 `forEach` 里往普通的 `ArrayList` 里添加元素，会丢失数据（实测 10 万个只剩约 14000 个）；要用 `collect` 这样的归约操作。
