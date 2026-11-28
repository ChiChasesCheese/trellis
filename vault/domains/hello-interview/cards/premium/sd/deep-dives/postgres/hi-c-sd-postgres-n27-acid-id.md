---
id: hi-c-sd-postgres-n27-acid-id
node: sd.deep-dives.postgres.notes
type: qa
step: 27
---
## Q
**PostgreSQL · ACID 的隔离性与持久性**｜摘要 · 追问

隔离性和持久性在 PostgreSQL 里怎么实现？持久性能不能放松？

## A
- **隔离性（isolation）：** 决定并发事务彼此能看到什么。SQL 标准定义四个级别，PostgreSQL 都接受，但实际只有三种行为，因为它的多版本并发控制（MVCC）让任何级别都不会读到未提交的脏数据。
- **默认 Read Committed：** 只防脏读，不防不可重复读和幻读。
- **持久性（durability）：** 事务提交后就保证不丢，哪怕断电。靠预写日志（WAL）：先写日志、日志刷盘、之后才算提交；数据页可以以后再写，崩溃后重放日志恢复。
- **可以放松：** 例如 `synchronous_commit = off`，提交不等 WAL 刷盘，换来速度，代价是崩溃时可能丢最后几个事务的写入。适合可容忍丢失的数据。
