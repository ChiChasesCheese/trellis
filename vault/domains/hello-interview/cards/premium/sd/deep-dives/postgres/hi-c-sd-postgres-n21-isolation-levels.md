---
id: hi-c-sd-postgres-n21-isolation-levels
node: sd.deep-dives.postgres.notes
type: qa
step: 19
---
## Q
**PostgreSQL · 三个隔离级别与 PostgreSQL 的特殊之处**｜摘要 · 必会

PostgreSQL 有哪些隔离级别？每个级别防住什么？哪里比 SQL 标准更强？

## A
- **Read Committed（默认）：** 每条语句只看到语句开始前已提交的数据；同一事务里前后两次相同查询可能看到不同结果（不可重复读）。性能好。
- **Repeatable Read：** 事务开始时拍一个快照，整个事务都看这个快照；PostgreSQL 的实现还防住了幻读，比 SQL 标准要求的更强。
- **Serializable：** 最强，效果等同串行执行，防住所有异常，代价是需要重试。
- **只有三种实际行为：** Read Uncommitted 在 PostgreSQL 里等同 Read Committed，因为多版本并发控制（MVCC）本来就让任何级别都不会读到脏数据。
- **异常对照：** 脏读：三级都不会；不可重复读：只有 Read Committed 会；幻读：只有 Read Committed 会，PostgreSQL 的 Repeatable Read 已经防住；序列化异常（如写偏斜）：只有 Serializable 防得住。
- **2026 亮点：** 跨区域强一致的分布式 SQL（如 Aurora DSQL）是快照隔离加乐观并发控制：事务不互相阻塞、没有死锁，冲突在提交时裁决并返回 40001，写偏斜要靠 `FOR UPDATE` 或把约束落到被写的行上；应用必须把整个事务写成可重试且幂等。
