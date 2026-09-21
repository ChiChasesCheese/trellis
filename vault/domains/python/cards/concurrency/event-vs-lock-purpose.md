---
id: event-vs-lock-purpose
node: concurrency.locks-races
type: qa
source: python-docs
---
## Q
`threading.Event` 解决的是什么问题，它和 `Lock` 在用途上有什么不同？

## A
`Event` 内部维护一个初始为 `False` 的标志位，一个线程调用 `set()` 把它置为 `True`，所有正在 `wait()` 的线程都会被唤醒继续执行；已经是 `True` 时 `wait()` 立即返回，不阻塞。它解决的是“一个线程通知多个线程某件事发生了”的一次性广播（broadcast）问题，不涉及互斥访问共享资源；而 `Lock` 解决的是“同一时刻只允许一个线程进入临界区”的互斥问题。两者可以配合使用：用 `Event` 做优雅关闭信号，用 `Lock` 保护共享数据。
