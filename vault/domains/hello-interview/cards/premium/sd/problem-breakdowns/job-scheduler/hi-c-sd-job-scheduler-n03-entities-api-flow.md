---
id: hi-c-sd-job-scheduler-n03-entities-api-flow
node: sd.problem-breakdowns.job-scheduler.notes
type: qa
step: 3
---
## Q
**分布式任务调度器 · 实体、接口与数据流**｜摘要 · 必会

调度器的实体与接口怎么设计？数据流是什么样？为什么先写数据流？

## A
- **路径：** 这类偏数据处理、不太面向用户的题，按"实体 → 接口 → 数据流 → 高层设计 → 深入"的顺序走。
- **实体：**
  - Task：要执行的任务；
  - Job：某个任务在某个时间、带某组参数的实例；
  - Schedule：何时执行，cron 表达式或具体日期时间；
  - User：安排并查看自己作业的人。
- **接口：**
  - `POST /jobs`，体里是 task_id、schedule（如 `0 10 * * *`）、parameters；
  - `GET /jobs?user_id=&status=&start_time=&end_time=` → Job[]。
- **数据流（五步）：** 用户提交 → 作业持久化 → worker 在计划时间取走执行 → 失败则指数退避重试 → 更新状态。
- **为什么先写：** 与面试官对齐核心功能；给高层设计画路线图；提前发现瓶颈。先简单，再逐步加复杂。
