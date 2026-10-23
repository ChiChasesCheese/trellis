---
id: hft-java-memory-model-volatile
node: java.memory-model
type: qa
step: 2
---
## Q
`volatile` 保证什么、不保证什么？为什么 `volatile int count; count++` 仍然会丢更新？

## A
`volatile` 保证两件事：**可见性**（写完后，后面的读一定看到）和**有序性**（`volatile` 写之前的操作不会被重排到它之后，读之后的操作不会被重排到它之前）。所以可以用 `volatile` 标志位来发布数据。

它**不保证原子性**。`count++` 是“读、加 1、写”三步：两个线程同时读到 5，各自写回 6，丢了一次更新。两个线程各加 100 万次，结果会明显小于 200 万。要原子更新就用 `AtomicInteger`、CAS 或锁。

代价上，`volatile` 写在 x86 上需要一条全栅栏（排空写缓冲），大约十几到几十个 CPU 周期，所以不要在不需要最强保证的地方滥用。
