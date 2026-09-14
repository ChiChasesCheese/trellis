---
id: stream-changes-clause-alternative
node: pipelines.stream-offset-bookmark
type: qa
source: snowflake-docs
---
## Q
什么时候应该用 `SELECT … CHANGES` 子句而不是创建流（Stream）来读取变更？

## A
流保存一个事务性的偏移量，并在 DML 消费时自动前移，适合绝大多数持续的 CDC 管道。`CHANGES` 子句是只读的替代方案：用 `AT | BEFORE` 指定起点（可选 `END` 指定终点），查询任意两个时间点之间的变更追踪元数据，不创建偏移量、也不消费记录，多个查询可以读取不同区间。适合需要自行管理任意时间区间的少数场景；前提是表已开启 `CHANGE_TRACKING = TRUE` 或已经建过流，开启之前的时段没有变更元数据。
