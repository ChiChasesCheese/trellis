---
id: event-loop-single-thread-one-task-at-a-time
node: asyncio.blocking-and-threads
type: qa
source: python-docs
---
## Q
事件循环运行在哪个线程里？同一时刻这个线程能同时跑几个 Task？

## A
事件循环运行在一个线程里（通常是主线程），同一时刻该线程只能执行一个 Task；一个 Task 执行到 `await` 让出控制权时才会被挂起，事件循环再去运行队列里的下一个 Task——这正是为什么一段没有让出点的阻塞/CPU 密集代码会冻结循环上所有其它任务。
