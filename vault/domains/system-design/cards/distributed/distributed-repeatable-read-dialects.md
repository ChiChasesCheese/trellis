---
id: distributed-repeatable-read-dialects
node: distributed.transactions.isolation
type: qa
---
## Q
Postgres and MySQL/InnoDB both offer `REPEATABLE READ`. Name three behavioral differences that bite in production.

## A
- **Phantoms**: InnoDB RR blocks them for *locking* reads via next-key (gap) locks; Postgres RR is snapshot isolation — plain reads never see phantoms, but nothing prevents a concurrent insert from breaking an invariant you checked (write skew stays possible in both).
- **Write-write conflicts**: Postgres RR **aborts** the second transaction with `could not serialize access due to concurrent update` (SQLSTATE 40001) — your app *must* have a retry loop. InnoDB instead **blocks on the row lock** and proceeds with the newly committed row, so you get no error and a possibly wrong result.
- **Locking reads see a different world**: in InnoDB, `SELECT ... FOR UPDATE` reads the **latest committed** row, not the transaction's snapshot — so a plain `SELECT` and a `SELECT ... FOR UPDATE` in the same transaction can return different values for the same row. Postgres keeps the snapshot and errors instead.

Takeaway for design docs: "repeatable read" names a *level*, not a behavior — always state the engine, and always write the retry loop.

## Q zh
Postgres 和 MySQL/InnoDB 都提供 `REPEATABLE READ`。说出三个会在生产环境中咬人的行为差异。

## A zh
- **幻读**：InnoDB 的 RR 通过 next-key（间隙）锁阻止*加锁*读遇到幻读；Postgres 的 RR 是快照隔离——普通读永远不会看到幻读，但没有任何机制阻止一次并发插入破坏你刚检查过的不变量（两者都仍然可能发生写倾斜）。
- **写写冲突**：Postgres 的 RR 会**中止**第二个事务，报 `could not serialize access due to concurrent update`（SQLSTATE 40001）——你的应用*必须*有重试循环。InnoDB 则是**在行锁上阻塞**，然后基于刚提交的新行继续执行，所以你不会得到错误，却可能得到一个错误的结果。
- **加锁读看到的是不同的世界**：在 InnoDB 中，`SELECT ... FOR UPDATE` 读的是**最新已提交**的行，而不是这个事务的快照——所以同一个事务里的一个普通 `SELECT` 和一个 `SELECT ... FOR UPDATE` 可能对同一行返回不同的值。Postgres 则坚持用快照，并直接报错。

写设计文档时的要点："repeatable read" 指的是一个*级别*的名字，不是一种具体行为——永远要写清楚是哪个引擎，并且永远要写重试循环。
