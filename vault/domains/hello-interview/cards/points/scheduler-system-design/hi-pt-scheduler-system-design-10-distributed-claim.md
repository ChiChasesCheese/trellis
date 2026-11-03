---
id: hi-pt-scheduler-system-design-10-distributed-claim
node: qb.lld.scheduler-system-design.points
type: qa
step: 10
---
## Q
**任务调度器（定时、周期、带优先级） · 分布式领取与围栏令牌**｜追问 · 出自：任务调度器（定时、周期、带优先级） › 深入 6

多个调度实例怎样避免同一个任务被执行两次？实例假死又怎么办？语义是什么？

## A
**领取。** 任务存数据库，实例扫描到点且未被领取的任务，用 `SELECT ... FOR UPDATE SKIP LOCKED` 或带版本号的条件更新标记被某实例领取，带租约过期时间；崩溃后租约到期别的实例接管。
**假死。** 租约过期后原实例可能还在跑，结果提交要带围栏令牌（fencing token），旧令牌结果被拒绝。
**语义。** 至少一次，任务要幂等；任务按编号哈希分片减少扫描竞争。
**恢复。** 重启后读库重建定时堆，错过的按 misfire 策略处理。
