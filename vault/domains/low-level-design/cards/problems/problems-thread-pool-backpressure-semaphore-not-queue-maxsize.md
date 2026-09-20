---
id: problems-thread-pool-backpressure-semaphore-not-queue-maxsize
node: problems.components.thread-pool
type: qa
step: 2
tags: [grown]
---
## Q
给线程池的任务队列做背压（队满时挡住 `submit()` 的调用方），为什么不直接给内部队列传 `maxsize`，而是在 `submit()` 前面单独包一个信号量？

## A
因为 `shutdown()` 需要往队列里投递哨兵任务来唤醒每一个还卡在 `get()` 上的 worker——如果队列本身设了容量上限，这次投递可能因为队列已满而被同一个机制挡住，关闭操作反而被『队满』这个和关闭无关的条件卡住了。正确做法是内部队列永远不设容量上限，背压改由 `submit()` 前面的 `threading.Semaphore(queue_capacity)` 实现：`submit()` 先 `acquire()`（满了就在这里挡住调用方），拿到许可才真正入队；worker 取到任务后立刻 `release()`，把许可还给下一个提交者。这样『背压』和『投递哨兵关闭池子』彻底解耦：队列自己永远不会因为满而阻塞任何操作，信号量的许可数才是真正的容量上限。
