---
id: leetcode-c-cpython-timsort-application
node: topics.uncategorised
type: qa
anki: 1787365291905
tags: [algorithm::binary-insertion-sort, algorithm::galloping-search, algorithm::natural-merge-sort, algorithm::timsort, application, case, case::cpython-timsort, category::runtimes-os, chapter::03, chapter::08, chapter::10, leetcode, system::cpython]
---
## Q
CPython Timsort 怎样利用部分有序数据？run、powersort 与 galloping 各负责什么？

## A
先识别并规范化自然升序/降序 runs，短 run 用二分插入补长；powersort 控制 run 的合并树，避免不平衡导致反复搬移；归并中一侧连续获胜时，galloping 用指数搜索加二分批量找到边界。

**Evidence**

CPython 官方 listsort.txt 将实现描述为 adaptive stable natural mergesort，并记录 powersort merge strategy、run detection 与 galloping。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FCPython%20Timsort%EF%BC%9A%E8%87%AA%E7%84%B6%20Runs%E3%80%81%E7%A8%B3%E5%AE%9A%E5%BD%92%E5%B9%B6%E4%B8%8E%20Powersort)
