---
id: uth-compose-thread-pool-4-real
node: compose.thread-pool
type: qa
step: 4
---
## Q
**真实实现多做了什么：状态打包、回收、拒绝**｜Java ThreadPoolExecutor · JDK 21

`ThreadPoolExecutor` 在「原子整数 + 任务队列 + 线程集合」之外还做了什么？默认的 `Executors` 工厂方法有什么陷阱？

## A
**结构。** 状态和线程数打包进同一个 `AtomicInteger`，一次 CAS（比较并交换）就能原子地「检查状态 + 占名额」，判断线程数不用加锁。只有真正新增、移除工人时，才拿 `mainLock` 去改 `workers` 集合。

**细节。**

- 工人（`Worker`）继承 AQS（抽象队列同步器），当成一把不可重入的锁：`shutdown()` 时只中断没在跑任务的空闲工人。
- 回收：线程数超过 core（核心线程数）时，`getTask` 用 `poll(keepAliveTime)` 取任务，超时没取到就退出；任务抛异常会让线程退出，`processWorkerExit` 补一个新的。
- 拒绝：默认 `AbortPolicy` 抛异常，另有调用者自己执行、丢弃、丢最旧三种。

**为什么。** 「先排队、队满再扩线程」：线程比队列贵，能排就不新建。

**坑。** `newFixedThreadPool` 用无界的 `LinkedBlockingQueue`，队列永远不满，线程不会超过 core，`maximumPoolSize` 形同虚设，任务堆积会撑爆内存；`newCachedThreadPool` 用 `SynchronousQueue`、最大线程数 `Integer.MAX_VALUE`，线程会无限增长。

**对应 LeetCode：** 无直接对应的题
