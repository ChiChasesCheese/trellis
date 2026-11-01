---
id: hi-pt-scheduler-system-design-7-timer-structure
node: qb.lld.scheduler-system-design.points
type: qa
step: 7
---
## Q
**任务调度器（定时、周期、带优先级） · 计时的数据结构**｜出自：任务调度器（定时、周期、带优先级） › 深入 1

定时堆和时间轮各自的复杂度与适用场景是什么？选哪个？

## A
**小根堆。** 插入 O(log n)，取最早 O(1)，简单，几十万任务够用。
**时间轮。** 时间切格子，任务挂对应格，插入和触发 O(1)，适合百万级定时器且精度固定（如 Netty、Kafka 延迟队列）；层级时间轮处理远期。
**选择。** 选堆；任务量到百万以上或都是短延迟时换时间轮。
