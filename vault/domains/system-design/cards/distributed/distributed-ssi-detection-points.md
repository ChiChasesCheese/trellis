---
id: distributed-ssi-detection-points
node: distributed.transactions.concurrency-control
type: qa
---
## Q
SSI lets transactions run on snapshots without blocking, then aborts the ones whose premises went stale. Concretely, at which two points does the engine notice that a transaction acted on outdated information?

## A
Both detections target the same event — a read that a concurrent write invalidated — caught from the two possible directions:

- **Detecting a stale read (write came first)**: when the transaction reads, MVCC shows there is a version of this object written by a concurrent, not-yet-visible transaction — its snapshot is ignoring a write. Nothing aborts yet (the writer might still roll back); if that writer commits, the reader's premise is stale, and the reader is aborted if it tries to commit a write afterwards.
- **Detecting a later write into someone's read set (read came first)**: reads leave markers on the data/index ranges they touched (Postgres SIRead locks — non-blocking, outliving the read). A concurrent transaction writing into a marked range flags a read-write dependency on the reader; commit-time analysis aborts one party when such dependencies could form a cycle.

Why both directions are needed: the reader and writer can commit in either order, and whichever runs second must be able to see the collision. Waiting until commit to abort keeps false positives lower — the premise-invalidating writer might have aborted, or the reader might turn out to be read-only.

## Q zh
SSI 让事务在快照上无阻塞地运行，然后把那些前提已失效的事务中止掉。具体来说，引擎在哪两个检测点上发现一个事务依据了过时的信息？

## A zh
两个检测针对的是同一件事——一次被并发写入作废的读——只是从两个可能的方向捕捉：

- **检测过期的读（写在前）**：事务读取时，MVCC 显示这个对象存在一个由并发的、对本快照尚不可见的事务写下的版本——它的快照正在忽略一个写入。此时还不中止（写者可能回滚）；如果那个写者提交了，读者的前提就过期了，读者之后再试图提交写入时会被中止。
- **检测写入落进别人的读集（读在前）**：读操作会在触碰过的数据/索引区间上留下标记（Postgres 的 SIRead 锁——不阻塞、比读本身活得久）。并发事务写入被标记的区间时，会在读者身上记下一条 read-write 依赖；提交时的分析发现这类依赖可能成环，就中止其中一方。

为什么两个方向都需要：读者和写者的提交顺序不定，后运行的那个必须能看见这次碰撞。而把中止推迟到提交时能降低误杀——作废前提的写者可能已经中止，读者也可能最终只读不写。
