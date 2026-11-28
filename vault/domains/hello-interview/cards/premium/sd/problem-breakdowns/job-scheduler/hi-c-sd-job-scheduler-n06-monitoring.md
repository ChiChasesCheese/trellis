---
id: hi-c-sd-job-scheduler-n06-monitoring
node: sd.problem-breakdowns.job-scheduler.notes
type: qa
step: 6
---
## Q
**分布式任务调度器 · 查看作业状态与全局二级索引**｜摘要 · 必会

用户怎么高效查看自己所有作业的执行状态？

## A
- **状态更新：** 作业执行时在 Executions 表更新状态，如 COMPLETED、FAILED、IN_PROGRESS、RETRYING。
- **问题：** 按 userId 查询在当前设计里要两步：先在 Jobs 表找出用户所有 job_id（全表扫描，低效），再去 Executions 表查每个作业的状态。
- **解法：** 在 Executions 表上加全局二级索引（GSI）：分区键 user_id，排序键 执行时间 + job_id。这样能高效找到用户的所有执行记录，按执行时间排序、分页、按状态过滤。
- **代价：** GSI 增加写开销和成本，但换来高效的用户查询，同时不影响"找马上要跑的作业"这个主访问路径。
- **替代：** 在基表里重复存 user_id 会让数据模型更复杂更难维护，用 GSI 是 DynamoDB 里常见的多访问模式做法。
