---
id: storage-btree-clustered-vs-heap
node: storage.internals.btree
type: qa
---
## Q
InnoDB stores the full row inside the primary-key B-tree's leaf pages (clustered); Postgres leaves rows in a heap file and every index points into it. What does each layout win and lose on the read and write paths?

## A
- **Clustered (InnoDB)**: primary-key lookups and PK-range scans are one tree traversal — the leaf *is* the row, and rows adjacent in key order are adjacent on disk. Cost: **secondary indexes store the primary key** instead of a row address, so a secondary lookup is *two* B-tree descents (secondary → PK tree); a fat primary key fattens every secondary index; and inserts in random PK order scatter row data across leaf pages.
- **Heap (Postgres)**: all indexes are equal citizens pointing at a row's heap location (CTID), so no double descent and the PK isn't special. Cost: every index hit pays a **heap hop** for the row (softened by index-only scans), and when a row moves, *every* index needs the new address — a reason Postgres works hard to keep updated rows on the same page (HOT).

Rule of thumb: clustered shines when access is dominated by primary-key ranges; heap is more forgiving for many secondary indexes.

## Q zh
InnoDB 把完整的行存在主键 B-tree 的叶子页面里（clustered，聚簇）；Postgres 把行留在 heap 文件中、每个索引都指向它。在读写路径上，两种布局各赢得什么、失去什么？

## A zh
- **聚簇（InnoDB）**：主键查找和主键范围扫描只需一次树遍历 — 叶子*就是*行，key 序相邻的行在磁盘上也相邻。代价：**二级索引存的是主键**而不是行地址，所以二级查找要*两次* B-tree 下行（二级索引 → 主键树）；肥大的主键会撑肥每个二级索引；按随机主键顺序插入会把行数据打散到各叶子页面。
- **Heap（Postgres）**：所有索引一律平等，指向行的 heap 位置（CTID），没有二次下行，主键也不特殊。代价：每次命中索引都要为取行付一次 **heap 跳转**（index-only scan 可缓解），而行一旦搬家，*每个*索引都要新地址 — 这是 Postgres 努力把更新后的行留在同一页面（HOT）的原因之一。

经验法则：访问以主键范围为主时聚簇最亮眼；二级索引很多时 heap 更宽容。
