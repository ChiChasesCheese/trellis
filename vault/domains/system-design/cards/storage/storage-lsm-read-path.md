---
id: storage-lsm-read-path
node: storage.internals.lsm
type: qa
---
## Q
Walk the read path for a point lookup in an LSM-tree, and name the structure that keeps misses cheap.

## A
1. Check the **memtable** (in-memory, newest data).
2. Check immutable memtables awaiting flush.
3. Check SSTables newest-to-oldest, level by level; first hit wins (newer versions shadow older).

**Bloom filters** (one per SSTable) keep this cheap: they answer "definitely not here" with no I/O, so a lookup skips most files and misses don't touch disk ~99% of the time. Without them, every miss would read every level.

## Q zh
漫步 LSM-tree 中点查找的读路径，命名让 miss 保持便宜的结构。

## A zh
1. 检查**memtable**（内存，最新数据）。
2. 检查不可变 memtable 等待刷新。
3. 从最新到最旧检查 SSTable，级别按级别；首次命中胜出（新版本遮蔽旧版本）。

**Bloom filter**（每个 SSTable 一个）保持这便宜：它们用无 I/O 回答"肯定不在这"，所以查询跳过大多数文件，miss 不接触磁盘~99% 的时间。没有它们，每个 miss 会读每个级别。
