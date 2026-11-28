---
id: hi-sdx-cont-rr-dialects
node: sd.patterns.dealing-with-contention.more
type: qa
step: 2
---
## Q
**同叫可重复读，PostgreSQL 与 InnoDB 差在哪**｜补充 · 处理争用 · 追问

面试官：「PostgreSQL 和 MySQL InnoDB 都有 REPEATABLE READ。生产里最容易踩到的三处行为差异是什么？」

## A
**结论。** 「可重复读」只是级别名，不是统一行为。差异在三处：写写冲突时一个报错、一个阻塞后继续；加锁读看到的版本不同；幻读的挡法不同。设计文档里必须写明是哪个引擎，并写好重试循环。

**要点。**
- **写写冲突：** PostgreSQL 让第二个事务失败，报 could not serialize access（SQLSTATE 40001），应用必须重试。InnoDB 让它阻塞在行锁上，等对方提交后基于最新行继续，不报错，如果先快照读再写绝对值，结果可能是错的。
- **加锁读：** InnoDB 的 SELECT ... FOR UPDATE 读最新已提交的行，不是事务快照，同一事务里普通 SELECT 和 FOR UPDATE 对同一行可能读到不同的值。PostgreSQL 保持快照，行被改过就报错。
- **幻读：** InnoDB 对加锁读用 next-key（间隙）锁挡住插入。PostgreSQL 的可重复读是快照隔离，普通读不会出现幻读，但并发插入仍可能破坏你刚检查过的约束。
- **共同点：** 两者都挡不住写偏斜。

**面试里这样说。** 「我会说清是 PostgreSQL 还是 InnoDB：前者撞上并发更新直接报 40001，我写重试循环；后者会阻塞并基于最新行继续，所以我用 UPDATE n = n + 1 这种原子写，不先读再写绝对值。」

**易错。**
- **把一个引擎的结论搬到另一个：** 同名级别行为不同。
- **没有重试循环：** PostgreSQL 的 40001 是正常结果，不是异常。
