---
id: hi-c-sd-scaling-writes-b01-lsm-tree
node: sd.patterns.scaling-writes.beyond
type: qa
step: 1
---
## Q
**写扩展 · LSM 树为什么写得快**｜拓展 · 加分

Cassandra、LevelDB 的"追加式"到底怎么实现的，读为什么变慢？

## A
- **写入路径：** 先顺序追加到提交日志（WAL）保证不丢，再写入内存里有序的 memtable；memtable 满了就整体刷成不可变的有序文件（SSTable）。全程没有随机写盘。
- **读为什么慢：** 同一个键的不同版本可能散落在 memtable 和多个 SSTable 里，读要逐个查找并合并；用布隆过滤器（Bloom filter）跳过不含该键的文件，缓解但不消除。
- **后台合并（compaction）：** 把多个 SSTable 合并成更少、更大的文件，丢弃被覆盖和已删除的数据。这会产生写放大（同一份数据被重复写盘多次）以及合并期间的磁盘 I/O 争抢。
- **对比 B 树：** B 树原地更新，每次写可能随机写一个页；读通常一次定位。LSM 用读和后台合并的成本换了写的顺序性。
- **面试说法：** 写多读少、数据只追加选 LSM 系；读多或要范围扫描和事务选 B 树系。
