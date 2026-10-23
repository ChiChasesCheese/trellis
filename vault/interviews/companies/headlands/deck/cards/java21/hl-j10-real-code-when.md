---
id: hl-j10-real-code-when
node: java21.j10-virtual-threads
type: qa
step: 26
---
## Q
一个 k 路合并器每路数据源配一个生产者线程，生产者用虚拟线程；而对数组求和的并行实现却不该用虚拟线程。分别为什么？

## A
- **k 路合并（该用）**：生产者大部分时间阻塞在 `q.put(...)`（有界队列满了等消费者）或数据源 I/O 上，是 **I/O 型**，「等」占多数。`ArrayBlockingQueue.put` 基于 `ReentrantLock` + `Condition`，阻塞时虚拟线程卸载、不 pin。开 k 个很便宜；虚拟线程同样支持 `interrupt` 和 `join(Duration)`。`Thread.ofVirtual().factory()` 还可交给 `StructuredTaskScope`。
- **数组求和（不该用）**：纯计算，**CPU 密集**，瓶颈是核数，虚拟线程只是多路复用在核数个载体上，不会多出并行度，也不会抢占。应该用 `ForkJoinPool` 或并行流。
