---
id: analytics-row-vs-column-layout
node: analytics.olap
type: qa
---
## Q
An analytical query averages one column over 100M rows. Why does a row-store (OLTP) engine do orders of magnitude more I/O than a column store, even with the same data?

## A
A row store lays each row's columns contiguously, so reading one column drags **every other column of every row** through disk and memory — and B-tree indexes don't help a full scan.

A column store lays each **column** contiguously: the query reads only the 1–2 columns it touches, and those columns compress far better (similar values adjacent), often 10x+ — so bytes scanned drops by both column selection *and* compression.

That's the whole OLTP/OLAP split: point reads and updates want rows together; scans and aggregates want columns together.

## Q zh
一个分析查询在 100M 行上平均一列。为什么行存储（OLTP）引擎做比列存储数量级更多的 I/O，即使数据相同？

## A zh
行存储连续放置每行的列，所以读一列拖**每行的每个其他列**通过磁盘和内存 — 和 B-tree 索引不帮助完整扫描。

列存储连续放置每**列**：查询仅读它接触的 1–2 列，那些列压缩远好得多（相似值相邻），通常 10x+ — 所以扫描的字节通过列选择*和*压缩下降。

那是整个 OLTP/OLAP 分裂：point 读和更新想行一起；扫描和聚合想列一起。
