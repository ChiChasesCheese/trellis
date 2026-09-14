---
id: task-conditional-cost-practices
node: pipelines.task-conditional-execution
type: cloze
source: snowflake-docs
---
降低任务成本的做法：把 {{c1::`SCHEDULE`}} 设得不那么频繁；用{{c2::自动挂起和自动重试}}参数避免在持续失败的任务上浪费资源；对只在特定条件下（如流有新数据）才需要运行的任务，使用{{c3::触发式任务（triggered task）}}或 `WHEN SYSTEM$STREAM_HAS_DATA` 条件；为无服务器功能设置{{c4::预算（budget）和支出告警}}。
