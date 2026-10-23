---
id: hl-javaq-j-q45-lsm-btree
node: java-questions.j-storage
type: qa
step: 7
---
## Q
比较 B 树与 LSM 树在写、读、写放大、典型系统上的差异。LSM 的写入路径是什么？

## A
- **B 树**：页式结构，读 O(log n) 次页访问；更新 = 读页-改-写页（随机 I/O，可能写放大）；范围查询好；写延迟尖刺来自页分裂；写放大是页大小 vs 记录大小；典型：PostgreSQL、MySQL InnoDB。
- **LSM 树**：写 → WAL + 内存表（memtable）→ 刷成不可变有序文件（SSTable）→ 后台合并（compaction）。写是顺序追加，吞吐高；读可能要查多个文件，靠 Bloom filter / 索引缩小；点查靠 Bloom filter，范围查询要合并多路；合并反复重写数据带来**写放大 + 空间放大**；典型：RocksDB、Cassandra、HBase。
- **写放大**：实际写入设备的字节 / 应用写入字节；用 `iostat`、设备 SMART、存储引擎统计测。
