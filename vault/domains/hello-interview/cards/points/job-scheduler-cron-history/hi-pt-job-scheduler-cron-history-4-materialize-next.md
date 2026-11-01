---
id: hi-pt-job-scheduler-cron-history-4-materialize-next
node: qb.sd.job-scheduler-cron-history.points
type: qa
step: 4
---
## Q
**分布式任务调度器 · cron 只物化下一次**｜出自：分布式任务调度器 › 整体设计

五百万个 cron 任务，未来一年的触发点要不要全部展开成 Run 行？怎么保证周期持续？

## A
**要点。** 只物化"下一次"这一条 Run：它被分发的同一个事务里再算出再下一次并插入。
**为什么。** 五百万个 cron 任务只占五百万行，而不是展开一年的触发点。
**写入路径。** API 层校验 cron 表达式，计算第一个触发时间，同事务写 Job 与一条 SCHEDULED 的 Run。
