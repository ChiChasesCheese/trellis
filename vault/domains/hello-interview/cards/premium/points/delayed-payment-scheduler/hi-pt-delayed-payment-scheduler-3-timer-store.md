---
id: hi-pt-delayed-payment-scheduler-3-timer-store
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 3
---
## Q
**延迟支付调度服务 · 定时器放哪里**｜必会 · 出自：延迟支付调度服务 › 深入 1

延迟转账需要一个“到点触发”的定时器，候选有：Redis 有序集合、消息队列延迟投递、Kafka、数据库表加扫描。选哪个，为什么？

## A
**要点。** 预约行本身就是定时器：在 `execute_at` 上建只含未完成状态的部分索引，扫描器每秒按时间取前 200 条。

**为什么不选别的。** Redis 有序集合崩溃可能丢，也无法和扣款放进一个事务；队列延迟投递有上限；Kafka 没有延迟；每分钟全表扫描随数据量变慢。

**精度。** 1 秒扫描加排队，p99 约 2–3 秒。
