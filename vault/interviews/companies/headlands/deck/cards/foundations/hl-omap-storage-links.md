---
id: hl-omap-storage-links
node: foundations.ordered-maps-trees
type: qa
step: 32
---
## Q
跳表和 B+ 树在分布式存储和数据库里有哪些应用？LSM-tree 的写入路径是什么？

## A
- **LSM-tree** 写入路径：先写日志，再写入内存里的有序结构 **memtable**；内存表满了整体排序落盘成不可变的有序文件（SSTable）。LevelDB、RocksDB 的 memtable 默认是**跳表**，HBase 的 MemStore 底层用 `ConcurrentSkipListMap`。选跳表因为并发写入友好、范围扫描顺着第 0 层走、实现简单。
- **B+ 树**：关系数据库（InnoDB、PostgreSQL）的主索引。每个节点装满一个磁盘页，几百个 key，树高通常只有 3–4 层；叶子用链表串起来，范围扫描顺序读。
- **Redis 的 `ZSET`**（元素较多时）：跳表 + 哈希表，跳表负责按分数排序和范围查询，哈希表负责按成员 O(1) 查分数。
