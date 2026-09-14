---
id: dt-vs-materialized-view-refresh
node: pipelines.dynamictable-incremental-vs-full-refresh
type: qa
source: snowflake-docs
---
## Q
需要一个包含多表连接、聚合和窗口函数的多步转换结果，并保持近实时。为什么动态表比手写全量重建的定时任务更合适？

## A
动态表支持连接、聚合和窗口函数等多步管道，并能在定义支持时只对变化的行做增量刷新，由 Snowflake 负责调度和按依赖顺序协调；手写定时任务通常每次重建整个结果，或者需要自己实现增量逻辑和编排。动态表还能只调整一个参数（目标延迟）就从批处理过渡到近实时，而不必重写管道。
