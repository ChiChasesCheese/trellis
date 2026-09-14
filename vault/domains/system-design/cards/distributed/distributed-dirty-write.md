---
id: distributed-dirty-write
node: distributed.transactions.isolation
type: qa
---
## Q
A car sale updates two rows: `listings.buyer` and `invoices.recipient`. Two concurrent buyers' transactions interleave so that Alice wins the listing but Bob gets the invoice. Name the anomaly, and how even the weakest standard isolation level prevents it.

## A
**Dirty write** — a transaction overwrites a value that another *uncommitted* transaction has written. Interleaved dirty writes let two transactions each win on a different row, producing a mixed outcome neither of them wrote — and rollback becomes ill-defined (whose value do you restore?).

Prevention is universal: even **read committed** — effectively every real database — makes a writer take a **row-level lock held until commit/abort**; the second writer to any row simply waits for the first transaction to finish, so writes to one object serialize per transaction, not per statement.

Distinguish from **lost update**, which read committed does *not* prevent: there the second write happens *after* the first transaction committed — no uncommitted data is overwritten; the problem is the stale read it was based on.

## Q zh
一次售车要更新两行：`listings.buyer` 和 `invoices.recipient`。两个并发买家的事务交错执行，结果 Alice 抢到了车，发票却开给了 Bob。说出这个异常的名字，以及为什么连最弱的标准隔离级别都能防住它。

## A zh
**Dirty write（脏写）**——一个事务覆盖了另一个*未提交*事务写下的值。脏写交错会让两个事务各自在不同的行上"获胜"，产生一个谁都没写过的混合结果——而且回滚也变得没有定义（该恢复成谁的值？）。

防御是普适的：即使是 **read committed**——实际上所有真实数据库——都会让写者持有**行级锁直到提交或中止**；第二个写同一行的事务只需等第一个事务结束，因此对单个对象的写以事务为单位串行化，而不是以语句为单位。

注意与 **lost update（丢失更新）**区分，后者 read committed 防不住：那里第二次写发生在第一个事务*提交之后*——没有覆盖任何未提交数据；问题出在它所依据的那次已经过期的读。
