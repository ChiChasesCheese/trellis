---
id: hi-c-sd-postgres-n20-lock-vs-serializable
node: sd.deep-dives.postgres.notes
type: qa
step: 21
---
## Q
**PostgreSQL · 行级锁与可串行化怎么选**｜摘要 · 必会

`SELECT ... FOR UPDATE` 和可串行化（SERIALIZABLE）各自怎么解决并发问题？怎么选？

## A
- **行级锁：** 读的时候加 `FOR UPDATE`，锁住这一行，其他想对同一行加锁的事务要等到你提交，这样检查和写入之间没人能插入。
- **可串行化：** `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE`，数据库保证效果如同事务依次执行，冲突时回滚其中一个，应用必须重试。
| 维度 | 行级锁 | 可串行化 |
|---|---|---|
| 并发 | 高，只在碰同一行时冲突 | 低，冲突就回滚重试 |
| 开销 | 小，只管锁 | 大，要跟踪读写依赖 |
| 适用 | 清楚要锁哪些行（竞价、库存） | 事务复杂、说不清该锁什么 |
| 要处理的错误 | 死锁 | 序列化失败 |
- **默认选行级锁**，知道要锁什么就用它；事务复杂到无法判断锁哪些行时才用可串行化。
