---
id: hl-j10-pinning-not-all-sync
node: java21.j10-virtual-threads
type: qa
step: 19
---
## Q
JDK 21 下，判断四段代码是否 pin：(a) `synchronized(lock){counter++;}` (b) `synchronized(lock){Thread.sleep(50);}` (c) `ReentrantLock` 里 `sleep(50)` (d) `FileInputStream.read`。并说出 pinning 的症状。

## A
- (a) **不 pin**：`synchronized` 里只做内存中的短操作没事，没有阻塞就没有「该卸载而不能」。
- (b) **pin**：持 monitor 时阻塞。
- (c) **不 pin**：`ReentrantLock` 基于 `LockSupport.park`，可卸载。
- (d) 文件 I/O 不卸载，载体被占住（调度器补偿多开载体），不是 monitor 引起的 pin。

结论：问题不是「用了 `synchronized`」，而是**在 `synchronized` 里做 I/O 或 sleep**。症状：吞吐莫名封顶在核数；载体全被钉住时其他虚拟线程饿死；极端情况下被钉住的线程等的事件要靠另一个没载体可跑的虚拟线程触发，造成死锁。
