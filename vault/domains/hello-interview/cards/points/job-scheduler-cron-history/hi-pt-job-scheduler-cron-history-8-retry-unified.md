---
id: hi-pt-job-scheduler-cron-history-8-retry-unified
node: qb.sd.job-scheduler-cron-history.points
type: qa
step: 8
---
## Q
**分布式任务调度器 · 重试统一成更晚的到期**｜出自：分布式任务调度器 › 整体设计

任务执行失败或租约过期时如何重试？为什么不单独做一条重试路径？超过次数怎么办？

## A
**做法。** 执行报错或租约过期都视为一次失败：attempt 加一，按指数退避加抖动算出新触发时间，把 Run 改回 SCHEDULED。
**为什么。** 重试被统一成一次更晚的到期，复用同一套发现与触发机制，不需要第二条路径。
**终态。** 超过最大次数置 DEAD 并写入死信队列（DLQ），同时告警。
