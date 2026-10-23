---
id: hl-ld03-lock-design
node: problems.ld03-async-tcp-channel
type: qa
step: 15
---
## Q
异步 TCP 通道的并发设计是什么：锁怎么用、系统调用放哪、为什么不做无锁？

## A
并发设计：一把 `ReentrantLock` 保护两个环和所有标志；`Condition changed` 用于 `poll(timeout)`、`offer(msg, timeout)`、`awaitClosed`；等待写成 `while (!条件) cond.await();`（可能虚假唤醒）。用 `ReentrantLock` 而非 `synchronized`：JDK 21 虚拟线程里 `synchronized` 内阻塞会钉住载体线程。不做无锁：瓶颈是系统调用 / `wakeup` / 线程交接而不是锁（锁内是几十字节拷贝）；两个环是 SPSC 可换成 ld01 的无锁环，先测量。
