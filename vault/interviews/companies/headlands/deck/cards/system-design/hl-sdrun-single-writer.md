---
id: hl-sdrun-single-writer
node: system-design.how-to-run
type: qa
step: 21
---
## Q
单写者原则（single-writer principle）是什么？在交易系统里怎么落地？

## A
**一个可变状态只由一个线程写**，不需要锁、不需要 CAS，只需要「写完发布、读之前获取」的内存序（release / acquire）。这是 mechanical sympathy 的核心。

落地：
- 每个品种分片 = 一个线程 = 一份订单簿 + 一份策略状态；线程之间只靠 **SPSC 环**（单生产者单消费者环形队列）交换不可变的消息；
- 跨线程共享的少量数据（熔断开关、参考价）：单写者 + 其他线程只读（`volatile` / `VarHandle.getAcquire`）。
