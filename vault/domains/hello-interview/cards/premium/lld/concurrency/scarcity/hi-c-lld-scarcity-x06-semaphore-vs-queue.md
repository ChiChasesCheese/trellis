---
id: hi-c-lld-scarcity-x06-semaphore-vs-queue
node: lld.concurrency.scarcity.exam
type: qa
step: 6
---
## Q
**并发稀缺资源 · 为什么不能只用信号量做连接池**｜考点 · 必会

面试官问："用 Semaphore(10) 不就能做连接池了吗？"怎么回答？

## A
- **信号量能限数量：** 最多 10 个线程同时用连接
- **不能交出对象：** 具体的 `Connection` 放在哪、拿哪一个、归还放回哪里，信号量不管
- **自己补：** 要再加一个线程安全的容器，并保护它，等于重写阻塞队列
- **结论：** 阻塞队列同时解决数量限制（空则阻塞）和对象分发
