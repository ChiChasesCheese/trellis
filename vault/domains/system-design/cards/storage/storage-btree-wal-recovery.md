---
id: storage-btree-wal-recovery
node: storage.internals.btree
type: qa
---
## Q
B-trees write pages in place. Why does that force a write-ahead log, and what is the torn-page problem?

## A
In-place page writes aren't atomic: crash mid-write and the tree is inconsistent — worse, a page split touches **multiple pages**, so a crash between them can orphan data. So every modification is first appended to the **WAL** (sequential, fsynced); on recovery the engine replays the log to restore consistency. Every committed write is therefore written **twice** (WAL + page).

**Torn page**: a 8KB page over 4KB disk sectors can be half-old/half-new after a crash — corrupt in a way replay alone can't fix. Postgres counters with **full-page writes** (first touch after each checkpoint logs the entire page image); MySQL uses a doublewrite buffer.

## Q zh
B 树原地写页。为什么这会强制要求 write-ahead log，什么是 torn-page 问题？

## A zh
原地页写不是原子的：在写的中间崩溃，树变得不一致——更糟的是，页分裂接触**多个页**，在它们之间崩溃可能孤立数据。所以每个修改先被 append 到 **WAL**（顺序，fsynced）；恢复时引擎重放日志来恢复一致性。因此每个已提交的写被写了**两次**（WAL + page）。

**Torn page**：8KB 页跨 4KB 磁盘扇区，崩溃后可能半旧半新——损坏方式单独重放无法修复。Postgres 用**全页写**（每个检查点之后首次接触日志整个页镜像）来对抗；MySQL 使用 doublewrite 缓冲。
