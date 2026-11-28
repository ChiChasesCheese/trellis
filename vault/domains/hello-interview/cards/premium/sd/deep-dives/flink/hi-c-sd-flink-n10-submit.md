---
id: hi-c-sd-flink-n10-submit
node: sd.deep-dives.flink.notes
type: qa
step: 18
---
## Q
**Flink · 提交作业后发生了什么**｜摘要 · 追问

调用 `execute` 之后，Flink 内部依次做什么？

## A
- **① 生成作业图（JobGraph）：** 编译器把逻辑上的 DataStream 操作转成优化过的执行计划。
- **② 提交给作业管理器（JobManager）：** 它是集群的协调者。
- **③ 分发任务：** 作业管理器把作业图拆成任务，分给任务管理器（TaskManager）。
- **④ 执行：** 任务管理器运行任务，每个任务处理数据的一部分。
- **集群形态：** 本地集群或远程集群都用同一个接口提交。
