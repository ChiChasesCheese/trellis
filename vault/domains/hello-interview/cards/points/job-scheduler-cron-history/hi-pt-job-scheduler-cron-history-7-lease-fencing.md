---
id: hi-pt-job-scheduler-cron-history-7-lease-fencing
node: qb.sd.job-scheduler-cron-history.points
type: qa
step: 8
---
## Q
**分布式任务调度器 · 租约与围栏令牌**｜必会 · 出自：分布式任务调度器 › 深入 2

worker 随时可能死，怎样保证至少执行一次？旧 worker 只是网络卡住并没有死，醒来后会出什么问题，如何防？

## A
**租约。** worker 领取时写 `lease_until`，续约检查 attempt 未变；到期没续约，扫描器判失败并重试，这给出至少一次。
**围栏。** 所有状态写入（完成、失败、续约）都带 attempt，数据库用 `WHERE attempt = ?` 拒绝过期写入；外部副作用把 run_id 作为幂等键传给下游。
**边界。** 副作用靠任务幂等吸收；无法检查幂等的任务提供"至多一次"开关，租约丢失置 UNKNOWN 交人工或回调。
