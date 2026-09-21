---
id: queue-daemon-sentinel
node: concurrency.queues
type: qa
source: python-docs
---
## Q
生产者-消费者模式里，工作线程 `while True: item = q.get(); ...` 是一个死循环，如何让这些消费者线程能随程序一起退出？

## A
两种常见做法：① 把消费者线程创建为守护线程（`daemon=True`），主线程用 `q.join()` 等所有任务处理完后退出，此时守护消费者线程会被直接终止，不需要它们自己跳出循环；② 显式放入一个“哨兵值”（sentinel，如 `None`）作为特殊条目，消费者 `get()` 到哨兵后主动 `break` 退出循环——这种方式能让消费者做完清理工作再退出，比强行终止守护线程更干净。
