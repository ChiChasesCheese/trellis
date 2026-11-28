---
id: hi-c-sd-dealing-with-contention-x10-isolation-misconception
node: sd.patterns.dealing-with-contention.exam
type: qa
step: 10
---
## Q
**处理竞争 · 隔离级别误解**｜考点 · 追问

"我们把数据库设成可重复读（REPEATABLE READ）就不会有并发问题了"，这句话错在哪？

## A
- **错在：** 隔离级别只保证一个事务反复读同一数据时一致，并不让"读-判断-写"自动变原子；同一行的丢失更新靠条件写、锁或版本检查防，写偏斜在可重复读下依然会发生。
- **只有 SERIALIZABLE：** 才保证结果等价于事务串行执行，能抓住写偏斜，但要追踪读写依赖，中止的事务需重试，是最贵的。
- **实务：** 默认级别配条件写、行锁或版本检查，跨行约束才升级到 SERIALIZABLE 或落到单行；应用必须能重试序列化错误。
- **注意：** 级别的默认值因数据库而异（PostgreSQL 读已提交，MySQL 可重复读）。
