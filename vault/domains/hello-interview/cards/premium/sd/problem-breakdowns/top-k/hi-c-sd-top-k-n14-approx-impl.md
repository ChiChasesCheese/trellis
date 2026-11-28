---
id: hi-c-sd-top-k-n14-approx-impl
node: sd.problem-breakdowns.top-k.notes
type: qa
step: 14
---
## Q
**Top K · 深入五：CMS 在 Redis 与 Flink 里怎么落地**｜摘要 · 追问

近似 Top K 可以放在 Redis 里，也可以放在 Flink 状态里。各自怎么做，短板是什么？滑动窗口行不行？

## A
- **Redis（可以）：** Redis 原生支持 CMS 和有序集合。消费者对每个事件执行 `CMS.INCRBY`，再 `CMS.QUERY`，把结果 `ZADD` 进有序集合，集合裁剪到 1000 条；还可以在消费者本地记住门槛，已经低于前 1000 的就不必 ZADD。
  - 短板：持久性。每个事件都改动草图，可能 CMS 已更新、有序集合还没更新就宕机；从 Kafka 重建很慢，Redis 的 AOF 日志又无法对应到 Kafka 偏移量。别以为"近似就可以丢"，面试官正是会追问这里。
- **Flink（更好）：** CMS 和有序列表放进 Flink 状态，由 Flink 做检查点，宕机后从检查点加 Kafka 重放恢复。更可靠，也更快（数据结构在内存里）；只是自写作业代码，不增加新基础设施。短板：双方都得懂 Flink，要能讲清作业结构和状态管理。
- **滑动窗口：** 滚动窗口只加不减，Redis 与 Flink 两种做法都行；滑动要删除旧事件。CMS 在"只减去之前加过的"前提下支持删除，Redis 没有 `CMS.DECRBY`，Flink 或自写内存结构可以，但已超出面试期望。
