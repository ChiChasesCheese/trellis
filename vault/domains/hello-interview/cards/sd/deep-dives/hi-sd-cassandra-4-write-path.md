---
id: hi-sd-cassandra-4-write-path
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 4
---
## Q
**写路径：commit log、memtable、SSTable**｜系统设计 · 深入专题

为什么 Cassandra 写得特别快？一次写入依次经过什么？

## A
**要点。** 底层是 LSM 树（log-structured merge tree），写入几乎全是追加：

1. 先顺序追加到提交日志（commit log），相当于预写日志（WAL），保证宕机不丢。
2. **排序后写入 memtable：** 再写入内存里按主键排序的 memtable。
3. 达到大小或时间阈值后，memtable 刷成磁盘上不可变的 SSTable，对应的 commit log 即可清理。

删除也只是追加一条墓碑（tombstone）。

**为什么。** 把随机写变成顺序写，这就是它与 B 树型数据库（关系库、DynamoDB）的核心区别：用读取更复杂换写入更快。

**读路径。** 先查 memtable，再用布隆过滤器（bloom filter）判断哪些 SSTable 可能含该键，从新到旧读，取最新值；SSTable 按主键排序，并有字节偏移索引。

**维护。** 压缩（compaction）把多个 SSTable 合并为更少的，丢掉旧版本和已删除的行（连墓碑一起清理），因为都是有序的所以很高效。
