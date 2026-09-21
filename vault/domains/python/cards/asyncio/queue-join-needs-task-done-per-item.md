---
id: queue-join-needs-task-done-per-item
node: asyncio.sync-primitives
type: qa
source: python-docs
---
## Q
在 `asyncio.Queue` 生产者-消费者（producer-consumer）模式里，`await queue.join()` 靠什么判断「所有任务都处理完了」，从而解除阻塞？

## A
`Queue` 内部维护一个「未完成任务数」：每 `put()` 一个新项目该数就 +1，消费者每处理完一项必须显式调用 `task_done()` 让它 -1；`join()` 会一直阻塞到这个计数降为 0。如果消费者忘记调用 `task_done()`，即使队列已经空了，`join()` 也会永远卡住不返回。
