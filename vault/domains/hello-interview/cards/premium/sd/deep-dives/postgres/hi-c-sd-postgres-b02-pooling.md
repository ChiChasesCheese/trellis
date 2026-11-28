---
id: hi-c-sd-postgres-b02-pooling
node: sd.deep-dives.postgres.beyond
type: qa
step: 2
---
## Q
**PostgreSQL · 连接池的模式与边界**｜拓展 · 加分

PgBouncer 的几种池化模式有什么区别？事务级池化会破坏什么？

## A
- **为什么需要：** 每个连接是一个后端进程，默认最大连接数只有 100，成千上万的应用连接直接连上去既耗内存又增加调度开销。
- **会话级（session）池化：** 客户端整个会话独占一个数据库连接，兼容性最好，但复用率最低。
- **事务级（transaction）池化：** 事务结束就把连接还给池，复用率最高，是大规模的常见选择。
- **代价：** 同一个客户端的下一个事务可能落在另一个数据库连接上，所以依赖会话状态的功能会失效或出错：`SET` 设置的会话参数、会话级咨询锁、`LISTEN/NOTIFY`、SQL 级 `PREPARE` 预备语句等（PgBouncer 1.21 起可用 `max_prepared_statements` 跟踪协议级预备语句，但仍要确认版本与驱动）。
- **2026 亮点：** 事务级池不再等于放弃预备语句：PgBouncer 1.21 起支持协议级命名预备语句，1.24 起 `max_prepared_statements` 默认 200，驱动走 extended protocol 照常工作，所以高并发下可以默认选事务级池；仍然不可用的是 SQL 级 `PREPARE`、`SET`、`LISTEN`、会话级咨询锁和 `WITH HOLD` 游标。池本身单线程，要用 `so_reuseport` 加滚动重启做多实例。
- **用法建议：** 事务级池化时，应用只依赖事务内的状态；需要会话状态的少数路径单独走会话级连接。池大小要参考数据库核数而不是应用实例数。
