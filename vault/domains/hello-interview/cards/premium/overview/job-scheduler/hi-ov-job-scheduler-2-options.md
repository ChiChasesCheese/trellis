---
id: hi-ov-job-scheduler-2-options
node: sd.problem-breakdowns.job-scheduler
type: qa
step: 2
tags: [通览]
---
## Q
**分布式任务调度器 · 高层设计**｜通览

分布式任务调度器的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** 创建服务、Jobs 表、Executions 表、延迟队列、worker。

**每条路径。**
- **调度作业：** POST /jobs 经创建服务写入 Jobs 表（定义）和 Executions 表（每次实例）；到点前由定时任务捞出推进队列，worker 取走执行并更新状态；周期作业执行完再算下一次时间，插入新的执行记录。
- **监控状态：** worker 在 Executions 表更新状态，GET /jobs 查询 Executions 上以 user_id 为分区键的全局二级索引，按时间排序、分页、按状态过滤。

**存储。** 用键值或宽列库（如 DynamoDB），因为不要强一致、关系少、写量大；Jobs 以 job_id 为分区键，Executions 以执行时间取整到小时为分区键，只需查当前和下一小时桶。
