---
id: hi-pt-job-scheduler-cron-history-10-long-multistage
node: qb.sd.job-scheduler-cron-history.points
type: qa
step: 10
---
## Q
**分布式任务调度器 · 长任务、多阶段与资源匹配**｜出自：分布式任务调度器 › 深入 4

任务可能跑数周、分多阶段且不能丢进度、还声明了 CPU 内存需求，调度器各怎么应对？

## A
**长任务。** 租约只覆盖 worker 还活着，续约带进度检查点；失联后新 worker 从最近检查点继续。
**多阶段。** 每阶段拆成独立 Run，上游完成才把下游置 SCHEDULED（DAG），输出落外部存储；更复杂时引入 Temporal 一类引擎，调度器只负责何时启动工作流。
**资源匹配。** 最小可行是按资源类别分队列；更进一步做过滤加打分的装箱，本质上变成集群调度器。
