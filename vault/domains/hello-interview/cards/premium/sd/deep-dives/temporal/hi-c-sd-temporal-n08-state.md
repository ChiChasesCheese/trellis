---
id: hi-c-sd-temporal-n08-state
node: sd.deep-dives.temporal.notes
type: qa
step: 13
---
## Q
**Temporal · Workflow 状态怎么存：分片、事件历史、可变状态**｜摘要 · 追问

数百万个 Workflow 怎样分给 History Service？事件历史和可变状态（Mutable State）有什么区别？

## A
- **History 分片（shard）：** Workflow Execution 被划分到固定数量的 History 分片，每个 History 实例拥有其中一部分，负责这些分片里 Workflow 的请求和计时器。实例增减或故障时，分片的归属可以在实例间迁移。
- **事件历史（Event History）：** 持久的事实记录，Workflow 的状态可以从中恢复。
- **可变状态（Mutable State）：** 服务端关于 Workflow 当前状态的物化视图：待处理的 Activity、未完成的计时器、子 Workflow 等。理论上每次都扫描事件历史可以重建，但太贵。有了它，History Service 能快速回答"这个 Workflow 现在怎么样"，而事件历史仍是恢复它的持久记录。
- **存储：** 自托管时可用 PostgreSQL、MySQL 或 Cassandra；Temporal 管理事件历史、可变状态和内部任务的 schema。
