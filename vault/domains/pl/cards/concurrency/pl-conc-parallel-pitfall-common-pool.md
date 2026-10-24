---
id: pl-conc-parallel-pitfall-common-pool
node: concurrency.parallelism
type: qa
step: 10
---
## Q
Java 并行流里放阻塞调用（调用远程服务、`sleep`）为什么会出问题？公共线程池（common pool）的陷阱是什么？

## A
并行流默认使用整个 JVM 共享的 `ForkJoinPool.commonPool()`，线程数是 CPU 核数减 1（本机是 11）。它是为 **CPU 密集、不阻塞**的任务设计的。

实验：在并行流里对 100 个元素各 `Thread.sleep(100)`（模拟一次 100 毫秒的远程调用）：
```java
IntStream.range(0, 100).parallel().forEach(i -> {
    try { Thread.sleep(100); } catch (Exception e) {}
});
```
输出：`100 blocking tasks (100 ms each) in parallel stream: 2.15 s`。理论值是 100 个任务 ÷ 12 个并发 ≈ 9 轮，约 0.9 秒；本机 100 毫秒的睡眠实际约 0.2 秒，所以测得 2 秒多。如果不并行而是每个任务一个虚拟线程，所有睡眠重叠，总时间约一次睡眠的时间。关键是：**并发度被限制在核数，而不是任务数**。

更危险的是副作用：
1. **公共池是全进程共享的。** 一个请求的并行流把 11 个线程全部堵在远程调用上，别处的所有并行流和 `CompletableFuture.supplyAsync`（默认也用公共池）一起饿死。症状是延迟毛刺，而 CPU 使用率很低。
2. **小数据更慢**：1000 个元素的并行流重复 2000 次，顺序 12 毫秒，并行 36 毫秒（一次测量），因为拆分、调度、合并的固定开销大于计算。
3. **共享可变状态**：在 `forEach` 里往 `ArrayList` 里 `add`，会丢元素。

对策：
- 阻塞型的 I/O 用虚拟线程或独立的线程池，不要放在并行流里。
- 要使用并行流，必须是纯函数式、无阻塞的 CPU 计算；需要隔离时，在自定义的 `ForkJoinPool` 里执行 `pool.submit(() -> stream.parallel()...)`。
- 对延迟敏感的服务，默认不用并行流，除非有基准测试证明有利。
