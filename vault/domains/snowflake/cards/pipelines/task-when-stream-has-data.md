---
id: task-when-stream-has-data
node: pipelines.task-conditional-execution
type: qa
source: snowflake-docs
---
## Q
一个每小时调度的任务用 MERGE 消费流（Stream），但大多数小时流里都没有新数据。如何避免每次都白白启动仓库跑一遍？

## A
在任务定义中加上 `WHEN SYSTEM$STREAM_HAS_DATA('<stream_name>')` 条件。每次到点时先评估这个条件：流中没有未消费的变更时返回 FALSE，这次运行被跳过，不会执行任务主体，也就不会为空跑消耗仓库计算资源；只有流中有数据时才真正执行 MERGE。这是「按调度检查、有数据才运行」的组合用法。
