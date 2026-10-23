---
id: hft-architecture-threading-model
node: architecture.threading
type: qa
step: 1
---
## Q
低延迟交易系统常说"一核一线程，线程之间只用 SPSC 队列传消息"，这是什么意思？

## A
把系统拆成几个长期运行的线程，比如行情线程、若干策略分片线程、下单网关线程、日志线程。每个线程用 CPU 亲和性（affinity）**钉在一个自己独占的核**上，操作系统不会把它调去别的核，也不会在这个核上跑别的任务。

线程之间不共享可写的数据，只通过队列传递不可变的消息。队列是 **SPSC**（单生产者单消费者，single-producer single-consumer）：每条队列恰好一个线程写、一个线程读。

每个可变状态（例如某个品种的订单簿）只属于一个线程，称为**单写者原则（single writer principle）**，这样既不需要锁，也方便推理和重放。
