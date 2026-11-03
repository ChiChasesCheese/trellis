---
id: hi-pt-job-scheduler-cron-history-3-fencing-protocol
node: qb.sd.job-scheduler-cron-history.points
type: qa
step: 3
---
## Q
**分布式任务调度器 · Run 状态与 worker 协议**｜必会 · 出自：分布式任务调度器 › 核心实体与接口

调度器里"任务定义"和"执行实例"为什么要分成两个实体？worker 与调度器之间的协议需要哪些调用，每次带什么？

## A
**实体。** Job 是定义（类型、cron 与时区、重试策略、超时、优先级、资源需求）；Run 是一次执行（状态 SCHEDULED、QUEUED、RUNNING、SUCCEEDED、FAILED、DEAD，attempt，租约持有者与到期时间）。
**协议。** `lease`、`heartbeat`、`complete`、`fail`，每次都带 run_id 与 attempt，作为围栏令牌（fencing token）。
