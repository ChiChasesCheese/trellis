---
id: queue-join-taskdone
node: concurrency.queues
type: qa
source: python-docs
---
## Q
`queue.Queue` 的 `join()` 和 `task_done()` 配合起来解决什么问题？

## A
`Queue` 内部维护一个“未完成任务数”，每 `put()` 一个条目计数加一，消费者线程每处理完一个条目调用一次 `task_done()`，计数减一。`join()` 会阻塞主线程，直到这个计数归零，也就是所有已入队的任务都被 `get()` 取出并显式标记完成，而不只是“队列已清空”——`get()` 只是把条目移出队列，不代表处理已经结束。这让主线程能可靠地等到所有任务真正处理完，而不用轮询队列长度。
