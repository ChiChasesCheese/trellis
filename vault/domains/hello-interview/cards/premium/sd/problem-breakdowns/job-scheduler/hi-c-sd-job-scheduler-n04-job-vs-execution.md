---
id: hi-c-sd-job-scheduler-n04-job-vs-execution
node: sd.problem-breakdowns.job-scheduler.notes
type: qa
step: 4
---
## Q
**分布式任务调度器 · 为什么要把作业定义和执行实例分开**｜摘要 · 必会

最简单的"一个 Jobs 表存 cron 表达式"为什么行不通？怎么分表？

## A
- **最简方案：** 创建时存一行，状态 PENDING，包含 user_id、task_id、scheduled_at、parameters。持久化后系统崩溃也能恢复，并能追踪状态。数据库选谁都行：无需强一致、关系少，选 DynamoDB 这类键值库便于以后扩展；偏开源就 Cassandra；Postgres、MySQL 也行，但后期扩展要多花心思。
- **问题：** 一次性作业没问题；周期作业只存 cron 表达式（`0 10 * * *`）时，要找出"接下来几分钟要运行的作业"就得逐个计算数据库里所有 cron 表达式，不可扩展。
- **关键洞察：** 把"定义"和"执行实例"分开，就像日历里一个"每周一"的事件和每个具体周一的出现。
  - Jobs 表（分区键 job_id）：存定义（用户、任务、计划类型与表达式、参数）；
  - Executions 表：存每一次该运行的实例，含 job_id、状态、尝试次数。
- **常见模式：** 定义 vs 实例，出现在日历（事件 vs 出现）、通知（模板 vs 单条通知）等许多系统里。
