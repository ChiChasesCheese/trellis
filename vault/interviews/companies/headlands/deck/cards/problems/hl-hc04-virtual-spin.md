---
id: hl-hc04-virtual-spin
node: problems.hc04-queue-mean-snapshot
type: qa
step: 14
---
## Q
并发读测试里，纯自旋的读者跑在虚拟线程上会出什么问题？怎么解决？

## A
虚拟线程由 JVM 调度，可开几十万个，跑在少量载体线程（数量 = CPU 核数）上。阻塞时让出载体线程，但**纯自旋**（`while (!flag) {}`）永不让出载体线程。自旋的虚拟线程数 ≥ 载体线程数时，其他虚拟线程（如写者）被饿死，程序挂住。

解决：自旋循环里加 `Thread.yield()`，或读者用平台线程。

相关：`synchronized` 块内阻塞会钉住（pin）载体线程，所以写者身份和队列同步用 `VarHandle` / `ReentrantLock` 更合适。

测试里起 5 个读 / 写线程几乎免费：`Executors.newVirtualThreadPerTaskExecutor()`、`Thread.ofVirtual()`。

读者拿到的 `seq` 单调不减也可断言。
