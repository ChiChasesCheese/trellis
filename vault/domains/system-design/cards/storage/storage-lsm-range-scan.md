---
id: storage-lsm-range-scan
node: storage.internals.lsm
type: qa
---
## Q
Point lookups aside — why is a *range scan* (`WHERE ts BETWEEN a AND b`) structurally harder for an LSM-tree than for a B-tree, and why don't Bloom filters help here?

## A
A B-tree holds the range as **one contiguous, already-merged run of leaf pages** — descend once, walk sibling pages. An LSM-tree's range is **scattered across every layer**: the memtable plus each SSTable may hold a slice of it, with newer layers shadowing older versions and tombstones hiding deletes. So the engine must open an iterator on *every* component and **k-way merge them on the fly**, comparing heads and discarding shadowed/deleted entries as it goes — CPU and I/O paid per overlapping file.

Bloom filters are useless here because they answer only *exact-key membership*; a range query can't enumerate the keys it's looking for, so **no file can be ruled out** by its filter — only min/max key metadata per file prunes anything.

This is why range-heavy, read-latency-sensitive workloads lean B-tree, and why leveled compaction (fewer overlapping files per level) hurts LSM range scans less than size-tiered.

## Q zh
撇开点查不谈 — 为什么*范围扫描*（`WHERE ts BETWEEN a AND b`）对 LSM-tree 在结构上比对 B-tree 更难，为什么 Bloom filter 在这里帮不上忙？

## A zh
B-tree 把这个范围保存为**一段连续的、已经合并好的叶子页面** — 下行一次，沿兄弟页面顺序走。LSM-tree 的范围则**散落在每一层**：memtable 和每个 SSTable 都可能持有它的一个切片，较新的层覆盖旧版本，tombstone 隐藏删除。所以引擎必须在*每个*组件上打开迭代器并**边走边做 k 路归并**，比较各头部、丢弃被覆盖/已删除的条目 — 每个有重叠的文件都要付 CPU 和 I/O。

Bloom filter 在这里没用，因为它只回答*精确 key 的成员性*；范围查询无法枚举它要找的 key，所以**没有任何文件能被 filter 排除** — 只有每个文件的 min/max key 元数据能剪掉一些。

这就是范围扫描繁重、读延迟敏感的负载偏向 B-tree 的原因，也是 leveled compaction（每层重叠文件更少）比 size-tiered 对 LSM 范围扫描伤害更小的原因。
