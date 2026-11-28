---
id: hi-c-sd-flink-b03-two-phase-commit
node: sd.deep-dives.flink.beyond
type: qa
step: 3
---
## Q
**Flink · 两阶段提交的汇实现端到端精确一次**｜拓展 · 加分

想让写 Kafka 或数据库真正端到端精确一次，Flink 具体怎么做？

## A
- **两阶段提交汇**（two-phase commit sink）： 处理期间把输出写进一个未提交的事务；检查点屏障到达时执行预提交（flush）；等作业管理器确认这次检查点全部成功，才提交事务。
- **故障时：** 恢复到上次检查点，未提交的事务被中止，已预提交但未确认的事务可再次提交，所以结果不重复也不缺失。
- **Kafka 作为汇：** 用 Kafka 事务，下游消费者要设置 `isolation.level=read_committed`，否则会读到未提交的数据。
- **代价：** 输出只在检查点完成时才可见，端到端延迟至少是一个检查点间隔；事务有超时，检查点太久会让事务过期而丢失。
- **选择：** 能做幂等 upsert 就不要上两阶段提交，它更简单。
