---
id: leetcode-c-sqlite-btree-pages-application
node: topics.uncategorised
type: qa
anki: 1787359913693
tags: [algorithm::b-tree, algorithm::linked-list, algorithm::ordered-search, algorithm::page-split, application, case, case::sqlite-btree-pages, category::storage-databases, leetcode, system::sqlite]
---
## Q
SQLite 为什么使用高扇出 B-tree，而不是把普通二叉搜索树直接存到磁盘？

## A
磁盘访问单位是 page。B-tree 的一个 interior page 保存 K 个有序 key 和 K+1 个 child page number，一次 I/O 能排除大块搜索空间；高 fan-out 让树高远低于二叉树。所有叶子保持相同深度，范围数据仍有序。

**Evidence**

SQLite 官方 file format 定义 interior B-tree page 为 K keys + K+1 child pointers，并要求同一 interior page 的所有 children 具有相同 depth。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FSQLite%20B-tree%EF%BC%9A%E6%8A%8A%E5%B9%B3%E8%A1%A1%E6%A0%91%E5%8F%98%E6%88%90%E7%A3%81%E7%9B%98%E9%A1%B5)
