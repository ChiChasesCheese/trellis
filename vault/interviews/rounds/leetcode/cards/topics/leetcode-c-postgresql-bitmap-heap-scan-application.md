---
id: leetcode-c-postgresql-bitmap-heap-scan-application
node: topics.uncategorised
type: qa
anki: 1787361365398
tags: [algorithm::batch-i-o, algorithm::bitmap, algorithm::set-intersection, application, case, case::postgresql-bitmap-heap-scan, category::storage-databases, chapter::08, chapter::16, leetcode, system::postgresql]
---
## Q
PostgreSQL Bitmap Heap Scan 为什么可能比多个普通 Index Scan 更少随机 I/O？lossy bitmap 是什么？

## A
它先把 tuple locations 合并成 bitmap，再按 heap block 顺序批量访问。内存不足时 lossy bitmap 只记某 page 可能命中，读取该 page 后必须 recheck tuples。

**Evidence**

PostgreSQL 官方 bitmap scan 文档定义 BitmapAnd/Or、physical-order heap scan 与 exact/lossy behavior。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FPostgreSQL%20Bitmap%20Heap%20Scan%EF%BC%9A%E9%9B%86%E5%90%88%E4%BD%8D%E5%9B%BE%E4%B8%8E%E6%89%B9%E9%87%8F%E5%9B%9E%E8%A1%A8)
