---
id: pl-conc-green-threads-best-practice
node: concurrency.green-threads
type: qa
step: 8
---
## Q
有了便宜的 goroutine 和虚拟线程之后，资深工程师在并发量、池化和阻塞处理上的做法和 OS 线程时代有什么不同？

## A
**一句话**：任务模型从「少量昂贵线程 + 任务队列」变成「一个任务一个线程」，限流则不再靠线程池大小，而靠显式的信号量。

实测（一次测量）：10 万个各睡 1 秒的任务，Go 总耗时 1.08 秒，Java 虚拟线程 1.48 秒；而 Java 200 线程的固定线程池处理 2000 个同样的任务就要 11.35 秒。线程池大小曾经是「并发度上限」，现在它成了人为瓶颈。

做法：
1. **不要池化**虚拟线程和 goroutine。每个任务一个：Java `newVirtualThreadPerTaskExecutor`，Go 直接 `go`。池化它们等于给廉价资源加了排队。
2. **并发度用信号量或带容量的 channel 限制**，上限由下游（数据库连接、第三方限流）决定，而不是线程数。
3. **每个 goroutine 都要有退出路径**：传 `context.Context`，在阻塞点 `select` 监听 `ctx.Done()`，由父级等待（`WaitGroup`、`errgroup`）。启动者负责收尾，否则泄漏。
4. **CPU 密集任务不要放进虚拟线程**。虚拟线程是协作式调度，长计算会占住载体线程；放进平台线程池或 `ForkJoinPool`。Go 虽然会抢占，但无上限地启动 CPU goroutine 同样只会增加切换。
5. **避免长时间持有的 `ThreadLocal`**：几十万个虚拟线程各带一份，内存会炸；改用显式参数或 ScopedValue。

什么时候打破：当下游本身只能承受很少的并发（比如单个文件），池化或串行才是对的。
