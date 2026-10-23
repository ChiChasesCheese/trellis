---
id: hl-sd02-exactly-once
node: system-design.sd02-job-scheduler
type: qa
step: 24
---
## Q
为什么调度器不承诺 exactly-once？outbox / inbox 模式起什么作用？

## A
精确一次 = 至少一次交付 + 接收方去重。调度器能做到的是「至少一次 + 稳定的幂等键」，「接收方是否真的做了去重」不在它的控制范围内。

若下游是同一个数据库，可以把「写入业务结果」与「记录已处理 jobId」放在一个事务里（outbox / inbox 模式），这时才能说「效果上恰好一次」。

senior 信号的一句话：「**交付**可以重复，**效果**要靠幂等键去重。」
