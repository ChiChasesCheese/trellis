---
id: hl-os-spsc-what-why
node: foundations.os-processes-threads-ipc
type: qa
step: 23
---
## Q
SPSC 环形缓冲（single-producer single-consumer ring buffer）是什么？为什么「单生产者单消费者」让它能做到无锁无 CAS？

## A
**环形缓冲**：固定大小的数组当作首尾相连的环使用，写到末尾回到开头。**SPSC**：只有一个生产者写、一个消费者读，可以放在共享内存里让两个不同进程通信。

对比 `ArrayBlockingQueue` / `LinkedBlockingQueue`：每次 `put` / `take` 要加锁，有竞争时阻塞（park / unpark，约 1.5 µs / 次交接），`LinkedBlockingQueue` 还要分配节点；跨进程根本不能用。

SPSC 约束的好处：只有生产者修改 `tail` 和槽位内容，只有消费者修改 `head`，**每个变量只有一个写者**，不需要原子读改写、不需要 CAS、没有系统调用，只需保证**可见性与顺序**。
