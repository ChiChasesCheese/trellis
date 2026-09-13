---
id: leetcode-c-cpython-compact-dict-application
node: topics.uncategorised
type: qa
anki: 1787359913093
tags: [algorithm::collision-resolution, algorithm::dynamic-array, algorithm::hash-table, algorithm::open-addressing, application, case, case::cpython-compact-dict, category::runtimes-os, leetcode, system::cpython]
---
## Q
CPython dict 如何同时做到紧凑、平均 O(1) lookup 和 insertion order？为什么还要控制 load factor？

## A
稀疏 dk_indices 只保存到紧凑 dk_entries 的 index；open addressing 用 hash 与 perturb sequence 解决碰撞；combined table 的 entries 近似 append-only，所以迭代 entries 就得到 insertion order。表保留 EMPTY slot，并在约三分之二满时扩容，限制 probe 长度并保证查找终止。

**Evidence**

CPython 官方 dictobject.c 注释完整定义 dk_indices/dk_entries 布局、ordered iteration、PERTURB_SHIFT 探测和 two-thirds usable fraction。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FCPython%20dict%EF%BC%9A%E7%B4%A7%E5%87%91%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E6%89%B0%E5%8A%A8%E6%8E%A2%E6%B5%8B)
