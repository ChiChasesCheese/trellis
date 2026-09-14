---
id: distributed-phantoms-predicate-locks
node: distributed.transactions.isolation
type: qa
---
## Q
What is a phantom, why can't row locks stop it, and how do databases approximate predicate locks in practice?

## A
A **phantom**: one transaction's write (an insert, or an update moving a row into range) changes the result of another transaction's **search condition** — e.g. two bookings both query "room 101 free 12–1pm?", find no rows, and both insert. Row locks fail because **you can't lock a row that doesn't exist yet**.

- **Predicate locks** — lock the condition itself, check every write against all outstanding predicates — are correct but too expensive.
- Real systems use **index-range (next-key) locks**: lock the index entries covering the searched range, including gaps, so a conflicting insert blocks (InnoDB next-key locking; serializable 2PL generally). No usable index → the lock degrades to the whole table.

Same read-predicate-then-write shape as [[distributed-write-skew]], but on rows that don't exist yet.

## Q zh
什么是幻读（phantom）？为什么行锁挡不住它？数据库在实践中是怎样近似谓词锁的？

## A zh
**幻读**：一个事务的写入（一次插入，或者一次把某行更新进查询范围的更新）改变了另一个事务的**搜索条件**的结果——比如两个订房请求都查询"101 号房 12-1 点是否空闲？"，都没查到行，于是都插入了。行锁失效是因为**你没法锁一个还不存在的行**。

- **谓词锁**——直接锁住条件本身，让每次写都对照所有未完成的谓词做检查——是正确的，但代价太高。
- 现实系统用**索引范围（next-key）锁**：锁住覆盖所查范围的索引条目，包括间隙，这样一次冲突的插入就会被阻塞（InnoDB 的 next-key locking；serializable 下的 2PL 普遍这样做）。没有可用索引 → 锁会退化成锁住整张表。

和 [[distributed-write-skew]] 是同一种"先按谓词读、再写"的形状，只不过这里的行还不存在。
