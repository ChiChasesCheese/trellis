---
nodes:
- asyncio.sync-primitives
title: asyncio.Queue：异步生产者消费者队列
corpus: python-docs
section: 32-asyncio-queue
url: https://docs.python.org/3/library/asyncio-queue.html
tags:
- canonical
---

# asyncio.Queue：异步生产者消费者队列

asyncio.Queue 是专为协程之间传递数据设计的队列，API 和 queue.Queue 神似（put/get/join/task_done）但内部用协程友好的方式实现等待，满队列时 put() 会 await 而不是阻塞线程，空队列时 get() 同理，这样事件循环在等待期间可以去处理其他协程。文档还提供了 PriorityQueue（按优先级出队）和 LifoQueue（后进先出）两个变体，接口和普通 Queue 完全一致，只是出队顺序不同。这是实现异步生产者消费者流水线的标准工具：比如一个协程负责抓取数据放入队列，多个消费者协程并发处理队列里的数据，用 join() 等待所有数据处理完毕。相比手写信号量控制并发，用队列解耦生产和消费的速度差异往往是更清晰的设计。
