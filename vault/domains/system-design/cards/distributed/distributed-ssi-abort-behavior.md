---
id: distributed-ssi-abort-behavior
node: distributed.transactions.concurrency-control
type: qa
---
## Q
Your Postgres app moves to `SERIALIZABLE` and starts throwing 40001 errors under load. What is SSI doing, and what are the levers?

## A
SSI never blocks; it tracks each transaction's **read set** (SIRead predicate locks) and aborts a transaction when a dangerous read-write dependency structure appears. Two properties to state:

- **Aborts are conservative** — the structure is a *potential* cycle, so SSI produces **false positives**: transactions that were actually serializable still get aborted. The rate climbs superlinearly with contention, and long-running transactions widen the window during which conflicts can be discovered.
- **Predicate-lock memory is finite**: when a transaction's read set exceeds the tracking budget (`max_pred_locks_per_transaction`), locks **escalate from tuple to page to relation granularity**, which coarsens the tracking and *increases* false aborts. Big sequential scans under SERIALIZABLE are self-defeating.

Levers: a **retry loop with backoff on 40001** (mandatory — it is a normal outcome, not an error); keep transactions short and read sets narrow (index them so they don't scan); mark long analytics as `READ ONLY DEFERRABLE`, which waits for a safe snapshot and can then never abort or cause aborts; and if contention is genuinely on hot rows, switch that path to explicit pessimistic locking instead.

## Q zh
你的 Postgres 应用切到了 `SERIALIZABLE`，在负载下开始抛 40001 错误。SSI 在做什么？有哪些可以调的杠杆？

## A zh
SSI 从不阻塞；它跟踪每个事务的**读集**（SIRead 谓词锁），一旦出现危险的读写依赖结构就中止一个事务。有两个特性要说清楚：

- **中止是保守的**——检测到的结构只是一个*可能的*环，所以 SSI 会产生**误报**：一些实际上是可串行化的事务也会被中止。这个比例随争用超线性上升，而长事务会拉长冲突可能被发现的窗口。
- **谓词锁的内存是有限的**：当一个事务的读集超过跟踪预算（`max_pred_locks_per_transaction`）时，锁会**从行级升级到页级再到关系级**，这会让跟踪变粗，反而*增加*误报中止。在 SERIALIZABLE 下做大的全表扫描会适得其反。

可调杠杆：**对 40001 做带退避的重试循环**（必须做——这是正常结果，不是错误）；保持事务短、读集窄（给它们建索引，避免全表扫描）；把长时间的分析查询标记成 `READ ONLY DEFERRABLE`，它会等待一个安全的快照，之后就再也不会中止也不会导致别人中止；如果争用真的集中在热行上，就把那条路径换成显式的悲观锁。
