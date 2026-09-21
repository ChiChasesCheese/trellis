---
id: event-loop-job-queue-model
node: asyncio.event-loop
type: qa
source: python-docs
---
## Q
asyncio 事件循环（event loop）在最底层是怎样驱动任务运行的？

## A
事件循环内部维护一份待运行任务（job）的集合，近似一个队列：循环从中取出一个任务并把控制权交给它，任务运行到暂停（如遇到 `await` 让出）或结束，再把控制权还给循环；循环随即取下一个任务继续。全程单线程、协作式（cooperative），任务需要主动让出才有其它任务运行的机会。
