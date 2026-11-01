---
id: hi-sd-temporal-6-architecture
node: qb.sd.job-scheduler-cron-history.pre-sd-deep-dives-temporal
type: qa
step: 6
---
## Q
**Temporal 的服务架构**｜系统设计 · 关键技术

Temporal 集群内部由哪些服务组成？各自管什么？工作流状态怎样存、怎样保证“更新状态”和“安排下一步”不会因崩溃而脱节？

## A
**组件。**

- Frontend：无状态入口，客户端和 Worker 都连它
- History Service：拥有工作流的持久状态，处理活动完成、信号、定时器等
- Matching Service：管理任务队列（Task Queue），把任务交给轮询的 Worker
- Worker：你自己的进程，轮询任务、执行代码、回报结果；Temporal 服务本身不运行你的代码

**状态存储。** 工作流分散到固定数量的历史分片（History Shard），每个 History 实例拥有其中一部分。除执行历史（Event History）外，还维护可变状态（Mutable State），它是当前待处理活动、定时器和子工作流的物化视图，避免每次都扫描全部历史。

**一致性。** 状态更新与一个持久的转移任务（Transfer Task）一并提交，后台再把任务发给 Matching，这就是事务性发件箱（transactional outbox）：提交后崩溃也不会丢掉下一步。存储可用 PostgreSQL、MySQL 或 Cassandra。
