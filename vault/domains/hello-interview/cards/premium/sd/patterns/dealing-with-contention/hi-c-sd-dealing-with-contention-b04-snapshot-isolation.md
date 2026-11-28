---
id: hi-c-sd-dealing-with-contention-b04-snapshot-isolation
node: sd.patterns.dealing-with-contention.beyond
type: qa
step: 4
---
## Q
**处理竞争 · PostgreSQL 的可重复读到底是什么**｜拓展 · 加分

在 PostgreSQL 里 `REPEATABLE READ` 能防丢失更新吗？它和 SERIALIZABLE 的差别落在哪？

## A
- **PostgreSQL 的可重复读是快照隔离**（snapshot isolation）： 事务开始时拿一份数据快照，之后一直读它。
- **能防同一行的丢失更新：** 如果你要更新的行在快照之后被别人改过并提交，你会得到序列化错误（"could not serialize access"），应用重试。后写者不会悄悄覆盖。
- **不能防写偏斜：** 两个事务读快照、各改不同行，都能提交，所以值班例子依然出错。
- **SERIALIZABLE（SSI）多做的事：** 追踪读写依赖，发现可能的环就中止其中一个，有时会误杀，所以必须准备重试。
- **MySQL 注意：** InnoDB 的可重复读语义不同（普通读用快照、写语句读最新版本），不要把 PostgreSQL 的结论搬过去。
