---
id: storage-btree-latches
node: storage.internals.btree
type: qa
---
## Q
B-trees need latches (lightweight page locks) on the read *and* write path, while an LSM engine's in-memory writes get away with almost none. What structural difference explains this, and how do B-trees keep latching cheap?

## A
B-trees mutate shared pages **in place**: a reader descending the tree can otherwise observe a page mid-modification, or follow pointers that a concurrent **page split** is rewiring across multiple pages. So every page access takes a **latch** — a short-lived physical lock protecting the page's bytes (distinct from transaction locks, which protect logical rows for a transaction's duration).

Kept cheap via **latch crabbing**: take the child's latch, release the parent's as soon as the child is known safe (won't split/merge), so writers hold a short chain, not the whole path — plus tricks like B-link sideways pointers letting readers recover from a concurrent split.

The LSM contrast: files on disk are **immutable**, and the active memtable is a concurrent in-memory structure (e.g. a skip list) swapped out **atomically** when full — nothing shared is ever rewritten under a reader's feet, so the whole page-latching protocol has nothing to protect.

## Q zh
B-tree 在读*和*写路径上都需要 latch（轻量级页面锁），而 LSM 引擎的内存写入几乎不需要。什么结构性差异解释了这一点，B-tree 又靠什么让 latch 开销保持低廉？

## A zh
B-tree **原地**修改共享页面：否则一个正在下行的读者可能观察到修改到一半的页面，或者沿着正被并发**页面分裂**跨多页重连的指针走。所以每次页面访问都要拿 **latch** — 一种保护页面字节的短生命周期物理锁（区别于事务锁，后者在事务期间保护逻辑行）。

靠 **latch crabbing** 保持低廉：先拿子页面的 latch，一旦确认子页面安全（不会分裂/合并）就立刻释放父页面的，写者只持有一小段链而非整条路径 — 外加 B-link 横向指针等技巧，让读者能从并发分裂中恢复。

LSM 的对比：磁盘上的文件是**不可变的**，活跃 memtable 是并发内存结构（如 skip list），写满时**原子地**换出 — 没有任何共享内容会在读者脚下被重写，所以整套页面 latch 协议根本没有要保护的对象。
