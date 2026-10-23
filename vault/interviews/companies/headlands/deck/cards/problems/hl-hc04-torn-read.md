---
id: hl-hc04-torn-read
node: problems.hc04-queue-mean-snapshot
type: qa
step: 12
---
## Q
什么是撕裂读（torn read）？为什么单写者多读者读均值时「sum 和 size 各自 volatile」不行？

## A
每个线程有自己的 CPU 缓存和寄存器，编译器和 CPU 还会重排指令，所以一个线程写的值，另一个不一定马上看到。**撕裂读**：写者先更新 `sum` 再更新 `size`，读者在两次写之间读到「新 sum + 旧 size」，算出根本不存在过的均值。

例：队列全是 7，size=3，sum=21，均值 7。写者 push 7：先 `sum=28`，再 `size=4`；读者恰好读到 `sum=28, size=3` → 9.33，从未存在过。

两个 `volatile` 字段只保证**每个字段单独**可见，读者分两次读，中间可插进写者的更新，仍会撕裂。128 位的和本来就要两个 64 位字，C++ 里 `std::atomic<__int128>` 在许多平台上不是无锁的（内部可能用锁）。

**happens-before**（JMM 规则）：同一线程内前面语句先于后面；`volatile` 写先于之后对它的读；`start()` 先于线程内所有动作；线程内所有动作先于别人 `join()` 返回。

方案：
- 直接读 `QueueMean.getMean()`：数据竞争，未定义；
- 整个类 `synchronized`：正确但读写互斥，JDK 21 虚拟线程在 `synchronized` 里阻塞会钉住载体线程；
- 两个 `volatile`：撕裂；
- **不可变快照 + 一次发布**（见下一张）。
