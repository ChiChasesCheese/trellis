---
nodes:
- concurrency.queues
title: queue 模块：线程安全队列
corpus: python-docs
section: 25-queue
url: https://docs.python.org/3/library/queue.html
tags:
- canonical
---

# queue 模块：线程安全队列

queue.Queue 是专为多线程生产者消费者模式设计的线程安全队列，内部已经用锁保护好了，不需要使用者自己再加锁。文档重点讲了任务完成协议：消费者处理完一个任务要调用 task_done()，生产者可以调用 join() 阻塞等待队列里所有任务都被标记完成，这是判断一批任务是否全部处理完的标准写法，比自己维护计数器可靠。终止队列常用的模式是放入一个哨兵值（sentinel，如 None），消费者读到哨兵就知道该退出了。文档还介绍了更轻量的 SimpleQueue，去掉了任务跟踪的开销，适合只需要简单传递数据不需要 join()/task_done() 的场景。这是无共享状态、靠消息传递协调线程这一设计原则最直接的工程实现。
